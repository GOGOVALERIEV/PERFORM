"""
YouTube Transcript Scraper
==========================
Extracts transcripts from YouTube videos using multiple strategies:

Strategy 1: Selenium + Innertube API
  - Load video page in headless Chrome
  - Extract captionTracks from ytInitialPlayerResponse
  - Use the browser's authenticated session to call get_transcript Innertube endpoint

Strategy 2: yt-dlp subtitle download (most reliable)
  - Uses yt-dlp's Python API which accesses alternate YouTube APIs (android player)
  - Bypasses timedtext endpoint rate-limiting

Strategy 3: Selenium + UI scraping
  - Click "Show transcript" in the YouTube UI
  - Scrape transcript segments from the DOM

Usage:
    python yt_transcript_selenium.py <video_id>
    python yt_transcript_selenium.py <video_id> --method selenium
    python yt_transcript_selenium.py <video_id> --method ytdlp
    python yt_transcript_selenium.py <video_id> --method ui
    python yt_transcript_selenium.py <video_id> --method all  (try everything, report results)
"""

import sys
import os
import io
import json
import re
import time
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Fix Windows console encoding for Unicode characters (music notes, etc.)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ---------------------------------------------------------------------------
# Strategy 1: Selenium + captionTracks extraction
# ---------------------------------------------------------------------------

def _create_chrome_driver():
    """Create a headless Chrome driver with realistic settings."""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from webdriver_manager.chrome import ChromeDriverManager

    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def _handle_consent(driver):
    """Dismiss the YouTube cookie consent dialog if present."""
    try:
        driver.execute_script("""
            var buttons = document.querySelectorAll('button');
            for (var b of buttons) {
                if (b.textContent.includes('Reject all') || b.textContent.includes('Accept all')) {
                    b.click(); break;
                }
            }
        """)
        time.sleep(2)
    except Exception:
        pass


def _extract_caption_tracks_from_page(driver):
    """
    Extract captionTracks from the ytInitialPlayerResponse embedded in page source.
    Returns list of dicts with baseUrl, languageCode, etc.
    """
    page_source = driver.page_source
    match = re.search(
        r'ytInitialPlayerResponse\s*=\s*(\{.*?\})\s*;',
        page_source,
        re.DOTALL
    )
    if match:
        try:
            data = json.loads(match.group(1))
            tracks = (data.get("captions", {})
                      .get("playerCaptionsTracklistRenderer", {})
                      .get("captionTracks", []))
            return tracks
        except (json.JSONDecodeError, KeyError):
            pass

    # Fallback: try via JS execution
    try:
        tracks = driver.execute_script("""
            try {
                return ytInitialPlayerResponse.captions
                    .playerCaptionsTracklistRenderer.captionTracks;
            } catch(e) { return null; }
        """)
        if tracks:
            return tracks
    except Exception:
        pass

    return []


def get_transcript_selenium(video_id, lang="en"):
    """
    Strategy 1: Use Selenium to load the page, extract caption track URLs,
    then try to fetch the subtitle content via the browser session.
    """
    driver = _create_chrome_driver()
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        driver.get(url)
        time.sleep(5)
        _handle_consent(driver)

        title = driver.title
        print(f"  Page title: {title}")

        tracks = _extract_caption_tracks_from_page(driver)
        if not tracks:
            print("  No caption tracks found in page")
            return None, {"title": title, "tracks": 0}

        print(f"  Found {len(tracks)} caption track(s)")
        for t in tracks:
            lc = t.get("languageCode", "?")
            name = t.get("name", {})
            if isinstance(name, dict):
                name = name.get("simpleText", "unnamed")
            print(f"    - {lc}: {name}")

        # Choose the best track (prefer specified language)
        chosen = None
        for t in tracks:
            if t.get("languageCode", "").startswith(lang):
                chosen = t
                break
        if not chosen:
            chosen = tracks[0]

        base_url = chosen.get("baseUrl", "")
        if not base_url:
            print("  No baseUrl found in chosen track")
            return None, {"title": title, "tracks": len(tracks)}

        # Try fetching the subtitle via JS fetch within the page context
        print(f"  Fetching subtitle via browser fetch (lang={chosen.get('languageCode')})...")
        result = driver.execute_script("""
            var resp = await fetch(arguments[0]);
            return await resp.text();
        """, base_url)

        if result and '<text' in result:
            lines = _parse_timedtext_xml(result)
            if lines:
                return lines, {"title": title, "tracks": len(tracks), "method": "browser_fetch_xml"}

        # Try JSON format
        json_url = base_url + ("&" if "?" in base_url else "?") + "fmt=json3"
        result = driver.execute_script("""
            var resp = await fetch(arguments[0]);
            return await resp.text();
        """, json_url)

        if result and len(result) > 100:
            try:
                data = json.loads(result)
                lines = _parse_json3_transcript(data)
                if lines:
                    return lines, {"title": title, "tracks": len(tracks), "method": "browser_fetch_json3"}
            except json.JSONDecodeError:
                pass

        print("  Browser fetch returned empty/blocked response (timedtext rate-limited)")
        return None, {"title": title, "tracks": len(tracks), "blocked": True}

    finally:
        driver.quit()


def _parse_timedtext_xml(xml_text):
    """Parse YouTube timedtext XML into a list of text lines."""
    lines = []
    try:
        root = ET.fromstring(xml_text)
        for elem in root.iter('text'):
            text = elem.text or ""
            text = (text.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&#39;", "'")
                    .replace("&quot;", '"'))
            text = text.strip()
            if text:
                lines.append(text)
    except ET.ParseError:
        for m in re.finditer(r'<text[^>]*>(.*?)</text>', xml_text, re.DOTALL):
            text = m.group(1).strip()
            text = (text.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&#39;", "'")
                    .replace("&quot;", '"'))
            if text:
                lines.append(text)
    return lines


def _parse_json3_transcript(data):
    """Parse YouTube JSON3 subtitle format into a list of text lines."""
    lines = []
    events = data.get("events", [])
    for event in events:
        segs = event.get("segs", [])
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if text and text != "\n":
            lines.append(text)
    return lines


# ---------------------------------------------------------------------------
# Strategy 2: yt-dlp subtitle download
# ---------------------------------------------------------------------------

def get_transcript_ytdlp(video_id, lang="en"):
    """
    Strategy 2: Use yt-dlp to download subtitles.
    yt-dlp uses alternate YouTube APIs (android player) that bypass timedtext blocking.
    Returns (lines, metadata) or (None, metadata).
    """
    try:
        import yt_dlp
    except ImportError:
        print("  yt-dlp not installed. Install with: pip install yt-dlp")
        return None, {"error": "yt-dlp not installed"}

    url = f"https://www.youtube.com/watch?v={video_id}"

    # Use a temp directory for the subtitle file
    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, "%(id)s")
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [lang],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }

        info = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"  yt-dlp extraction error: {e}")
            return None, {"error": str(e)}

        title = info.get("title", "Unknown") if info else "Unknown"

        # Find the downloaded subtitle file
        sub_files = list(Path(tmpdir).glob(f"*.{lang}*.vtt")) + \
                    list(Path(tmpdir).glob(f"*.{lang}*.srt")) + \
                    list(Path(tmpdir).glob("*.vtt")) + \
                    list(Path(tmpdir).glob("*.srt"))

        if not sub_files:
            # Check all files in tmpdir
            all_files = list(Path(tmpdir).iterdir())
            print(f"  No subtitle files found. Files in tmpdir: {[f.name for f in all_files]}")
            return None, {"title": title, "error": "No subtitle file downloaded"}

        sub_file = sub_files[0]
        print(f"  Downloaded subtitle: {sub_file.name}")

        # Parse the VTT/SRT file
        content = sub_file.read_text(encoding="utf-8")
        lines = _parse_vtt(content)

        return lines, {"title": title, "method": "yt-dlp", "sub_file": sub_file.name}


def _parse_vtt(vtt_text):
    """Parse VTT subtitle text into clean transcript lines (no timestamps, no dupes)."""
    lines = []
    seen = set()

    for line in vtt_text.split("\n"):
        line = line.strip()
        # Skip VTT headers, timestamps, and empty lines
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r'^\d{2}:\d{2}', line):
            continue
        if line.startswith("NOTE"):
            continue
        if re.match(r'^\d+$', line):  # SRT sequence numbers
            continue

        # Remove VTT position tags like <00:00:01.360>
        line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', line)
        # Remove other HTML-like tags
        line = re.sub(r'<[^>]+>', '', line)
        line = line.strip()

        if line and line not in seen:
            seen.add(line)
            lines.append(line)

    return lines


# ---------------------------------------------------------------------------
# Strategy 3: Selenium UI scraping (click "Show transcript")
# ---------------------------------------------------------------------------

def get_transcript_ui(video_id):
    """
    Strategy 3: Use Selenium to click "Show transcript" and scrape from the UI.
    This relies on the UI loading transcript data (which may also be blocked).
    """
    from selenium.webdriver.common.by import By

    driver = _create_chrome_driver()
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        driver.get(url)
        time.sleep(5)
        _handle_consent(driver)

        title = driver.title
        print(f"  Page title: {title}")

        # Reload after consent
        driver.get(url)
        time.sleep(5)

        # Remove overlays
        driver.execute_script("""
            document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove());
            document.querySelectorAll('ytd-popup-container').forEach(e => e.remove());
        """)
        time.sleep(1)

        # Scroll down
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)

        # Expand description
        driver.execute_script("""
            var btn = document.querySelector('tp-yt-paper-button#expand');
            if (btn) btn.click();
        """)
        time.sleep(2)

        # Click "Show transcript"
        clicked = driver.execute_script("""
            var sections = document.querySelectorAll('ytd-video-description-transcript-section-renderer');
            for (var s of sections) {
                var btn = s.querySelector('button');
                if (btn) { btn.click(); return true; }
            }
            // Fallback: find any button with transcript text
            var buttons = document.querySelectorAll('button');
            for (var b of buttons) {
                if (b.textContent.trim() === 'Show transcript') {
                    b.click(); return true;
                }
            }
            return false;
        """)

        if not clicked:
            print("  Could not find 'Show transcript' button")
            return None, {"title": title, "error": "No transcript button"}

        print("  Clicked 'Show transcript', waiting for panel...")
        time.sleep(8)  # Wait for transcript segments to load

        # Extract transcript segments from the DOM
        segments = driver.execute_script("""
            var result = [];
            // Try modern transcript view
            var segs = document.querySelectorAll(
                'ytd-transcript-segment-renderer, ' +
                'ytd-transcript-segment-list-renderer .segment'
            );
            for (var s of segs) {
                var textEl = s.querySelector('.segment-text, yt-formatted-string');
                var timeEl = s.querySelector('.segment-timestamp, .segment-start-offset');
                if (textEl) {
                    result.push({
                        text: textEl.textContent.trim(),
                        time: timeEl ? timeEl.textContent.trim() : ''
                    });
                }
            }
            return result;
        """)

        if segments:
            lines = [s["text"] for s in segments if s["text"]]
            return lines, {"title": title, "method": "ui_scrape", "segments": len(segments)}
        else:
            print("  No transcript segments found in DOM (likely blocked by rate limit)")
            return None, {"title": title, "error": "No segments in DOM"}

    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# Combined approach
# ---------------------------------------------------------------------------

def get_transcript(video_id, method="auto", lang="en"):
    """
    Get transcript for a YouTube video.

    Args:
        video_id: YouTube video ID
        method: "auto" | "selenium" | "ytdlp" | "ui" | "all"
        lang: Language code (default "en")

    Returns:
        (lines, metadata) where lines is a list of transcript text lines
    """
    print(f"\n{'='*60}")
    print(f"Video: {video_id}")
    print(f"Method: {method} | Language: {lang}")
    print(f"{'='*60}")

    results = {}

    if method in ("auto", "all", "selenium"):
        print(f"\n--- Strategy 1: Selenium + captionTracks ---")
        lines, meta = get_transcript_selenium(video_id, lang)
        results["selenium"] = (lines, meta)
        if lines and method == "auto":
            print(f"\n  SUCCESS: {len(lines)} lines via Selenium")
            return lines, meta

    if method in ("auto", "all", "ytdlp"):
        print(f"\n--- Strategy 2: yt-dlp ---")
        lines, meta = get_transcript_ytdlp(video_id, lang)
        results["ytdlp"] = (lines, meta)
        if lines and method == "auto":
            print(f"\n  SUCCESS: {len(lines)} lines via yt-dlp")
            return lines, meta

    if method in ("auto", "all", "ui"):
        print(f"\n--- Strategy 3: Selenium UI scraping ---")
        lines, meta = get_transcript_ui(video_id)
        results["ui"] = (lines, meta)
        if lines and method == "auto":
            print(f"\n  SUCCESS: {len(lines)} lines via UI scraping")
            return lines, meta

    # If "all" method, report everything
    if method == "all":
        print(f"\n{'='*60}")
        print("RESULTS SUMMARY:")
        print(f"{'='*60}")
        for name, (lines, meta) in results.items():
            status = f"{len(lines)} lines" if lines else "FAILED"
            print(f"  {name}: {status} | {meta}")
        # Return the first successful result
        for name in ("selenium", "ytdlp", "ui"):
            if name in results and results[name][0]:
                return results[name]

    # If a specific method was requested
    if method in results:
        return results[method]

    return None, {"error": "No method succeeded"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Transcript Scraper")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--method", default="auto",
                        choices=["auto", "selenium", "ytdlp", "ui", "all"],
                        help="Extraction method (default: auto)")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument("--output", "-o", help="Output file path (default: transcript_<id>.txt)")
    parser.add_argument("--preview", type=int, default=30,
                        help="Number of lines to preview (default: 30)")
    args = parser.parse_args()

    lines, meta = get_transcript(args.video_id, args.method, args.lang)

    if lines:
        print(f"\n{'='*60}")
        print(f"TRANSCRIPT: {len(lines)} lines")
        if "title" in meta:
            print(f"Title: {meta['title']}")
        if "method" in meta:
            print(f"Method: {meta['method']}")
        print(f"{'='*60}")

        for i, line in enumerate(lines[:args.preview]):
            print(f"  {line}")
        if len(lines) > args.preview:
            print(f"  ... ({len(lines) - args.preview} more lines)")

        # Save to file
        output_file = args.output or f"transcript_{args.video_id}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\nSaved to: {output_file}")
    else:
        print(f"\nFAILED to extract transcript.")
        print(f"Metadata: {meta}")
        sys.exit(1)

    return lines


if __name__ == "__main__":
    main()

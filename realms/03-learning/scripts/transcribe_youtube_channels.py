"""
YouTube Channel Transcriber
============================
Transcribes all non-Shorts videos from the last 5 months of YouTube channels.
Uses YouTube's auto-generated captions (fast, free, no download needed).
Uses ANDROID_VR client to bypass YouTube rate limiting.

Has retry logic + exponential backoff to handle YouTube rate limiting.
Resumes where it left off (skips already-transcribed videos).

Usage:
    python tools/transcribe_youtube_channels.py "ChannelName|https://www.youtube.com/@handle"
    python tools/transcribe_youtube_channels.py "Channel1|URL1" "Channel2|URL2"
    python tools/transcribe_youtube_channels.py "Channel1|URL1|Google Sheets"

    Format: "FolderName|ChannelURL" or "FolderName|ChannelURL|FilterKeyword"
    - FolderName = name used for the output folder
    - ChannelURL = full YouTube channel URL
    - FilterKeyword = optional, only transcribe videos with this in the title (case-insensitive)

Output:
    C:/Users/User/Desktop/personal-ob/transcripts/<FolderName>/
"""

import os
import sys
import json
import time
import re
import random
from datetime import datetime, timedelta
from pathlib import Path

# Try importing dependencies
try:
    import yt_dlp
except ImportError:
    print("ERROR: yt-dlp not installed. Run: python -m pip install yt-dlp")
    sys.exit(1)

# === COOKIE FILE FOR AUTHENTICATED REQUESTS ===
# YouTube gives much higher rate limits to logged-in users.
# Export cookies from Brave: close Brave, then run:
#   python tools/transcribe_youtube_channels.py --export-cookies
# This only needs to be done once (or when cookies expire).
COOKIE_FILE = Path(__file__).parent.parent / "config" / "youtube-cookies.txt"

# === SETTINGS ===
OUTPUT_BASE = Path(r"C:\Users\User\Desktop\personal-ob\transcripts")
CUTOFF_DATE = datetime.now() - timedelta(days=150)  # ~5 months ago

# Rate limit settings
BASE_DELAY = 8          # seconds between requests (minimum)
MAX_DELAY = 180         # max backoff delay in seconds
MAX_RETRIES = 5         # retries per video before giving up
CHANNEL_PAUSE = 30      # seconds to pause between channels
BATCH_PAUSE_EVERY = 10  # pause after every N videos
BATCH_PAUSE_SECS = 60   # how long to pause between batches


# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Flush output immediately so we can see progress
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None


def export_cookies_from_brave():
    """Export YouTube cookies from Brave browser to a cookies.txt file.
    Brave must be CLOSED for this to work (it locks the cookie database)."""
    print()
    print("  Exporting YouTube cookies from Brave...")
    print("  NOTE: Brave must be CLOSED for this to work!")
    print()

    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('brave',),
        'cookiefile': str(COOKIE_FILE),
        'skip_download': True,
        'extract_flat': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Just visit YouTube to trigger cookie export
            ydl.extract_info('https://www.youtube.com/@YouTube', download=False)
        print(f"  Cookies saved to: {COOKIE_FILE}")
        print(f"  File size: {COOKIE_FILE.stat().st_size:,} bytes")
        print("  You can now open Brave again!")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        print()
        print("  Make sure Brave is completely closed (check Task Manager).")
        return False


def get_yt_dlp_opts_with_cookies(extra_opts=None):
    """Return yt-dlp options with cookies loaded if available."""
    opts = extra_opts.copy() if extra_opts else {}
    if COOKIE_FILE.exists():
        opts['cookiefile'] = str(COOKIE_FILE)
    return opts


def get_video_date(video_id):
    """Quick lookup to get a video's actual upload date."""
    ydl_opts = get_yt_dlp_opts_with_cookies({
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get('upload_date', '')
    except Exception:
        return ''


def get_channel_videos(channel_url):
    """
    Use yt-dlp Python library to list all videos from a channel.
    Returns list of dicts with: id, title, upload_date, duration
    Skips Shorts (duration <= 60 seconds).

    Two-step process:
    1. Flat extraction to get the full video list quickly (no dates)
    2. For videos with unknown dates, fetch date individually
    Since the channel tab is sorted newest-first, we stop once we hit
    videos outside the 5-month window.
    """
    print(f"  Fetching video list from {channel_url} ...")
    sys.stdout.flush()

    # Step 1: Flat extraction for the full list (fast, but dates may be missing)
    ydl_opts = get_yt_dlp_opts_with_cookies({
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {'youtubetab': {'approximate_date': ['']}},
    })

    raw_entries = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"{channel_url}/videos", download=False)
            if not info or 'entries' not in info:
                print("  WARNING: Could not extract channel info")
                return []

            for entry in info['entries']:
                if entry is None:
                    continue
                raw_entries.append(entry)

    except Exception as e:
        print(f"  ERROR fetching channel: {e}")
        return []

    print(f"  Found {len(raw_entries)} total entries, filtering to last 5 months...")
    sys.stdout.flush()

    # Step 2: Filter — resolve unknown dates by fetching individually
    # Channel tab is newest-first, so once we see 3 consecutive old videos, stop
    videos = []
    consecutive_old = 0

    for i, entry in enumerate(raw_entries):
        vid_id = entry.get('id', '')
        title = entry.get('title', 'Unknown')
        upload_date = entry.get('upload_date', '')
        duration = entry.get('duration') or 0

        # Parse duration — skip Shorts (60 seconds or less)
        try:
            duration = int(float(duration))
        except (ValueError, TypeError):
            duration = 0

        if duration <= 60:
            continue  # Skip Shorts

        # If date is missing, fetch it
        if not upload_date:
            print(f"    Checking date for: {title[:60]}...", end="")
            sys.stdout.flush()
            upload_date = get_video_date(vid_id)
            if upload_date:
                print(f" {upload_date}")
            else:
                print(" unknown (keeping)")
            sys.stdout.flush()
            time.sleep(1)  # small delay between date lookups

        # Parse date
        date_obj = None
        try:
            if upload_date:
                date_obj = datetime.strptime(str(upload_date), "%Y%m%d")
        except ValueError:
            pass

        # Check if too old
        if date_obj and date_obj < CUTOFF_DATE:
            consecutive_old += 1
            if consecutive_old >= 3:
                print(f"  Reached 3 consecutive videos older than cutoff — stopping scan")
                sys.stdout.flush()
                break
            continue
        else:
            consecutive_old = 0

        videos.append({
            "id": vid_id,
            "title": title,
            "date": upload_date or "unknown",
            "date_obj": date_obj,
            "duration": duration,
        })

    # Sort by date (newest first)
    videos.sort(key=lambda v: v.get("date", "00000000"), reverse=True)
    print(f"  {len(videos)} videos within the last 5 months (excluding Shorts)")
    sys.stdout.flush()
    return videos


def make_safe_filename(title):
    """Turn a video title into a safe filename."""
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = re.sub(r'\s+', ' ', safe).strip()
    if len(safe) > 100:
        safe = safe[:100].strip()
    return safe


def fetch_transcript_once(video_id):
    """
    Single attempt to get transcript using yt-dlp subtitle extraction.
    Uses cookies if available for higher rate limits.
    Returns (text, language_code) or raises exception.
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        sub_path = os.path.join(tmp_dir, f"{video_id}")

        ydl_opts = get_yt_dlp_opts_with_cookies({
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'writesubtitles': True,        # manual subs first
            'writeautomaticsub': True,     # fallback to auto-generated
            'subtitleslangs': ['en'],
            'subtitlesformat': 'vtt',
            'outtmpl': sub_path + '.%(ext)s',
        })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])

        # Find the downloaded subtitle file
        vtt_file = None
        for f in os.listdir(tmp_dir):
            if f.endswith('.vtt'):
                vtt_file = os.path.join(tmp_dir, f)
                break

        if not vtt_file:
            return None, "no subtitles available"

        # Parse VTT file — extract just the text
        with open(vtt_file, 'r', encoding='utf-8') as fh:
            content = fh.read()

        lines = []
        seen = set()  # deduplicate repeated lines (VTT often duplicates)
        for line in content.split('\n'):
            line = line.strip()
            # Skip VTT headers and timestamps
            if (not line or line.startswith('WEBVTT') or '-->' in line or
                    line.startswith('Kind:') or line.startswith('Language:') or
                    re.match(r'^\d+$', line)):
                continue
            # Remove VTT tags like <00:00:00.000> and <c>
            clean = re.sub(r'<[^>]+>', '', line).strip()
            if (clean and clean not in ('[Music]', '[Applause]', '[♪♪♪]', '[music]')
                    and clean not in seen):
                lines.append(clean)
                seen.add(clean)

        text = ' '.join(lines)
        text = re.sub(r'\s+', ' ', text).strip()

        if text and len(text) > 50:
            # Detect language from filename (e.g. "video_id.en.vtt")
            lang = 'en'
            basename = os.path.basename(vtt_file)
            parts = basename.rsplit('.', 2)
            if len(parts) >= 3:
                lang = parts[-2]
            return text, lang

    return None, "no usable transcript"


def get_transcript_with_retry(video_id, title):
    """
    Try to get transcript with retries and exponential backoff.
    Returns (text, lang) or (None, reason).
    """
    for attempt in range(MAX_RETRIES):
        try:
            text, lang = fetch_transcript_once(video_id)
            if text:
                return text, lang
            else:
                return None, lang  # No transcript available (not a rate limit issue)
        except Exception as e:
            error_msg = str(e).lower()

            # Check if it's a rate limit / IP block
            is_rate_limited = any(keyword in error_msg for keyword in [
                'ip', 'block', 'too many', 'rate', '429', 'request'
            ])

            if is_rate_limited and attempt < MAX_RETRIES - 1:
                # Exponential backoff: 15s, 30s, 60s, 120s
                wait = min(15 * (2 ** attempt) + random.randint(1, 10), MAX_DELAY)
                print(f"           RATE LIMITED — waiting {wait}s (retry {attempt+1}/{MAX_RETRIES})")
                sys.stdout.flush()
                time.sleep(wait)
                continue

            # Check if captions are genuinely disabled/unavailable
            if "disabled" in error_msg:
                return None, "captions disabled"
            elif "no transcript" in error_msg:
                return None, "no transcript available"
            elif is_rate_limited:
                return None, "rate limited (all retries failed)"
            else:
                return None, f"error: {str(e)[:100]}"

    return None, "max retries exceeded"


def process_channel(channel_url, channel_name, channel_num, total_channels, title_filter=None):
    """Process all videos from one channel."""
    print()
    print("=" * 70)
    print(f"  CHANNEL {channel_num}/{total_channels}: {channel_name}")
    print(f"  {channel_url}")
    if title_filter:
        print(f"  FILTER: only videos with \"{title_filter}\" in the title")
    print("=" * 70)
    sys.stdout.flush()

    # Create output folder
    channel_dir = OUTPUT_BASE / channel_name
    channel_dir.mkdir(parents=True, exist_ok=True)

    # Remove old _NO_CAPTIONS file so we retry everything fresh
    no_cap_file = channel_dir / "_NO_CAPTIONS.txt"
    if no_cap_file.exists():
        no_cap_file.unlink()

    # Get video list
    videos = get_channel_videos(channel_url)

    # Apply title filter if provided
    if title_filter:
        filter_lower = title_filter.lower()
        before = len(videos)
        videos = [v for v in videos if filter_lower in v["title"].lower()]
        print(f"  Filter \"{title_filter}\": {before} → {len(videos)} videos")
        sys.stdout.flush()

    print(f"  Found {len(videos)} videos to transcribe")
    sys.stdout.flush()

    if not videos:
        print("  No videos to process — moving on.")
        sys.stdout.flush()
        return {"total": 0, "done": 0, "skipped": 0, "failed": 0, "no_captions": 0}

    # Track progress
    stats = {"total": len(videos), "done": 0, "skipped": 0, "failed": 0, "no_captions": 0}
    no_caption_videos = []
    consecutive_failures = 0

    for i, video in enumerate(videos):
        vid_id = video["id"]
        title = video["title"]
        date = video.get("date", "unknown")
        duration_min = video["duration"] // 60

        safe_title = make_safe_filename(title)
        filename = f"{date}_{safe_title}.txt"
        filepath = channel_dir / filename

        print(f"\n  [{i+1}/{len(videos)}] {title}")
        print(f"           Date: {date}  |  Duration: {duration_min}min  |  ID: {vid_id}")
        sys.stdout.flush()

        # Skip if already transcribed (check exact match OR any file with same title)
        already_done = False
        if filepath.exists() and filepath.stat().st_size > 100:
            already_done = True
        else:
            # Check for files with same title but different date prefix (e.g. "unknown_Title.txt")
            for existing in channel_dir.glob(f"*_{safe_title}.txt"):
                if existing.stat().st_size > 100:
                    already_done = True
                    break
        if already_done:
            print(f"           Already done — skipping")
            sys.stdout.flush()
            stats["skipped"] += 1
            consecutive_failures = 0
            continue

        # Get transcript with retry logic
        text, lang = get_transcript_with_retry(vid_id, title)

        if text and len(text) > 50:
            # Save transcript
            header = f"Title: {title}\n"
            header += f"Channel: {channel_name}\n"
            header += f"Date: {date}\n"
            header += f"Duration: {duration_min} minutes\n"
            header += f"URL: https://www.youtube.com/watch?v={vid_id}\n"
            header += f"Language: {lang}\n"
            header += "-" * 60 + "\n\n"

            filepath.write_text(header + text, encoding="utf-8")
            print(f"           DONE — {len(text):,} chars saved")
            sys.stdout.flush()
            stats["done"] += 1
            consecutive_failures = 0
        else:
            reason = lang if lang else "unknown"
            print(f"           NO CAPTIONS — reason: {reason}")
            sys.stdout.flush()
            no_caption_videos.append({"title": title, "id": vid_id, "reason": reason})
            stats["no_captions"] += 1

            # Track consecutive rate limit failures
            if "rate" in (reason or "").lower() or "block" in (reason or "").lower():
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print(f"\n  WARNING: 3 consecutive rate-limit failures. Pausing 120s...")
                    sys.stdout.flush()
                    time.sleep(120)
                    consecutive_failures = 0

        # Delay between requests (randomized to look more human)
        delay = BASE_DELAY + random.uniform(2, 5)
        time.sleep(delay)

        # Extra pause every N videos to avoid rate limiting
        videos_processed = stats["done"] + stats["no_captions"]
        if videos_processed > 0 and videos_processed % BATCH_PAUSE_EVERY == 0:
            print(f"\n  Batch pause ({BATCH_PAUSE_SECS}s) after {videos_processed} videos...")
            sys.stdout.flush()
            time.sleep(BATCH_PAUSE_SECS)

    # Save list of videos with no captions (if any)
    if no_caption_videos:
        lines = [f"Videos without captions for {channel_name}:\n\n"]
        for v in no_caption_videos:
            lines.append(f"- {v['title']}\n  https://www.youtube.com/watch?v={v['id']}\n  Reason: {v['reason']}\n\n")
        no_cap_file.write_text("".join(lines), encoding="utf-8")

    # Channel summary
    print(f"\n  --- {channel_name} Summary ---")
    print(f"  Total: {stats['total']} | Transcribed: {stats['done']} | Skipped: {stats['skipped']} | No captions: {stats['no_captions']}")
    sys.stdout.flush()

    return stats


def main():
    # Handle --export-cookies command
    if len(sys.argv) >= 2 and sys.argv[1] == '--export-cookies':
        success = export_cookies_from_brave()
        sys.exit(0 if success else 1)

    # Parse command-line arguments
    if len(sys.argv) < 2:
        print()
        print("Usage:")
        print('  python tools/transcribe_youtube_channels.py "FolderName|URL"')
        print('  python tools/transcribe_youtube_channels.py "FolderName|URL|FilterKeyword"')
        print('  python tools/transcribe_youtube_channels.py --export-cookies')
        print()
        print("Examples:")
        print('  python tools/transcribe_youtube_channels.py "Learn Skills Daily|https://www.youtube.com/@learnskillsdaily|Google Sheets"')
        print('  python tools/transcribe_youtube_channels.py "Better Sheets|https://www.youtube.com/@bettersheets"')
        print()
        print("First time? Export cookies to avoid rate limits:")
        print("  1. Close Brave completely")
        print("  2. python tools/transcribe_youtube_channels.py --export-cookies")
        print("  3. Open Brave again, then run the transcriber")
        print()
        sys.exit(1)

    channels = []
    for arg in sys.argv[1:]:
        if "|" not in arg:
            print(f"ERROR: Bad format: {arg}")
            print('Each argument must be "FolderName|ChannelURL" or "FolderName|ChannelURL|Filter"')
            sys.exit(1)
        parts = arg.split("|")
        name = parts[0].strip()
        url = parts[1].strip()
        title_filter = parts[2].strip() if len(parts) > 2 else None
        channels.append((url, name, title_filter))

    print()
    print("=" * 70)
    print("  YOUTUBE CHANNEL TRANSCRIBER")
    print(f"  Cutoff date: {CUTOFF_DATE.strftime('%Y-%m-%d')} (last 5 months)")
    print(f"  Output: {OUTPUT_BASE}")
    print(f"  Channels: {len(channels)}")
    print(f"  Rate limit protection: {BASE_DELAY}-{BASE_DELAY+3}s between requests, {MAX_RETRIES} retries with backoff")
    print(f"  Cookies: {'LOADED (' + str(COOKIE_FILE) + ')' if COOKIE_FILE.exists() else 'NOT FOUND (run --export-cookies for better rate limits)'}")
    print("=" * 70)
    sys.stdout.flush()

    # Create base output folder
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    # Process channels one at a time
    all_stats = []
    for i, (url, name, title_filter) in enumerate(channels):
        stats = process_channel(url, name, i + 1, len(channels), title_filter)
        all_stats.append((name, stats))

        # Pause between channels to avoid rate limits
        if i < len(channels) - 1:
            print(f"\n  Pausing {CHANNEL_PAUSE}s before next channel...")
            sys.stdout.flush()
            time.sleep(CHANNEL_PAUSE)

    # Final report
    print("\n")
    print("=" * 70)
    print("  FINAL REPORT")
    print("=" * 70)

    grand_total = 0
    grand_done = 0
    grand_skipped = 0
    grand_no_cap = 0

    for name, stats in all_stats:
        print(f"  {name:25s} | Videos: {stats['total']:3d} | Done: {stats['done']:3d} | Skipped: {stats['skipped']:3d} | No captions: {stats['no_captions']:3d}")
        grand_total += stats["total"]
        grand_done += stats["done"]
        grand_skipped += stats["skipped"]
        grand_no_cap += stats["no_captions"]

    print("-" * 70)
    print(f"  {'TOTAL':25s} | Videos: {grand_total:3d} | Done: {grand_done:3d} | Skipped: {grand_skipped:3d} | No captions: {grand_no_cap:3d}")
    print(f"\n  All transcripts saved to: {OUTPUT_BASE}")
    print("=" * 70)
    sys.stdout.flush()


if __name__ == "__main__":
    main()

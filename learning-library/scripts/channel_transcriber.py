"""Channel transcriber — pull English captions for every video on a YouTube channel.

Built from the learning-system youtube_transcriber.py + project-test's
youtube-rate-limit-tricks.md lessons:
- pace caption requests (YouTube blocks timedtext after ~13 rapid hits)
- exponential backoff on failures
- resumable via a state file (rerun continues where it stopped)

Usage:
    python channel_transcriber.py --channel https://www.youtube.com/@Handle --out ../channels/luke-iha
    python channel_transcriber.py --channel CHANNEL_URL --limit 5   # small test batch
"""

from __future__ import annotations

import argparse
import json
import random
import re
import tempfile
import time
from pathlib import Path

import yt_dlp

STATE_FILE = "state.json"
COOKIE_FILE = "youtube_cookies.txt"  # next to this script's --out folder
MIN_DELAY = 5.0  # logged-in pacing (anonymous blocked after ~13 rapid)
MAX_DELAY = 10.0


def safe_name(value: str) -> str:
    value = value.replace("\\", "")
    return re.sub(r"\s+", " ", re.sub(r'[<>:"/|?*]', "", value)).strip()[:90] or "untitled"


def channel_videos(channel_url: str, limit: int | None) -> list[dict]:
    options = {"extract_flat": "in_playlist", "quiet": True, "no_warnings": True}
    if limit:
        options["playlistend"] = limit
    url = channel_url.rstrip("/")
    if "/videos" not in url:
        url += "/videos"
    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(url, download=False)
    entries = [
        {
            "id": e["id"],
            "title": e.get("title", ""),
            "url": f"https://www.youtube.com/watch?v={e['id']}",
            "duration": e.get("duration") or 0,
        }
        for e in (data or {}).get("entries", [])
        if e
    ]
    return entries


def fetch_caption(video_url: str, language: str) -> tuple[str | None, dict]:
    """Download the caption track (json3) and return joined text + video info."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output = str(Path(temp_dir) / "caption")
        options = {
            "writeautomaticsub": True,
            "writesubtitles": True,
            "subtitleslangs": [language],
            "subtitlesformat": "json3",
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "outtmpl": output,
            "ignore_no_formats_error": True,
            # rate-limit bypass (project-test lessons): cookies + JS challenge solver
            "cookiefile": str(COOKIE_FILE),
            "js_runtimes": {"node": {}},
            "remote_components": ["ejs:github"],
        }
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(video_url, download=True)
        files = list(Path(temp_dir).glob("*.json3"))
        if not files:
            return None, info or {}
        document = json.loads(files[0].read_text(encoding="utf-8"))
        parts: list[str] = []
        for event in document.get("events", []):
            text = "".join(segment.get("utf8", "") for segment in event.get("segs", []))
            text = text.replace("\n", " ").strip()
            if text and text not in parts:
                parts.append(text)
        return (" ".join(parts) or None), info or {}


def write_transcript(text: str, info: dict, out_dir: Path, language: str) -> Path:
    video_id = info.get("id", "video")
    title = info.get("title", video_id)
    header = "\n".join([
        f"Title: {title}",
        f"Channel: {info.get('channel') or info.get('uploader') or 'unknown'}",
        f"Published: {info.get('upload_date') or 'unknown'}",
        f"Duration: {info.get('duration') or '?'}s",
        f"URL: {info.get('webpage_url') or ''}",
        f"Caption source: {language} captions (YouTube)",
        "", "---", "",
    ])
    path = out_dir / f"{video_id}_{safe_name(title)}.txt"
    path.write_text(header + text, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe a YouTube channel via captions")
    parser.add_argument("--channel", required=True, help="YouTube channel URL")
    parser.add_argument("--out", required=True, help="Output folder (transcripts go to <out>/transcripts)")
    parser.add_argument("--language", default="en")
    parser.add_argument("--limit", type=int, default=None, help="Only first N videos (for testing)")
    args = parser.parse_args()

    out_dir = Path(args.out)
    transcript_dir = out_dir / "transcripts"
    transcript_dir.mkdir(parents=True, exist_ok=True)
    state_path = out_dir / STATE_FILE
    cookie_path = Path(__file__).parent / "youtube_cookies.txt"
    if cookie_path.exists():
        global COOKIE_FILE
        COOKIE_FILE = cookie_path
        print(f"Using cookies: {cookie_path}")
    else:
        print("WARNING: no cookies file found - anonymous mode (will hit rate limits)")

    state: dict = {"done": {}, "failed": {}}
    if state_path.exists():
        state.update(json.loads(state_path.read_text(encoding="utf-8")))

    videos = channel_videos(args.channel, args.limit)
    print(f"Channel videos found: {len(videos)}")
    todo = [v for v in videos if v["id"] not in state["done"]]
    print(f"Already done: {len(videos) - len(todo)} | To fetch: {len(todo)}")

    for index, video in enumerate(todo, 1):
        title = video["title"][:60]
        for attempt in range(1, 4):
            try:
                text, info = fetch_caption(video["url"], args.language)
                if text:
                    path = write_transcript(text, info, transcript_dir, args.language)
                    state["done"][video["id"]] = {"title": video["title"], "file": path.name}
                    print(f"[{index}/{len(todo)}] OK: {title}")
                else:
                    state["failed"][video["id"]] = {"title": video["title"], "error": "no caption track"}
                    print(f"[{index}/{len(todo)}] NO CAPTIONS: {title}")
                break
            except Exception as exc:
                wait = 30 * attempt + random.uniform(0, 10)
                print(f"[{index}/{len(todo)}] ERROR ({exc}); retry in {wait:.0f}s")
                time.sleep(wait)
        else:
            state["failed"][video["id"]] = {"title": video["title"], "error": "retries exhausted"}

        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        if index < len(todo):
            pause = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"    pacing pause {pause:.0f}s")
            time.sleep(pause)

    print(f"\nDONE. Transcripts: {transcript_dir}")
    print(f"OK: {len(state['done'])} | Failed: {len(state['failed'])}")


if __name__ == "__main__":
    main()

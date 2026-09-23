"""Fetch caption tracks for one YouTube video or a small channel batch.

This is adapted from the proven project-test bulk workflow. It uses yt-dlp to
retrieve captions only; it never downloads the video stream.
"""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import yt_dlp


def safe_name(value: str) -> str:
    value = value.replace("\\", "")
    return re.sub(r"\s+", " ", re.sub(r'[<>:"/|?*]', "", value)).strip()[:100] or "untitled"


def extract_caption_text(video_url: str, language: str) -> tuple[str | None, dict]:
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
            "extractor_args": {"youtube": {"player_client": ["android_vr"]}},
            "ignore_no_formats_error": True,
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
        return " ".join(parts) or None, info or {}


def write_transcript(text: str, info: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    video_id = info.get("id", "video")
    title = info.get("title", video_id)
    path = output_dir / f"{video_id}_{safe_name(title)}.txt"
    header = "\n".join([
        f"Title: {title}",
        f"Channel: {info.get('channel') or info.get('uploader') or 'unknown'}",
        f"Published: {info.get('upload_date') or 'unknown'}",
        f"URL: {info.get('webpage_url') or ''}",
        "", "---", "",
    ])
    path.write_text(header + text, encoding="utf-8")
    return path


def channel_entries(url: str, months: int, limit: int) -> list[dict]:
    cutoff = datetime.now() - timedelta(days=months * 30)
    options = {"extract_flat": "in_playlist", "playlistend": limit, "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(options) as downloader:
        data = downloader.extract_info(url.rstrip("/") + "/videos", download=False)
    entries: list[dict] = []
    for entry in (data or {}).get("entries", []):
        if not entry or (entry.get("duration") or 0) <= 60:
            continue
        date = entry.get("upload_date")
        if date:
            try:
                if datetime.strptime(date, "%Y%m%d") < cutoff:
                    continue
            except ValueError:
                pass
        entries.append(entry)
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Save YouTube caption transcripts")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="One YouTube video URL")
    source.add_argument("--channel", help="YouTube channel URL")
    parser.add_argument("--output", default="learning-library/raw/youtube")
    parser.add_argument("--language", default="en")
    parser.add_argument("--months", type=int, default=3)
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()
    output = Path(args.output)
    urls = [args.url] if args.url else [f"https://www.youtube.com/watch?v={item['id']}" for item in channel_entries(args.channel, args.months, args.limit)]
    for url in urls:
        text, info = extract_caption_text(url, args.language)
        if not text:
            print(f"No {args.language} caption track: {url}")
            continue
        print(write_transcript(text, info, output))


if __name__ == "__main__":
    main()

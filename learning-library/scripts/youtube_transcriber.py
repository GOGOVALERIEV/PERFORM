"""
youtube_transcriber.py — pull the transcript (captions) of one YouTube video.

Used by uni-app Transcribe Bot:  python youtube_transcriber.py <youtube_url>
Prints the clean transcript text to stdout. Optional: --out <file> to also save.

Uses yt_dlp (same engine as channel_transcriber.py): manual subs first,
auto-generated as fallback. Output: one subtitle line per row, duplicates
(auto-caption rolling window) removed.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yt_dlp


def parse_vtt(path: Path) -> str:
    """VTT -> plain text, deduped (auto-captions repeat lines on each cue)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = []
    seen = set()
    for line in raw.splitlines():
        line = line.strip()
        if not line or line == "WEBVTT" or "-->" in line:
            continue
        if re.match(r"^[0-9]+$", line):  # cue numbers
            continue
        if line.startswith("[") or line.startswith("(") and line.endswith(")"):
            continue  # [Music], (applause) markers etc. — keep? drop noise
        line = re.sub(r"<[^>]+>", "", line)  # strip inline tags
        if line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return "\n".join(lines)


def fetch_transcript(url: str, langs=("bg", "en")) -> tuple[str, str]:
    """Returns (video_title, transcript_text). Uses saved cookies if present (higher rate limits)."""
    tmp = Path(tempfile.mkdtemp(prefix="yttrans_"))
    opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": list(langs),
        "subtitlesformat": "vtt",
        "outtmpl": str(tmp / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    cookie_file = Path(__file__).parent / "youtube_cookies.txt"
    if cookie_file.exists() and cookie_file.stat().st_size > 100:
        opts["cookiefile"] = str(cookie_file)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        vid = info.get("id", "video")

    vtts = sorted(tmp.glob("*.vtt"), key=lambda p: (0 if "bg" in p.name else 1))
    if not vtts:
        print(f"NO_SUBTITLES: no captions found for {title}", file=sys.stderr)
        sys.exit(2)

    text = parse_vtt(vtts[0])
    if not text.strip():
        print(f"NO_SUBTITLES: caption file empty for {title}", file=sys.stderr)
        sys.exit(2)
    return title, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default=None, help="also save transcript to this file")
    args = ap.parse_args()

    title, text = fetch_transcript(args.url)
    output = f"# {title}\n\n{text}\n"
    print(output)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()

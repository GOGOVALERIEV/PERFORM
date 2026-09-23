"""Pull every video from the Luke Iha YouTube channel and extract all links
(especially Google Docs) from each video's description.

Output: learning-library/raw/youtube/luke_iha_links.md
"""

from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yt_dlp

CHANNEL_ID = "UCH6T9yyI_SqV_H25Y4I7FKQ"
OUTPUT = Path(__file__).resolve().parents[1] / "raw" / "youtube" / "luke_iha_links.md"
CACHE = Path(__file__).resolve().parents[1] / "raw" / "youtube" / "luke_iha_descriptions.json"

URL_RE = re.compile(r"https?://[^\s\)\]\>\"']+|docs\.google\.com/[^\s\)\]\>\"']+")


def channel_videos() -> list[dict]:
    options = {"extract_flat": "in_playlist", "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(f"https://www.youtube.com/channel/{CHANNEL_ID}/videos", download=False)
    return [
        {"id": e["id"], "title": e.get("title", ""), "url": f"https://www.youtube.com/watch?v={e['id']}"}
        for e in (data or {}).get("entries", [])
        if e
    ]


def fetch_description(video: dict) -> dict:
    options = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": ["android_vr"]}},
        "ignore_no_formats_error": True,
    }
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(video["url"], download=False)
            return {
                "id": video["id"],
                "title": info.get("title", video["title"]),
                "url": video["url"],
                "published": info.get("upload_date", ""),
                "view_count": info.get("view_count", 0),
                "description": info.get("description", "") or "",
            }
        except Exception as exc:  # retry with backoff
            if attempt == 2:
                print(f"FAILED {video['id']}: {exc}")
                return {**video, "description": "", "error": str(exc)}
            time.sleep(3 * (attempt + 1))
    return video


def main() -> None:
    videos = channel_videos()
    print(f"Channel videos: {len(videos)}")

    # Reuse cache if a previous run was interrupted
    done: dict[str, dict] = {}
    if CACHE.exists():
        done = {v["id"]: v for v in json.loads(CACHE.read_text(encoding="utf-8"))}
        print(f"Resuming: {len(done)} already fetched")

    todo = [v for v in videos if v["id"] not in done]
    print(f"To fetch: {len(todo)}")

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(fetch_description, v) for v in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            result = fut.result()
            done[result["id"]] = result
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(list(done.values()), ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[{i}/{len(todo)}] {result.get('title', result['id'])[:70]}")

    ordered = [done[v["id"]] for v in videos if v["id"] in done]

    lines = [
        "# Luke Iha — All Video Links + Description Sauce",
        "",
        f"Channel: https://www.youtube.com/channel/{CHANNEL_ID}",
        f"Pulled: {time.strftime('%Y-%m-%d %H:%M')}",
        f"Videos: {len(ordered)}",
        "",
        "---",
        "",
        "## Quick index — every Google Doc / Notion / freebie link found",
        "",
    ]

    doc_index: list[str] = []
    for v in ordered:
        for url in URL_RE.findall(v.get("description", "")):
            if "docs.google.com" in url or "notion" in url:
                doc_index.append(f"- [{v['title']}]({v['url']}) → {url}")

    lines.extend(doc_index if doc_index else ["_(none found)_"])
    lines.extend(["", "---", ""])

    for v in ordered:
        desc = v.get("description", "")
        urls = URL_RE.findall(desc)
        lines.extend([f"## {v['title']}", f"- URL: {v['url']}", f"- Published: {v.get('published', '?')}"])
        if urls:
            lines.append("- Links in description:")
            lines.extend([f"  - {u}" for u in urls])
        if desc.strip():
            lines.extend(["", "**Description:**", "", "```", desc.strip(), "```"])
        lines.extend(["", "---", ""])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSaved: {OUTPUT}")
    print(f"Google Doc links found: {sum(1 for d in doc_index)}")


if __name__ == "__main__":
    main()

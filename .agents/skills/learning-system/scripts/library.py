"""Small, dependency-free manifest for the PERFORM learning library."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_LIBRARY = Path("learning-library")


def safe_name(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in " ._-" else "_" for char in name)
    return cleaned.strip(" .") or "untitled"


def append_manifest(library: Path, record: dict) -> None:
    library.mkdir(parents=True, exist_ok=True)
    manifest = library / "manifest.jsonl"
    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_file(args: argparse.Namespace) -> None:
    source = Path(args.file).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Not a file: {source}")
    library = Path(args.library)
    destination_dir = library / "raw" / args.kind
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / safe_name(source.name)
    if destination.exists() and file_digest(destination) != file_digest(source):
        destination = destination_dir / f"{destination.stem}-{file_digest(source)[:10]}{destination.suffix}"
    if not destination.exists():
        shutil.copy2(source, destination)
    append_manifest(library, {
        "id": file_digest(destination),
        "added_at": datetime.now(timezone.utc).isoformat(),
        "kind": args.kind,
        "title": args.title or source.stem,
        "source_url": args.source_url,
        "path": destination.as_posix(),
        "sha256": file_digest(destination),
    })
    print(destination)


def add_text(args: argparse.Namespace) -> None:
    library = Path(args.library)
    destination_dir = library / "raw" / args.kind
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{safe_name(args.title)}.txt"
    destination.write_text(args.text, encoding="utf-8")
    append_manifest(library, {
        "id": file_digest(destination),
        "added_at": datetime.now(timezone.utc).isoformat(),
        "kind": args.kind,
        "title": args.title,
        "source_url": args.source_url,
        "path": destination.as_posix(),
        "sha256": file_digest(destination),
    })
    print(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Register PERFORM learning material")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY))
    subparsers = parser.add_subparsers(required=True)

    file_parser = subparsers.add_parser("add-file")
    file_parser.add_argument("file")
    file_parser.add_argument("--kind", default="local")
    file_parser.add_argument("--title")
    file_parser.add_argument("--source-url")
    file_parser.set_defaults(func=add_file)

    text_parser = subparsers.add_parser("add-text")
    text_parser.add_argument("title")
    text_parser.add_argument("text")
    text_parser.add_argument("--kind", default="note")
    text_parser.add_argument("--source-url")
    text_parser.set_defaults(func=add_text)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

"""Import explicitly requested files from MEGA without storing credentials in code."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def logged_in_mega():
    try:
        from mega import Mega
    except ImportError as error:
        raise SystemExit("Install the mega.py package first: pip install mega.py") from error
    email = os.environ.get("MEGA_EMAIL")
    password = os.environ.get("MEGA_PASSWORD")
    if not email or not password:
        raise SystemExit("Set MEGA_EMAIL and MEGA_PASSWORD in the session environment; do not put them in a script.")
    return Mega().login(email, password)


def main() -> None:
    parser = argparse.ArgumentParser(description="List or import an explicitly requested MEGA path")
    parser.add_argument("path", help="Exact MEGA path, file name, or share link")
    parser.add_argument("--output", default="learning-library/raw/mega")
    parser.add_argument("--list", action="store_true", help="List matching item(s) without downloading")
    args = parser.parse_args()
    client = logged_in_mega()
    item = client.find(args.path)
    if not item:
        raise SystemExit(f"No MEGA item found for: {args.path}")
    if args.list:
        print(item)
        return
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    downloaded = client.download(item, dest_path=str(output))
    print(downloaded)


if __name__ == "__main__":
    main()

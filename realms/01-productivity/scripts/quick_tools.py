"""
Quick Tools — Useful utilities George can use daily.
Run any function from Claude Code or import into other scripts.

Usage from Claude Code:
  python scripts/quick_tools.py screenshot
  python scripts/quick_tools.py clipboard "text to copy"
  python scripts/quick_tools.py organize_downloads
"""
import sys
import os
import shutil
from datetime import datetime

# === SCREENSHOT TOOL ===
def take_screenshot(filename=None):
    """Take a screenshot and save to Desktop."""
    try:
        import pyautogui
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print(f"Screenshot saved: {path}")
        return path
    except Exception as e:
        print(f"Error: {e}")
        return None

# === ORGANIZE DOWNLOADS ===
def organize_downloads():
    """Sort Downloads folder into subfolders by file type."""
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        "Spreadsheets": [".xls", ".xlsx", ".csv"],
        "Presentations": [".ppt", ".pptx", ".key"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Installers": [".exe", ".msi", ".dmg"],
        "Code": [".py", ".js", ".html", ".css", ".json", ".md"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    }

    moved = 0
    for filename in os.listdir(downloads):
        filepath = os.path.join(downloads, filename)
        if os.path.isdir(filepath):
            continue

        ext = os.path.splitext(filename)[1].lower()
        target_folder = "Other"

        for category, extensions in categories.items():
            if ext in extensions:
                target_folder = category
                break

        target_dir = os.path.join(downloads, target_folder)
        os.makedirs(target_dir, exist_ok=True)

        target_path = os.path.join(target_dir, filename)
        if not os.path.exists(target_path):
            shutil.move(filepath, target_path)
            moved += 1

    print(f"Organized {moved} files in Downloads folder.")
    return moved

# === DISK SPACE CHECK ===
def check_disk_space():
    """Show disk space usage for main drives."""
    for drive in ['C:']:
        try:
            total, used, free = shutil.disk_usage(drive + '/')
            print(f"\nDrive {drive}")
            print(f"  Total: {total // (1024**3)} GB")
            print(f"  Used:  {used // (1024**3)} GB ({used/total*100:.1f}%)")
            print(f"  Free:  {free // (1024**3)} GB ({free/total*100:.1f}%)")
        except Exception as e:
            print(f"  Error reading {drive}: {e}")

# === LIST BIG FILES ===
def find_big_files(path=None, min_mb=100):
    """Find files larger than min_mb in a directory."""
    if not path:
        path = os.path.expanduser("~")

    big_files = []
    print(f"Scanning {path} for files > {min_mb}MB...")

    for root, dirs, files in os.walk(path):
        # Skip system/hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '.git', 'AppData']]
        for f in files:
            try:
                fp = os.path.join(root, f)
                size = os.path.getsize(fp)
                if size > min_mb * 1024 * 1024:
                    big_files.append((fp, size))
            except (PermissionError, OSError):
                continue

    big_files.sort(key=lambda x: x[1], reverse=True)

    print(f"\nFound {len(big_files)} files > {min_mb}MB:")
    for fp, size in big_files[:20]:
        print(f"  {size // (1024**2):>6} MB  {fp}")

    return big_files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Quick Tools — Available commands:")
        print("  python scripts/quick_tools.py screenshot")
        print("  python scripts/quick_tools.py organize_downloads")
        print("  python scripts/quick_tools.py disk_space")
        print("  python scripts/quick_tools.py big_files [path] [min_mb]")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "screenshot":
        take_screenshot()
    elif cmd == "organize_downloads":
        organize_downloads()
    elif cmd == "disk_space":
        check_disk_space()
    elif cmd == "big_files":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        min_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        find_big_files(path, min_mb)
    else:
        print(f"Unknown command: {cmd}")

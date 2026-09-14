#!/usr/bin/env python3
"""Clean up test artifacts from Tony Stark run."""
import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

# 1. Delete Google Calendar events created today
print("="*60)
print("DELETING GOOGLE CALENDAR EVENTS")
print("="*60)

try:
    from google_helper import get_calendar
    cal = get_calendar()
    now = datetime.now(timezone.utc)
    start = (now - timedelta(hours=20)).isoformat()
    end = (now + timedelta(hours=12)).isoformat()

    events = cal.events().list(calendarId='primary', timeMin=start, timeMax=end, singleEvents=True).execute().get('items', [])
    today = now.astimezone().date()
    deleted = 0
    for e in events:
        s = e['start'].get('dateTime')
        if s:
            sd = datetime.fromisoformat(s)
            if sd.astimezone().date() == today:
                desc = e.get('description', '')
                summary = e.get('summary', '')
                if 'Tony Stark auto-block' in desc or summary in ['DEEP WORK (fresh brain)', 'Habits', 'GRIT WORK (determination)']:
                    cal.events().delete(calendarId='primary', eventId=e['id']).execute()
                    print(f"   ✅ Deleted: {summary}")
                    deleted += 1
    print(f"\n   Total deleted: {deleted}")
except Exception as e:
    print(f"   ⚠️ Calendar cleanup failed: {e}")

# 2. Wipe Clockify entries
print("\n" + "="*60)
print("WIPING CLOCKIFY ENTRIES")
print("="*60)

try:
    import json, urllib.request
    env = {}
    with open(BASE / 'config' / '.env', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k] = v

    API_KEY = env.get('CLOCKIFY_API_KEY', '')
    WORKSPACE = env.get('CLOCKIFY_WORKSPACE_ID', '')

    req = urllib.request.Request(
        "https://api.clockify.me/api/v1/user",
        headers={'X-Api-Key': API_KEY}
    )
    with urllib.request.urlopen(req) as r:
        uid = json.loads(r.read().decode())['id']

    start = (datetime.now(timezone.utc) - timedelta(hours=20)).strftime('%Y-%m-%dT%H:%M:%SZ')
    req2 = urllib.request.Request(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE}/user/{uid}/time-entries?start={start}&page-size=200",
        headers={'X-Api-Key': API_KEY}
    )
    with urllib.request.urlopen(req2) as r:
        entries = json.loads(r.read().decode())

    for e in entries:
        del_req = urllib.request.Request(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE}/time-entries/{e['id']}",
            method='DELETE',
            headers={'X-Api-Key': API_KEY}
        )
        urllib.request.urlopen(del_req)

    print(f"   ✅ Wiped {len(entries)} Clockify entries")
except Exception as e:
    print(f"   ⚠️ Clockify cleanup failed: {e}")

# 3. Delete test state files
print("\n" + "="*60)
print("DELETING TEST STATE FILES")
print("="*60)

state_dir = BASE / 'state'
today_str = datetime.now(timezone.utc).astimezone().date().isoformat()
deleted_files = 0
for f in state_dir.glob('*.json'):
    if today_str in f.name or 'chat-answers' in f.name:
        f.unlink()
        print(f"   ✅ Deleted: {f.name}")
        deleted_files += 1
print(f"\n   Total deleted: {deleted_files}")

# 4. Clean up Daily.md test entries
print("\n" + "="*60)
print("CLEANING DAILY.MD TEST ENTRIES")
print("="*60)

try:
    ob_dir = Path.home() / 'Desktop' / 'personal-ob' / 'Goals'
    daily_path = ob_dir / 'Daily.md'
    if daily_path.exists():
        with open(daily_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove all September 14, 2026 entries
        marker = "## September 14, 2026"
        while marker in content:
            start = content.find(marker)
            end = content.find("\n## ", start + 1)
            if end == -1:
                end = len(content)
            removed = content[start:end]
            content = content[:start] + content[end:]
            # Extract the day name for logging
            name_line = removed.split('\n')[0] if removed else ""
            print(f"   ✅ Removed: {name_line.strip()}")

        with open(daily_path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("   Daily.md cleaned")
except Exception as e:
    print(f"   ⚠️ Daily.md cleanup failed: {e}")

print("\n" + "="*60)
print("CLEANUP COMPLETE")
print("="*60)

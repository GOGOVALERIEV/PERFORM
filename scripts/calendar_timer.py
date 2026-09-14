"""
Calendar Timer Bridge — makes Clockify follow Google Calendar automatically.

THE IDEA:
  Google Calendar says what you SHOULD be doing right now.
  Clockify records what the timer is actually running on.
  This script checks every minute and keeps them in sync:
    - A calendar event is happening now  -> a Clockify timer runs with that event's name
    - The event changes                  -> old timer stops, new one starts
    - No event happening                 -> timer stops

USAGE:
  python scripts/calendar_timer.py          # run forever (check every 60s)
  python scripts/calendar_timer.py --once   # do ONE sync check, then exit (for testing)

It logs everything to output/calendar_timer.log so you can see what it did.
"""
import sys, io
# UTF-8 fix — but under pythonw.exe (no console window) sys.stdout is None, so guard for that.
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
if sys.stderr is not None and (getattr(sys.stderr, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

import os
import json
import time
import urllib.request
from datetime import datetime, timezone, timedelta

from pathlib import Path
PROJECT = str(Path(__file__).resolve().parent.parent)
LOG_PATH = os.path.join(PROJECT, "output", "calendar_timer.log")
CHECK_EVERY_SECONDS = 60

# ---------- load API key from .env ----------
env = {}
with open(os.path.join(PROJECT, "config", ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v

API_KEY = env["CLOCKIFY_API_KEY"]
WORKSPACE = env["CLOCKIFY_WORKSPACE_ID"]

# ---------- project tagging ----------
# Load the project name -> id map (created by scripts/_setup_projects.py once).
PROJECTS = {}
_pj_path = os.path.join(PROJECT, "config", "clockify_projects.json")
if os.path.exists(_pj_path):
    with open(_pj_path, encoding="utf-8") as f:
        PROJECTS = json.load(f)

# Rules: if the event title contains any of these words, tag it with that project.
# First matching rule wins, so order matters (most specific first).
PROJECT_RULES = [
    (("eat", "lunch", "dinner", "break", "food", "rest", "nap"), "Break"),
    (("twitter", "english", "habit", "gym", "walk", "workout"), "Habits"),
    (("errand", "money", "card", "bank", "personal", "reach out", "friend",
      "groceries", "clean", "appointment"), "Personal"),
    (("ad", "ads", "badar", "boris", "upload", "batch", "outreach", "client",
      "meta", "offer", "portfolio"), "Work"),
    (("learn", "docs", "course", "read", "video", "main block", "study",
      "angles", "hooks", "quiz", "lfs", "machine"), "Learning"),
]

def project_for(title):
    """Pick the project id for an event title based on keywords. None if no match."""
    t = (title or "").lower()
    for keys, name in PROJECT_RULES:
        if any(k in t for k in keys):
            return PROJECTS.get(name)
    return None

# ---------- tiny helpers ----------
def log(msg):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    if sys.stdout is not None:
        print(line)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def clockify(path, method="GET", body=None):
    """Call the Clockify REST API. Returns parsed JSON (or None for empty replies)."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        "https://api.clockify.me/api/v1" + path,
        data=data,
        method=method,
        headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        raw = r.read().decode("utf-8")
        return json.loads(raw) if raw else None

def utc_now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------- the three questions the loop asks ----------
def current_calendar_event(cal):
    """What event is happening RIGHT NOW on the primary calendar?
    Returns its title, or None. All-day events are ignored (they're not time blocks).
    If events overlap, the one that started most recently wins."""
    # Window must have width: Google returns NOTHING if timeMin == timeMax,
    # so we ask "what overlaps the next 1 second".
    now = datetime.now(timezone.utc)
    items = cal.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=(now + timedelta(seconds=1)).isoformat(),
        singleEvents=True,
    ).execute().get("items", [])
    timed = [e for e in items if "dateTime" in e.get("start", {})]
    if not timed:
        return None
    timed.sort(key=lambda e: e["start"]["dateTime"])
    return timed[-1].get("summary", "(no title)")

def running_timer():
    """What Clockify timer is running right now? Returns its description, or None."""
    uid = clockify("/user")["id"]
    entries = clockify(f"/workspaces/{WORKSPACE}/user/{uid}/time-entries?in-progress=true")
    return entries[0]["description"] if entries else None

def stop_timer():
    uid = clockify("/user")["id"]
    clockify(f"/workspaces/{WORKSPACE}/user/{uid}/time-entries",
             method="PATCH", body={"end": utc_now_str()})

def start_timer(description, project_id=None):
    body = {"start": utc_now_str(), "description": description}
    if project_id:
        body["projectId"] = project_id   # color-code the entry by category
    clockify(f"/workspaces/{WORKSPACE}/time-entries", method="POST", body=body)

# ---------- one sync cycle ----------
# Blip-proofing: a single network hiccup can make the calendar look empty for one
# cycle. If we stopped the timer on that, one block would split into fragments.
# So we only stop after this many CONSECUTIVE empty reads.
EMPTY_STRIKES_BEFORE_STOP = 2
STATE = {"empty_strikes": 0}

def sync(cal):
    should_be = current_calendar_event(cal)   # what the calendar says
    is_running = running_timer()              # what the stopwatch says

    # CASE A: calendar says nothing is happening now.
    if should_be is None:
        if is_running is not None:
            STATE["empty_strikes"] += 1
            if STATE["empty_strikes"] < EMPTY_STRIKES_BEFORE_STOP:
                # Probably just a blip — keep the current timer running, wait one more cycle.
                log(f"calendar empty (strike {STATE['empty_strikes']}/{EMPTY_STRIKES_BEFORE_STOP}) "
                    f"— keeping '{is_running}' running")
                return
            stop_timer()
            log(f"STOPPED timer: {is_running}")
            STATE["empty_strikes"] = 0
        return

    # CASE B: there IS an event now — real signal, clear any blip count.
    STATE["empty_strikes"] = 0
    if should_be == is_running:
        return  # already in sync, nothing to do

    if is_running is not None:
        stop_timer()
        log(f"STOPPED timer: {is_running}")

    pj = project_for(should_be)
    start_timer(should_be, pj)
    tag = " [" + next((n for n, i in PROJECTS.items() if i == pj), "no project") + "]"
    log(f"STARTED timer: {should_be}{tag}")

# ---------- main ----------
if __name__ == "__main__":
    sys.path.insert(0, os.path.join(PROJECT, "tools"))
    from google_helper import get_calendar

    cal = get_calendar()
    once = "--once" in sys.argv

    log(f"Bridge running ({'single check' if once else 'every %ds' % CHECK_EVERY_SECONDS})")
    while True:
        try:
            sync(cal)
        except Exception as e:
            log(f"ERROR (will retry): {type(e).__name__}: {e}")
            try:
                cal = get_calendar()  # rebuild connection in case it went stale
            except Exception:
                pass
        if once:
            break
        time.sleep(CHECK_EVERY_SECONDS)

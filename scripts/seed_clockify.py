"""
Seed Clockify with today's tasks — the "press play" menu.

THE MODEL (what George wants):
  Google Calendar = the PLAN (task + time + how long). Claude fills it.
  Clockify        = what George LOOKS AT. He presses ▶ to start, ⏹ to stop.
  This script copies today's calendar blocks INTO Clockify as a ready-to-start
  list, each tagged with its color project, each showing its planned minutes.

  NOTHING auto-starts. The old auto-tracking bridge (calendar_timer.py) is
  DISABLED on purpose — George controls his own clock.

USAGE:
  python scripts/seed_clockify.py           # seed today's calendar tasks into Clockify
  python scripts/seed_clockify.py --wipe     # delete today's Clockify entries first, then seed

Each task is created as a tiny 1-second placeholder so it appears in today's
list with a play icon. Pressing ▶ starts a real timer with the same name+color.
"""
import sys, os, json, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

PROJECT = "C:/Users/User/Desktop/project-test"
sys.path.insert(0, os.path.join(PROJECT, "tools"))
sys.path.insert(0, os.path.join(PROJECT, "scripts"))
from google_helper import get_calendar
# reuse the project map + keyword->project logic so colors match everywhere
from calendar_timer import project_for, PROJECTS, WORKSPACE, API_KEY


def clk(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request("https://api.clockify.me/api/v1" + path, data=data, method=method,
        headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode(); return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_msg": e.read().decode()}


def todays_calendar_tasks():
    """Read today's timed calendar blocks -> [(label, project_id), ...]."""
    cal = get_calendar()
    now = datetime.now(timezone.utc)
    items = cal.events().list(
        calendarId="primary",
        timeMin=(now - timedelta(hours=20)).isoformat(),
        timeMax=(now + timedelta(hours=12)).isoformat(),
        singleEvents=True, orderBy="startTime",
    ).execute().get("items", [])

    today = now.astimezone().date()
    tasks = []
    for e in items:
        s = e["start"].get("dateTime"); en = e["end"].get("dateTime")
        if not s or not en:
            continue  # skip all-day events
        sd = datetime.fromisoformat(s)
        if sd.astimezone().date() != today:
            continue
        minutes = int((datetime.fromisoformat(en) - sd).total_seconds() // 60)
        title = e.get("summary", "(no title)")
        short = title.split(" — ")[0].split(" - ")[0].strip()  # trim long titles
        label = f"{short} ({minutes} min)" if minutes else short
        tasks.append((label, project_for(title)))
    return tasks


def wipe_today():
    uid = clk("/user")["id"]
    start = (datetime.now(timezone.utc) - timedelta(hours=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = clk(f"/workspaces/{WORKSPACE}/user/{uid}/time-entries?start={start}&page-size=200")
    for e in entries:
        clk(f"/workspaces/{WORKSPACE}/time-entries/{e['id']}", "DELETE")
    print(f"Wiped {len(entries)} existing entries.")


def seed():
    tasks = todays_calendar_tasks()
    now = datetime.now(timezone.utc).replace(microsecond=0)
    print("Seeding Clockify with today's tasks:")
    for i, (label, pj) in enumerate(tasks):
        st = (now - timedelta(seconds=(len(tasks) - i) * 2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        en = (now - timedelta(seconds=(len(tasks) - i) * 2 - 1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        body = {"start": st, "end": en, "description": label}
        if pj:
            body["projectId"] = pj
        res = clk(f"/workspaces/{WORKSPACE}/time-entries", "POST", body)
        name = next((n for n, x in PROJECTS.items() if x == pj), "no project")
        print(f"  ▶ {label}   [{name}]   {'OK' if res and 'id' in res else res}")
    print("\nDone. Open Clockify — press ▶ on a task to start it, ⏹ to stop.")


if __name__ == "__main__":
    if "--wipe" in sys.argv:
        wipe_today()
    seed()

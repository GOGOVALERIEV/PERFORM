#!/usr/bin/env python3
"""
Tony Stark — The Real Productivity Machine
8-step workflow: Scan → Check → Calculate → List → Time → Calendar → Clockify → Evaluate
"""

import json
import sys
import os
import random
import datetime
import subprocess
import webbrowser
import re
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
STATE_DIR = BASE_DIR / "state"
LOGS_DIR = BASE_DIR / "logs"
OB_DIR = Path.home() / "Desktop" / "personal-ob" / "Goals"
TODO_DIR = Path.home() / "Desktop" / "personal-ob" / "ToDo"
TODO_DAILY_DIR = TODO_DIR / "Daily"
TODO_ALL = TODO_DIR / "All.md"

TODO_DIR.mkdir(exist_ok=True)
TODO_DAILY_DIR.mkdir(exist_ok=True)
(Path.home() / "Desktop" / "personal-ob" / "ToDo" / "Weekly").mkdir(exist_ok=True)
(Path.home() / "Desktop" / "personal-ob" / "ToDo" / "Monthly").mkdir(exist_ok=True)
STATE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

TODAY = datetime.date.today().isoformat()
NOW = datetime.datetime.now().isoformat()


TEST_MODE = False

TEST_EVAL_ANSWERS = {
    "quality": "8 — wrote strong front for the gout angle",
    "progress": "Finished 2 ad fronts, uploaded to Meta",
    "time_wasted": "30 min scrolling Twitter before the deep work block",
    "focus": "7 — strong in first 3 hours, drifted after dinner"
}

# Preload answers from file (for chat mode)
PRELOAD_ANSWERS = None
GATE_ANSWERS = None

def load_preload_answers(filepath):
    """Load answers from a JSON file for chat-based execution."""
    global PRELOAD_ANSWERS
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            PRELOAD_ANSWERS = json.load(f)
    except Exception as e:
        print(f"⚠️ Could not preload answers: {e}")
        PRELOAD_ANSWERS = None

def load_gate_answers(filepath):
    """Load Obsidian Gate decisions from a JSON file."""
    global GATE_ANSWERS
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            GATE_ANSWERS = json.load(f)
    except Exception as e:
        print(f"⚠️ Could not preload gate answers: {e}")
        GATE_ANSWERS = None


def load_questions():
    with open(CONFIG_DIR / "tony-stark-questions.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_state(filename):
    path = STATE_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(filename, data):
    with open(STATE_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def log_event(step, message):
    line = f"[{NOW}] [{step}] {message}\n"
    with open(LOGS_DIR / "tony-stark.log", "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())


def read_obsidian_active_queue():
    """Read Daily System.md for Active Queue"""
    path = OB_DIR / "Daily System.md"
    if not path.exists():
        return "Daily System.md not found."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find Active Queue section
    start = content.find("## Active Queue")
    if start == -1:
        return content[:2000]
    end = content.find("##", start + 1)
    if end == -1:
        end = len(content)
    return content[start:end]


def read_obsidian_daily():
    """Read today's section from Daily.md"""
    path = OB_DIR / "Daily.md"
    if not path.exists():
        return "Daily.md not found."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find today's section
    today_str = datetime.date.today().strftime("%B %d, %Y")
    start = content.find(f"## {today_str}")
    if start == -1:
        # Try without year
        today_str2 = datetime.date.today().strftime("%B %d")
        start = content.find(f"## {today_str2}")
    if start == -1:
        return f"No entry for {today_str} found."
    end = content.find("##", start + 1)
    if end == -1:
        end = len(content)
    return content[start:end]


def generate_day_name():
    """Random name that feels good"""
    names = [
        "The Forge", "The Grind", "The Leap", "The Build",
        "Storm", "Hammer", "Ascent", "Breakthrough",
        "Iron Day", "Deep Cut", "The Push", "Zero Hour",
        "Crucible", "Launchpad", "Overdrive", "Reckoning"
    ]
    return random.choice(names)


# --- Helpers for the Obsidian Gate ---

def _find_section_indices(content, header):
    """Return (start, end) indices of a markdown section under a header."""
    start = content.find(header)
    if start == -1:
        return None, None
    next_h2 = content.find("\n## ", start + 1)
    end = next_h2 if next_h2 != -1 else len(content)
    return start, end


def extract_daily_tasks(content, date_str):
    """Extract '- [ ] ...' lines from today's Daily.md section. Skip machine time blocks."""
    start, end = _find_section_indices(content, f"## {date_str}")
    if start is None:
        return []
    section = content[start:end]
    tasks = []
    for line in section.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            # Skip machine-generated time blocks (have HH:MM — HH:MM pattern)
            if re.search(r'\d{1,2}:\d{2}\s*[-–—]\s*\d{1,2}:\d{2}', stripped):
                continue
            tasks.append(stripped)
    return tasks


def extract_active_queue_items(content):
    """Extract numbered / '- [ ]' items from the Active Queue section."""
    start, end = _find_section_indices(content, "## Active Queue")
    if start is None:
        return []
    section = content[start:end]
    items = []
    for line in section.split("\n"):
        stripped = line.strip()
        if re.match(r'^\d+\.', stripped) or stripped.startswith("- [ ]"):
            items.append(stripped)
    return items


def remove_line_from_file(filepath, line_text):
    """Remove the first exact matching line from a file, preserving the rest."""
    path = Path(filepath)
    if not path.exists():
        return False
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    cleaned = [ln for ln in lines if line_text not in ln]
    if len(cleaned) == len(lines):
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)
    return True


def append_time_blocks_to_daily(date_str, blocks):
    """Append time blocks under today's section in Daily.md. Returns True if appended."""
    path = OB_DIR / "Daily.md"
    if not path.exists():
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    start, end = _find_section_indices(content, f"## {date_str}")
    if start is None:
        return False
    # Check if Time Blocks section already exists in this section
    section = content[start:end]
    if "**Time Blocks:**" in section:
        return False
    block_text = "\n\n**Time Blocks:**\n"
    for b in blocks:
        block_text += f"- [ ] {b['start']} — {b['end']}: {b['name']}\n"
    new_content = content[:end] + block_text + content[end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def parse_task_duration(line):
    """Parse 'Task name (60min)' into (clean_name, minutes). Returns (name, None) if no match."""
    clean = line.strip()
    # Try (60min), (1h), (30m), (90 m)
    m = re.search(r'\((\d+)\s*min\)', clean, flags=re.IGNORECASE)
    if m:
        return clean[:m.start()].strip(), int(m.group(1))
    m = re.search(r'\((\d+)\s*h(?:ou)?r?\)', clean, flags=re.IGNORECASE)
    if m:
        return clean[:m.start()].strip(), int(m.group(1)) * 60
    m = re.search(r'\((\d+)\s*m\)', clean, flags=re.IGNORECASE)
    if m:
        return clean[:m.start()].strip(), int(m.group(1))
    return clean, None


def parse_today_tasks(task_str):
    """Split a multi-line task string into list of (name, duration_min or None)."""
    tasks = []
    for line in task_str.split("\n"):
        line = line.strip().lstrip("-").strip().lstrip("*").strip()
        if not line:
            continue
        name, dur = parse_task_duration(line)
        if name:
            tasks.append({"name": name, "duration": dur, "done": False})
    return tasks


def write_daily_todo(tasks, calc):
    """Create or overwrite ToDo/Daily/YYYY-MM-DD.md with task list (no schedule yet)."""
    date_str = datetime.date.today().strftime("%B %d, %Y")
    daily_file = TODO_DAILY_DIR / f"{TODAY}.md"
    day_name = generate_day_name()
    lines = [
        f"## {date_str} — {day_name}",
        "",
        f"**Energy:** {calc['energy']}",
        f"**Main Block:** {calc['main_block']}",
        "",
        "### Tasks",
    ]
    for t in tasks:
        dur = f" ({t['duration']}min)" if t.get("duration") else ""
        lines.append(f"- [ ] {t['name']}{dur}")
    lines += ["", "### Schedule", ""]
    content = "\n".join(lines)
    with open(daily_file, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    log_event("TODO", f"Daily todo created: {daily_file}")
    return str(daily_file)


def add_tasks_to_all(tasks):
    """Append new tasks from today's list to ToDo/All.md if they don't already exist."""
    if not TODO_ALL.exists():
        with open(TODO_ALL, "w", encoding="utf-8") as f:
            f.write("# All Tasks\n\n")
    with open(TODO_ALL, "r", encoding="utf-8") as f:
        existing = f.read().lower()
    with open(TODO_ALL, "a", encoding="utf-8") as f:
        for t in tasks:
            name = t["name"]
            if name.lower() not in existing:
                dur = f" ({t['duration']}min)" if t.get("duration") else ""
                f.write(f"- [ ] {name}{dur}\n")
                existing += f" {name.lower()} "
    log_event("TODO", f"Synced {len(tasks)} tasks to All.md")


def read_daily_todo():
    """Read today's todo file and return list of task dicts."""
    daily_file = TODO_DAILY_DIR / f"{TODAY}.md"
    if not daily_file.exists():
        return []
    with open(daily_file, "r", encoding="utf-8") as f:
        content = f.read()
    tasks = []
    in_tasks = False
    for line in content.split("\n"):
        if line.strip().startswith("### Tasks"):
            in_tasks = True
            continue
        if line.strip().startswith("### Schedule"):
            in_tasks = False
            continue
        if in_tasks and line.strip().startswith("- [ ]"):
            stripped = line.strip()[6:].strip()
            name, dur = parse_task_duration(stripped)
            tasks.append({"name": name, "duration": dur, "done": False})
    return tasks


def write_schedule_to_daily(blocks):
    """Write or replace the schedule section in today's daily todo file."""
    daily_file = TODO_DAILY_DIR / f"{TODAY}.md"
    if not daily_file.exists():
        return False
    with open(daily_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Find schedule section
    sch_start = content.find("### Schedule")
    if sch_start != -1:
        content = content[:sch_start + len("### Schedule")] + "\n"
    else:
        content += "\n### Schedule\n"
    for b in blocks:
        dur = ""
        if b.get("duration"):
            dur = f" ({b['duration']}min)"
        content += f"- {b['start']} — {b['end']}: {b['name']}{dur}\n"
    with open(daily_file, "w", encoding="utf-8") as f:
        f.write(content)
    log_event("TODO", "Schedule written to daily todo")
    return True


def remove_done_from_all(done_names):
    """Remove completed task lines from ToDo/All.md."""
    if not TODO_ALL.exists():
        return 0
    with open(TODO_ALL, "r", encoding="utf-8") as f:
        lines = f.readlines()
    removed = 0
    kept = []
    for ln in lines:
        lower_ln = ln.lower()
        match = False
        for name in done_names:
            if name.lower() in lower_ln and ln.strip().startswith("- [ ]"):
                match = True
                break
        if match:
            removed += 1
        else:
            kept.append(ln)
    with open(TODO_ALL, "w", encoding="utf-8") as f:
        f.writelines(kept)
    log_event("TODO", f"Removed {removed} done tasks from All.md")
    return removed


def seed_clockify_from_blocks(blocks):
    """Create Clockify entries with actual planned start/end + duration."""
    import urllib.request, urllib.error, json
    # Load env
    env_path = CONFIG_DIR / ".env"
    env = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if ln and not ln.startswith("#") and "=" in ln:
                    k, v = ln.split("=", 1)
                    env[k] = v
    api_key = env.get("CLOCKIFY_API_KEY")
    workspace = env.get("CLOCKIFY_WORKSPACE_ID")
    if not api_key or not workspace:
        return False, "Clockify credentials missing in config/.env"

    def clk(path, method="GET", body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            f"https://api.clockify.me/api/v1{path}",
            data=data, method=method,
            headers={"X-Api-Key": api_key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                raw = r.read().decode()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            return {"_error": e.code, "_msg": e.read().decode()}

    # Wipe today's entries
    uid = clk("/user")
    if not uid or "id" not in uid:
        return False, f"Could not get Clockify user: {uid}"
    uid = uid["id"]
    now = datetime.datetime.now(datetime.timezone.utc)
    start = (now - datetime.timedelta(hours=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = clk(f"/workspaces/{workspace}/user/{uid}/time-entries?start={start}&page-size=200")
    wiped = 0
    for e in (entries or []):
        r = clk(f"/workspaces/{workspace}/time-entries/{e['id']}", "DELETE")
        wiped += 1

    # Seed new entries with real durations
    today = datetime.date.today()
    created = 0
    for i, b in enumerate(blocks):
        if b.get("type") == "personal":
            continue
        sh, sm = map(int, b["start"].split(":"))
        eh, em = map(int, b["end"].split(":"))
        start_dt = datetime.datetime(today.year, today.month, today.day, sh, sm, tzinfo=datetime.timezone.utc)
        end_dt = datetime.datetime(today.year, today.month, today.day, eh, em, tzinfo=datetime.timezone.utc)
        if end_dt <= start_dt:
            end_dt += datetime.timedelta(days=1)
        body = {
            "start": start_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": b["name"],
        }
        res = clk(f"/workspaces/{workspace}/time-entries", "POST", body)
        if res and "id" in res:
            created += 1
    return True, f"Wiped {wiped} entries, created {created} entries with real durations."


def delete_calendar_events_in_window(service, window_start_hours=-6, window_end_hours=18):
    """Delete all non-all-day calendar events in the given window."""
    now = datetime.datetime.now(datetime.timezone.utc)
    time_min = (now + datetime.timedelta(hours=window_start_hours)).isoformat()
    time_max = (now + datetime.timedelta(hours=window_end_hours)).isoformat()
    events_result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    items = events_result.get("items", [])
    deleted = 0
    for ev in items:
        if ev.get("start", {}).get("dateTime"):
            try:
                service.events().delete(calendarId="primary", eventId=ev["id"]).execute()
                deleted += 1
            except Exception as e:
                log_event("CAL_DEL", f"Failed to delete {ev.get('summary')}: {e}")
    log_event("CAL_DEL", f"Deleted {deleted} calendar events")
    return deleted


def run_clockify_seed_script():
    """Actually run seed_clockify.py --wipe and return (ok, message)."""
    seed_script = BASE_DIR / "scripts" / "seed_clockify.py"
    if not seed_script.exists():
        return False, "seed_clockify.py not found"
    try:
        result = subprocess.run(
            [sys.executable, str(seed_script), "--wipe"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=BASE_DIR,
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, f"Exit code {result.returncode}: {result.stderr}"
    except Exception as e:
        return False, str(e)


# ============================================================================
# STEP 1: THE SCAN (Boris Questions)
# ============================================================================
def step_1_scan():
    print("\n" + "="*60)
    print("STEP 1: THE SCAN (Boris NLPP Intake)")
    if PRELOAD_ANSWERS:
        print("   [CHAT MODE — answers pre-loaded]")
    print("="*60)

    questions = load_questions()["step_1_scan"]["questions"]
    answers = {}

    for q in questions:
        print(f"\n🔹 {q['label']}")
        print(f"   {q['text']}")
        if q.get("help"):
            print(f"   ({q['help']})")
        if PRELOAD_ANSWERS and q["id"] in PRELOAD_ANSWERS:
            answer = PRELOAD_ANSWERS[q["id"]]
            print(f"   [PRELOADED]: {answer}")
        else:
            answer = input("   Your answer: ").strip()
        answers[q["id"]] = {
            "label": q["label"],
            "answer": answer,
            "timestamp": NOW
        }
        log_event("STEP1", f"{q['id']}: {answer}")

    # Save state
    save_state(f"morning-scan-{TODAY}.json", answers)
    log_event("STEP1", "Scan complete. Saved to state.")

    return answers


# ============================================================================
# STEP 2: MACHINE CHECK (Cross-reference)
# ============================================================================
def step_2_machine_check(scan_answers):
    print("\n" + "="*60)
    print("STEP 2: MACHINE CHECK")
    print("="*60)

    active_queue = read_obsidian_active_queue()
    daily_md = read_obsidian_daily()

    print("\n📋 ACTIVE QUEUE (from Daily System.md):")
    print(active_queue[:1500] + "..." if len(active_queue) > 1500 else active_queue)

    print("\n📝 TODAY'S DAILY.md:")
    print(daily_md[:1500] + "..." if len(daily_md) > 1500 else daily_md)

    # Extract energy level
    energy = scan_answers.get("sinusoid", {}).get("answer", "middle").lower()
    boardroom = scan_answers.get("boardroom", {}).get("answer", "")
    goal_anchor = scan_answers.get("goal_anchor", {}).get("answer", "")

    check_result = {
        "energy": energy,
        "boardroom": boardroom,
        "goal_anchor": goal_anchor,
        "active_queue_snippet": active_queue[:500],
        "daily_md_snippet": daily_md[:500],
        "timestamp": NOW
    }

    save_state(f"machine-check-{TODAY}.json", check_result)
    log_event("STEP2", "Machine check complete.")

    return check_result


# ============================================================================
# STEP 3: CALCULATE TODAY (Priority Algorithm)
# ============================================================================
def step_3_calculate(machine_check):
    print("\n" + "="*60)
    print("STEP 3: CALCULATE TODAY")
    print("="*60)

    energy = machine_check["energy"]
    goal = machine_check["goal_anchor"]

    # Load active queue
    queue = read_obsidian_active_queue()

    # Parse top item from queue
    lines = queue.split("\n")
    top_item = "Top of Active Queue"
    for line in lines:
        if line.strip().startswith("1.") or line.strip().startswith("- [ ]"):
            top_item = line.strip().lstrip("1.").lstrip("- [ ]").strip()
            break

    # Decision logic
    if "bottom" in energy or "low" in energy:
        main_block = "DO NOW + habits only. Protection mode."
        recommendation = "Bottom of wave. One small task + habits. Nothing else."
    elif "top" in energy or "high" in energy:
        main_block = top_item
        recommendation = "Top of wave. Full load. Main Block: " + top_item
    else:
        main_block = top_item
        recommendation = "Middle wave. Moderate load. Main Block: " + top_item

    # If goal anchor is specific and different from queue top, use it
    if goal and len(goal) > 5 and goal.lower() not in top_item.lower():
        recommendation += f"\n   NOTE: Goal anchor ('{goal}') differs from queue top. Override if stronger."

    calculation = {
        "energy": energy,
        "main_block": main_block,
        "recommendation": recommendation,
        "goal_anchor": goal,
        "timestamp": NOW
    }

    save_state(f"calculation-{TODAY}.json", calculation)

    print(f"\n⚡ ENERGY: {energy}")
    print(f"🎯 MAIN BLOCK: {main_block}")
    print(f"📌 RECOMMENDATION: {recommendation}")
    log_event("STEP3", f"Main block: {main_block}")

    return calculation


# ============================================================================
# STEP 4: MAKE THE LIST (Write to Obsidian)
# ============================================================================
def step_4_make_list(calculation):
    print("\n" + "="*60)
    print("STEP 4: MAKE THE LIST")
    print("="*60)

    day_name = generate_day_name()
    date_str = datetime.date.today().strftime("%B %d, %Y")
    main_block = calculation["main_block"]

    # Create skeleton ToDo/Daily/YYYY-MM-DD.md (tasks filled in later after context)
    daily_file = TODO_DAILY_DIR / f"{TODAY}.md"
    skeleton = f"""## {date_str} — {day_name}

**Energy:** {calculation['energy']}
**Main Block:** {main_block}

### Tasks
<!-- tasks will be populated after chat context -->

### Schedule

"""
    with open(daily_file, "w", encoding="utf-8") as f:
        f.write(skeleton)

    list_state = {
        "day_name": day_name,
        "date": date_str,
        "daily_file": str(daily_file),
        "timestamp": NOW
    }
    save_state(f"day-list-{TODAY}.json", list_state)

    print(f"\n📝 Skeleton daily todo created: {daily_file}")
    log_event("STEP4", f"Skeleton created: {day_name}")

    return list_state


# ============================================================================
# STEP 5: DAY CONTEXT (Ask about actual schedule)
# ============================================================================
def step_5_context():
    print("\n" + "="*60)
    print("STEP 5: DAY CONTEXT")
    print("   What is your day ACTUALLY like? (Not the ideal — the real)")
    print("="*60)

    questions = load_questions()["step_5_context"]["questions"]
    answers = {}

    for q in questions:
        print(f"\n🔹 {q['label']}")
        print(f"   {q['text']}")
        if q.get("help"):
            print(f"   ({q['help']})")
        if TEST_MODE:
            answer = "12:00-02:00 | College 14:00-16:00 | 5 hours | Ship ads"
            print(f"   [TEST ANSWER]: {answer}")
        elif PRELOAD_ANSWERS and q["id"] in PRELOAD_ANSWERS:
            answer = PRELOAD_ANSWERS[q["id"]]
            print(f"   [PRELOADED]: {answer}")
        else:
            answer = input("   Your answer: ").strip()
        answers[q["id"]] = {
            "label": q["label"],
            "answer": answer,
            "timestamp": NOW
        }
        log_event("STEP5-CTX", f"{q['id']}: {answer}")

    save_state(f"day-context-{TODAY}.json", answers)
    log_event("STEP5-CTX", "Day context complete.")
    return answers


# ============================================================================
# STEP 5B: TIME CALCULATOR (Builds blocks around actual day)
# ============================================================================
def _parse_ampm(hour, ampm):
    h = int(hour)
    ap = ampm.lower().strip()
    if ap == "pm" and h != 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    return h


def _time_to_min(h, m):
    return (h % 24) * 60 + m


def _min_to_str(mins):
    mins = mins % (24 * 60)
    return f"{mins // 60:02d}:{mins % 60:02d}"


def step_5_time_calculator(calculation, day_context=None):
    print("\n" + "="*60)
    print("STEP 5: TIME CALCULATOR")
    print("   Building per-task blocks around YOUR actual day.")
    print("="*60)

    if day_context:
        day_start = day_context.get("day_start", {}).get("answer", "12:00-02:00")
        fixed_walls = day_context.get("fixed_walls", {}).get("answer", "")
        deep_capacity = day_context.get("deep_work_hours", {}).get("answer", "3")
        must_do = day_context.get("must_do", {}).get("answer", calculation.get("main_block", "work"))
        today_tasks_str = day_context.get("today_tasks", {}).get("answer", "")
    else:
        day_start = "12:00-02:00"
        fixed_walls = ""
        deep_capacity = "3"
        must_do = calculation.get("main_block", "work")
        today_tasks_str = ""

    # Parse wake / sleep boundaries
    time_match = re.findall(r'(\d{1,2}):(\d{2})', day_start)
    if len(time_match) >= 2:
        start_h, start_m = int(time_match[0][0]), int(time_match[0][1])
        end_h, end_m = int(time_match[-1][0]), int(time_match[-1][1])
    else:
        start_h, start_m = 12, 0
        end_h, end_m = 2, 0

    wake_m = _time_to_min(start_h, start_m)
    sleep_m = _time_to_min(end_h, end_m)
    if sleep_m <= wake_m:
        sleep_m += 24 * 60

    # Parse walls (colon and am/pm tolerant)
    walls = []
    colon_pattern = re.findall(r'(\d{1,2}):(\d{2})\s*[-–—]\s*(\d{1,2}):(\d{2})', fixed_walls)
    for w in colon_pattern:
        ws = _time_to_min(int(w[0]), int(w[1]))
        we = _time_to_min(int(w[2]), int(w[3]))
        if we <= ws:
            we += 24 * 60
        walls.append({"start_m": ws, "end_m": we, "name": "FIXED WALL", "type": "personal"})
    # am/pm style: "8 pm to 11 pm", "8pm-11pm"
    ampm_pattern = re.findall(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*[-–—to]+\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)', fixed_walls, flags=re.IGNORECASE)
    for w in ampm_pattern:
        sh = _parse_ampm(w[0], w[2])
        sm = int(w[1]) if w[1] else 0
        eh = _parse_ampm(w[3], w[5])
        em = int(w[4]) if w[4] else 0
        ws = _time_to_min(sh, sm)
        we = _time_to_min(eh, em)
        if we <= ws:
            we += 24 * 60
        walls.append({"start_m": ws, "end_m": we, "name": "FIXED WALL", "type": "personal"})
    # Parse breaks (same am/pm / colon tolerance as walls, but keep name)
    break_str = day_context.get("breaks", {}).get("answer", "") if day_context else ""
    breaks = []
    # Range style: "15:00-15:30 lunch"
    for w in re.findall(r'(\d{1,2}):(\d{2})\s*[-–—]\s*(\d{1,2}):(\d{2})\s*(.+)', break_str):
        bs = _time_to_min(int(w[0]), int(w[1]))
        be = _time_to_min(int(w[2]), int(w[3]))
        if be <= bs: be += 24 * 60
        breaks.append({"start_m": bs, "end_m": be, "name": w[4].strip(), "type": "break"})
    # Single time: "15:00 lunch" -> default 30 min
    for w in re.findall(r'(\d{1,2}):(\d{2})\s+(.+)', break_str):
        bs = _time_to_min(int(w[0]), int(w[1]))
        be = bs + 30
        breaks.append({"start_m": bs, "end_m": be, "name": w[2].strip(), "type": "break"})
    # am/pm range: "3pm-4pm gym"
    for w in re.findall(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*[-–—to]+\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s*(.+)', break_str, flags=re.IGNORECASE):
        sh = _parse_ampm(w[0], w[2]); sm = int(w[1]) if w[1] else 0
        eh = _parse_ampm(w[3], w[5]); em = int(w[4]) if w[4] else 0
        bs = _time_to_min(sh, sm); be = _time_to_min(eh, em)
        if be <= bs: be += 24 * 60
        breaks.append({"start_m": bs, "end_m": be, "name": w[6].strip(), "type": "break"})
    # Single am/pm: "3pm lunch" -> default 30 min
    for w in re.findall(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)\s+(.+)', break_str, flags=re.IGNORECASE):
        sh = _parse_ampm(w[0], w[2]); sm = int(w[1]) if w[1] else 0
        bs = _time_to_min(sh, sm); be = bs + 30
        breaks.append({"start_m": bs, "end_m": be, "name": w[3].strip(), "type": "break"})

    # Merge walls + breaks into fixed_blocks
    fixed_blocks = walls + breaks
    fixed_blocks.sort(key=lambda x: x["start_m"])

    # Parse tasks from today's_tasks answer
    tasks = parse_today_tasks(today_tasks_str) if today_tasks_str.strip() else []
    if not tasks:
        # fallback from must_do
        tasks = [{"name": must_do, "duration": None}]

    # Calculate available free minutes
    total_day = sleep_m - wake_m
    fixed_total = sum(b["end_m"] - b["start_m"] for b in fixed_blocks)
    free_minutes = total_day - fixed_total

    # Assign durations to tasks without them
    explicit = sum(t["duration"] or 0 for t in tasks)
    undefined = [t for t in tasks if not t["duration"]]
    if undefined:
        remaining = max(0, free_minutes - 60 - explicit)  # reserve 60 min buffer/wind-down
        per_undef = remaining // len(undefined) if remaining > 0 else 30
        for t in undefined:
            t["duration"] = max(15, per_undef)
    else:
        if explicit > free_minutes:
            scale = free_minutes / explicit if explicit > 0 else 1
            for t in tasks:
                t["duration"] = max(15, int(t["duration"] * scale))

    # Schedule blocks: interleave tasks, walls, personal blocks
    blocks = []
    cursor = wake_m

    # Wake block (30 min)
    blocks.append({
        "name": "Wake up + eat",
        "start_m": cursor, "end_m": min(cursor + 30, sleep_m),
        "type": "personal"
    })
    cursor = blocks[-1]["end_m"]

    # Merge fixed blocks (walls + breaks) and tasks in chronological order
    remaining_tasks = list(tasks)
    for fb in fixed_blocks:
        # Fill gap before fixed block
        while cursor < fb["start_m"] and remaining_tasks:
            t = remaining_tasks.pop(0)
            end_t = min(cursor + t["duration"], fb["start_m"])
            blocks.append({
                "name": t["name"],
                "start_m": cursor, "end_m": end_t,
                "type": "deep_work"
            })
            cursor = end_t
        blocks.append(fb)
        cursor = fb["end_m"]

    # After last fixed block, fill remaining day
    while cursor < sleep_m and remaining_tasks:
        t = remaining_tasks.pop(0)
        end_t = min(cursor + t["duration"], sleep_m)
        blocks.append({
            "name": t["name"],
            "start_m": cursor, "end_m": end_t,
            "type": "deep_work"
        })
        cursor = end_t

    # Wind-down / buffer before sleep
    if cursor < sleep_m:
        blocks.append({
            "name": "Buffer / wind down",
            "start_m": cursor, "end_m": sleep_m,
            "type": "personal"
        })

    # Convert start_m/end_m to strings, add durations
    for b in blocks:
        b["start"] = _min_to_str(b["start_m"])
        b["end"] = _min_to_str(b["end_m"])
        b["duration"] = b["end_m"] - b["start_m"]
        if b["duration"] < 0:
            b["duration"] += 24 * 60
    blocks.sort(key=lambda b: b["start_m"])

    # Write to daily todo file and All.md
    write_daily_todo(tasks, calculation)
    add_tasks_to_all(tasks)
    write_schedule_to_daily(blocks)

    time_state = {
        "day_window": day_start,
        "fixed_walls": fixed_walls,
        "tasks": tasks,
        "blocks": blocks,
        "timestamp": NOW
    }
    save_state(f"time-blocks-{TODAY}.json", time_state)

    print(f"\n⏰ Total day window: {day_start} | Free time: {free_minutes} min")
    print(f"📅 Scheduled blocks:")
    for b in blocks:
        print(f"   {b['start']} - {b['end']}: {b['name']} ({b['duration']}min) [{b['type']}]")
    log_event("STEP5", f"Scheduled {len(blocks)} blocks, {len(tasks)} tasks")

    return time_state


# ============================================================================
# STEP 5.5: OBSIDIAN GATE — Review existing tasks before writing new ones
# ============================================================================
def _resolve_gate_decision(task_text, decision_map):
    """Find a decision for task_text in decision_map.
    Tries exact match, then prefix/substring match. Returns (decision, matched_key)."""
    if not decision_map:
        return None, None
    # Exact match
    if task_text in decision_map:
        return decision_map[task_text], task_text
    # Try exact after normalizing whitespace
    for key, val in decision_map.items():
        if key.strip() == task_text.strip():
            return val, key
    # Try prefix match: gate-preload key is a prefix of the full task line
    for key, val in decision_map.items():
        kstrip = key.strip()
        tstrip = task_text.strip()
        if tstrip.startswith(kstrip) or kstrip in tstrip:
            return val, key
    return None, None


def step_5_5_obsidian_gate(time_blocks):
    print("\n" + "="*60)
    print("STEP 5.5: OBSIDIAN GATE")
    print("   Review existing tasks. Keep, fuck this, or not today.")
    print("="*60)

    date_str = datetime.date.today().strftime("%B %d, %Y")
    gate_decisions = {"daily_md": {}, "active_queue": {}, "time_blocks_appended": True}

    # --- Daily.md review ---
    daily_path = OB_DIR / "Daily.md"
    daily_tasks = []
    if daily_path.exists():
        with open(daily_path, "r", encoding="utf-8") as f:
            content = f.read()
        daily_tasks = extract_daily_tasks(content, date_str)

    if daily_tasks:
        print("\n📋 Tasks found in Daily.md under today's section:")
        for task in daily_tasks:
            decision, matched_key = _resolve_gate_decision(task, GATE_ANSWERS.get("daily_md", {}) if GATE_ANSWERS else None)
            if decision is not None:
                print(f"   [{decision.upper()}] {task}")
            else:
                print(f"\n   Task: {task}")
                try:
                    decision = input("   Decision [keep / fuck this / not today]: ").strip().lower()
                except (EOFError, OSError):
                    decision = "keep"
            gate_decisions["daily_md"][task] = decision
            if decision == "fuck this":
                removed = remove_line_from_file(daily_path, task)
                log_event("GATE", f"Removed from Daily.md: {task} (ok={removed})")
                print(f"      🗑️ Removed from Daily.md")
            elif decision == "not today":
                print(f"      ⏸️ Left in Daily.md, skipped for calendar")
            else:
                print(f"      ✅ Kept")

    # --- Daily System.md review ---
    system_path = OB_DIR / "Daily System.md"
    aq_items = []
    if system_path.exists():
        with open(system_path, "r", encoding="utf-8") as f:
            content = f.read()
        aq_items = extract_active_queue_items(content)

    if aq_items:
        print("\n🎯 Active Queue items in Daily System.md:")
        for item in aq_items:
            decision, matched_key = _resolve_gate_decision(item, GATE_ANSWERS.get("active_queue", {}) if GATE_ANSWERS else None)
            if decision is not None:
                print(f"   [{decision.upper()}] {item}")
            else:
                print(f"\n   Item: {item}")
                try:
                    decision = input("   Decision [keep / fuck this / not today]: ").strip().lower()
                except (EOFError, OSError):
                    decision = "keep"
            gate_decisions["active_queue"][item] = decision
            if decision == "fuck this":
                removed = remove_line_from_file(system_path, item)
                log_event("GATE", f"Removed from Active Queue: {item} (ok={removed})")
                print(f"      🗑️ Removed from Daily System.md")
            elif decision == "not today":
                print(f"      ⏸️ Left in queue, not scheduled today")
            else:
                print(f"      ✅ Kept")

    # --- Append new time blocks to Daily.md (only if not already there) ---
    appended = append_time_blocks_to_daily(date_str, time_blocks["blocks"])
    log_event("GATE", f"Time blocks appended: {appended}")
    if appended:
        print("\n📝 Time blocks appended to today's Daily.md section.")
    else:
        print("\n📝 Time blocks already present in today's Daily.md section. No duplicate.")

    save_state(f"obsidian-gate-{TODAY}.json", gate_decisions)
    print(f"\n📋 Gate decisions saved to state/obsidian-gate-{TODAY}.json")
    return gate_decisions


# ============================================================================
# STEP 6: GOOGLE CALENDAR PUSH
# ============================================================================
def step_6_calendar_push(time_blocks):
    print("\n" + "="*60)
    print("STEP 6: GOOGLE CALENDAR PUSH")
    print("="*60)

    sys.path.insert(0, str(BASE_DIR / "scripts"))
    try:
        from google_helper import get_calendar
        service = get_calendar()
    except Exception as e:
        print(f"   ⚠️ Google Calendar not available: {e}")
        print("   Manual step: copy these blocks into Google Calendar.")
        log_event("STEP6", f"FAILED: {e}")
        return False

    today = datetime.date.today()

    # WIPE today before writing
    deleted = delete_calendar_events_in_window(service, window_start_hours=-6, window_end_hours=18)
    print(f"   🗑️ Deleted {deleted} existing events.")

    created = 0
    for block in time_blocks["blocks"]:
        if block["type"] == "personal":
            continue

        start_hour, start_min = map(int, block["start"].split(":"))
        end_hour, end_min = map(int, block["end"].split(":"))

        start_dt = datetime.datetime(today.year, today.month, today.day, start_hour, start_min)
        end_dt = datetime.datetime(today.year, today.month, today.day, end_hour, end_min)
        if end_dt <= start_dt:
            end_dt += datetime.timedelta(days=1)

        event = {
            "summary": block["name"],
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "Europe/Sofia"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "Europe/Sofia"},
            "description": f"Tony Stark auto-block | Type: {block['type']}",
        }
        try:
            service.events().insert(calendarId="primary", body=event).execute()
            created += 1
            print(f"   ✅ Created: {block['name']} ({block['start']} - {block['end']})")
        except Exception as e:
            print(f"   ❌ Failed: {block['name']} — {e}")

    log_event("STEP6", f"Wiped {deleted}, created {created} calendar events")
    print(f"\n📅 {created} events pushed to Google Calendar")
    return created > 0


# ============================================================================
# STEP 7: CLOCKIFY SEED
# ============================================================================
def step_7_clockify_seed(time_blocks):
    print("\n" + "="*60)
    print("STEP 7: CLOCKIFY SEED")
    print("="*60)

    ok, msg = seed_clockify_from_blocks(time_blocks["blocks"])
    if ok:
        print(f"   ✅ Clockify seeded successfully.")
        print(f"   {msg}")
        log_event("STEP7", "Clockify seeded OK")
        return True
    else:
        print(f"   ⚠️ Clockify seed failed: {msg}")
        log_event("STEP7", f"FAILED: {msg}")
        return False


# ============================================================================
# STEP 8: END OF DAY EVALUATION
# ============================================================================
def step_8_evaluate():
    print("\n" + "="*60)
    print("STEP 8: END OF DAY EVALUATION")
    print("="*60)
    print("   (Run this with: python scripts/tony_stark.py --evening)")
    print("   Not running now — this is the morning routine.")
    return True


def open_tools():
    """Open Google Calendar, Clockify, and Obsidian — the Tony Stark dashboard."""
    print("\n" + "="*60)
    print("OPENING THE TONY STARK DASHBOARD")
    print("="*60)

    # 1. Open Google Calendar in Brave
    calendar_url = "https://calendar.google.com/calendar/u/0/r/day"
    try:
        # Try Brave specifically first
        brave_paths = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        ]
        brave_found = None
        for p in brave_paths:
            if os.path.exists(p):
                brave_found = p
                break
        if brave_found:
            subprocess.Popen([brave_found, calendar_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("   ✅ Opened Google Calendar in Brave")
        else:
            webbrowser.open(calendar_url)
            print("   ✅ Opened Google Calendar in default browser")
    except Exception as e:
        print(f"   ⚠️ Could not open Calendar: {e}")
        print(f"   Manual: {calendar_url}")

    # 2. Open Clockify desktop
    clockify_path = r"C:\Program Files\Clockify\ClockifyWindows.exe"
    try:
        if os.path.exists(clockify_path):
            subprocess.Popen([clockify_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("   ✅ Opened Clockify desktop")
        else:
            print(f"   ⚠️ Clockify not found at: {clockify_path}")
            print("   Manual: Search 'Clockify' in Start menu")
    except Exception as e:
        print(f"   ⚠️ Could not open Clockify: {e}")

    # 3. Open Obsidian vault
    obsidian_vault = Path.home() / "Desktop" / "personal-ob"
    try:
        # Try opening Obsidian app with the vault
        obsidian_exe = Path.home() / "AppData" / "Local" / "Obsidian" / "Obsidian.exe"
        if obsidian_exe.exists():
            subprocess.Popen([str(obsidian_exe), f"--vault={obsidian_vault}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("   ✅ Opened Obsidian vault")
        else:
            # Fallback: open the folder
            os.startfile(str(obsidian_vault))
            print("   ✅ Opened Obsidian vault folder")
    except Exception as e:
        print(f"   ⚠️ Could not open Obsidian: {e}")
        print(f"   Manual: {obsidian_vault}")


def step_8_evaluate_evening():
    print("\n" + "="*60)
    print("STEP 8: THE RUTHLESS READING + TASK CLEANUP")
    if TEST_MODE:
        print("   [TEST MODE — using dummy answers]")
    print("="*60)

    date_str = datetime.date.today().strftime("%B %d, %Y")
    questions = load_questions()["step_8_evaluation"]["questions"]
    quote = load_questions()["step_8_evaluation"]["closing_quote"]
    answers = {}

    for q in questions:
        print(f"\n🔹 {q['label']}")
        print(f"   {q['text']}")
        if TEST_MODE:
            answer = TEST_EVAL_ANSWERS.get(q["id"], "test")
            print(f"   [TEST ANSWER]: {answer}")
        else:
            answer = input("   Your answer: ").strip()
        answers[q["id"]] = answer
        log_event("STEP8", f"{q['id']}: {answer}")

    # ruthless reading (same logic)
    quality = answers.get("quality", "")
    progress = answers.get("progress", "")
    wasted = answers.get("time_wasted", "")
    focus = answers.get("focus", "")

    print("\n" + "="*60)
    print("THE RUTHLESS READING")
    print("="*60)
    reading_lines = [f"QUALITY: {quality}", f"PROGRESS: {progress}", f"TIME WASTED: {wasted}", f"FOCUS: {focus}", ""]
    if "10" in quality or "9" in quality:
        reading_lines.append("- Quality was high. Good. But did you ship, or just polish?")
    elif "5" in quality or "4" in quality or "3" in quality:
        reading_lines.append("- Quality was mediocre. Why? Fix the input, not the output.")
    else:
        reading_lines.append("- Quality unclear. Be honest.")
    if progress and len(progress) > 5:
        reading_lines.append("- You named something that moved. That counts.")
    else:
        reading_lines.append("- No specific progress. That means nothing shipped.")
    if wasted and len(wasted) > 5:
        reading_lines.append(f"- Leaked time to: {wasted}.")
    else:
        reading_lines.append("- No waste identified? You're not perfect.")
    if "10" in focus or "9" in focus:
        reading_lines.append("- Focus was strong. Weaponize it.")
    elif "5" in focus or "4" in focus:
        reading_lines.append("- Focus was split. Phone in another room tomorrow.")
    else:
        reading_lines.append("- Focus was trash.")
    reading_lines += ["", f"{quote}", ""]
    reading = "\n".join(reading_lines)
    print(reading)

    # --- Task cleanup ---
    print("\n📝 TASK CLEANUP")
    daily_file = TODO_DAILY_DIR / f"{TODAY}.md"
    tasks_today = read_daily_todo() if daily_file.exists() else []
    done_names = []
    if tasks_today:
        print(f"   Today's tasks ({date_str}):")
        for t in tasks_today:
            dur = f" ({t['duration']}min)" if t.get("duration") else ""
            print(f"   - [ ] {t['name']}{dur}")
        print("\n   Which tasks got done? (comma-separated names, or 'none' / 'all')")
        done_input = input("   Done: ").strip()
        if done_input.lower() in ("all", "everything", "yes"):
            done_names = [t["name"] for t in tasks_today]
        elif done_input.lower() not in ("none", "no", "nothing", ""):
            done_names = [x.strip() for x in done_input.split(",") if x.strip()]

    if done_names:
        # Remove from daily file
        with open(daily_file, "r", encoding="utf-8") as f:
            content = f.read()
        for name in done_names:
            content = content.replace(f"- [ ] {name}", f"- [x] ~~{name}~~")
        with open(daily_file, "w", encoding="utf-8") as f:
            f.write(content)
        # Remove from All.md
        removed = remove_done_from_all(done_names)
        print(f"   ✅ Marked {len(done_names)} done in daily todo, cleaned {removed} from All.md")
        log_event("STEP8", f"Cleaned {done_names} — {removed} from All.md")
    else:
        print("   ⏸️ No tasks marked done.")

    eval_state = {
        "answers": answers,
        "reading": reading,
        "done_tasks": done_names,
        "timestamp": NOW
    }
    save_state(f"evaluation-{TODAY}.json", eval_state)
    log_event("STEP8", "Evaluation + cleanup complete")

    return eval_state


# ============================================================================
# MAIN
# ============================================================================
def main():
    global TEST_MODE, PRELOAD_ANSWERS

    if "--evening" in sys.argv:
        step_8_evaluate_evening()
        return

    if "--preload" in sys.argv:
        try:
            preload_file = sys.argv[sys.argv.index("--preload") + 1]
            load_preload_answers(preload_file)
            print(f"\n📂 PRELOAD MODE — reading answers from: {preload_file}\n")
        except (IndexError, ValueError):
            print("⚠️ --preload requires a file path. Usage: --preload answers.json")
            return

    if "--step" in sys.argv:
        try:
            step_num = int(sys.argv[sys.argv.index("--step") + 1])
        except (IndexError, ValueError):
            step_num = 0
    else:
        step_num = 0

    print("\n" + "="*60)
    print("TONY STARK — MORNING ROUTINE")
    print(f"Date: {TODAY}")
    print("="*60)

    # ---- Step 1: Scan ----
    if step_num == 0 or step_num == 1:
        scan = step_1_scan()
    else:
        scan = load_state(f"morning-scan-{TODAY}.json")

    # ---- Step 2: Machine Check ----
    if step_num == 0 or step_num == 2:
        check = step_2_machine_check(scan)
    else:
        check = load_state(f"machine-check-{TODAY}.json")

    # ---- Step 3: Calculate ----
    if step_num == 0 or step_num == 3:
        calc = step_3_calculate(check)
    else:
        calc = load_state(f"calculation-{TODAY}.json")

    # ---- Step 4: Skeleton ----
    if step_num == 0 or step_num == 4:
        day_list = step_4_make_list(calc)
    else:
        day_list = load_state(f"day-list-{TODAY}.json")

    # ---- Step 5: Context + Time Calculator ----
    if step_num == 0 or step_num == 5:
        day_context = step_5_context()
        time_blocks = step_5_time_calculator(calc, day_context)
    else:
        day_context = load_state(f"day-context-{TODAY}.json")
        time_blocks = load_state(f"time-blocks-{TODAY}.json")

    # ---- Step 6: Calendar ----
    if step_num == 0 or step_num == 6:
        step_6_calendar_push(time_blocks)

    # ---- Step 7: Clockify ----
    if step_num == 0 or step_num == 7:
        step_7_clockify_seed(time_blocks)

    # ---- Step 8: Dashboard ----
    if step_num == 0:
        step_8_evaluate()
        open_tools()

    print("\n" + "="*60)
    print("MORNING ROUTINE COMPLETE")
    print("="*60)
    print(f"\nState files saved in: {STATE_DIR}")
    print(f"Log file: {LOGS_DIR / 'tony-stark.log'}")


if __name__ == "__main__":
    main()

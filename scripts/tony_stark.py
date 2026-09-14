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

    daily_entry = f"""## {date_str} — {day_name}

*Energy: {calculation['energy']}. Main Block: {main_block}*

**Main Block (the ONE win):**
- [ ] {main_block}

**Habits (non-negotiable):**
- [ ] Twitter — 25 min: read Boris's tweets, note 3 that got engagement + why
- [ ] English — 30 min: rewrite a hook from yesterday in own words, compare, log mistakes

**If juice left:**
- [ ] One small unblock task (5 min max)

**Deferred:**
- (check Active Queue for next item if Main Block finishes early)

---
"""

    # Append to Daily.md
    daily_path = OB_DIR / "Daily.md"
    if daily_path.exists():
        with open(daily_path, "r", encoding="utf-8") as f:
            existing = f.read()
        # Check if today's entry already exists
        if date_str in existing[:1000]:
            print(f"   ⚠️ Entry for {date_str} already exists. Appending below.")
            existing += "\n\n" + daily_entry
        else:
            existing = daily_entry + "\n\n" + existing
    else:
        existing = daily_entry

    with open(daily_path, "w", encoding="utf-8") as f:
        f.write(existing)

    # Save state
    list_state = {
        "day_name": day_name,
        "date": date_str,
        "entry": daily_entry,
        "timestamp": NOW
    }
    save_state(f"day-list-{TODAY}.json", list_state)

    print(f"\n📝 Written to Daily.md: {date_str} — {day_name}")
    print(f"   Main Block: {main_block}")
    log_event("STEP4", f"List created: {day_name}")

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
def step_5_time_calculator(calculation, day_context=None):
    print("\n" + "="*60)
    print("STEP 5: TIME CALCULATOR")
    print("   Building blocks around YOUR actual day.")
    print("="*60)

    energy = calculation["energy"]

    # Parse day context
    if day_context:
        day_start = day_context.get("day_start", {}).get("answer", "12:00-02:00")
        fixed_walls = day_context.get("fixed_walls", {}).get("answer", "")
        deep_capacity = day_context.get("deep_work_hours", {}).get("answer", "3")
        must_do = day_context.get("must_do", {}).get("answer", calculation.get("main_block", "work"))
    else:
        day_start = "12:00-02:00"
        fixed_walls = ""
        deep_capacity = "3"
        must_do = calculation.get("main_block", "work")

    # Parse capacity
    try:
        deep_hours = int([c for c in deep_capacity if c.isdigit()][0]) if any(c.isdigit() for c in deep_capacity) else 3
    except:
        deep_hours = 3

    # Parse start/end
    import re
    time_match = re.findall(r'(\d{1,2}):(\d{2})', day_start)
    if len(time_match) >= 2:
        start_h, start_m = int(time_match[0][0]), int(time_match[0][1])
        end_h, end_m = int(time_match[-1][0]), int(time_match[-1][1])
    else:
        start_h, start_m = 12, 0
        end_h, end_m = 2, 0

    # Parse fixed walls
    walls = []
    wall_pattern = re.findall(r'(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})', fixed_walls)
    for w in wall_pattern:
        walls.append({
            "start_h": int(w[0]), "start_m": int(w[1]),
            "end_h": int(w[2]), "end_m": int(w[3])
        })

    # Build free blocks
    blocks = []

    # Wake up block
    blocks.append({"name": "Wake up + eat", "start": f"{start_h:02d}:{start_m:02d}",
                  "end": f"{start_h+1:02d}:{start_m:02d}", "type": "personal"})

    # Fixed walls (sacred)
    for wall in walls:
        blocks.append({
            "name": "FIXED WALL",
            "start": f"{wall['start_h']:02d}:{wall['start_m']:02d}",
            "end": f"{wall['end_h']:02d}:{wall['end_m']:02d}",
            "type": "personal"
        })

    # Deep work (the big block)
    if "bottom" in energy or "low" in energy:
        deep_hours = min(deep_hours, 2)
    elif "top" in energy or "high" in energy:
        deep_hours = max(deep_hours, 4)

    # Find largest free gap for deep work (naive: after last wall or after wake)
    deep_start_h = 15 if not walls else walls[-1]["end_h"] + 1
    deep_end_h = deep_start_h + deep_hours
    blocks.append({
        "name": f"DEEP WORK: {must_do}",
        "start": f"{deep_start_h:02d}:00",
        "end": f"{deep_end_h:02d}:00",
        "type": "deep_work"
    })

    # Grit work (whatever is left)
    grit_start_h = deep_end_h + 1
    grit_end_h = min(grit_start_h + 2, end_h - 1)
    if grit_end_h > grit_start_h:
        blocks.append({
            "name": "GRIT WORK (remaining tasks)",
            "start": f"{grit_start_h:02d}:00",
            "end": f"{grit_end_h:02d}:00",
            "type": "work"
        })

    # Habits
    habits_start = end_h - 2
    if habits_start > deep_end_h:
        blocks.append({
            "name": "Habits (Twitter + English)",
            "start": f"{habits_start:02d}:00",
            "end": f"{habits_start+1:02d}:00",
            "type": "habits"
        })

    # Wife / wind down
    if end_h > 21:
        blocks.append({
            "name": "Wife time / wind down",
            "start": f"{end_h-1:02d}:00",
            "end": f"{end_h:02d}:{end_m:02d}",
            "type": "personal"
        })

    # Sort by start time
    def parse_time(t):
        h, m = map(int, t.split(":"))
        return h * 60 + m
    blocks.sort(key=lambda b: parse_time(b["start"]))

    time_state = {
        "deep_work_hours": f"{deep_hours} hours",
        "day_window": day_start,
        "fixed_walls": fixed_walls,
        "must_do": must_do,
        "blocks": blocks,
        "timestamp": NOW
    }
    save_state(f"time-blocks-{TODAY}.json", time_state)

    print(f"\n⏰ Deep Work Capacity: {deep_hours} hours")
    print(f"🧠 Must Do: {must_do}")
    print(f"📅 Fixed Walls: {fixed_walls if fixed_walls else 'None'}")
    print("\n📅 Proposed Blocks:")
    for b in blocks:
        print(f"   {b['start']} - {b['end']}: {b['name']} ({b['type']})")
    log_event("STEP5", f"Time calculated: {deep_hours}h deep work, {len(blocks)} blocks")

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
def step_7_clockify_seed():
    print("\n" + "="*60)
    print("STEP 7: CLOCKIFY SEED")
    print("="*60)

    ok, msg = run_clockify_seed_script()
    if ok:
        print(f"   ✅ Clockify seeded successfully.")
        print(msg[:800])
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
    print("STEP 8: THE RUTHLESS READING")
    if TEST_MODE:
        print("   [TEST MODE — using dummy answers]")
    print("="*60)

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

    # Generate ruthless reading
    quality = answers.get("quality", "")
    progress = answers.get("progress", "")
    wasted = answers.get("time_wasted", "")
    focus = answers.get("focus", "")

    print("\n" + "="*60)
    print("THE RUTHLESS READING")
    print("="*60)

    reading = f"""
QUALITY: {quality}
PROGRESS: {progress}
TIME WASTED: {wasted}
FOCUS: {focus}

ANALYSIS:
"""

    # Simple logic for the reading
    if "10" in quality or "9" in quality:
        reading += "- Quality was high. Good. But did you ship, or just polish?\n"
    elif "5" in quality or "4" in quality or "3" in quality:
        reading += "- Quality was mediocre. Why? Distracted? Unprepared? Fix the input, not the output.\n"
    else:
        reading += "- Quality unclear. Be honest with yourself.\n"

    if progress and len(progress) > 5:
        reading += "- You named something that moved. That counts.\n"
    else:
        reading += "- No specific progress named. That means nothing shipped.\n"

    if wasted and len(wasted) > 5:
        reading += f"- You leaked time to: {wasted}. Tomorrow, that leak gets plugged.\n"
    else:
        reading += "- No time waste identified. Either you're lying or you're perfect. You're not perfect.\n"

    if "10" in focus or "9" in focus:
        reading += "- Focus was strong. This is your weapon. Use it more.\n"
    elif "5" in focus or "4" in focus:
        reading += "- Focus was split. Phone in another room tomorrow. No exceptions.\n"
    else:
        reading += "- Focus was trash. Why did you even sit down?\n"

    reading += f"""
THE FIX FOR TOMORROW:
One thing. Not five. One. Name it now or it doesn't exist.

{quote}
"""

    print(reading)

    # Save
    eval_state = {
        "answers": answers,
        "reading": reading,
        "timestamp": NOW
    }
    save_state(f"evaluation-{TODAY}.json", eval_state)
    log_event("STEP8", "Evaluation complete")

    return eval_state


# ============================================================================
# MAIN
# ============================================================================
def main():
    global TEST_MODE, PRELOAD_ANSWERS, GATE_ANSWERS

    stop_after = None
    if "--stop-after" in sys.argv:
        try:
            stop_after = int(sys.argv[sys.argv.index("--stop-after") + 1])
            print(f"⏹️  Will halt after step {stop_after}.")
        except (IndexError, ValueError):
            pass

    if "--preload" in sys.argv:
        try:
            preload_file = sys.argv[sys.argv.index("--preload") + 1]
            load_preload_answers(preload_file)
            print(f"\n📂 PRELOAD MODE — reading answers from: {preload_file}\n")
        except (IndexError, ValueError):
            print("⚠️ --preload requires a file path. Usage: --preload answers.json")
            return

    if "--gate-preload" in sys.argv:
        try:
            gate_file = sys.argv[sys.argv.index("--gate-preload") + 1]
            load_gate_answers(gate_file)
            print(f"\n🔒 GATE PRELOAD — reading gate decisions from: {gate_file}\n")
        except (IndexError, ValueError):
            print("⚠️ --gate-preload requires a file path. Usage: --gate-preload gate.json")
            return

    if "--evening" in sys.argv:
        step_8_evaluate_evening()
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

    # ---- Steps 1–5 ----
    if step_num == 0 or step_num == 1:
        scan = step_1_scan()
    else:
        scan = load_state(f"morning-scan-{TODAY}.json")

    if step_num == 0 or step_num == 2:
        check = step_2_machine_check(scan)
    else:
        check = load_state(f"machine-check-{TODAY}.json")

    if step_num == 0 or step_num == 3:
        calc = step_3_calculate(check)
    else:
        calc = load_state(f"calculation-{TODAY}.json")

    if step_num == 0 or step_num == 4:
        day_list = step_4_make_list(calc)
    else:
        day_list = load_state(f"day-list-{TODAY}.json")

    if step_num == 0 or step_num == 5:
        day_context = step_5_context()
        time_blocks = step_5_time_calculator(calc, day_context)
    else:
        day_context = load_state(f"day-context-{TODAY}.json")
        time_blocks = load_state(f"time-blocks-{TODAY}.json")

    if stop_after == 5:
        print("\n⏹️  Stopped after Step 5. Run again with --gate-preload to continue.")
        save_state(f"stopped-{TODAY}.json", {"step": 5, "reason": "gate required"})
        return

    # ---- Step 5.5: Obsidian Gate ----
    # (loaded from state if resuming, or run fresh)
    gate_state_file = f"obsidian-gate-{TODAY}.json"
    if GATE_ANSWERS or not Path(STATE_DIR / gate_state_file).exists():
        step_5_5_obsidian_gate(time_blocks)
    else:
        print("\n🔒 Obsidian Gate already completed today. Skipping.")

    if stop_after == 55:
        print("\n⏹️  Stopped after Step 5.5. Ready for Calendar + Clockify.")
        return

    # ---- Steps 6–8 ----
    if step_num == 0 or step_num == 6:
        step_6_calendar_push(time_blocks)

    if step_num == 0 or step_num == 7:
        step_7_clockify_seed()

    if step_num == 0:
        step_8_evaluate()
        open_tools()  # Tony Stark dashboard

    print("\n" + "="*60)
    print("MORNING ROUTINE COMPLETE")
    print("="*60)
    print(f"\nState files saved in: {STATE_DIR}")
    print(f"Log file: {LOGS_DIR / 'tony-stark.log'}")


if __name__ == "__main__":
    main()

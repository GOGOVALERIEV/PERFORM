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


# ============================================================================
# STEP 1: THE SCAN (Boris Questions)
# ============================================================================
def step_1_scan():
    print("\n" + "="*60)
    print("STEP 1: THE SCAN (Boris NLPP Intake)")
    print("="*60)

    questions = load_questions()["step_1_scan"]["questions"]
    answers = {}

    for q in questions:
        print(f"\n🔹 {q['label']}")
        print(f"   {q['text']}")
        if q.get("help"):
            print(f"   ({q['help']})")
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
# STEP 5: TIME CALCULATOR
# ============================================================================
def step_5_time_calculator(calculation):
    print("\n" + "="*60)
    print("STEP 5: TIME CALCULATOR")
    print("="*60)

    # George's profile
    wakes = "12 PM"
    peak_brain = "3 PM → 10 PM"
    grit_mode = "8 PM → 2 AM+"
    energy = calculation["energy"]

    # Calculate deep work block
    if "bottom" in energy or "low" in energy:
        deep_work = "1-2 hours max (protection mode)"
        blocks = [
            {"name": "Wake up + eat", "start": "12:00", "end": "14:00", "type": "personal"},
            {"name": "DO NOW (one small thing)", "start": "15:00", "end": "17:00", "type": "work"},
            {"name": "Habits only", "start": "17:00", "end": "18:00", "type": "habits"},
            {"name": "Rest / wife time", "start": "18:00", "end": "22:00", "type": "personal"},
        ]
    elif "top" in energy or "high" in energy:
        deep_work = "5 hours deep work + 2 hours grit"
        blocks = [
            {"name": "Wake up + eat", "start": "12:00", "end": "14:00", "type": "personal"},
            {"name": "Warm up / admin", "start": "14:00", "end": "15:00", "type": "personal"},
            {"name": "DEEP WORK (fresh brain)", "start": "15:00", "end": "20:00", "type": "deep_work"},
            {"name": "Wife time / break", "start": "20:00", "end": "21:00", "type": "personal"},
            {"name": "Habits", "start": "21:00", "end": "22:00", "type": "habits"},
            {"name": "GRIT WORK (determination)", "start": "22:00", "end": "01:00", "type": "work"},
            {"name": "Wind down", "start": "01:00", "end": "02:00", "type": "personal"},
        ]
    else:
        deep_work = "3-4 hours deep work"
        blocks = [
            {"name": "Wake up + eat", "start": "12:00", "end": "14:00", "type": "personal"},
            {"name": "DEEP WORK", "start": "15:00", "end": "19:00", "type": "deep_work"},
            {"name": "Wife time", "start": "19:00", "end": "20:00", "type": "personal"},
            {"name": "Habits", "start": "20:00", "end": "21:00", "type": "habits"},
            {"name": "Extra work", "start": "21:00", "end": "23:00", "type": "work"},
        ]

    time_state = {
        "deep_work_hours": deep_work,
        "peak_window": peak_brain,
        "grit_window": grit_mode,
        "blocks": blocks,
        "timestamp": NOW
    }
    save_state(f"time-blocks-{TODAY}.json", time_state)

    print(f"\n⏰ Deep Work: {deep_work}")
    print(f"🧠 Peak Brain: {peak_brain}")
    print(f"🔥 Grit Mode: {grit_mode}")
    print("\n📅 Proposed Blocks:")
    for b in blocks:
        print(f"   {b['start']} - {b['end']}: {b['name']} ({b['type']})")
    log_event("STEP5", f"Time calculated: {deep_work}")

    return time_state


# ============================================================================
# STEP 6: GOOGLE CALENDAR PUSH
# ============================================================================
def step_6_calendar_push(time_blocks):
    print("\n" + "="*60)
    print("STEP 6: GOOGLE CALENDAR PUSH")
    print("="*60)

    # Import google_helper
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
    created = 0

    for block in time_blocks["blocks"]:
        if block["type"] == "personal":
            continue  # Skip personal blocks for calendar

        start_hour, start_min = map(int, block["start"].split(":"))
        end_hour, end_min = map(int, block["end"].split(":"))

        start_dt = datetime.datetime(today.year, today.month, today.day, start_hour, start_min)
        end_dt = datetime.datetime(today.year, today.month, today.day, end_hour, end_min)

        # Handle next-day end times
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

    log_event("STEP6", f"Created {created} calendar events")
    print(f"\n📅 {created} events pushed to Google Calendar")
    return created > 0


# ============================================================================
# STEP 7: CLOCKIFY SEED
# ============================================================================
def step_7_clockify_seed():
    print("\n" + "="*60)
    print("STEP 7: CLOCKIFY SEED")
    print("="*60)

    seed_script = BASE_DIR / "scripts" / "seed_clockify.py"
    if seed_script.exists():
        print(f"   Running: {seed_script}")
        print("   (This will wipe today's entries and seed from calendar)")
        # Note: We can't easily run this inline because it expects CLI args
        # and may have the crash bug. We log the instruction instead.
        print("\n   💻 MANUAL COMMAND:")
        print(f"   cd C:\\Users\\User\\Desktop\\PERFORM && python scripts\\seed_clockify.py --wipe")
        log_event("STEP7", "Clockify seed command prepared")
        return True
    else:
        print("   ⚠️ seed_clockify.py not found. Skipping.")
        log_event("STEP7", "FAILED: script not found")
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


def step_8_evaluate_evening():
    print("\n" + "="*60)
    print("STEP 8: THE RUTHLESS READING")
    print("="*60)

    questions = load_questions()["step_8_evaluation"]["questions"]
    quote = load_questions()["step_8_evaluation"]["closing_quote"]
    answers = {}

    for q in questions:
        print(f"\n🔹 {q['label']}")
        print(f"   {q['text']}")
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
        time_blocks = step_5_time_calculator(calc)
    else:
        time_blocks = load_state(f"time-blocks-{TODAY}.json")

    if step_num == 0 or step_num == 6:
        step_6_calendar_push(time_blocks)

    if step_num == 0 or step_num == 7:
        step_7_clockify_seed()

    if step_num == 0:
        step_8_evaluate()

    print("\n" + "="*60)
    print("MORNING ROUTINE COMPLETE")
    print("="*60)
    print(f"\nNext steps:")
    print(f"1. Check Daily.md: {OB_DIR / 'Daily.md'}")
    print(f"2. Open Google Calendar and verify blocks")
    print(f"3. Run Clockify seed: python scripts\\seed_clockify.py --wipe")
    print(f"4. Open Clockify desktop app")
    print(f"5. At end of day: python scripts\\tony_stark.py --evening")
    print(f"\nState files saved in: {STATE_DIR}")
    print(f"Log file: {LOGS_DIR / 'tony-stark.log'}")


if __name__ == "__main__":
    main()

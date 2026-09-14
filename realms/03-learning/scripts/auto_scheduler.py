"""
Auto-Scheduler — Run your outreach scripts on autopilot.
Uses the 'schedule' library to run scripts at set times.

HOW TO USE:
1. Edit the schedule below to add/remove scripts
2. Run: python scripts/auto_scheduler.py
3. Leave the terminal open — it runs until you close it
4. Or set it up in Windows Task Scheduler to start at boot

WHAT IT DOES:
- Checks for email replies every 2 hours
- Sends follow-ups daily at 9 AM
- Validates new leads nightly at 11 PM
- Runs lead finder daily at 8 AM
"""
import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

# Paths
OUTREACH = "C:/Users/User/Desktop/outreach"
PROJECT_TEST = "C:/Users/User/Desktop/PERFORM"
PYTHON = sys.executable

def run_script(script_path, description):
    """Run a Python script and log the result."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Running: {description}")
    print(f"  Script: {script_path}")

    if not os.path.exists(script_path):
        print(f"  [SKIP] File not found: {script_path}")
        return

    try:
        result = subprocess.run(
            [PYTHON, script_path],
            capture_output=True, text=True, timeout=300,
            encoding='utf-8', errors='replace'
        )
        if result.returncode == 0:
            print(f"  [OK] Completed successfully")
            if result.stdout.strip():
                # Show last 3 lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:
                    print(f"  > {line}")
        else:
            print(f"  [ERROR] Exit code {result.returncode}")
            if result.stderr.strip():
                print(f"  > {result.stderr.strip()[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] Script took longer than 5 minutes")
    except Exception as e:
        print(f"  [ERROR] {e}")


def check_replies():
    run_script(f"{OUTREACH}/emailing/check_replies.py", "Check email replies")

def send_followups():
    run_script(f"{OUTREACH}/emailing/follow_up.py", "Send follow-up emails")

def find_leads():
    run_script(f"{OUTREACH}/leads/find_google.py", "Find new leads via Google")

def validate_leads():
    run_script(f"{OUTREACH}/leads/validate_leads.py", "Validate lead emails")


# === SCHEDULE ===
# Uncomment the lines you want to activate

# schedule.every(2).hours.do(check_replies)           # Check replies every 2 hours
# schedule.every().day.at("09:00").do(send_followups)  # Follow-ups at 9 AM
# schedule.every().day.at("08:00").do(find_leads)      # Find leads at 8 AM
# schedule.every().day.at("23:00").do(validate_leads)  # Validate leads at 11 PM

# === FOR TESTING: Run everything once now ===
# Uncomment this block to test all scripts immediately:
# check_replies()
# send_followups()
# find_leads()
# validate_leads()


if __name__ == "__main__":
    jobs = schedule.get_jobs()
    if not jobs:
        print("=" * 50)
        print("  AUTO-SCHEDULER")
        print("=" * 50)
        print("\nNo jobs scheduled! Open this file and uncomment")
        print("the schedule lines you want to activate.")
        print("\nExample: Remove the # before:")
        print('  schedule.every(2).hours.do(check_replies)')
        print("\nThen run this script again.")
        sys.exit(0)

    print("=" * 50)
    print("  AUTO-SCHEDULER — Running")
    print("=" * 50)
    print(f"\nActive jobs: {len(jobs)}")
    for job in jobs:
        print(f"  - {job}")
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

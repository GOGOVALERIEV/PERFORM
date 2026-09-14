import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_calendar

cal = get_calendar()
TZ = "Europe/Sofia"

def ev(title, start, end):
    body = {
        "summary": title,
        "start": {"dateTime": f"2026-06-14T{start}:00", "timeZone": TZ},
        "end":   {"dateTime": f"2026-06-14T{end}:00",   "timeZone": TZ},
    }
    created = cal.events().insert(calendarId="primary", body=body).execute()
    print(f"  + {start}-{end}  {title}")
    return created

print("Creating today's blocks (June 14):")
# Eat block starts a few min in the past so it's HAPPENING NOW (the bridge test)
ev("Eat / Lunch", "15:15", "15:50")
ev("Main Block — Learn the docs (Angles/Hooks first -> explain back) + 2 course videos", "15:50", "18:20")
ev("Twitter - 25 min (read Boris's tweets, note 3 winners + why)", "18:20", "18:45")
ev("English - 30 min (rewrite a hook from the angles doc from memory)", "18:45", "19:15")
ev("Errands - count money, new card code, UBB phone-pay setup", "19:15", "19:35")

# Friends maintenance this week (Friends scored 4) — Monday evening, 20 min
body = {
    "summary": "Reach out to ONE person you actually want to connect with (20 min)",
    "start": {"dateTime": "2026-06-15T19:00:00", "timeZone": TZ},
    "end":   {"dateTime": "2026-06-15T19:20:00", "timeZone": TZ},
}
cal.events().insert(calendarId="primary", body=body).execute()
print("  + Mon 19:00-19:20  Friends maintenance (reach out to one person)")
print("DONE.")

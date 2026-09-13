# Clockify Skill

Use when George says "seed clockify", "push to clockify", "timer", or "time tracking".

## What It Does
Reads today's Google Calendar blocks → seeds Clockify timers with planned minutes → color-tagged by project.

## Key Commands
```bash
python scripts/seed_clockify.py --wipe    # Clear today, seed fresh
python scripts/seed_clockify.py           # Seed without wiping
```

## Project Colors (from config/clockify_projects.json)
- Learning 🟦
- Habits 🟩
- Personal 🟧
- Break ⬜
- Work 🟪

## Keyword→Project Mapping
Same as `calendar_timer.py` PROJECT_RULES:
- "learn", "read", "study" → Learning
- "twitter", "english", "habit" → Habits
- "ad", "client", "meta", "lfs" → Work
- "personal", "errand" → Personal
- "break", "lunch", "rest" → Break

## The Rule
George presses ▶️ himself. Nothing auto-tracks.
After seeding: open Calendar (Brave) + Clockify desktop (`C:\Program Files\Clockify\ClockifyWindows.exe`).

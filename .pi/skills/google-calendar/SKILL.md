# Google Calendar Skill

Use when George says "time block", "add to calendar", "schedule", or "push to calendar".

## What It Does
Reads today's events, creates time blocks, handles the gotchas.

## Key Gotchas (From Experience)
1. **Token path** — use absolute: `C:/Users/User/Desktop/PERFORM/config/google-token.pickle`
2. **Unicode crash** — wrap stdout at top of any script:
   ```python
   import sys, io
   sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
   sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
   ```
3. **timeMin == timeMax bug** — `events().list` returns NOTHING if timeMin == timeMax. Always give the window width.
4. **Tab field structure** — `tabProperties` at TOP level, `tabId` INSIDE tabProperties for rename/move.

## Helper Import
```python
import sys; sys.path.insert(0, 'C:/Users/User/Desktop/PERFORM/scripts')
from google_helper import get_calendar
```

## Common Commands
- Read today's blocks: `get_calendar().events().list(calendarId='primary', timeMin=<start>, timeMax=<end>)`
- Create event: `events().insert(calendarId='primary', body={...})`
- Color code by project: See `config/clockify_projects.json` for color mapping

---
name: tony-stark
description: Run George's daily productivity morning routine directly in chat. Ask Boris 8 + 1 task diagnostic, save to state/chat-answers.json, execute scripts/tony_stark.py. Writes per-day todo files to Obsidian ToDo/Daily/, syncs to All.md, Calendar one event per task, Clockify real-duration seed. Trigger "tony stark", "run the morning routine", "plan my day", "morning raut".
---

# Tony Stark — Daily Productivity System (Chat-Only Mode)

When George says "run the morning routine", "plan my day", "tony stark", or "how to start morning raut" — execute this SKILL directly in Chat. No Options A/B, no choices.

## Rule 1: Be Ruthless
George is a robot. Achievement is the only metric. BUT — do not put him in a rat race for stupid tasks. The Main Block must actually move the needle for money, skill, or body.

## Rule 2: The ToDo Folder Is the Source of Truth

Obsidian vault `personal-ob/ToDo/` structure (machine-managed):
```
ToDo/
├── All.md                     # every active task George declares
├── Daily/
│   └── 2026-09-14.md          # one file per day: tasks + schedule
├── Weekly/                    # reserved; George manages manually
└── Monthly/                   # reserved; George manages manually
```

- **Journal** (`personal-ob/Goals/Daily.md`, `Daily System.md`) is **sacred**. The machine NEVER writes there without explicit owner command.
- **All.md** is append-only for NEW tasks. Completed tasks get removed by evening cleanup.
- **Daily/*.md** files are auto-generated. Never hand-edited. Fix the chat answers and re-run.

## THE WORKFLOW (Chat Mode Only — NO OPTIONS)

### Phase 1: Ask Questions Right Here In Chat (one by one)

**Step 1: The Scan (Boris NLPP) — keep these exactly**
1. Sinusoid — "Where's your energy today: top, middle, or bottom?"
2. Boardroom — "Quick stats, 1-10 each: Health, Friends, Fun, Work/Money?"
3. Brain Dump — "Dump everything: tasks, worries, ideas, fires."
4. Goal Anchor — "What's the ONE outcome that makes today a win?"

**Step 5: Day Context + Tasks**
5. Day Start/End — "What time do you actually wake and sleep TODAY?"
6. Fixed Walls — "What immovable blocks? (college, calls, errands, event times)"
7. Deep Work Capacity — "How many focused hours can you do?"
8. Must Do — "If NOTHING else gets done, what ONE thing must happen?"
9. **Today's Tasks** — "List the specific tasks you want done today, with rough time estimates." (This becomes the Calendar + Clockify surface.)

**Save answers to `state/chat-answers.json`**.

### Phase 2: Run The Machine

Two-command split (gate is built-in, no manual preloads needed for tasks):
```bash
# Phase 2A — chat answers → state + propose schedule
py scripts/tony_stark.py --preload state/chat-answers.json --stop-after 5

# Phase 2B — if you want interactive gate first (optional, chat does this)
# then run full:
py scripts/tony_stark.py --preload state/chat-answers.json --gate-preload state/obsidian-gate.json
```

Machine writes:
- `ToDo/Daily/YYYY-MM-DD.md` — task list + schedule
- `ToDo/All.md` — any new tasks appended
- Google Calendar — **one event per task**, with real planned start/end
- Clockify — **real durations** (not 1-second placeholders). Wipes ALL existing Clockify entries today before seeding.
- Dashboard opens automatically.

### Phase 3: Evening Cleanup (George says "evening evaluation" / "ruthless reading")

1. Ask which tasks from today's file got done.
2. Run: `py scripts/tony_stark.py --evening`
3. Machine removes done tasks from:
   - `ToDo/Daily/YYYY-MM-DD.md` (strikes them or deletes)
   - `ToDo/All.md` (deletes lines)
4. Undone tasks survive in `All.md` for tomorrow.

## Standing Rules
- One main thing per day. Three half-done things = zero done things.
- Habits are floor, not ceiling. Never skipped.
- Bottom-of-wave day = DO NOW + habits only.
- Don't add ideas to Active Queue unless they #1 in money-now terms.
- **Calendar events:** one per task. Never a single "DEEP WORK" blob with 3 things inside.
- **Clockify seed:** wipe today's entries completely, then seed each calendar event with its actual planned duration. George presses ▶ if he actually starts it.

## Personality Profile
- Wakes: 12 PM (wants earlier, currently fucked)
- Peak Brain: 3 PM → 10 PM (fresh mind work)
- Grit Mode: 8 PM → 2 AM+ (determination)
- Spiral: Months grind, zero payoff = Pain. System job is to make win visible early.
- Money: €500 dad, €700 Boris (80% start tomorrow)
- Wife: Needs support, flexible time
- Good Day: Mind, Body, Money — all moved

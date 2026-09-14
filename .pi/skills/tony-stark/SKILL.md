---
name: tony-stark
description: Run George's daily productivity morning routine directly in chat. Ask 8 diagnostic questions, save answers to state/chat-answers.json, then execute scripts/tony_stark.py to generate Daily.md, push Google Calendar events, and seed Clockify. Trigger when George says "run the morning routine", "plan my day", "tony stark", or "how to start morning raut".
---

# Tony Stark — Daily Productivity System (Chat-Only Mode)

When George says "run the morning routine", "plan my day", "tony stark", or "how to start morning raut" — execute this SKILL directly in Chat. No Options A/B, no choices. Just ask 8 questions one by one and run the machine.

## Rule 1: Be Ruthless
George is a robot. Achievement is the only metric. BUT — do not put him in a rat race for stupid tasks. The Main Block must actually move the needle for money, skill, or body.

## THE WORKFLOW (Chat Mode Only — NO OPTIONS)

### Phase 1: Ask 8 Questions Right Here In Chat (one by one)

**Step 1: The Scan (Boris NLPP)**
1. Sinusoid — "Where's your energy today: top, middle, or bottom?"
2. Boardroom — "Quick stats, 1-10 each: Health, Friends, Fun, Work/Money?"
3. Brain Dump — "Dump everything: tasks, worries, ideas, fires."
4. Goal Anchor — "What's the ONE outcome that makes today a win?"

**Step 5: Day Context**
5. Day Start/End — "What time do you actually wake and sleep TODAY?"
6. Fixed Walls — "What immovable blocks? (college, calls, errands)"
7. Deep Work Capacity — "How many focused hours can you do?"
8. Must Do — "If NOTHING else gets done, what ONE thing must happen?"

**Save answers to `state/chat-answers.json`** (in PERFORM folder)

### Phase 2: Run The Machine

Execute with preload:
```bash
py scripts/tony_stark.py --preload state/chat-answers.json
```

Output:
- Step 2: Machine Check (Read Obsidian, Calculate)
- Step 3: Calculate Today (Pick Main Block)
- Step 4: Make The List (Write Daily.md)
- Step 5: Time Calculator (Build blocks around actual day)
- Step 6: Google Calendar Push (Creates events)
- Step 7: Clockify Seed Command (prepared)
- Step 8: End of Day Evaluation — Not now, at evening

### Phase 3: Opening Dashboard
Opens Google Calendar, Clockify, Obsidian — automatically.

## Evening Option (Only After Day Is Done)

When George says "evening evaluation" or "ruthless reading" — ask these 4:
1. Quality of Work (1-10, what shipped?)
2. Progress (what needle moved?)
3. Time Wasted (where did you leak time?)
4. Focus (deep work presence 1-10)

Then run `tony_stark.py --evening` and read output.

## Standing Rules
- One main thing per day. Three half-done things = zero done things.
- Habits are floor, not ceiling. Never skipped.
- Bottom-of-wave day = DO NOW + habits only.
- Don't add ideas to Active Queue unless they #1 in money-now terms.

## Personality Profile
- Wakes: 12 PM (wants earlier, currently fucked)
- Peak Brain: 3 PM → 10 PM (fresh mind work)
- Grit Mode: 8 PM → 2 AM+ (determination)
- Spiral: Months grind, zero payoff = Pain. System job is to make win visible early.
- Money: €500 dad, €700 Boris (80% start tomorrow)
- Wife: Needs support, flexible time
- Good Day: Mind, Body, Money — all moved

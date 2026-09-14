# Tony Stark Open Issues

## Issue 1: Boris NLPP Scan Questions Are Disconnected from Output

**Problem:** Steps 1–4 (Sinusoid, Boardroom, Brain Dump, Goal Anchor) were brought from Boris NLPP but they don't flow into the Time Calculator or the task schedule. The user answers them, but the machine only looks at the "Today's Tasks" list and Fixed Walls. Energy, boardroom scores, and goal anchor are displayed but don't change what actually gets scheduled.

**Next session:**
1. Research Boris NLPP original design — what were those 4 questions supposed to DO?
2. Reconnect them:
   - `sinusoid` → should limit number of tasks (top = full, middle = 1 big, bottom = do now + habits only)
   - `boardroom` → if any score < 4, schedule a maintenance session
   - `goal_anchor` → should be the #1 task, not separate from "today's tasks"
   - `braindump` → maybe extract and suggest tasks to add?
3. Decide: remove/adjust the 10-question split so the Boris scan feels meaningful again.

## Issue 2: Fixed Wall Language for Task/Wall Overlap

When user lists "event 8–11" as a fixed wall AND "networking at event (240min)" as a task, the scheduler:
- Blocks 8–11 as sacred
- Drops the 4-hour networking into whatever afternoon gap exists
- Squeezes other tasks

**Fix:** Either auto-merge task with matching wall, or warn that a task overlaps a wall.

## Issue 3: Break Parser Edge Cases

`00:00 eat` parsed but needs better handling — should probably be `23:30 eat after event` or post-sleep. Single-time breaks default to 30min which may not match intent.

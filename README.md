# PERFORM — Life Helper System

## What This Is
Not a project. Not a chaos folder. A **life helper machine**.

## The Structure

```
PERFORM/
├── .pi/skills/          ← Pi skills (auto-loaded) — tony-stark, google-calendar, clockify, meta-ads, lfs-operator
├── .pi/prompts/         ← prompt templates (optional)
├── config/              ← API keys, tokens, registry
├── realms/              ← ORGANIZED work areas (one per life area)
│   ├── 01-productivity/ ← Daily life ops (Calendar, Clockify)
│   ├── 02-work/         ← Ads, copywriting, LFS, research
│   ├── 03-learning/     ← Courses, transcripts, skill building
│   ├── 04-outreach/     ← Portfolio, leads, network
│   └── 05-business/     ← Firm, funnels, payments
├── scripts/             ← Shared libraries (google_helper.py, etc.)
├── docs/                ← Business bible, terms, guides
├── input/               ← Data for scripts
├── output/              ← Results (auto-cleaned)
├── state/               ← Runtime state (Tony Stark)
├── logs/                ← Jerry's log
└── CLAUDE.md            ← ~500-token thin index
```

## How to Use
1. Open the right `realms/<name>/` folder
2. Read `SKILL.md`
3. Run the script
4. Stay organized

## The Machine
**Morning:** Run `tony-stark` (5 questions + day context → machine calculates → Google Calendar → Clockify → Obsidian)
**Evening:** Run `tony-stark --evening` (quality, progress, time wasted, focus → ruthless reading)

## Rules
1. One realm per task — don't mix productivity stuff with work scripts
2. Clean, finished files only — no dumps
3. Every realm gets a SKILL.md — like TONY STARK
4. Git push after every meaningful change

## Commit
Latest: af8a333 ("Step 5: Day context questions")

Repo: https://github.com/GOGOVALERIEV/PERFORM

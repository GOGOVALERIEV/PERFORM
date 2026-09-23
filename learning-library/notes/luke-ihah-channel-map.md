# Luke Iha — Channel Sauce Map

Pulled: 2026 (this session)
Channel: https://www.youtube.com/channel/UCH6T9yyI_SqV_H25Y4I7FKQ

## What was captured

| File | What it is |
|---|---|
| `raw/youtube/luke_iha_links.md` | All 48 videos + every link in every description |
| `raw/youtube/luke_iha_descriptions.json` | Full descriptions (JSON, reusable) |
| `raw/youtube/luke_doc_1_master.txt` | Google Doc linked in 8 newest videos — **sales page** (Genesis testimonials wall) |
| `raw/youtube/luke_doc_2_openclaw.txt` | Google Doc in OpenClaw video — **sales letter** ($97 bootcamp pitch) |
| `raw/youtube/aimarketers/*.html` | **THE REAL SAUCE** — full articles from Luke's free newsletter theaimarketers.ai |

## The real sauce: theaimarketers.ai

Luke's descriptions gated the docs behind an email opt-in (`lukes-best-copy-trainings-yt-a` = ClickFunnels opt-in, no direct docs). But his free newsletter is a **public Ghost blog with full articles**:

- `/eliminate-claude-speak/` — Anthropic's own prompt to strip "Claude speak" from AI writing
- `/top10-antiaislop-skills/` — Top 10 skills that kill AI-slop writing tells
- `/grok-bot-guides/` — 5 Grok bot guides
- Plus weekly Monday Memos and "Need to Know News" issues (see site archive `/page/2/`)

## Key links from descriptions (deduplicated)

- Proof doc (testimonials): https://docs.google.com/document/d/10rZQrvmFq1noTdzh-LLyn8ei02a-hJ3TLQUGn5DVnYk/edit?tab=t.0
- Copy review form: https://docs.google.com/forms/d/e/1FAIpQLSftC7CiaunmP1QL082NQR5arFldHT5K7qwJorhUcRkbtg5eHQ/viewform
- Free trainings opt-in (email gate): https://www.copycoders.ai/lukes-best-copy-trainings-yt-a
- Newsletter (full articles, public): https://www.theaimarketers.ai/
- OpenClaw workflow doc (bootcamp pitch): https://docs.google.com/document/d/19Ki7xdY5BbcOdvrA-3i0csvyrA2-3NTVefdaxrMzLQg/edit?tab=t.0

## Verdict (honest)

The Google Docs he links are NOT the sauce — they're funnels. The sauce is:
1. **The video content itself** — ✅ DONE: all 48 transcripts captured
2. **theaimarketers.ai articles** (free, public, full-text)
3. **His descriptions** (each contains a full topic breakdown of the video)

## Transcripts (COMPLETE)

All 48 video transcripts live in `channels/luke-iha/transcripts/` (one .txt per video).
Pulled via `scripts/channel_transcriber.py` (yt-dlp + YouTube cookies + node JS challenge solver,
paced 5-10s between requests to dodge the caption rate limit).
Resumable — rerun the script and it skips videos already in `channels/luke-iha/state.json`.
Start with the reading order in `channels/luke-iha/README.md`.

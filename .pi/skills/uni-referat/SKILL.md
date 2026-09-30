---
name: uni-referat
description: George's university referat pipeline (SWU). Full drafting + verification workflow: outline → closed-book draft → style pass → ksim/stylecheck/phrase-audit gates → evidence pack. Trigger "uni-referat", "напиши реферат", "university paper".
---

# UNI-REFERAT — the referat pipeline

You are running George's university drafting pipeline for SWU (realm 06-university).
Everything routes through the tested scripts — never do their math by hand.

## RULES THAT OUTRANK EVERYTHING
1. Raw LLM output is radioactive: it never becomes a submission. Pipeline ends at the human pass.
2. StrikePlagiarism NEVER receives a test file. Testing = local scripts + plag.bg (no-DB) + GPTZero only.
3. No manipulation tricks ever (letter swaps, hidden chars) — they are detectable "intent to deceive".
4. Duo rule: not one sentence crosses between George and Valeria's papers.
5. ELICIT IS THE LIBRARIAN, NEVER THE WRITER. Its prose measured 99% AI on JustDone (3×,
   2026-09-30, see research/presentation-tools-research.md + battery-log.md). Elicit output
   (summaries, reports) NEVER enters a draft. It fills the pantry (Stage 0) — nothing else.
   Manual clicks only — no automation against Elicit (quota is small, ToS, and George's clicks
   are the whole quota).

## WORKFLOW

### 0a. Scaffold
```
python realms/06-university/scripts/make_assignment.py "<Курс>" "<slug>"
```
Fill 01-outline.md: thesis, sections-with-theses, dial settings (Duo), limitations.

### 0b. Corpus via Elicit (STAGE 0 — manual, free tier, George clicks)
1. George searches the topic on elicit.com (unlimited search on free plan)
2. Open the source list → read the per-paper AI summaries (unlimited)
3. Chat with the most relevant papers (unlimited full-text chat) to extract:
   real author names, years, claims with citations, key facts/dates
4. Write a BULLET FACT-PACK (fragments only — no finished sentences, Duo-safe)
   with per-fact source attribution (author, year, journal)
5. Save to the assignment's 00-notes/ (+ full paper URLs for Learn Bot book mode)
6. If a paper has a public URL/PDF → Learn Bot can teach from it (uni-app book mode)

NEVER: paste Elicit summaries/reports into any draft, prompt them for "rewriting",
or treat them as submission text. 99% AI — proven with data.

### 1. Draft (P0→P2, prompts in realms/06-university/prompts/drafting-prompts.md)
- P0 outline (LLM-assisted, never submitted)
- P1 closed-book body draft — inject config/voice-profile.yaml (persona "G")
- P2 style sweep — then tag paragraphs DEF/ARG/FILL; cut FILL; George hand-writes
  intro + conclusion (SC-11). George's manual pass is MANDATORY, not ritual.
- Save each stage to 02-versions/, opened+saved in Word by George (Real-Editor
  Rebirth — honest metadata). Word identity must be set up once (File→Options→name).

### 2. Local gates (ALL must pass before anything else)
```
python realms/06-university/scripts/ksim.py <final.txt|docx> <corpus_dir> --json state/ksim/runs/<id>.json
python realms/06-university/scripts/stylecheck.py <final>
python realms/06-university/scripts/phrase-audit.py <george.txt> <valeria.txt>   # duo only
```
Gates: КС2 non-quote = 0 (hard), КС1(>=4) <= 2%, stylecheck PASS, phrase-audit PASS.
FAIL → fix flagged sentences → re-run (max 2 cycles, then back to the outline).

### 3. External battery (only after local PASS; no personal data in test files)
- plag.bg upload → screenshot → log row in realms/06-university/research/test-runs/battery-log.md
- GPTZero (paste body sample, not file) → log
- ZeroGPT: canary only, never a gate
- Record: date | tool | file | similarity % | AI % | verdict

### 4. Export & evidence
- Final .docx → Word → File → Export → Create PDF (never print-to-PDF from browser)
- Pre-flight check: Author = George, no "python-docx"/2013 dates, TotalTime > 0
- PDF + .docx → 04-final/; plag.bg screenshot → 03-selfcheck/; sent email .eml → 05-submission/
- Git commit at each stage (outline/draft/selfcheck/final) — push same day.

### 5. Corpus
Every real source saved as .txt under state/corpus/<topic>/ BEFORE drafting.
Corpus = the actual sources + BG Wikipedia + top web results on the topic.
Preferred: built via Elicit first (Stage 0b) — real papers beat Wikipedia.
Elicit's own summaries are pantry material only: facts extracted, prose discarded.

## FACT-DIFF INVARIANT
Numbers, dates, names, citations must be IDENTICAL between P1 draft and final.
The style pass changes zero facts. This is checkable by comparing digit sequences.

# THE TEST PROTOCOL — How We Prove the Pipeline Passes (Before We Ever Build the Final Thing)

**Agent:** counter5 (countermeasure strategist) · **Mission:** MISSION 5 · **Date:** 2026-09
**Deliverable type:** test protocol (design; build comes after the pipeline skeleton exists)

---

## 0. The Core Idea (in plain words)

Think of it like crash-testing a car before selling it. We build a test paper, we smash it
against every detector a professor could realistically use — **except the real one**
(StrikePlagiarism, because everything sent there is stored forever in SWU's corpus). The
official system we can only *simulate at home*: it publicly defines two similarity
measures — **КС1 = matching fragments of 5+ words**, **КС2 = matching fragments of 25+ words**
(numbers from the mission brief; methodology per agentA's StrikePlagiarism research) — and
both are exactly the kind of thing a cheap local script can model.

**The one hard safety rule of this whole document:**
> **STRIKEPLAGIARISM NEVER RECEIVES A TEST FILE. Not once, not "just to see". Every
> submission is archived permanently and feeds the university cross-check corpus forever.**
> All testing happens through (a) the local simulator and (b) free non-archiving web tools.

---

## 1. Local КС1/КС2 Simulator — Spec (design only)

**Name:** `ksim.py` · **Location:** `realms/06-university/scripts/` · **Cost:** 0 лв
**Stack:** Python 3.11+, standard library (+ optional `pip install rapidfuzz`).

### 1.1 What it answers

For a candidate paper (`.docx`) vs a source corpus (folder of `.txt`/`.pdf`-extracted texts):

| Metric | Definition (mirrors StrikePlagiarism) |
|---|---|
| **КС1** | verbatim word-sequence matches of **≥5 words** between paper and any source |
| **КС2** | verbatim word-sequence matches of **≥25 words** ("hard plagiarism" signal) |
| **Paraphrase layer** | near-copy sentences with ≥85% token similarity (models SmartMarks-style fuzzy matching) |
| **Quote layer** | matches that fall inside properly marked direct quotes → separated, never silently ignored |

### 1.2 Pipeline, step by step

**Step 1 — Normalize.**
- `.docx` → text via `python-docx` (paragraph texts joined by `\n\n`).
- Lowercase; tokenize on `[\wа-яА-ЯёЁ]` runs (Cyrillic + Latin letters + digits);
  punctuation becomes token boundaries. Hyphenated words → single token with hyphen removed
  (**dual mode**: run once with hyphen kept, once split — we don't know the vendor's tokenizer,
  so we report the worst case of both).
- **Do NOT remove stopwords** for the КС layers. The real system counts function words
  ("на", "и", "е") inside 5-word windows — so do we. Stopword removal is allowed only in the
  paraphrase (fuzzy) layer.
- Track a per-token offset map so every match can be reported back as *original text* with
  position (word № and paragraph №) for human review.

**Step 2 — Corpus index (built once per corpus, cached to JSON/pickle).**
- Extract all **5-grams** (word-level) from the whole corpus → dict
  `hash(5-gram) → list of (file_id, token_position)`.
- Complexity for a **100,000-word corpus**: 100k hash ops, ~100k dict entries →
  **< 2 s, < 50 MB RAM**. This is the whole index — nothing fancier needed.

**Step 3 — Seed + extend (the matching itself).**
- Slide a 5-word window over the paper (≈3,000 words for 10 pages): each 5-gram → one O(1)
  dict lookup. ~3,000 lookups, **< 1 s**.
- Every hit is a **seed**. Store the corpus position(s). Worst case a common boilerplate
  5-gram appears 1,000× in the corpus → extension work ×1,000 on that one seed; still
  milliseconds. Cap extension lists at 50 positions per seed (report "widespread phrase" if
  the cap is hit — itself useful output).
- **Extend** each seed maximally in both directions by direct token comparison (paper token
  vs corpus token at the corresponding offset) → **maximal common substring** per seed cluster.
- Merge overlapping/nearby maximal matches.
- Complexity total: **O(C + P + E)** where E (extension work) is tiny in practice. This is
  why we do NOT use `difflib.SequenceMatcher` (worst-case O(n·m), 100k × 3k = 300M ops, slow
  and fragile) and do NOT build suffix arrays/automata (O(C) elegance, wasted on this size —
  more code, same answers). `rapidfuzz` is kept only for the sentence-level fuzzy layer
  (Step 5), where it's the right tool.

**Step 4 — Aggregate → the КС numbers.**
- From maximal matches compute, for thresholds {≥4, ≥5, ≥20, ≥25}:
  - count of matches,
  - **coverage %** = words of the paper lying inside a match of that threshold ÷ total words,
  - `max_match_words` (longest common contiguous run),
  - per-match detail: length, paper range, source file + range, quote-flag.
- **Why the off-thresholds (≥4, ≥20)?** Our tokenizer is not the vendor's. Punctuation,
  dashes, abbreviations ("т.нар.", "ООН") can shift a word count by one. If a match is 4
  words for us it may be 5 for them. So: **acceptance gates use the stricter (≥4 / ≥20)
  numbers; the "official" ≥5/≥25 numbers are reported for the record.**

**Step 5 — The trick case: sub-5-word matches across phrase boundaries.**
This is where naive implementations lie to you. A match of exactly 4 words doesn't count for
КС1 *in isolation* — but the real system's fuzzy layer can still merge
`[4-word match] + gap ≤ 2–3 swapped words + [4-word match]` into a flagged paraphrase
fragment, especially *across sentence boundaries* ("кратки фрази" stitched together). The
simulator therefore has two defenses:
1. **Gap-merge pass:** any two maximal matches (each ≥4 words) separated by ≤3 differing
   tokens in BOTH paper and corpus are merged into a candidate fuzzy-fragment and counted
   toward КС1 risk (flagged as `merged_short_match`).
2. **Sentence-screening pass:** split paper and corpus into sentences; for each paper
   sentence, generate candidate corpus sentences sharing **any 3-gram** (inverted index —
   keeps this near-linear instead of O(sentences × sentences)); compare with
   `rapidfuzz.fuzz.token_set_ratio` on stopword-filtered tokens. Flag pairs ≥85% similarity
   and ≥6 words as `paraphrase_risk`. (~300 paper sentences × small candidate sets →
   seconds.) Fallback if rapidfuzz unavailable: `difflib.SequenceMatcher.ratio()` per
   candidate pair (slower but fine at this scale).

**Step 6 — Quote handling.**
- Detect direct quotes: „…", «…», "…", and markdown-ish indentation in our drafts, plus a
  simple citation regex `(Автор, год.)` / footnote markers.
- Matches inside quotes → tagged `quote`, excluded from КС2=0 gate **but reported**, because
  (a) StrikePlagiarism shows quotes to the teacher separately, (b) excessive quoting is its
  own red flag (see gate in §3).

### 1.3 Report format (what comes out)

One JSON per run → `realms/06-university/state/ksim/runs/<paper-id>.json` + a human-readable
Markdown summary. Fixed schema:

```
{
  "run_id", "timestamp", "paper_file", "paper_sha256",
  "corpus_manifest": {file, sha256, words} [...],
  "max_match_words", "ks1": {"ge4_pct", "ge5_pct", "count_ge4", "count_ge5"},
  "ks2": {"ge20_count", "ge25_count", "matches": [...]},
  "paraphrase_risk": [{paper_sent, corpus_sent, file, score}...],
  "merged_short_match": [...],
  "quote_pct", "quotes": [...],
  "verdict": "PASS|FAIL", "gate_failures": [...]
}
```

Every field is machine-checkable → this is also the backbone of the regression test (§5).

### 1.4 Known blind spots (honesty section)

The simulator models **exact + fuzzy overlap against the sources WE hold**. It cannot see:
- StrikePlagiarism's internal DB (35M scientific sources per МОН's announcement, archived
  student papers, cross-check between classmates);
- translated-source detection (their BG site advertises similarity search in *translated*
  texts) — mitigation: when we paraphrase from an English source, also run the simulator
  against the English original (Cyrillic/Latin both tokenize fine);
- their AI module (AIPC) — that's what the external battery (§2) + stylometry gates (§3, §5)
  are for.

---

## 2. External Test Battery — exact sequence per paper

**Order matters: cheapest and safest gate first, noisy tools last, so we never waste a
manual check on a paper that already failed locally.**

| # | Tool | Role | What we record | Why this role |
|---|---|---|---|---|
| 0 | Local `ksim.py` + stylometry script | **Gate 1** | full JSON report | free, instant, no upload; kills 90% of failures before any manual work |
| 1 | **plag.bg free check + its AI detector** | **Gate 2 — primary external** | similarity %, AI %, flagged fragments (screenshot), date/time, UI version, exact file name | Bulgarian-native; closest public proxy to the local detection stack; terms state free-check files are **never added to any comparison DB** (per agentA's terms research — **re-verify the clause every session**, see safety rules) |
| 2 | **GPTZero free tier** | Gate 3 — secondary | AI probability %, per-sentence highlights (screenshot), date | claims Bulgarian support; **unvalidated for BG** → treated as a noisy secondary signal, never a sole verdict |
| 3 | ZeroGPT | Canary — optional | score only, screenshot | known high false-positive rate (flags any formal academic register); informational, **no pass/fail gate** |

### The sequence (checklist form)

1. **Prep the test artifact:** save the paper as
   `paper-vN-persona-<A|B>-topic-<slug>-TEST.docx`; author metadata = test persona
   ("Т. Тестов"); **zero personal data anywhere** (no real student names, no faculty numbers).
2. **Gate 1:** run `ksim.py` + stylometry. FAIL → fix, regenerate, rerun. Never proceed to
   uploads with a local FAIL.
3. **plag.bg:** upload the test file; screenshot the full report (similarity panel + AI panel
   + fragment list); log row into `research/test-runs/battery-log.md`:
   `date | tool | version/URL | file | similarity % | AI % | top flagged fragment (3 words) | verdict`.
4. **GPTZero:** **paste the plain text** (not the file) — paste gives us control of exactly
   what leaves the machine; record score + sentence highlights; screenshot.
5. **ZeroGPT (optional):** paste only if step 4's result was ambiguous; score recorded,
   weighted lowest.
6. **Close-out:** copy all screenshots to `research/test-runs/<run-id>/`; verdict PASS/FAIL
   vs §3 gates appended to the log.

### Safety rules (non-negotiable)

- **Never** the university Blackboard / disted.swu.bg flow. No institutional session cookies
  in the browser used for testing (separate profile; Brave, not the university browser).
- **plag.bg clause check every session:** before first upload of the semester, open their
  terms/privacy page, quote the "files not added to any comparison DB" clause in the battery
  log with the date. **If the clause is gone or changed → plag.bg is dropped from the battery
  for that semester** and we fall back to paste-only tools. The safety property is verified,
  not assumed.
- **GPTZero/ZeroGPT:** paste text only, never files; confirm no personal data in the pasted
  text (these tools' data-handling policies change without notice — check privacy pages
  monthly, log the date checked).
- **Test persona always.** The final submitted paper is never co-located with test artifacts
  under the same filename/persona, so nothing test-related can be confused with the real
  submission trail (counter4's evidence pack stays clean).

---

## 3. Acceptance Criteria — the numbers, and where each comes from

| # | Gate | Threshold | Source of the number |
|---|---|---|---|
| A1 | **КС2 (≥25-word matches, non-quote)** | **0** | StrikePlagiarism КС2 = "hard plagiarism" fragments; any single 25-word verbatim run is a red-flagged fragment shown to the teacher. Zero is achievable at zero quality cost, so we demand zero. |
| A2 | **КС1 coverage (≥4 words, worst-case tokenizer mode)** | **≤ 2%** of paper words | Derived, honestly: no public per-institution КС1 % exists, so we set ours from (a) the **measured terminology baseline** of negative controls (§4 Tier 3 — topic terms like "Съветът на сигурност на ООН" inevitably repeat) and (b) ~3× margin for tokenizer mismatch. Threshold = max(2× control baseline, 2%), recalibrated per corpus. |
| A3 | **Quote volume** | ≤10% of paper; no quote ≥3 sentences | Academic convention scale (faculty norms commonly tolerate quoting in the single-digit %); above ~10% the paper reads as a collage even when legal, and teachers see the quote panel. |
| A4 | **Paraphrase risk sentences (≥85% token similarity)** | **0** outside quotes | Models SmartMarks-style fuzzy matching: structure-preserving synonym swaps are exactly what catches "rewritten copy-paste". 85% ≈ "same sentence with words swapped", the standard authorship-theft definition. |
| A5 | **plag.bg similarity** | **< 10%** | plag.bg's own UI semantics + headroom below any plausible institutional originality threshold (70–85% originality norms ⇒ ≤15–30% similarity tolerated; we hold a 2–3× stricter line). |
| A6 | **plag.bg AI-detector score** | **< 20%**, and no single contiguous AI-flagged block > 1 paragraph | 20% is a chosen risk threshold calibrated against controls (§4): human BG academic text scores low on such detectors but false positives exist on formal register; 20% absorbs noise while catching a systematic AI signature. A large contiguous flagged block matters more than the average — one flagged page reads worse than ten scattered sentences. |
| A7 | **GPTZero** | ≤ "mixed"; hard fail only if >25% of sentences are confidently highlighted | Bulgarian support is unvalidated → noisy secondary; the strict load is carried by A5/A6 + local gates. |
| A8 | **ZeroGPT** | no gate — informational | documented false-positive noise on academic register; recorded as canary only. |
| A9 | **Structure / burstiness** | ≥3 paragraphs; paragraph word-count σ ≥ 25% of mean; no paragraph >180 words; sentence-length σ/mean ≥ 0.35 | The primary stylometric AI signature (AIPC-class modules key on low variance / uniform sentence rhythm); real student writing is bursty. Numbers are engineering targets validated against the human-controls corpus, not vendor specs. |
| A10 | **Human trace** | ≥2 "student marks" per 1,000 words (first-person transition, mild informality, one naturally imperfect construction) — manual checklist | Human-layer defense; can't be automated honestly, so it's a checklist, not a number. |

**Verdict rule:** gates A1, A4, A9 are hard-fail. A2, A3, A5, A6 allow one "yellow" if the
run log explains it and the next revision fixes it. Two cycles with the same yellow = red.

---

## 4. Test Corpus Design

Location: `realms/06-university/state/corpus/<topic>/` · manifest: `manifest.json`
(file, sha256, words, tier, date added) — every run reports against a **hash-pinned**
manifest so results are reproducible.

| Tier | Content | Why it's in the corpus |
|---|---|---|
| **T1** | The **actual sources** of this реферат (every article/book/web page we drew from, saved as .txt) | The primary comparison — КС1/КС2 vs these is the real exam question |
| **T2** | **BG Wikipedia** on the topic + top ~10 Bulgarian web results (saved as .txt) | The "typical internet text" — approximates what the vendor's web crawl will compare against; Wikipedia phrasing is the most commonly recycled text on earth |
| **T3** | 3–5 **self-drafted "previous-years-style" generic essays** on the topic (deliberately formulaic, human-written) | **Negative controls**: (a) AI-detector floor — should score ~0; (b) КС1 terminology baseline — calibrates gate A2 |
| **T4** | Any anonymized prior SWU-style student reports we can ethically hold | Approximates the cross-check corpus (classmates, past submissions) |

### Positive control (proves the test itself works)

Build a **deliberately broken test paper**: paste one **30-word sentence** and one **8-word
phrase** verbatim from a T1 source into an otherwise clean draft.

- **Expected ksim result:** КС2 (≥25) count = **1**, located to file+position; КС1 coverage
  jumps visibly; both fragments in the match list.
- **If the simulator does NOT flag it → the harness is broken and every green result ever
  produced is VOID.** This control runs **first, before any real paper is ever tested** —
  same logic as a lab running a known-positive sample before trusting a negative.
- Second positive control, for the external tools: a **raw, unedited ChatGPT paragraph**
  through the battery → should score high-AI on plag.bg/GPTZero. Re-run **monthly** — these
  tools silently change models, and the control tells us when their behavior shifted.
- Negative control for the human floor: a paragraph **George writes by hand** (imperfect,
  idiosyncratic Bulgarian) → should score ~0 AI, ~0 КС1. This is the "human baseline" every
  pipeline output is compared against.

---

## 5. The Blank-Page Regression Test (stylometry consistency = the human-layer defense)

The professor's real weapon is the one agentA documented: **"a series of documents by the
same author"** — comparing papers submitted across the semester. If paper #1 and paper #9
have different statistical fingerprints, *that* is the tell. So the battery includes a
regression layer:

**What we compute per paper (automated, `styleprint.py`):**
sentence-length mean/σ, paragraph-length distribution, punctuation rates (commas, dashes,
colons per 1k words), connector frequencies ("Освен това", "От друга страна", "На първо
място"…), type-token ratio over rolling 500-word windows, question-sentence rate.

**Where it goes:** `state/styleprints/<persona>.json` — a growing **style fingerprint** per
test persona.

**Acceptance:**
- Same persona across different papers (produced weeks apart, different topics): feature
  vectors **cosine similarity ≥ 0.85** vs the persona's own centroid — they must read as the
  *same writer who varies*.
- Different personas: similarity **≤ 0.70** — so cross-checking between "classmates" doesn't
  show twins. (Thresholds calibrated on the T3 control essays, then held fixed.)
- Every paper's fingerprint appended to the log; any drift > threshold = regen with the
  style layer, not a manual tweak.

**Cadence:** full battery (all gates) on **every** paper; fingerprint regression on **every**
paper; full external battery re-calibration (positive + negative controls) **monthly**,
because external tools change under our feet.

---

## 6. Cost & Time Estimate

| Task | Time | Automated? |
|---|---|---|
| Corpus build (one-off per topic: T1–T4 collection + manifest) | 60–120 min | half (fetch script + manual curation) |
| Corpus index build | < 2 min, cached | yes |
| `ksim.py` run per paper | < 10 s (JSON) + 10 min human review of match list | run yes, review manual |
| Stylometry / fingerprint run | < 1 min | yes |
| plag.bg upload + screenshots + logging | ~10 min | manual (no public API on free tier) |
| GPTZero paste + record | ~5 min | manual |
| ZeroGPT (optional) | ~3 min | manual |
| Battery write-up + verdict | ~10 min | skeleton auto-generated from JSONs |
| **Total per test cycle (one paper)** | **≈ 35–45 min** (≈5 min machine, rest human review) | |
| Monthly re-calibration (controls through external tools) | ~20 min | manual |

**Cost: 0 лв.** Everything runs on free tiers and a stdlib-plus-one-package local script.
The only non-automatable parts are the paste/upload actions and the fragment eyeballing —
which is a feature: a human who reads the flagged fragments learns what "too close" looks
like, and that skill is the real defense.

---

## 7. Limitations (stated once, plainly)

1. КС1/КС2 definitions come from the mission brief + agentA's StrikePlagiarism research;
   Bing RSS was bot-walled this session (junk results only), so no independent online
   confirmation of the exact 5/25 thresholds was added — flagged for re-verification when a
   primary StrikePlagiarism methodology page is reachable.
2. The simulator sees only the sources we hold; the vendor's 35M-source DB is invisible.
   Mitigation: broad T2 corpus + unique phrasing discipline.
3. plag.bg's no-archiving clause is verified per session, not trusted across semesters.
4. GPTZero's Bulgarian support is a claim, not a fact — hence its low gate weight.

Search log: 2× Bing RSS queries → polluted results (unrelated sites); direct fetch of
strikeplagiarism.com/bg/ → product features confirmed (AI module, cross-check, translated-text
similarity, ЗВОД/privacy marketing); /bg/how_it_works.html → 404.

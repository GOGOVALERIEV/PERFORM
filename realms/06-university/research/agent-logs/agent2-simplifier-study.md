# Agent 2 Report — Simplifier, Study Methods & Memory Research
Date: 2026 (research session). Scope: research only, no code built.
Verification legend: ✅ verified live during this session (URL given) · ⚠️ unverified / general knowledge, treat with care.

---

## Q1. Long-document processing with LLMs in 2026 (200–500 page books / large PDFs)

### 1.1 The token math first (why this problem is smaller than it looks)
- ✅ Gemini counts a PDF page at **~258 tokens/page** for typical documents (https://ai.google.dev/gemini-api/docs/document-processing). Even if humanities prose runs denser, a realistic figure is **~250–400 tokens/page**.
- Therefore:
  - 200-page book ≈ 50k–80k tokens
  - 300-page book ≈ 75k–120k tokens
  - 500-page book ≈ 125k–200k tokens
- **All current flagship models (1M-token contexts) fit a whole 500-page book in one prompt.** This is the headline fact: George's "huge books" are *not* huge for a 2026 model.

### 1.2 Which models, verified pricing/context (official pages, fetched live)
| Model | Context | Input $/MTok | Output $/MTok | Notes |
|---|---|---|---|---|
| Gemini 2.5 Pro | 1M | $1.25 (<200k prompt) / $2.50 (>200k) | $10 / $15 | ✅ ai.google.dev/pricing |
| Gemini 3.1 Pro Preview | (1M ⚠️ assumed from family) | $2.00 (<200k) / $4.00 (>200k) | $12 / $18 | ✅ pricing page |
| Gemini 2.5 Flash | 1M | $0.30 | $2.50 | ✅ pricing page — the workhorse for chunk jobs |
| Claude Sonnet 5 | 1M | $2.00 | $10 | ✅ docs.claude.com pricing |
| Claude Opus 5 | 1M | $5.00 | $25 | ✅ |
| Claude Fable 5.1 | 1M | $10.00 | $50 | ✅ |
| Claude Haiku 4.5 | 200K | $1.00 | $5.00 | ✅ |
| GPT-5.6 Sol | ⚠️ not verifiable from JS-rendered page | $4.00 | $20.00 | ✅ prices, ⚠️ context |
| GPT-5.6 Terra | ⚠️ | $2.00 | $12.00 | ✅ prices |
| GPT-5.6 Luna | ⚠️ | $0.20 | $1.20 | ✅ prices — ultra-cheap tier, good for map-reduce chunks |

Practical pick for the Simplifier: **Gemini 2.5 Flash / GPT-5.6 Luna for mechanical chunking**, **Gemini 2.5 Pro or Claude Sonnet 5 for the final synthesis** (better Bulgarian prose, better instruction-following on exam-style tasks).

### 1.3 Gemini's PDF-native path (the killer feature for this use case)
✅ Verified (https://ai.google.dev/gemini-api/docs/document-processing):
- Upload PDFs up to **50 MB / 1000 pages** via the Files API.
- **"You are not charged for tokens originating from the extracted native text in PDFs"** — for a *digital* (non-scanned) textbook, reading a 300-page book costs mostly output tokens, pennies.
- Pages are rendered as images too, so charts/maps in IR textbooks get "seen".
- Caveat: scanned books (image-only PDFs) are charged per rendered page (~258 tok/page ≈ still cheap).

### 1.4 The four strategies, and when each wins
1. **Direct long-context full read** — dump the whole book, ask for the exam brief once.
   - Best when: book ≤ ~200k tokens (almost always true here), and you want global structure (chronology, cross-chapter comparisons — exactly what IR/history exams demand).
   - Known weakness: **"Lost in the Middle"** (✅ Liu et al., arXiv:2307.03172 — confirmed title live) — recall is strongest at the beginning and end of context. Mitigation: request extraction *per chapter*, structured output, and don't rely on a single giant prompt for precision recall of mid-book details.
   - Cost example, 500-page book (~130k text tokens): input on Gemini 2.5 Pro ≈ **$0.16**; output 6k tokens ≈ $0.06 → **~$0.22/book**. On Gemini 2.5 Flash ≈ **$0.05/book**. ✅ computed from verified prices.
2. **Chunk + map-reduce** — split by chapter (PDF table of contents via PyMuPDF), summarize each chunk with a cheap model (map), then synthesize (reduce).
   - Best when: book is scanned/oversized, or you want page-cited notes you can audit. Deterministic, resumable, and each chunk summary can carry page numbers → kills hallucinated quotes.
   - Cost: same book, ~15 chunks × (8k in + 500 out) on Gemini 2.5 Flash ≈ **$0.05**, then reduce on Pro ≈ $0.05 → **~$0.10/book**.
3. **Hierarchical summarization (summaries of summaries)** — chunk notes → chapter summaries → thematic synthesis ("diplomacy", "theory", "chronology").
   - This is the best quality/effort ratio for **humanities texts** specifically: humanities arguments are narrative and cumulative, so a 3-level pyramid preserves the arc while forcing the model to compress 10× at each level. Recommended as the default backbone of the Simplifier.
4. **RAG (embed + retrieve) vs full-read**
   - RAG wins for: *one persistent library across all 6 courses*, "where did X say Y", building quotes bank, and free per-question querying all semester. Embedding a whole course library is ≈ $0.001–0.01/book.
   - Full-read wins for: producing *the exam brief* — the brief needs the global skeleton (which lectures cover which eras, how chapters argue against each other), and RAG retrieves fragments, not structure.
   - ✅ Practical consensus (practitioner literature; ⚠️ no single authoritative benchmark exists): **hybrid** — full-read once per book to make the brief (cents), plus a RAG layer over briefs + chunk notes for drilling and exam-week Q&A.

### 1.5 What works in practice for HUMANITIES texts (not code)
- ✅/⚠️ Practitioner consensus (Google/Anthropic long-context guides + community reports):
  1. **Give the model the reading goal up front** ("this is for a Bulgarian university written exam on Политология; produce theses, names, dates, likely questions") — task-directed summarization beats "summarize this book".
  2. **Demand page/section citations for every quote**, then verify quotes by string-searching the extracted text programmatically. Humanities exams punish paraphrased "quotes" that don't exist.
  3. **Bulgarian-language output works well** on Gemini 2.5/3.x and Claude — all are strong multilingual models; terminology should be asked for in both BG and English (BG exam + BG sources + EN textbooks).
  4. **Scanned Cyrillic books**: if OCR quality < ~90%, summarization quality degrades silently (the model "smooths over" garbage). Detect text layer first; OCR-routed pipeline per Q4.
  5. Slides (.pptx) digest differently than books — they are already summaries; feed them as the *skeleton* and use the book to fill meat underneath each slide topic.

**Bottom line cost estimate per book: $0.05–$0.30** with verified 2026 prices. A whole semester (6 courses × ~4 books + slides) ≈ **$2–10 total**. Cost is a non-issue; engineering time is the real cost.

---

## Q2. Simplifier output design — the "I read it all" brief

### 2.1 What the brief must contain (research-grounded design)
Grounded in: (a) testing-effect literature (see Q3) — a brief should *pre-build* retrieval cues, not just compress; (b) the BG exam formats (2.2); (c) what IR/history exams actually ask (definitions, chronology, compare/contrast, critique).

Recommended brief structure (per course unit / book):
1. **Essence page** — max 150 words: what the material claims overall, in exam-answer language. If George reads only this, he can survive small-talk about the topic.
2. **Key theses (10–15)** — numbered, one sentence each + "why it matters" clause. These are the answers to устен изпит ticket questions in embryo.
3. **Names / dates / terms table** — the raw material for flashcards (feeds Q3 directly):
   - Person → 1-line who + school + 1 work
   - Date → event (for История on МОО and Политическа история)
   - Term → definition in BG (+ EN synonym), tagged by theory (realism/liberalism/constructivism where applicable)
4. **Likely exam questions (8–12)** — written in Bulgarian, mapped to the material section that answers them, each with a 3–5 bullet model-answer outline. Generated from two angles: (i) "what would a lecturer test from this", (ii) classic IR/history question archetypes (define X, compare X and Y, trace the evolution of X, explain the role of X in Y).
5. **Quotes worth citing (3–7)** — exact, with page numbers, verified by string-match (see Q1.5). One good quote per essay makes an есе look read.
6. **Counterarguments / critiques** — 2–4 per theme. This is what turns a "тест pass" answer into an "есе 6.00" answer; BG humanities lecturers explicitly reward критика.
7. **Timeline + actors matrix** (for the two history courses) — chronological spine on one screen; who/what/when/why-they-matter grid.

### 2.2 How BG university exams are typically structured
- ⚠️ General knowledge on Bulgarian higher education (consistent across BG universities; could not be verified against a single official SWU document in this session):
  - **Устен изпит (oral)** — the classic "билети" system: student draws a ticket with 2–3 questions, has ~20 min prep, answers orally. Implication for the brief: theses must be pre-formatted as *speakable answers*, not paragraphs.
  - **Писмен изпит** — either a **тест** (multiple choice, often 20–40 questions, BG MCQs usually have А/Б/В/(Г) options) or **есе / отворени въпроси** (1–2 essay questions, 1–2 hours). Implication: need both term-drill precision (for тест) and 5-bullet answer skeletons (for есе).
  - **Текущо контролно / защита на курсова работа** — some disciplines pass via coursework defense instead of a session exam; course syllabi (учебни програми) state the form per дисциплина.
  - Grades: 2–6 scale, 3.00 pass. Verification grade: exam-for-grade-improvement procedures exist at SWU (✅ "ИЗПИТ ЗА ПОВИШАВАНЕ НА ОЦЕНКА" is an official SWU procedure page, https://www.swu.bg/bg/studentsbg/trproceduresbg — section headers verified; content not fetched).
- ✅ Verified SWU specifics (see full Q5): exam sessions, admission rules, поправителна сесия.
- ⚠️ Per-course exam format for George's 6 disciplines: **not verifiable without logging into AIS (ais.swu.bg)** — action item for George: pull his учебни планове/програми from AIS and record "форма на оценяване" per course; the Simplifier should then switch output modes (тест-drill vs билет-outlines vs есе-skeletons).

### 2.3 Output formats
- The brief should be **Markdown**, one file per discipline, with a fixed template (the 7 blocks above), because: (a) it diffs/versions in git, (b) Anki decks are generated *from* block 3 and block 4 mechanically, (c) Obsidian (already in George's system) links course notes together.
- Length discipline: the whole brief for one book should fit **2–4 pages**. If it's longer, it's a rewrite of the book, not a brief — enforce in the prompt ("hard limit: 1200 words per book brief").

---

## Q3. Memory & terminology training — what actually works (2026 evidence)

### 3.1 The evidence hierarchy (classic + still-cited literature)
- ⚠️ Canonical citations (stable, widely replicated):
  - **Dunlosky et al. 2013, Psychological Science in the Public Interest** — meta-review of 10 learning techniques: **practice testing** and **distributed (spaced) practice** = *high utility*; interleaving, elaborative interrogation, self-explanation = moderate; **summarization, highlighting, rereading = low utility**. Direct implication: George's current plan (rereading huge materials) is the *worst*-evidence method; the Simplifier must convert notes into *tests*, not prettier notes.
  - **Roediger & Karpicke 2006** — the testing effect: retrieval practice beats restudy for long-term retention.
  - **Method of loci / memory palace** — robust for *ordered* material (chronologies); multiple RCTs show large short-term gains, but maintenance requires the palace rehearsal habit; poor fit for bulk term volume.
  - ⚠️ No 2026-specific new meta-review on terminology learning was found/verifiable in this session; the above hierarchy remains the standard reference (still cited in 2024–2026 literature).

### 3.2 Spaced repetition algorithms: SM-2 → FSRS
- Anki's legacy **SM-2** uses fixed intervals; **FSRS (Free Spaced Repetition Scheduler)** models memory as three states — **Difficulty, Stability, Retrievability** (DSR) — and schedules each card to hit a target **desired retention** (default **90%**; above ~95% workload explodes).
- ✅ Verified (Anki manual, deck options — ankitects/anki-manual src/deck-options.md): FSRS is **built into Anki since 23.10** (AnkiMobile 23.10+); enable it in deck options, click **Optimize** to fit parameters to George's own review history; "Compute minimum recommended retention" helper exists.
- ✅ Latest Anki release: **26.09.2** (GitHub releases API).
- ✅ FSRS core on PyPI: `fsrs` v6.3.2 (py-fsrs, https://github.com/open-spaced-repetition/py-fsrs) — 4 ratings (Again/Hard/Good/Easy), scheduler + optional per-user optimizer. MIT license.
- Effectiveness: ⚠️ per the FSRS project's own benchmark (fsrs4anki wiki "The Benchmark"; Expertium's blog), FSRS achieves the same retention with meaningfully fewer reviews than SM-2 (roughly 10–30% fewer in their published comparisons — project-authored, not independently peer-reviewed).
- **Verdict for the Simplifier: FSRS-in-Anki is the default choice** — free, offline, evidence-aligned, and programmatically loadable (3.4).

### 3.3 Card design for IR/history terminology
- **Cloze deletion** ({{c1::...}}) is the fastest programmatic format and forces active recall of the *exact term* — best for "definition → term" direction ( BG: "доктрината, според която държавите действат на база национален интерес → {{c1::реализъм}}").
- **Basic bidirectional cards** for term ↔ definition (BG + EN) — the reverse direction trains production (needed for устен/есе).
- **Person → school/works**, **date → event** cards for the two history courses; keep one fact per card (minimum information principle, ⚠️ Wozniak's "20 rules" — widely accepted heuristic).
- **Memory palace**: use *only* for the chronology spine (place 15–25 century-events on a familiar route in Blagoevgrad). Programmatic palace generation is awkward and low-ROI for the 300-term volume; ⚠️ evidence supports it for order/sequence recall specifically.

### 3.4 Fastest programmatic path: notes → Anki deck (all three verified)
1. **CSV import** (simplest) — ✅ from the Anki manual (src/importing/text-files.md): plain UTF-8 text, fields separated by comma/semicolon/tab, first line defines fields, supports `#separator`, `#html:true`, `#notetype` file headers; import target deck chosen at import time.
   - Pipeline: LLM extracts term/definition table (Q2 block 3) → Python writes CSV → File→Import in Anki. Zero extra dependencies.
2. **genanki (library, builds .apkg directly)** — ✅ `genanki` 0.13.1 on PyPI. Generates .apkg packages + cloze/basic models in code; note IDs must be stable (hash of term) so re-imports update instead of duplicate. Best for fully-automated deck builds.
3. **AnkiConnect (live API into a running Anki)** — ✅ project moved to https://git.sr.ht/~foosoft/anki-connect (README fetched): JSON-over-HTTP on **localhost:8765**, actions include `addNotes`, `addNote`, deck/note management; optional API key auth. Best for interactive "add this term to my deck" commands from chat.

Recommendation: **genanki for bulk semester decks; CSV as fallback; AnkiConnect for chat-driven one-off adds.** French/English vocab decks (Английски/Френски език) can be generated the same way from course texts.

---

## Q4. Extracting text from hard sources

### 4.1 Decision tree (route by source type)
```
PDF  → has text layer? ── yes → PyMuPDF direct extraction (no OCR)
     │                  └─ no  → scanned → OCR (4.2)
DOCX → python-docx / pandoc → markdown
PPTX → python-pptx (text per slide, keep slide # as anchor) / pandoc
EPUB → ebooklib (or pandoc) → markdown
```
✅ All libraries verified live on PyPI: **PyMuPDF 1.28.2**, **pdfminer.six 20260107**, **python-docx 1.2.0**, **python-pptx 1.0.2**, **ebooklib 0.20**, **pytesseract 0.3.13**.

### 4.2 OCR for scanned Bulgarian-Cyrillic PDFs
- **Tesseract 5 + `bul` language pack** — ✅ `bul.traineddata` confirmed present in both tesseract-ocr/tessdata_fast and (via tessdoc) tessdata_best repos. Usage: `--language bul+eng` (BG texts are full of Latin-script citations, English terms, numbers).
  - ⚠️ Practical expectation (community consensus, not benchmarked here): clean 300-dpi scans of modern typefaces → good accuracy; old/typewriter/lecture-copied pages → poor. Test on George's actual files first. `tessdata_best` = slower but more accurate than `tessdata_fast`.
  - **OCRmyPDF** ✅ (github.com/ocrmypdf/OCRmyPDF): wraps Tesseract, `ocrmypdf -l bul+eng input.pdf output.pdf` produces a searchable PDF + `--sidecar` text dump — ideal two-output format (archive + feed-to-LLM).
- **Cloud OCR:**
  - **Google Document AI** — ✅ Enterprise Document OCR: **$1.50/page** (1k–5M pages tier), **first 1,000 pages/month free**. Excellent layout/handwriting handling; Cyrillic supported. A 500-page scanned book ≈ **$0.60–0.75** (after free tier).
  - **Azure Document Intelligence (Read)** — ⚠️ standard published price is $1.50 per 1,000 pages ($0.0015/page), i.e. ~100× cheaper than Document AI for bulk; the pricing page is JS-rendered and I could not re-verify the number live this session — confirm before relying on it.
  - **Mathpix OCR API** — ✅ from **$0.002/image** (mathpix.com/pricing); best-in-class for formulas/tables; ⚠️ Bulgarian-Cyrillic support level not verified — use only if courses hit math/tables.
- **Gemini-as-OCR** — ✅ (document-processing docs): send scanned pages as PDF/images; ~258 tokens/page (≈ $0.0004/page on 2.5 Flash at the free/cheap end). For humanities scans this is often *better* than Tesseract because the model reads context (e.g., old spelling) — but it's non-deterministic, so for archival fidelity keep a Tesseract/OCRmyPDF copy too.

### 4.3 Practical pipeline for BG academic sources
1. Probe PDF for text layer (PyMuPDF `page.get_text()` on 5 random pages; if <50 chars/page → scanned).
2. Digital → extract with PyMuPDF (fast, preserves reading order decently) or pdfminer.six for strict layout; slides→python-pptx with slide numbers retained (lecturers' slide titles are the natural chapter structure for the brief).
3. Scanned → OCRmyPDF `-l bul+eng --sidecar`; if quality suspicious → cross-check a sample against Gemini's reading.
4. Everything normalized to Markdown with source anchors (`[p. 137]`) — these anchors are what make Q1.5 quote-verification and exam citations possible.

---

## Q5. Exam-period logistics at SWU "Neofit Rilski" (Blagoevgrad)

### 5.1 Official academic calendar 2026/2027 — ✅ VERIFIED
Source: https://www.swu.bg/bg/studentsbg/accalendarbg/78-studentscat/2348-2026-2027 ("КАЛЕНДАРЕН ГРАФИК за учебната 2026/2027 г.", page last updated 02.06.2026). Full regular-education schedule:

| Event | Dates | Length |
|---|---|---|
| **Зимен семестър — учебни занятия** | **17.09.2026 – 08.01.2027** | 15 weeks |
| Ваканция (зимна) | 24.12.2026 – 03.01.2027 | 2 weeks |
| **Изпитна сесия (зимна)** | **11.01.2027 – 29.01.2027** | 3 weeks |
| **Поправителна сесия (зимна)** | **01.02.2027 – 05.02.2027** | 1 week |
| Летен семестър — учебни занятия | 08.02.2027 – 21.05.2027 | 15 weeks |
| Изпитна сесия (летна) | 25.05.2027 – 08.06.2027 | 3 weeks |
| Поправителна сесия (летна) | 09.06.2027 – 16.06.2027 | 1 week |
| Извънредна ликвидационна сесия (IV курс) | 17.06.2027 – 23.06.2027 | 1 week |
| Годишна ликвидационна сесия | 23.08.2027 – 27.08.2027 | 1 week |
| Държавни изпити: предварителна / редовна / поправителна | 28.06–09.07 / 30.08–10.09.2027 / 24.01–04.02.2028 | — |

Official notes from the same page (✅): national holidays are non-teaching days even inside sessions; additional поправителна sessions can be approved by the rector; faculty-level exam schedules (графици по факултети) are drawn up within this frame.

### 5.2 Admission to the exam session — ✅ VERIFIED
Source: https://www.swu.bg/bg/studentsbg/trproceduresbg/79-lproctbgc/79-sessionbgart (page updated 12.10.2021):
- Admission is certified by **stamp + signature in the студентска книжка** by the "Студентско състояние" inspector, **only if**:
  1. All course obligations for the semester are fulfilled (seminars/papers per учебна програма), and
  2. The semester is **"заверен"** (certified) per the Faculty Council decision — info at the faculty office.
- Students who haven't fulfilled a discipline's obligations may, with unit-head permission, defer that course by one academic year.
- **Implication for George:** skipping lectures is survivable; skipping *seminar deliverables* is what blocks exam admission. The Simplifier's output doesn't replace those deliverables — keep them in the daily system.

### 5.3 Where materials live (what could and couldn't be verified)
- ✅ **AIS — Академична информационна система**: https://ais.swu.bg (linked from swu.bg as the academic info system). ⚠️ Content not inspectable from this session (sandbox DNS did not resolve subdomains) — syllabi, grades and exam announcements are expected there; George should log in once and confirm.
- ✅ University e-resources: e-catalog at **library.swu.bg/absw/abs.htm**, "Електронни бази" and "Електронни списания" under https://www.swu.bg/bg/elresourcesbg; SWU email is on **Microsoft 365** (Office 365/SharePoint tenant confirmed from the site's login links) — some faculties share materials via SharePoint/Teams.
- ✅ Faculty mapping (verified from faculty pages on swu.bg): **Философски факултет** runs **Политология** (and Философия, Социология, Психология); **Филологически факултет** runs the language programs (Английски, Френски etc.). ⚠️ История на МОО / Политическа история на Европа и САЩ most likely sit at the **Правно-исторически факултет** — not verified, check the faculty page.
- ⚠️ **Moodle:** no public Moodle/LMS instance of SWU was found (searches of swu.bg returned none; subdomain probes failed due to sandbox DNS). Whether individual lecturers use Moodle or just SharePoint/AIS announcements is **unverified** — confirm in person.
- ⚠️ Per-course exam formats and списъци на изпитите: published per faculty shortly before the session — the verified mechanism is "графици по факултети … се представят при заместник-ректора по образователните дейности" (from the calendar notes). Watch the faculty pages + AIS in the first week of January 2027.

### 5.4 Strategic timing for the Simplifier (from the verified calendar)
- Regular lectures end **08.01.2027**; exam window opens **11.01.2027** → George's real crunch is **3 weeks in January**. Best Simplifier cadence: brief + deck generated per course **within the last 2 weeks of December** (before the 24.12–03.01 break), then pure FSRS review during the session.
- **Поправителна сесия is only 1 week (01–05.02)** — there is no long recovery window; any course failed in January must be re-drilled immediately, which is exactly what an existing Anki deck solves (re-optimize, review at 0.95 desired retention for those cards).

---

## Sources (fetched live this session unless marked ⚠️)
**SWU / logistics**
- SWU academic calendar 2026/2027: https://www.swu.bg/bg/studentsbg/accalendarbg/78-studentscat/2348-2026-2027
- SWU exam-session admission: https://www.swu.bg/bg/studentsbg/trproceduresbg/79-lproctbgc/79-sessionbgart
- SWU procedures hub / students pages: https://www.swu.bg/bg/studentsbg/trproceduresbg, https://www.swu.bg/bg/elresourcesbg
- SWU faculties: https://www.swu.bg/bg/facultiesbg/fphilosbg, https://www.swu.bg/bg/facultiesbg/fphilbg
- AIS: https://ais.swu.bg (listed; not inspectable from sandbox)

**Models & long context**
- Gemini API pricing: https://ai.google.dev/pricing
- Gemini PDF/document processing: https://ai.google.dev/gemini-api/docs/document-processing
- Claude models overview: https://docs.claude.com/en/docs/about-claude/models/overview
- Claude pricing: https://docs.claude.com/en/docs/about-claude/pricing
- OpenAI pricing (GPT-5.6 family): https://platform.openai.com/docs/pricing
- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts", arXiv:2307.03172: https://arxiv.org/abs/2307.03172

**Memory & SRS**
- Anki manual, deck options (FSRS section): https://raw.githubusercontent.com/ankitects/anki-manual/main/src/deck-options.md
- Anki manual, text-file import: https://raw.githubusercontent.com/ankitects/anki-manual/main/src/importing/text-files.md (plus importing/packaged-decks.md for .apkg)
- Anki releases: https://github.com/ankitects/anki/releases (26.09.2)
- py-fsrs: https://github.com/open-spaced-repetition/py-fsrs (fsrs 6.3.2 on PyPI)
- FSRS4Anki wiki: https://github.com/open-spaced-repetition/fsrs4anki/wiki (Benchmark/ABC pages JS-loaded; referenced via wiki index)
- AnkiConnect: https://git.sr.ht/~foosoft/anki-connect (README)
- genanki: https://pypi.org/project/genanki/ (0.13.1)
- ⚠️ Dunlosky et al. 2013, *Psychological Science in the Public Interest* 14(1):4–58 (canonical, not re-fetched)
- ⚠️ Roediger & Karpicke 2006, *Psychological Science* 17(3):249–255 (canonical, not re-fetched)

**OCR & extraction**
- Tesseract language data: https://github.com/tesseract-ocr/tessdata_fast (bul.traineddata ✅), tessdoc: https://github.com/tesseract-ocr/tessdoc
- OCRmyPDF: https://github.com/ocrmypdf/OCRmyPDF
- Google Document AI pricing: https://cloud.google.com/document-ai/pricing
- Azure Document Intelligence pricing: https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/ (JS-rendered; ⚠️ $1.50/1k pages not re-verified)
- Mathpix pricing: https://mathpix.com/pricing
- PyPI (versions verified): pymupdf 1.28.2, pdfminer.six 20260107, python-docx 1.2.0, python-pptx 1.0.2, ebooklib 0.20, pytesseract 0.3.13

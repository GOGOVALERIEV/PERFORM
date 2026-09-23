# Agent 2 progress trail — Simplifier, Study Methods & Memory

- [t0] Boot. Network OK (curl 301 on swu.bg). Model: z-ai/glm-5.3-flash. No web-search tool — using curl fetches.
- [t1] Q5 first: SWU academic calendar 2026/2027 — fetching swu.bg (академичен календар page).
- [t2] FOUND official calendar: /bg/studentsbg/accalendarbg/78-studentscat/2348-2026-2027 (updated 02.06.2026). Зимен семестър: занятия 17.09.2026–08.01.2027, ваканция 24.12–03.01, изпитна сесия 11.01–29.01.2027, поправителна 01.02–05.02.2027. Full table captured for report.
- [t3] Checking Moodle/e-learning platforms (moodle.swu.bg, e-learning.swu.bg, eel.swu.bg) — DNS fails in sandbox; AIS at ais.swu.bg listed on swu.bg (can't verify content). SWU uses MS Office 365.
- [t4] Q1 model/pricing data captured from official pages: Gemini pricing (ai.google.dev/pricing — Gemini 3.1 Pro $2/$12, 2.5 Pro $1.25/$10, Flash tiers cheap; 1M ctx), Claude (docs.claude.com — Fable 5.1 $10/$50 1M ctx, Opus 5 $5/$25, Sonnet 5 $2/$10 1M ctx), OpenAI GPT-5.6 family (sol $4/$20, terra $2/$12, luna $0.20/$1.20).
- [t5] Next: context-window docs (Gemini), then FSRS/Anki, Tesseract BG, OCR cloud services.
- [t6] Q3 verified: Anki latest 26.09.2 (GitHub releases); FSRS built-in since 23.10, desired retention 90% (anki-manual deck-options.md); py-fsrs 6.3.2 on PyPI; Anki CSV import rules (text-files.md); AnkiConnect JSON HTTP API (sr.ht README); genanki 0.13.1.
- [t7] Q4 verified: bul.traineddata in tessdata_fast/best; OCRmyPDF; Google Document AI Enterprise OCR $1.50/page (first 1000 pages free); Mathpix OCR API from $0.002/image; Gemini File API PDF: 50MB/1000 pages, 258 tok/page, native-text tokens free. python-docx 1.2.0, python-pptx 1.0.2, pymupdf 1.28.2, ebooklib 0.20, pdfminer.six 20260107, pytesseract 0.3.13. arXiv 2307.03172 (Lost in the Middle) confirmed.
- [t8] Q5 verified: SWU exam-session admission rules (trproceduresbg/79-sessionbgart); Философски ф-т = Политология; Филологически ф-т = languages. Writing final report now.
- [t9] Final report written to agent2-simplifier-study.md (all 5 questions + Sources, verified/unverified marked).
DONE

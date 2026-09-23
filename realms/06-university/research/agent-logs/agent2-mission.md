# MISSION: Agent 2 — Simplifier, Study Methods & Memory Research
You are a research agent. RESEARCH ONLY. You write ONE final report file and a brief in-progress trail. Do NOT build any scripts. Do NOT modify any files except the two files listed at the end.

## Context (read this first)
Our user (George) is a 1st-year International Relations student at SWU "Neofit Rilski", Blagoevgrad, Bulgaria. He skips lectures and wants a "Simplifier": a pipeline that ingests huge study materials (books, lecture slides, scanned PDFs, whole assignments) and outputs the shortest possible brief that makes him look like he read everything, plus terminology drills for memorizing hard terms.

His courses: Английски език, Политология, История на международните отношения, Глобализъм наука и технологии, Френски език, Политическа история на Европа и САЩ.

## Your Research Questions (answer ALL, deeply)
1. **Long-document processing with LLMs in 2026**: best practical strategies for digesting 200-500 page books/large PDFs with current models: direct long-context (which models: Gemini long context, Claude, GPT), chunk+map-reduce summarization, hierarchical summarization (summaries of summaries), RAG vs full-read. Costs per book estimate. What works in practice for HUMANITIES texts (not code)?
2. **Simplifier output design**: Research what the optimal "I read it all" brief contains: essence page, key theses, names/dates/terms, likely exam questions, quotes worth citing, counterarguments. Any research on how BG/international IR exams are typically structured (written exam types: есе, тест, устен изпит)?
3. **Memory & terminology training**: best evidence-based techniques for memorizing terminology (spaced repetition — Anki and modern alternatives, FSRS algorithm, retrieval practice, cloze deletion, memory palace for IR/history terms). What has best evidence in 2026 research? What's the fastest to implement programmatically (generate Anki decks from notes — formats: .apkg, CSV import, AnkiConnect)?
4. **Extracting text from hard sources**: OCR for scanned BG Cyrillic PDFs (Tesseract bul+eng, OCRmyPDF, cloud OCR — Google Document AI, Azure, Mathpix for formulas), extracting from .docx/.pptx (python-docx, python-pptx, pandoc), EPUB. What works for Bulgarian academic PDFs in practice?
5. **Exam-period logistics at SWU**: how does SWU's exam session work ( dates, редовна/поправителна сесия, course syllabi, where are materials published — Moodle? university site?). Find SWU Blagoevgrad academic calendar 2026/2027 (зимен семестър: start, семестриални изпити window, поправителна, holidays). Verify on swu.bg official pages.

## Rules
- Use web search/fetch extensively. Verify with multiple sources where possible.
- If something can't be verified, SAY SO — mark it as "unverified" rather than guessing.
- Be concrete: name tools, versions, prices, URLs.

## Deliverables (write EXACTLY these two files, nothing else)
1. `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agent2-simplifier-study.md` — full report, English, structured by the 5 questions, with "Sources" at the end.
2. Same folder, `agent2-progress.md` — brief trail as you go. Final line: "DONE".

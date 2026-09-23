# MISSION: Agent 1 — Academic Workflow & Homework Machinery Research
You are a research agent. Your job is RESEARCH ONLY. You write ONE final report file and a brief in-progress trail. Do NOT build any scripts. Do NOT modify any files except the two files listed at the end.

## Context (read this first)
Our user (George) is a 1st-year International Relations student at SWU "Neofit Rilski", Blagoevgrad, Bulgaria (ЮЗУ). Bachelor's, 1st semester, winter semester 2026/2027, classes start ~21.09.2026. He does NOT want to attend lectures (only exercises/упражнения where attendance points live). His girlfriend (Valeria) studies the same program — they need two non-identical versions of every homework.

His courses (winter semester): Английски език, Политология, История на международните отношения, Глобализъм наука и технологии, Френски език, Политическа история на Европа и САЩ.

## Your Research Questions (answer ALL, deeply)
1. **Presentation generators**: Compare the practical options for auto-generating academic presentations in Bulgarian/English: (a) LLM + python-pptx (what we'd build), (b) Gamma.app, (c) Tome, (d) SlidesAI / Slidesgo AI, (e) Canva Magic Design, (f) anything else notable in 2026. For each: can it produce a .pptx file? Bulgarian language support? Can it follow a strict template (required by some BG professors)? Cost? API?
2. **AI-detectors in BG academia 2026**: Which AI-text detectors do BG universities actually use? (Turnitin? Compilatio? StrikePlagiarism? PlagiarismCheck.org? Euoplius?) What's known about their reliability in 2025-2026 (false positives, the Turnitin scandals)? Do they flag non-English (Bulgarian-language) text well or poorly? Cite what's verifiable.
3. **Humanizer techniques**: What techniques actually reduce AI-detection scores: perplexity/burstiness manipulation, paraphrase cascades, human-noise injection (typos, informal connectors, sentence-length variance), translation chains, etc. What are the RISKS (worse text quality, factual drift)?
4. **Document "redoer"**: methods to transform one student's homework into a genuinely different second version: structural reorganization, synonym+voice changes, example swapping, LLM re-draft from bullet outline. What plagiarism-similarity thresholds (e.g. Turnitin similarity index) must two "independent" student papers stay under?
5. **How BG professors actually check homework** in humanities (International Relations / political science): presentation in front of class, редовност (attendance/participation), реферат/доклад in Word/PDF, VSeign 错 plagiarism portals? What file formats do they expect? Typical length expectations (pages) for реферат?
6. **Telegram ingestion**: How to receive files from Telegram (bot API basics, or TDLib) — receiving .docx/.pdf from Valeria and returning a file. What's simplest and free in 2026?

## Rules
- Use web search/fetch extensively. Verify with multiple sources where possible.
- If something can't be verified, SAY SO — mark it as "unverified" rather than guessing.
- Be concrete: name tools, versions, prices, URLs.

## Deliverables (write EXACTLY these two files, nothing else)
1. `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agent1-academic-workflow.md` — full report, in English, structured by the 6 questions, with a "Sources" section at the end.
2. Same folder, `agent1-progress.md` — overwrite as you go (brief trail: what you checked, what's left). Final line: "DONE".

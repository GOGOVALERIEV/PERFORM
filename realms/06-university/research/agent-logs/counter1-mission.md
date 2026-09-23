# MISSION 1 — Beat the Similarity Engine (КС1/КС2 + SmartMarks)
You are a countermeasure strategist agent. THINK + DESIGN. Output: an actionable playbook, not research summary. You may do brief research (curl; Bing RSS: https://www.bing.com/search?q=Q&format=rss) but the deliverable is OPERATIONS.

## Context
SWU Blagoevgrad uses StrikePlagiarism inside Blackboard. Mechanics: КС1 = % of text with 5+ word matches vs internet/DBs; КС2 = % with 25+ word matches (the killer); SmartMarks = paraphrase detection (synonym-swap resistant, word-order/structure sensitive); home DB = every SWU paper ever; RefBooks 200M+; quotes only "safe" if perfectly formatted (quotation marks + citation + bibliography → purple layer, professor can exclude). No SWU threshold published; Shumen uses КС1>50% AND КС2>5% as "high similarity". Discipline: IR/political science, Bulgarian language, 8-15 page реферати.

## Your problem to solve
An LLM-assisted drafting pipeline (student gives topic → outline → LLM helps draft → final .docx) must produce papers where:
- КС2 ≈ 0% (no 25+ word match with ANY source)
- КС1 low and justified (only properly formatted quotes)
- SmartMarks shows nothing that looks like disguised copying

## Deliver — the playbook
1. **The generation protocol**: exact step-by-step (prompt → outline → draft loop) that structurally avoids sentence-level overlap with sources. Include the actual PROMPT TEXT (Bulgarian + English versions) for: (a) drafting from closed-source memory ("read, close, write from memory, reopen to verify"), (b) anti-КS2 transformations of unavoidable factual sentences (definitions, treaty names, dates — how to phrase around them: restructure, split, embed in own context, transform list→prose).
2. **Definitions & standard-phrase problem**: IR papers need definitions of реализъм, либерализъм etc. — these exist verbatim in thousands of sources. Exact tactics: quote them properly (limit? max 2-3 per paper), or re-derive definitions in own words with citation. Give decision rules.
3. **Quote hygiene spec**: max quotes per 10 pages, max length per quote, formatting rules per BG academic practice (крачки: кавички, ця. фигурни, интерпункция, вътрешна референция + библиография), and how the purple layer benefits the professor's one-click exclusion.
4. **The "long factual sentence" trap**: lists of names/dates (e.g. "Хелсинкският споразумение от 1975 г. бе подписано от 35 държави...") — how to fragment/restructure factual content so it can't match any 25-word stretch while staying accurate.
5. **Do/Don't table**: 10 things that raise КС undetectably-to-the-student (e.g. copying the assignment prompt's own phrasing, using the syllabus text, translating BG Wikipedia sentence-by-sentence) + counters for each.
6. **Self-check protocol**: exact workflow with plag.bg (what to look at: orange paraphrase marks, quote marks, % thresholds; when to stop editing; how to interpret numbers without a published SWU threshold).

Write to `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/counter1-similarity-playbook.md` (English or Bulgarian, clear, concrete, prompt texts included). Then `counter1-progress.md` trail, final line "DONE".

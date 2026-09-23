# MISSION B — The Popular/Simple AI Detectors a Professor Actually Uses + Bulgarian Performance
You are a research agent. RESEARCH ONLY, write ONE report. Use curl (HTML). Google/DuckDuckGo HTML is garbage via curl, but **Bing RSS works: https://www.bing.com/search?q=QUERY&format=rss** — use it for search.

## Context
George is a 1st-year IR student at SWU Blagoevgrad, Bulgaria. His professors may catch AI-written homework either via the university system (StrikePlagiarism — covered by another agent) OR by "something popular or really simple — either an AI or just a website". Your job: identify EXACTLY which simple tools a BG professor would realistically open in a browser in 2026, and how each handles BULGARIAN text. Also: how each can be evaded (perplexity/burstiness/structure), and which ones are dangerous.

## Research Questions
1. **The "professor opens a website" shortlist** — for EACH: Bulgarian support (official claim + tested evidence), free-tier reality, verdict for BG text: GPTZero, ZeroGPT, Copyleaks, Originality.ai, Quillbot AI detector, Scribbr AI detector, Grammarly AI detector, Sapling, Phrasly, Detecting-AI.com, Does-it-exist checks for Turnitin free web version. Which of these explicitly claim Bulgarian/multilingual support in 2026? (Copyleaks claims 30+ languages — verify BG is in the list and find accuracy data; Originality.ai multilingual model 1.0.2+? ZeroGPT "supports all languages"?)
2. **Accuracy on Bulgarian specifically**: any studies/tests 2024-2026 on detector accuracy for Slavic/Bulgarian text (search arXiv, Google Scholar via Bing, "AI detection Bulgarian", "GPTZero Bulgarian", "detector accuracy Slavic languages"). If none — say so explicitly and extrapolate ONLY from multilingual model documentation.
3. **How each tool's detection works** (perplexity/burstiness, classifier, watermarking?) and what specifically lowers scores: sentence-length variance, human-noise, structural edits, BG-specific artifacts (flexion-rich morphology = high perplexity naturally? — check if anyone researched that).
4. **False positive reality**: documented false-positive scandals/withdrawals (Vanderbilt/Turnitin known — find 2025-2026 updates: did other unis disable detectors? Any lawsuits? GPTZero accuracy independent tests).
5. **The BG professor's actual likely behavior**: given StrikePlagiarism is inside SWU's Blackboard, when would a professor ALSO use a free website? (e.g., suspicious text pasted manually). What leaves evidence? What's the risk profile of each path for a BG-language referat vs English-language homework?

## Deliverables
Write `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agentB-simple-detectors.md` — full report, English, VERDICT section at top: "The realistic 'simple tool' threat list for BG text, ranked, with what beats each". Then `agentB-progress.md` trail, final line "DONE".

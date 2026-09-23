# Agent E — MISSION 2 Progress Trail

**Mission:** GitHub open-source anti-AI-detection weapons for Bulgarian academic texts.
**Deliverable:** `agentE-github-weapons.md` — written. This file is the audit trail.

## Trail

1. **Setup** — Confirmed Python 3.12 + urllib; read mission file; cross-checked sibling agents (A/B/C verdicts) for the threat model: GPTZero claims BG (no published BG accuracy), JustDone 95–98% (mission context), Originality.ai self-reports bg 98.42% (vendor benchmark), StrikePlagiarism AI module = 97% vendor marketing (agentC), free tools = professor's first stop (agentB).
2. **GitHub Search API** — Wrote `scripts/agentE_github_search.py`. 11 queries specified in mission: 10 succeeded (humanizer, ai-humanizer, undetectable ai, bypass-ai-detector, anti-ai-detector, paraphrase evade, perplexity burstiness, gptzero bypass, turnitin bypass, ai-text-rewriter); 1 (ai text humanizer) hit 403 rate limit. Raw: `research/test-runs/agentE_github_search.json`.
3. **README fetches** — `scripts/agentE_fetch_readmes.py` via raw.githubusercontent (no API quota): 15/16 repos fetched OK (incl. blader/humanizer, academic-humanizer, lynote humanize-text, korcarc, humanizer-ru, AIGC-Detector-Rewriter, BypassAIGC, DIPPER repo, TempParaphraser, sepia, im-not-ai, HumanAI, humanizalo, humanizer-skill, qu-ai-wei). Also pulled 2 full SKILL.md files + lynote config + humanizer-ru SOURCES.md (verified-evidence table, gold mine).
4. **HuggingFace API** — Wrote `scripts/agentE_hf_search.py`. 10 searches + 4 model cards fetched. Key: "paraphrase-*" top models are EMBEDDINGS (debunked); real humanize LLMs mostly EN GGUF; BG models exist (SambaLingo-BG, mGPT) but no BG humanizer; local detectors found for the feedback loop; DIPPER + TempParaphraser models confirmed (EN, heavy).
5. **Academic papers** — Fetched DIPPER abstract live from arXiv abs page (DetectGPT 70.3%→4.6% @1%FPR; evades GPTZero/OpenAI/watermark; retrieval is the robust defense). arXiv search API + Bing RSS throttled/polluted in-session (406s, junk results) — worked around via official repos + humanizer-ru's verified citation table (arXiv IDs: 2506.07001 TPR −87.88%, 2501.03437 DAMAGE, 2601.08564 MASH 92% ASR, 2604.03136 StoryScope LAMP 95.5→93.9, 2509.24930 perplexity gap 29.5 vs 15.2, 2509.18880 DivEye 39.4%, 2510.02319 PIFE 82.6%, 2508.09622 AINL-Eval best 86.35%, 2603.23146 domain shift).
6. **Synthesis** — Wrote `agentE-github-weapons.md`: VERDICT (top 3 testable-today: translation-chain on OpenRouter / BG pattern-catalog skill / detector-informed minimal-edit loop), ranked repo inventory (20 repos), papers-with-code section, HF landscape, quantified mechanisms table, implementation notes with cost + A/B protocol.

## Key decisions
- Ranked OUT: DIPPER/TempParaphraser binaries (EN + GPU + research-only license), BypassAIGC (Chinese GUI), Unicode-spacing tricks, undetectable.ai wrappers.
- No Bulgarian humanizer exists → recommendation is pipeline + BG pattern catalog + closed measuring loop, all on existing OpenRouter tier (~$0.01–0.10/paper).

## Files produced
- `research/agent-logs/agentE-github-weapons.md` (report)
- `scripts/agentE_github_search.py`, `scripts/agentE_fetch_readmes.py`, `scripts/agentE_hf_search.py`, `scripts/agentE_arxiv_search*.py`
- `research/test-runs/agentE_github_search.json`, `agentE_hf_models.json`, `readmes/*.md` (16), `raw/*` (SKILL files, config, SOURCES.md)

DONE
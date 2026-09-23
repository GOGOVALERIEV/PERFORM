# MISSION 2 — GitHub: open-source anti-AI-detection weapons
You are a research agent. RESEARCH + WRITE one report. Use the GitHub API (no auth needed, 60 req/hr): https://api.github.com/search/repositories?q=QUERY&sort=stars&order=desc via urllib. Also HuggingFace: https://huggingface.co/api/models?search=QUERY. Web fetches for READMEs.

## Context
We generate Bulgarian academic texts. Strict detectors (JustDone 95-98%, GPTZero 97%) catch them. We need open-source tools/models that rewrite or generate text to reduce AI-detection scores. We have OpenRouter access to ~445 models (cheap paid tier OK, ~$0.01-0.10/paper).

## Research questions
1. **GitHub search** for: humanizer, ai-humanizer, undetectable, bypass-ai-detector, anti-ai-detector, paraphrase-evade, perplexity-burstiness, gptzero-bypass, turnitin-bypass, ai-text-rewriter. For top repos (sorted by stars, updated 2025-2026): name, stars, last update, what it does, does it support non-English, does it actually work (evidence), license.
2. **Academic papers with code**: papers on AI-text evasion with public implementations (paraphrase attacks, DIPPER, recursive paraphrasing). Which have usable code?
3. **HuggingFace models**: paraphrase/humanize models that run locally or via API (free inference), quality for Bulgarian/Cyrillic?
4. **Technique papers**: what MECHANISMS demonstrably reduce detector scores (perplexity manipulation, burstiness injection, word-order scrambling, translation chains)? Quantified results?
5. **Verdict**: top 3 GitHub approaches testable TODAY with our OpenRouter access on Bulgarian text, with concrete implementation notes.

## Deliverable
Write `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agentE-github-weapons.md` — ranked list + verdict. Then `agentE-progress.md` trail, final line "DONE".

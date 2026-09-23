# MISSION 3 — The hot new fast/cheap AI model (identify it) + what it can do
You are a research agent. RESEARCH + WRITE one report. Use: OpenRouter models API (https://openrouter.ai/api/v1/models — live, no auth), direct URL fetches, Wikipedia API. Search engines unreliable; try Bing RSS https://www.bing.com/search?q=Q&format=rss.

## Context
George heard about "a new AI that is 200x faster and ~200x cheaper" that is POPULAR right now (late 2026). He doesn't know the name. We need to identify it and test whether it's usable for generating Bulgarian academic text that scores LOWER on AI detectors.

## Research questions
1. **Identify the model**: what AI model/service made "200x faster / 200x cheaper" claims recently (2025-2026)? Candidates to check: Cerebras Inference (fast tokens/sec), DeepSeek V3.2-Exp (cheap API), Kimi K2/K2.5, MiniMax M2, Qwen3-Next, GLM-5 Air, Ling-1T/Ling-3.0, SambaNova, Groq, NexusFlow... Find which one matches "200x" hype and is popular NOW.
2. **Is it on OpenRouter?** Check https://openrouter.ai/api/v1/models for it (exact id + pricing). If yes: exact model id, price per M tokens, context.
3. **Can we use it via our existing OpenRouter key?** (We have a key with ~$39 balance.)
4. **Writing quality**: any evidence it writes natural/varied Bulgarian (or at least non-English) text? Any detector tests for it?
5. **Verdict**: is it testable TODAY through OpenRouter, at what cost per ~500-word paper (~7K tokens in+out), and is it worth adding to our benchmark?

## Deliverable
Write `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agentF-new-model.md` — the identified model + verdict. Then `agentF-progress.md` trail, final line "DONE".

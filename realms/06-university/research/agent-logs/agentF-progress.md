# agentF — progress trail (Mission 3: identify the hot fast/cheap AI model)

## 2026-09-21 session

1. Read agentF-mission.md. Scoped: identify "200x faster/~200x cheaper" model → OpenRouter status → key check → Bulgarian writing test → verdict report.
2. Pulled live OpenRouter models API (446 models → `tmp_or.json`). No Cerebras/Groq/SambaNova presence. Priced the cheap-fast class: Ling-3.0-flash ($0.021/$0.063 per M), DeepSeek V4 Flash ($0.04/$0.16), Qwen3.7-flash ($0.03/$0.13), GLM-5.3-FlashX ($0.37/$1.25), Kimi K3 ($1.7/$8.5), GPT-5.6 Sol ($2.0/$10.0).
3. Bing RSS proved useless (returned beds/Lidl stores regardless of query — as the mission warned). Wikipedia API + HN Algolia (stories AND comments) worked.
4. Identity found: HN item 49289844 — "Accelerating GPT-5.6 Sol Ultrafast" (Cerebras × OpenAI, Aug 13 2026, 713 pts). Fetched the full cerebras.ai blog: 750 out tok/s, 11x faster than Fable 5, HLE 2500 Qs in 11h11m. The exact "200x faster/cheaper" phrasing appears in the top comment thread (silicon POC, 14,000 tok/s, "etching 27B models", "subagents 200x faster/cheaper") — that's the meme George heard.
5. Checked Wikipedia: Kimi K3 = 2.8T largest open-weights (Jul 2026) — big, not the cheap one. Ling-3.0-flash card on HF: 124B/5.1B-active hybrid MoE.
6. Key verified against OpenRouter /auth/key (pay-as-you-go, $74.81 lifetime; HANDOVER: ~$39-44 remaining).
7. Live Bulgarian test (`agentF-live-test.py`, benchmark's exact system prompt, 2 topics): Ling-3.0-flash 310–346 tok/s @ ~$0.0001–0.0003/draft (natural BG prose, sample quoted in report); DeepSeek V4 Flash 84–104 tok/s; Qwen3.7-flash 67–80 tok/s; GLM-5.3-FlashX 429 rate-limited (retry later). Results → `agentF-live-results.json`.
8. Cross-checked scoreboard: batch2 already runs ling-3.0-flash + deepseek-v4-flash-0731 + qwen3.7-flash at $0.0006–0.0015/paper.
9. Wrote deliverable `agentF-new-model.md` (identity + OpenRouter status + live cost/quality + verdict).

## Findings summary
- The 200x hype = Cerebras CS-4 silicon powering OpenAI "GPT-5.6 Sol Ultrafast" (not on OpenRouter; OpenAI-API invite-gated, no public price).
- Its testable cheap-fast cousins ARE on OpenRouter; Ling-3.0-flash is cheapest/fastest (346 tok/s, ~$0.0006 per 500-word paper, natural Bulgarian).
- Verdict: don't chase Cerebras tier; add gpt-5.6-sol as one-shot frontier control (~$1.40/batch); retry GLM-5.3-FlashX after rate limit.

## Artifacts
- agentF-new-model.md (deliverable)
- agentF-live-test.py + agentF-live-results.json (live evidence)
- tmp_or.json (OpenRouter snapshot, 446 models)

DONE
# agentF — Mission 3: The hot new fast/cheap AI model (identified) + verdict

**Date:** 2026-09-21 · **Agent:** F (research) · **Status:** DONE
**Method:** OpenRouter models API (live, 446 models), direct fetches (cerebras.ai blog, HuggingFace model card), Wikipedia API (Kimi (AI)), Hacker News Algolia search (stories + comments), live API tests with our own key.

---

## 1. IDENTITY — what George heard about

**The "200x faster / ~200x cheaper" thing is the silicon-inference wave — and the name attached to it right now is Cerebras + OpenAI's GPT-5.6 Sol "Ultrafast".**

The single hottest story of late August/early September 2026 is:

> **"Accelerating GPT-5.6 Sol Ultrafast"** — Cerebras × OpenAI joint announcement (2026-08-13), ~713 HN points, cross-posted to openai.com ("Previewing Ultrafast").
> Source: https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai

**Official claims (fetched from the blog):**
- New API service tier "Ultrafast Mode" in the OpenAI API, powered by Cerebras CS-4 wafer-scale chips ("dinner plate chips" per HN).
- **Up to 750 output tokens/second** on GPT-5.6 Sol with no quality compromise.
- **11x faster than Fable 5** (Anthropic), **5x faster than Opus 4.8 on Fast mode** (Artificial Analysis-verified speeds).
- Humanity's Last Exam: 2,500 PhD-level questions in **11h11m** (clone Fable 5 took 78h27m) — ~7x end-to-end.
- GDP-Val (economically valuable knowledge work): 5.6x end-to-end speedup, no quality loss.

**Where the "200x" number comes from:** it is not Cerebras' own marketing (their official numbers are 5–11x). The "200x faster / 200x cheaper" language is the community math on that story — verbatim in the top comment thread ("subagents **200x faster/cheaper**", "at 14,000 tokens/sec…"), extrapolating from the silicon POC class: a ~27B model etched into an ASIC (Etched Sohu lineage / CS-4-class hardware) at **14,000 tok/s**, i.e. models become so fast and cheap that agent teams become the norm ("teams of Freds"). So George heard the hype correctly — the popular "thing" is the Cerebras/OpenAI Ultrafast service, and the "200x" is the speed/cost meme of the silicon class behind it.

**Candidates checked & ruled in/out:**

| Candidate | Check | Verdict |
|---|---|---|
| **Cerebras (Ultrafast / GPT-5.6 Sol)** | cerebras.ai blog fetched; HN thread | ✅ MATCH — the hype, ~713 pts, exact "200x faster/cheaper" meme in its comments |
| DeepSeek V4 / V4.1 Flash | HN: DeepSeek v4.1 Flash (Sep 10, 2026, 1015 pts) | Hot + cheap ($0.04/M) but no "200x" claim; part of same cheap-fast class |
| Ling-3.0-flash (InclusionAI) | HuggingFace card + OpenRouter | Cheap-fast class champion ($0.021/M, 346 tok/s in our test); no 200x phrasing |
| Kimi K3 (Moonshot) | Wikipedia: "largest open weights model ever, 2.8T" (Jul 2026) | Big, not cheap — $1.7/$8.5 per M on OpenRouter |
| MiniMax M3 / GLM-5.3 / Qwen3-Next | OpenRouter + HN | Mainstream 2026 gen; not the 200x story |
| Groq / SambaNova / NexusFlow | OpenRouter 446-model list | **Zero OpenRouter presence** (like Cerebras) |

---

## 2. Is it on OpenRouter?

**The Ultrafast service itself: NO.** Cerebras has **zero presence** in today's OpenRouter model list (verified: no `cerebras*` id or description match across all 446 models; same for Groq, SambaNova). Ultrafast lives only in the OpenAI API and is invite-gated ("available initially to a select group of customers, access expanding over time") with **no published price** — HN consensus: "if you have to ask…" (i.e. premium, not cheap).

**What IS on OpenRouter:**
- `openai/gpt-5.6-sol` (+ `~openai/gpt-sol-latest`) — the same model, regular speed, **$2.0/M in / $10.0/M out**, 1.05M context. Expensive, and *not* the fast tier.
- The economy-class models the hype is made of (all live, verified IDs):

| Model | in $/M | out $/M | ctx | note |
|---|---|---|---|
| `inclusionai/ling-3.0-flash` | **0.021** | **0.063** | 262K | cheapest real model on OpenRouter; 124B/5.1B-active hybrid MoE |
| `inclusionai/ling-3.0-flash-vl:free` | 0 | 0 | 262K | free tier variant (VL) |
| `deepseek/deepseek-v4-flash-0731` | 0.04 | 0.16 | 1.3M | DeepSeek's cheap flash |
| `qwen/qwen3.7-flash` | 0.03 | 0.13 | 1M | Qwen cheap flash |
| `z-ai/glm-5.3-flashx` | 0.37 | 1.25 | 1M | Z.ai "high-speed variant… up to 200 tokens/s" |
| `moonshotai/kimi-k3` | 1.7 | 8.5 | 1M | frontier open (control) |

> Note: `Ling-3.0-flash` at $0.063/M out vs `gpt-5.6-sol` at $10/M out = **~159x cheaper per output token** — this is the real, measurable "200x cheaper" cousin that we CAN touch.

---

## 3. Can we use it with our existing key?

**Yes — the economy class is testable right now.** Key: `~/.pi/agent/auth.json → openrouter.key` (pay-as-you-go; lifetime usage $74.81; HANDOVER says ~$39–44 remaining — consistent with mission's ~$39). Verified live this session: I generated real Bulgarian drafts through the key with `ling-3.0-flash` (paid) and `ling-3.0-flash-vl:free` (free tier, zero cost).

**The literal Ultrafast/Cerebras tier: no** — not on OpenRouter, no OpenAI API access as a consumer.

---

## 4. Writing quality — live Bulgarian test

I ran the benchmark's exact system prompt (`run_benchmark.py::call_pi` — "Ти си студент…", temperature 0.9) with two realistic referat prompts against 5 models. Results (agentF-live-results.json):

| Model | tok/s | full-draft cost | style stats (sent_avg / SD / TTR / rep4gram) |
|---|---|---|---|
| `ling-3.0-flash` | **310–346** | **$0.0001–0.0003** | 23–28 / 5.8–7.2 / 0.58–0.61 / 0.000–0.003 |
| `ling-3.0-flash-vl:free` | 74–138 | free | 22–23 / 5.9–7.0 / 0.58–0.59 / 0.002–0.006 |
| `deepseek-v4-flash-0731` | 84–104 | $0.0003–0.0013 | 18–26 / 5.7–9.7 / 0.58–0.59 / 0.000–0.004 |
| `qwen3.7-flash` | 67–80 | ~$0.001 | 13–15 / 4.6–4.7 / 0.73–0.78 / 0.000 |
| `glm-5.3-flashx` | — (HTTP 429, rate-limited) | — | retry later |

**Ling-3.0-flash output quality (evidence, tema1 excerpt):**

> "Управленските решения рядко се приемат в условия на пълна сигурност и достъп до всички нужни данни. Повечето организации се изправят пред ситуация, в която информацията е непълна, времето е ограничено… През 1957 година Херберт Саймън поставя основата на нов подход към разбирането на човешкото взимане на решения чрез концепцията за ограничена рационалност…"

Natural Bulgarian academic register: varied sentence openings, idiomatic phrasing ("поставя основата", "изправят пред ситуация"), no template openers, no markdown, facts woven in with original wording. **Fluency is NOT the constraint** — this class writes as well as any model we already benchmark. Caveats: it ignored the 500–600-word budget in one run (5,142 out tokens — needs `max_tokens` cap); note the internal spelling quirks are consistent with our other cheap models' output.

**Local style-gate signal:** our scoreboard already ran `ling-3.0-flash` (pol-izbori-m2) → local gate FAIL(2), `deepseek-v4-flash` → FAIL(2–4) — reproducible Bulgarian, caught by the project's own gates like everything else; external ZeroGPT/GPTZero scores pending (n/a in current scoreboard).

**Detector-Test evidence for the model class:** no public per-model detector studies exist for Ling-3.0 (none found on HN/Web). AgentB's detector research stands: GPTZero explicitly claims Bulgarian support (accuracy data unpublished), ZeroGPT is chaotic, plag.bg is gentle. The flash-class statistical profile in my runs (TTR 0.58–0.78, sentence-length SD 4.6–9.7, ~0 repeated 4-grams) shows **no pathological templating**, but that's a local-stats view — the strict detectors (GPTZero/JustDone 95%+) are the binding benchmark gates, and they need a real scored run (juice/balance permitting), same as for every model.

---

## 5. VERDICT — testable today? Worth adding?

**Not the literal hype product:** Cerebras "Ultrafast" (GPT-5.6 Sol ultrafast tier) is **not testable through OpenRouter** — no model id, no API access, invite + unlisted premium pricing. Do not add to the benchmark.

**The economically real version IS testable today, essentially free:**

| Model | cost per ~500-word paper (6.5K in + 7.5K out) |
|---|---|
| `ling-3.0-flash` | **~$0.0006** (≈ 0.06 cents) |
| `deepseek-v4-flash-0731` | ~$0.0015 |
| `qwen3.7-flash` | ~$0.0012 |
| `glm-5.3-flashx` | ~$0.012 |
| `openai/gpt-5.6-sol` (frontier control) | ~$0.088 |

With ~$39–44 of credit, the full benchmark (16 papers × 2 drafts) runs **hundreds of times for under a dollar** on the flash class. `ling-3.0-flash-vl:free` exists for zero-cost experimentation.

**Recommendation:**
1. **Keep** `ling-3.0-flash` + `deepseek-v4-flash-0731` + `qwen3.7-flash` as the workhorse economy tier (already in batch2 — confirms the class, now with hard numbers: Ling is the fastest and cheapest of the three).
2. **Add** `openai/gpt-5.6-sol` as a one-shot **frontier control** (~$0.09/paper, 16 papers ≈ $1.4) — the genuinely new research question implied by this mission is *whether frontier-class text scores differently* on ZeroGPT/GPTZero than the cheap class. One batch answers it.
3. **Retry** `glm-5.3-flashx` (Z.ai's 200-tok/s flagship) when the 429 rate limit clears — it's the only model making an explicit "200 tokens/s" claim.
4. Do NOT chase the Cerebras tier for detector work — it's a speed product for agents, not a text-generation economy, and it's unreachable from our stack.

**Net:** George's hearsay identified → **Cerebras × OpenAI "GPT-5.6 Sol Ultrafast"** (the 200x meme = silicon-class inference, 14,000 tok/s ASIC POC). Not on OpenRouter; but its cheap-fast cousins are already in our loop, cost pennies-per-thousand-papers, write natural Bulgarian, and the next valuable step is one frontier-control batch with `gpt-5.6-sol`.

---

**Sources (fetched live):**
- https://www.cerebras.ai/blog/accelerating-gpt-5-6-sol-ultrafast-with-openai (full text)
- HN item 49289844 (713 pts) + top comments (incl. "200x faster/cheaper" thread); story 45852751; "Qwen 3.8 27B @ 1500 tok/s on Cerebras" (Sep 3, 2026); "Etched Sohu vs Nvidia" (Aug 23, 2026)
- https://openrouter.ai/api/v1/models (snapshot: `tmp_or.json`, 446 models)
- https://huggingface.co/inclusionAI/Ling-3.0-flash (model card)
- https://en.wikipedia.org/w/api.php rest+parse: Kimi (AI), GLM (AI), MiniMax Group
- Live API runs: `agentF-live-test.py` → `agentF-live-results.json`
- `realms/06-university/state/benchmark/scoreboard.md`, `HANDOVER.md`, `research/agent-logs/agentB-simple-detectors.md`
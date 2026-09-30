# AI Presentation Tools — Research & Verdict (2026-09-29)

Tested live with real accounts/API probes (not marketing pages).

## Verified results

| Tool | API | Free plan (verified) | Verdict |
|---|---|---|---|
| **Gamma** | YES — `public-api.gamma.app/v0.2/generations` (401 "Invalid API key" = live). API = PAID plans only | 400 credits one-time, no card. PPTX/PDF/PNG export on free | WINNER (design quality) |
| **Manus** | YES — REST agent API, docs at manus.im/docs/integrations/manus-api.md | free daily credits (web app) | candidate, not yet tested |
| GenPPT | — | **"NO FREE PLAN"** (own pricing page): €1 trial → €25/mo | rejected |
| Canva | no practical deck-generation API | big free plan | manual use only |

## Gamma hands-on (дво presentation decks, same topic)
- Topic: "Студената война: произход, основни фази и край на биполярния свят"
- Flow: create/generate → outline → customize → full deck in ~90s. BG language supported.
- **Deck 1 (AI images):** text/facts great; AI images = garbled unreadable pseudo-words (known AI-image weakness)
- **Deck 2 (Stock photos):** real photos, zero garbled text → **LOCKED SETTING: Image source = Stock photos**
- Structure/facts correct (1947 Truman, Marshall 13 mld, 1949 NATO, 1955 Warsaw…)
- Account: George's Google via his own Brave profile w/ --remote-debugging-port=9222 (CDP attach works)

## Lessons for Shadow Scholar integration
1. Gamma login requires the USER's own browser session — OAuth from clean automation profiles
   bounces into Google signup + Windows DPAPI key prompt. CDP-attach to George's real Brave works.
2. For customer-facing product: Gamma API is paid → use our own pipeline (free, $0.01/deck) as
   engine; offer Gamma as manual/premium path.
3. Stock photos > AI images for academic decks (no garbled text).
4. Gamma settings persist between generations (language/topic) — fewer clicks to re-run.

## Open
- Manus free-tier deck test (pending George's go)
- Export deck → PPTX and run through JustDone text check (deck text is Gamma-model-written,
  NOT our 20%-AI pipeline — do not confuse the two)

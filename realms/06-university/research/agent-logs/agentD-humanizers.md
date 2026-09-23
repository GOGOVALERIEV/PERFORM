# AGENT D — ANTI-AI / HUMANIZER SERVICES: FULL LANDSCAPE 2025–2026

**Mission:** Map every "humanizer" (AI-text → human-sounding) service for our Bulgarian referat pipeline. Decide: which 3 can we test for FREE today on a 400-word Bulgarian text, and what do we actually believe will happen.
**Date of research:** 2026-09-21. **Method:** direct URL fetches of 30+ vendor sites (+pricing/detector/language pages), official Turnitin/GPTZero/JustDone documentation, one 12-tool independent benchmark (Jul 2026), 6 individual third-party detector-proven reviews (Dec 2025–Jan 2026), Reddit consensus thread (Dec 2025). No click-through tests were possible from this machine (bulk of tools require JS/interactive sessions — flagged as the #1 next step).

---

## ⚡ VERDICT — 3 services testable for FREE TODAY on a 400-word Bulgarian text

| # | Service | Why | How to test 400 BG words for free | Risk flag |
|---|---------|-----|-----------------------------------|-----------|
| 1 | **Humbot** (humbot.ai/humanize-ai) | Free tier ≈ 3,000 words/month, **500-word input cap** → entire 400-word referat fits in **ONE pass**; **Bulgarian is in its official language selector** (verified in page JSON). No payment. | Paste 400 words of BG AI draft → Humanize → scan output with JustDone free check + GPTZero free tier; repeat with "Advanced" mode. | No third-party test exists for BG. If it rewrites well, it's the only tool whose free allowance covers a full referat in 1 shot. |
| 2 | **HIX Bypass** (hixbypass.com/humanize-ai) | **Bulgarian is EXPLICITLY named on the product page** ("50+ languages including … Bulgarian …"). Free to use **without signup** (~80 words/chunk; signup unlocks more). | Split 400 words into 4×~100-word chunks, humanize each, stitch, re-check. Signup adds free words. | Free per-chunk limit is tiny; stitching 200-word texts back together is what independent testers had to do — results degrade on short chunks. |
| 3 | **WriteHuman** (writehuman.ai) | Bulgarian is in its **explicit 40+ language list** (verified in site JSON-LD). Free: **250 words/request, ~3–5 requests/month** → 400 words in 2 requests. Cleanest free UI. | 2 passes of ~200 words (or 1×250 + 1×150). Re-check with JustDone/GPTZero. | Independent Dec-2025 test: **GPTZero flagged WriteHuman's free model 100% AI on all 3 English samples.** BG = unverified, likely worse. |

**Also worth a 4th test slot (0 cost):** **Netus AI Bypasser** (free widget 150 words/pass, Bulgarian in its 36-language selector — official) and **Undetectable.ai** (250-word one-time free trial; strongest independent raw bypass score 79.7% but inflates text +79%).

> **Why these win vs the rest:** every other service either (a) has no Bulgarian in its language list (Grubby = *explicitly English-only*; uPass selector has no BG), (b) blocks free use by IP after ~100–300 words total (Phrasly, BypassGPT), or (c) is a tiny English-first clone (RewriteAI admits "results in other languages may be inaccurate").

---

## THE 3 REALITIES THAT DECIDE EVERYTHING (read first)

1. **No major humanizer even CLAIMS to beat JustDone or StrikePlagiarism.** Every vendor targets GPTZero, Turnitin, Originality.ai, Copyleaks, ZeroGPT, Winston, Sapling, Crossplag, Writer, Content at Scale. We are tested by **JustDone (~98% academic accuracy per its own page)** and, at SWU, **StrikePlagiarism AIPC**. The tools optimize for the wrong targets for us. ⚠️
2. **Turnitin does NOT run AI detection on Bulgarian (official).** Its own FAQ: AI paraphrase/bypasser detection is "only available for English submissions"; non-supported languages are *not processed at all*. Supported: English, Spanish, Japanese, Modern Arabic. Bulgaria is NOT in the list. (Nice — but our real threat is JustDone/StrikePlagiarism, not Turnitin.)
3. **Post-Aug-2025, strict detectors are winning the arms race.** Turnitin's own release notes: **2025-08-27 "Updated AI writing model to detect AI bypasser tools."** Independent 12-tool Jul-2026 benchmark: even the BEST tool averages ~10% residual GPTZero AI-score; most tools sit at 20–90%. Reddit (Dec 2025): "Turnitin and GPTZero started flagging almost everything… August vs December is night and day."

---

## RANKED TABLE — all services found (28)

Legend: **BG-official** = Bulgarian in an official language list (verified in fetched HTML/JSON). **Detectors claimed** = named on vendor site. **Indep. test** = third-party, detector-proven. Free = free tier usable today.

| # | Service | Free tier | Price (paid) | Languages | Detectors claimed | Independent test result | Notes |
|---|---------|-----------|--------------|-----------|-------------------|------------------------|-------|
| 1 | **Humbot** (humbot.ai) | ≈3,000 words/mo; 500 w/input | from ~$8–10/mo (JS-hidden) | **BG ✅** (selector) | GPTZero, Turnitin, Originality, ZeroGPT, Copyleaks | n/a (untested by 3rd parties) | Only major tool whose free allowance fits a 400-w referat in one pass |
| 2 | **HIX AI Bypass** (hixbypass.com) | ~80 w free no-signup; +~120 w signup; 125 w/account | $9.99–14.99/mo (5k words/mo); Unlimited $59.99/mo | **BG ✅ explicit** (50+) | Turnitin, GPTZero, Originality, Copyleaks, ZeroGPT, Crossplag, Sapling, Writer, BrandWell | Aced ZeroGPT; **GPTZero 100% AI, 2/2 samples** (Jan 2026) | Built-in checker ≠ real detectors (50% aligned); quality 4/10; em-dashes + random brackets |
| 3 | **WriteHuman** (writehuman.ai) | 250 w/request ×3–5/mo | $12–48/mo | **BG ✅ explicit** (40+) | GPTZero (claimed) | **GPTZero 100% AI on all 3 samples** (Dec 2025) | Clean UI; typos/grammar breaks in free output |
| 4 | **Netus AI Bypasser** (netus.ai) | ~150 w/input free widget; credits on signup | n/a (credits) | **BG ✅ explicit** (36) | Turnitin, Copyscape, Quetext (plagiarism angle) | n/a | Freeze-words + style-copy features unusual |
| 5 | **Undetectable.ai** | 250 w one-time free trial | $5–21/mo (10–50k words/mo) | 50+ (English best) | GPTZero, Turnitin, Originality… | Best raw bypass of benchmark: 79.7% bench, GPTZero avg 12.3%, Originality 4.9% — but **+79% word inflation** | Free model warns "AI detectors might still flag your text" |
| 6 | **Uncheck AI** | 150 w/mo, 100 w/process | 5k w/mo tier (Basic) | **BG ✅** (30+) | GPTZero, Copyleaks, ZeroGPT, Turnitin, Originality 3.0, Sapling | n/a | Multi-detector score panel |
| 7 | **BypassGPT** (bypassgpt.ai) | 125 w/input (IP-tied) | from $8/mo | **BG ✅** (selector) | GPTZero, Turnitin, Originality, Copyleaks, ZeroGPT, Sapling, Winston | Aced ZeroGPT; **GPTZero 100% AI** (Jan 2026) | "making AI systems being more natural" — broken grammar |
| 8 | **Rephrasy AI** (rephrasy.ai) | free tier (limited) | Growth $8.25/mo (100×2,000w) | 50+ (BG not verified in fetched copy) | Turnitin, GPTZero, Copyleaks, Originality, ZeroGPT | Reddit Dec-2025 **community favorite** (unofficial) | "Less synonym salad, more actual rewriting" per users |
| 9 | **Clever AI Humanizer** (cleverhumanizer.ai) | **free + unlimited, no signup** | Free | 12–16 langs (site); EN-first | GPTZero, ZeroGPT, Originality | **#1 in its own Jul-2026 benchmark: GPTZero avg 9.6%**; Dec-2025 review: 99% human on GPTZero on 1/3 samples | ⚠️ Benchmark run by its own maker — treat scores with salt, but method is published |
| 10 | **Grubby AI** (grubby.ai) | 300 w TOTAL (not per day) | ~$8–20/mo | **ENGLISH ONLY (explicit)** | GPTZero, Originality, ZeroGPT, Turnitin, Winston, Content at Scale, Copyleaks | GPTZero mode: 0% / 17% / 100% across 3 samples (Dec 2025) | Best-in-class manual editing UI; built-in detector tab showed false "Human 100%" |
| 11 | **uPass AI** (upass.ai) | 80 w/input; 300 w/mo bypasser+detector | from $14.99/mo | no BG in selector | Turnitin, GPTZero, Copyleaks, Originality, Winston, Content at Scale | n/a | Academic-oriented; modes Basic/Advanced/Aggressive |
| 12 | **RealTouch AI** | **600 w/day free** (account) | ~$5.83–11.92/mo | n/a (EN-first) | Turnitin, GPTZero, Copyleaks, Winston, Originality, ZeroGPT, Content at Scale, Sapling | 99.9% claim (vendor) | Generous daily free cap |
| 13 | **TwainGPT → now Verva** (verva.com) | 250 w free; 2,000-w input box | $8/20/40/mo | 100+ (BG unverified) | GPTZero, ZeroGPT, Copyleaks, QuillBot, Turnitin, Writer, Grammarly | Aced ZeroGPT (0.2% — best on bench); **GPTZero 62.5% avg; worst grammar of 12 tools** (Jul 2026) | Free promo "unlimited through April–May" has ended |
| 14 | **Phrasly AI** (phrasly.ai) | free tier; ~300 w TOTAL by **IP** | $2/3-day trial; $10.99–20/mo | multilingual (BG unverified) | Turnitin, GPTZero ("compliance" wording) | **100% AI on BOTH GPTZero and ZeroGPT at Aggressive setting** (Dec 2025) | Clean grammar but zero bypass; bloats text +40% |
| 15 | **GPTHumanizer.io** | 125 w | $9.9/mo unlimited | 100+ claim | Turnitin, GPTZero | n/a (own HIX-review blog only) | — |
| 16 | **Humanize AI Pro** (humanizeai.pro) | free core tool | from $4.99/mo | multi (BG unverified) | GPTZero, Turnitin, Copyleaks, … | GPTZero avg 29.6%, −2% word delta (best faithfulness) Jul 2026 | Paid ≈ free in results |
| 17 | **AIHumanize (aihumanize.io)** | ~2,000 w at signup | ~$6/mo; ~$20 unlimited | multi (BG unverified) | GPTZero, Turnitin, Copyleaks… | GPTZero avg 17.3%; +41% inflation (Jul 2026) | cheapest decent unlimited |
| 18 | **Walter Writes AI** | 300-w trial | ~$8/mo annual | multi (BG unverified) | Turnitin, GPTZero… | GPTZero avg 22.5% (Jul 2026) | slowest stable tool |
| 19 | **UnAIMyText** | free no-signup tier | credits | — | Turnitin, GPTZero… | worst text quality on bench; GPTZero 52.7% (Jul 2026) | — |
| 20 | **GPTHuman (gpthuman.ai)** | 300-w trial | ~$9/mo | — | — | GPTZero 89.4%, strict pass 5% (Jul 2026) | best *writing* quality, fails its core job |
| 21 | **StealthWriter** | 10 humanizations/day | $20–400/mo | — | Originality, GPTZero… | GPTZero 79.9%; strict pass 10% (Jul 2026) | fastest (3–4 s/1k words) |
| 22 | **StealthGPT** (stealthgpt.ai) | very limited (reported ~350 w/week) | $1 first week; then ~$12+/mo | "250+ languages" (BG unverified; /languages page 429-blocked) | GPTZero, Originality, ZeroGPT, Winston + | One Reddit claim: "only tool that survived Turnitin's 2025 update" — contested; another: "casual text came back as dissertations" | Heavy marketing ("mastered 5,000 languages") |
| 23 | **QuillBot AI Humanizer** | 125 w/session | $8.33/mo annual | 125+ langs (BG plausible, unverified) | n/a (not built for bypass) | **Worst on bench: 7.1% bypass, GPTZero 93.5%** (Jul 2026) | use as paraphraser only, never as bypasser |
| 24 | **Humanize.ai** (humanize.ai) | **100% free, unlimited, no signup** claim | free | 100+ claim | "passes ALL detectors" + Turnitin incl. | n/a | Free-only tool; own detector powered by external service; suspiciously good to be true — test first |
| 25 | **RewriteAI Humanizer** | 500 w/session free no-signup | freemium | **EN-first (explicit warning)** | GPTZero, Turnitin, Copyleaks, Originality, ZeroGPT | n/a | "Results in other languages may be inaccurate" — vendor's own words |
| 26 | **Conch AI** | ~10,000 tokens (~3,000 w) free | $9.99/mo | **primarily English** | — | ~72% bypass (Mar 2026 test) | writing assistant, not real humanizer |
| 27 | **JustDone AI Humanizer** (justdone.com/ai-humanizer) | freemium | paid | "in any language" claim | — | n/a — **it's the SAME company that runs our strictest detector** | Their own demo: 98% AI → 96% Human with *their* detector. ⚠️ Never feed it the same text you'll test with JustDone |
| 28 | **Originality.ai Humanizer** | free tool | paid | multi | — | n/a | Detector-maker selling the counter-tool — same arms-race circus as #27 |

*Also seen but not scored (tiny/no data):* YoloHumanize, Humanifyer, NeonHumanizer, StealthHumanizer (open-source Vercel), PrePostSEO Humanizer, AISEO (75% bypass, Sept 2025 data), NaturalWrite (500 free words, 83%), HumanizeAIText (200 free words, 80%), Monica AI, NoteGPT, Decopy, Grammarly Humanizer (tested; not a bypasser), Ahrefs Humanizer, Writesonic (200 w/session free).

---

## Q&A — the 6 research questions

### 1. Full list + free tier + limits + price → table above.
**Free tiers big enough for a 400-word text in one request:** Humbot (500 w/input), RealTouch (600 w/day), RewriteAI (500 w/session), Conch (~3,000 w), Humanize.ai (unlimited claim), Clever (unlimited claim), QuillBot (125 w), Netus (150 w). Everything else: 80–300 words **per account/IP/lifetime**.

### 2. Do they support Bulgarian? → THE decisive answer
- **Official claims (verified in fetched pages):** HIX Bypass (explicit: "50+ languages including … Bulgarian"), WriteHuman (explicit in 40+ list), Netus (explicit in 36-language list + `<option value="bg">`), Humbot (BG in language selector JSON), BypassGPT (BG in selector JSON), Uncheck AI (BG in selector JSON). StealthGPT claims "250+ / 5,000 languages" (unverifiable marketing). Verva/TwainGPT "100+". JustDone humanizer "any language".
- **Explicitly NOT:** Grubby ("only humanize AI text in English" — quoted), RewriteAI ("results in other languages may be inaccurate"), uPass (selector has no BG), Conch (primarily English).
- **Third-party tests on Bulgarian/non-English: NONE FOUND.** No YouTube test, no Reddit post, no benchmark covers Bulgarian or any Slavic language. Every independent test in 2025–2026 is English-only. → **BG support is 100% vendor claim, 0% verified. This is our single biggest unknown and must be empirically tested before any money or workflow investment.**

### 3. Which detectors do they claim to beat
GPTZero (almost all), Turnitin (most), Originality.ai (most), Copyleaks (many), ZeroGPT (many), Winston/Sapling/Crossplag/Writer/Content at Scale (several). **JustDone: NONE. StrikePlagiarism: NONE. Quetext/Copyscape: only Netus (plagiarism angle).** See table.

### 4. Independent tests 2025–2026 — do humanized texts actually pass?
- **Benchmark (cleverhumanizer.ai, Jul 2026, 12 tools × 60 passes, real APIs):** GPTZero avg-AI scores — Clever 9.6%, Grubby 10.1%, Undetectable 12.3%, WriteHuman 15.4%, AIHumanize 17.3%, Walter 22.5%, HumanizeAIPro 29.6%, UnAI 52.7%, TwainGPT 62.5%, StealthWriter 79.9%, GPTHuman 89.4%, QuillBot 93.5%. **Even #1 leaves ~10% on the table; 8 of 12 tools are caught >50%.**
- **Individual tests (Dec 2025–Jan 2026, same community):** HIX Bypass, BypassGPT, WriteHuman, Phrasly, Humanizeai.io — **all failed GPTZero at 100% AI** despite acing/claiming ZeroGPT. Grubby: mixed (0/17/100). Undetectable: best of the strict-detector set.
- **Pattern:** tools that crush ZeroGPT (≤0.2%) do it by butchering grammar — ZeroGPT behaves like a *formality meter*, not an authorship detector. It does NOT transfer to GPTZero/Turnitin/JustDone.
- **Reddit (r/studytips, Dec 2025):** after Turnitin's Aug-2025 update "detectors started flagging almost everything"; favorites: Rephrasy (natural rewrites), StealthGPT (fast but tone-shifting); consensus: "most free humanizers just shuffle words, same patterns keep showing up"; "no tool is safe forever."

### 5. Safety: facts/quality + reverse detection
- **Fact/quality loss is real and documented:** Undetectable +79% word inflation (content-match falls to 13.9/20); Phrasly +40%; HIX output contains "plai-nable", random square brackets; BypassGPT outputs broken grammar ("making AI systems being more natural"); TwainGPT had the worst grammar of the whole bench (8.5/20). **A humanized referat CANNOT be submitted unedited — it will read as worse-than-AI.** Numbers/facts do survive mostly (word-level rewrite), but citations/formatting can break (Grubby/Rephrasy offer citation protection for this reason).
- **Turnitin's bypasser detection (official, since 2025-08-27):** "Updated AI writing model to detect AI bypasser tools… attempting to modify AI-generated text." FAQ: ALSO detects "AI-generated text modified by AI paraphraser or bypasser (also called humanizers)". **English/Spanish/Japanese/Arabic only — Bulgarian not processed.** (Their Aug-2026 update merged paraphrase-detection into one AI flag.)
- **GPTZero:** officially "fully supports" EN/DE/PT/FR/ES; BG "used but unverified". It does detect across LLMs incl. watermarked-generation patterns.
- **JustDone (our enemy #1):** advertises detecting text "already run through a paraphraser or grammar tool"; 98% accuracy on academic text, 80% overall, 10.3% published error rate. **Humanizers don't even claim to beat it — because it isn't in their training/evasion targets.**

### 6. Free usable options for a 400-word Bulgarian text RIGHT NOW (exact limits)
| Service | Free words | Input cap | Works for 400 w? | BG |
|---|---|---|---|---|
| Humbot | ≈3,000/mo + 1,000 advanced | 500 w | **Yes, 1 pass** | ✅ |
| RealTouch | 600 w/day | 600 w | Yes, 1 pass | ❓ (EN-first) |
| RewriteAI | 500 w/session | 500 w | Yes, 1 pass | ⚠️ EN-warning |
| Humanize.ai | unlimited (claim) | ? | Maybe | ❓ |
| Clever AI Humanizer | unlimited (claim) | ? | Maybe | ❓ |
| HIX Bypass | ~80–125 w (no-signup); +120 on signup | ~125 w | 3–5 passes | ✅ |
| WriteHuman | 250 w ×3–5/mo | 250 w | 2 passes | ✅ |
| Netus | 150 w/input | 150 w | 3 passes | ✅ |
| Undetectable | 250 w one-time | 250 w | 2 passes | 50+ (EN best) |
| uPass | 300 w/mo | 80 w | ❌ (too small) | ❌ |
| Uncheck AI | 150 w/mo | 100 w | ❌ | ✅ |
| BypassGPT | 125 w/input (IP-tied) | 125 w | ❌ | ✅ |
| Grubby | 300 w lifetime | — | ❌ | ❌ English-only |
| Phrasly | ~300 w lifetime (IP) | — | ❌ | ❓ |
| QuillBot | 125 w/session | 125 w | teases only | ❓ |
| StealthGPT | ~350 w/week (reported) | ? | 2 passes | ❓ |

---

## RECOMMENDED TEST PROTOCOL (next agent run, needs a browser)
1. Take a **fixed 400-word Bulgarian referat paragraph** already known to score high-AI on JustDone.
2. Run it through Humbot (1×500w), HIX Bypass (4×100w, stitched), WriteHuman (2×250w), Netus (3×150w) — all free.
3. Score outputs: **JustDone free check** (RealDetector target #1), **GPTZero free tier**, and — if available — **StrikePlagiarism/plag.bg self-check**.
4. Pass if JustDone ≤ 10% AND GPTZero ≤ 5% with grammar intact (manual read for the nonsense-patterns this report documents).
5. Expectation-setting: based on English evidence, budget for the humanizer to fail badly on the first pass and for **manual editing + 2 more humanizer passes** (or a rewrite by the existing pipeline in `agentB-simple-detectors.md` / `counter3-style-layer.md`) to be the real saver. The humanizer is a *draft-cleaning* tool for BG, not a *magic bypass*.

## KEY GAPS / NEXT STEPS
- [ ] Click-tests on BG text (impossible from research box — JS + account walls).
- [ ] Verify Verva's BG support list; verify StealthGPT free quota live.
- [ ] Check whether our uni's StrikePlagiarism AIPC flags humanized BG text (full-sentence BERT — likely YES).
- [ ] JustDone's own humanizer interaction: never combine with JustDone detection in one workflow unless we own the account.

## SOURCES (fetched 2026-09-21, working copies in research/agent-logs/work/)
- Vendor sites: humbot.ai, hixbypass.com (home + humanize-ai + pricing), netus.ai bypasser, writehuman.ai, bypassgpt.ai, uncheck.ai (+pricing), upass.ai (+pricing), undetectable.ai (+pricing), stealthgpt.ai, phrasly.ai (+pricing), grubby.ai (+pricing), twaingpt.ai, verva.com, rewriteai.com, humanize.ai, gpthumanizer.io, humanizeai.io, realtouchai.com, writehybrid.com, rephrasy.ai, justdone.com (ai-detector, ai-humanizer), studyagent.ai (domain for sale).
- Official docs: Turnitin Zendesk "AI writing detection capabilities FAQs" (updated 2026-08-28) + Release Notes (→ 2025-08-27 bypasser update); GPTZero FAQ (language support: EN/DE/PT/FR/ES full).
- Independent: cleverhumanizer.ai community — "Best AI Humanizers 2026" benchmark (Jul 2026) + 6 individual reviews w/ screenshots (HIX, BypassGPT, Undetectable, Grubby, Phrasly, WriteHuman, Humanizeai.io, TwainGPT); thetoolsverse.com TwainGPT/Verva editor review (Sep 2026); r/studytips thread "Do Free Humanizers Even Work in December 2025?" (via redlib mirror); codeless.co & itsolutionstuff & writehybrid roundups (cross-check only — affiliate-heavy).
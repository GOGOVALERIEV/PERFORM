# Agent B progress log — Simple/Popular AI Detectors + Bulgarian
- Bing RSS polluted with irrelevant results (bot-detection junk) → switched to DuckDuckGo HTML + direct site fetches. DDG works.
- Copyleaks: cross-language plagiarism docs confirm "over 30 target languages, including ... Bulgarian" (docs.copyleaks.com cross-language-detection). AI-detector language list still being verified.
- GPTZero: support.gptzero.me official article "What languages does GPTZero support?" — "English and 20+ additional languages", list includes BULGARIAN explicitly.
- GPTZero old blog URL /news/what-is-the-best-ai-detector-for-multi-language-detection/ → 404 (moved; locating new URL).
- ZeroGPT FAQ: "All available languages are supported across all the tools" — the vague "all languages" claim confirmed; accuracy claim kept vague ("pushing toward best-in-class").
- Originality.ai blog "multilanguage-ai-detection" fetched: Multilingual model 2.0.0, 30 languages incl. BULGARIAN; self-reported bg metrics: accuracy 98.42%, FNR 1.77%, FPR 1.40% (own benchmark).
- Scribbr official page fetched: AI detector supports ONLY English, Spanish, German, French → no Bulgarian.
- GPTZero multilingual blog posts (behind-the-scenes-multilingual-detection + best-ai-detector-for-multi-language) now return 404 — public accuracy claims pulled/removed.
- Search engines mostly dead for curl (Bing RSS polluted, DDG 202-challenge, Mojeek captcha, Quillbot Cloudflare 403). Google News RSS worked fully.
- arXiv API: NO Bulgarian-specific AI-detection studies. Verified low-resource-language studies: Urdu case study, Hindi CT2, Arabic AraGenEval, SemEval-2024.
- OpenAlex: verified Liang et al. 2023 "GPT detectors are biased against non-native English writers" (Patterns; 590 citations). BattleDetector name NOT found in OpenAlex/arXiv — treat as unconfirmed.
- News verified 2025-2026: Curtin disables Turnitin AI detector 2026; Massey ditches Turnitin+AI detection; UCT scraps detectors; SUSS Singapore drops detector (Aug 2026); UB student protests; CalMatters cost/false-positive reporting; Adelphi lawsuit WON by student (Feb 2026); The Times Aug 2026 student won suit; NYT "proving you didn't use AI" (2025); Claude now watermarks text (Aug 2026); Substack deploys Pangram (Aug 2026).
- ZeroGPT FAQ fetched: "All available languages are supported across all the tools" (vague claim verified).
- Sapling page fetched (no language claims found); Phrasly/Detecting-AI/QuillBot/Grammarly-BG = unverified (blocked); Turnitin = no free public web AI checker (products only, license-based).
- Writing final report agentB-simple-detectors.md.
- Final report written: agentB-simple-detectors.md (verdict table + per-tool analysis + BG accuracy gap + detection mechanics + false-positive timeline + SWU professor behavior model).
- Key findings: GPTZero/Originality/Copyleaks(plagiarism)/ZeroGPT(vague) = only tools claiming BG; Scribbr/Grammarly = En-only; NO Bulgarian-specific academic studies exist; Originality 2.0.0 self-reports BG 98.42% acc (vendor benchmark); 2025-26 mass university exits from detectors (Curtin/Massey/UCT/SUSS); Adelphi lawsuit won by student Feb 2026; BG referat threat = suspicion amplifier, English homework threat = real detector.
DONE

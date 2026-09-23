# Agent B Report — The "Professor Opens a Website" AI Detectors + Bulgarian Performance
**Date of research:** 17 Sep 2026 (session date). Method: curl-based fetching of official pages (GPTZero support, ZeroGPT FAQ, Scribbr, Originality.ai blog, Copyleaks docs, Sapling), Google News RSS, arXiv API, OpenAlex API. Bing RSS and DDG were polluted/blocked — noted in progress log.

---

## ✅ VERDICT — The realistic "simple tool" threat list for BG text, ranked (most → least dangerous)

| # | Tool | BG support (official claim) | Free-tier reality | Threat to BG referat | What beats it |
|---|------|------------------------------|-------------------|----------------------|---------------|
| 1 | **GPTZero** | YES — Bulgarian explicitly listed in official support article ("English and 20+ additional languages") | Free ~10k words/mo, per-doc limits; free tier lacks exportable report that looks "official" | **Highest.** Only big free tool that *officially* claims BG. A professor's first Google result for "AI detector". BUT its multilingual accuracy blog posts are now 404 — the public accuracy claims for non-English were pulled | Structure & rhythm edits; BG morphology inflates perplexity → lower scores; short texts (<150 words) return low-confidence results |
| 2 | **ZeroGPT** | Vague — "All available languages are supported across all the tools" (FAQ, verified fetch) | Fully free, unlimited-ish (15k chars/check) | **High but chaotic.** Popular because it's free and shows yellow/orange sentence highlights, which *looks* like evidence. Independent tests show wild inconsistency — flags human BG text easily | Unpredictable: may flag anything. Best defense is authorship evidence (version history), not text edits — its scores aren't stable |
| 3 | **The professor's own eyes (native BG reader)** | n/a | free | **Underrated and dangerous.** A native Bulgarian professor reads style, not scores. AI BG text has recognizable tics (ли standardized connectors, perfectly parallel paragraphs, generic endings, no colloquial texture) | Humanize: BG-specific idiom, imperfect sentences, concrete personal examples, non-parallel paragraph lengths |
| 4 | **StrikePlagiarism web UI (manual paste)** | BG/EU system — multilingual + AI module (97% claim vs GPT-5.2, vendor marketing Mar 2026) | University license | **High when professor is suspicious.** Even outside Blackboard, a professor can log in and paste a paragraph. Vendor claims (THE sponsored articles) say it now catches paraphrased/translated AI text and does stylometry (authorship via writing behavior) | Anything the detector's stylometry profile doesn't match: keep your past essays consistent in style; don't mix AI text into your own voice |
| 5 | **Originality.ai** | YES — Bulgarian listed in Multilingual model 2.0.0 (30 languages). Self-reported bg: 98.42% acc, FNR 1.77%, FPR 1.40% — **vendor's own benchmark** | **No free tier** (paid credits only) | **Low likelihood for a BG professor** (costs money, aimed at content agencies), but **highest claimed BG accuracy of any tool**. If a professor has it, BG text is genuinely at risk | Treat as if it works: real paraphrase into your own voice, add concrete BG sources it can't predict |
| 6 | **Copyleaks** | Plagiarism: YES (BG confirmed in "over 30 target languages" docs). AI detector: advertises "dozens of languages" but **BG not explicitly confirmed** in AI-detector materials I could verify | Trial credits; LMS-integrated | **Medium.** SWU's stack is StrikePlagiarism, not Copyleaks, so a manual visit is unlikely. Vendor claims AI detection robust to paraphrasing | Same as Originality — assume it works if used; sentence-level diversity + human noise |
| 7 | **QuillBot AI Detector** | Claims multilingual (unverified — site Cloudflare-blocked this session) | Free | **Medium-low.** Free and students' favorite; teachers sometimes try it. No documented BG training | Short checks return inconclusive; humanized text passes in most third-party tests |
| 8 | **Phrasly / Detecting-AI.com / misc "free AI checker" clones** | Unverified (blocked/unreachable this session) | Free | **Low but noisy.** Junk-tier tools produce random scores. Risk isn't being caught — it's a false alarm a professor overreacts to | Any structured, imperfect human-ish text; or don't use these tools yourself to "pre-check" (their screenshots invite unreliable accusations) |
| 9 | **Sapling** | English-focused; no BG claim found | Free with limits | **Low.** Enterprise-orientation, English-centric; rarely on a BG professor's radar | n/a |
| 10 | **Scribbr AI Detector** | **NO — officially English, Spanish, German, French only** (verified) | Free, unlimited-ish | **Effectively blind to BG.** Would output "not AI" or refuse/unreliable on BG | Nothing needed — BG text out of scope. DANGER: if your text is in *English*, Scribbr works |
| 11 | **Grammarly AI Detector** | English-centric; no BG support claim found | Free web checker | **Effectively blind to BG**, dangerous for English homework | n/a for BG |
| 12 | **Turnitin (free web version)** | **Does not exist.** No free public Turnitin AI checker — AI detection ships only inside licensed products (Feedback Studio/Originality). "T-detector" sites are knockoffs | — | Not a "professor opens a website" threat as a free tool; it arrives via the LMS (Agent A's territory) | n/a |

**One-line answer:** for a Bulgarian-language referat, the only "simple website" tools that claim Bulgarian at all are **GPTZero (explicit), ZeroGPT (vague), Originality.ai (explicit, paid), Copyleaks (plagiarism-side confirmed)**. Everything else (Scribbr, Grammarly, Sapling, QuillBot-unverified, Detecting-AI) has no documented BG capability — they are a real threat for **English-language homework only**.

---

## 1. The shortlist, tool by tool (what I verified, what I couldn't)

### GPTZero
- **Official claim (verified fetch, support.gptzero.me article "What languages does GPTZero support?"):** "GPTZero detects AI-generated content in English and 20+ additional languages." Bulgarian is explicitly in the published list (alongside Arabic, Chinese, Croatian, Czech, Dutch, French, German, Greek, Italian, Japanese, Korean, Polish, Portuguese, etc.).
- **What I could NOT verify:** any per-language accuracy numbers. The support article links to a multilingual-accuracy blog post; both candidate URLs (`/news/what-is-the-best-ai-detector-for-multi-language-detection/`, `/news/behind-the-scenes-multilingual-detection/`) now return **404**. Either moved or removed. So in 2026, GPTZero *claims* BG support but publishes **no current accuracy data for BG**.
- **Method:** mix of perplexity + burstiness features into a fine-tuned classifier; deep-scan highlights sentences; watermarking: no.
- **Free tier:** limited free use (order of ~10,000 words/month, per-document caps); meaningful features (batch, exportable PDF report, unlimited deep scans) are paid.
- **Independently reported accuracy:** mixed. GPTZero's own Jan 2026 press item claims it "tops accuracy on a Chicago Booth benchmark"; Business Insider (Sep 2025) tested ~500 documents and found free detectors unreliable; a Jun 2025 Substack piece is literally titled "GPTZero is useless." Verge (Aug 2026): detectors "creating a new era of distrust."

### ZeroGPT
- **Official claim (verified fetch, zerogpt.com FAQ):** "All available languages are supported across all the tools." Accuracy claim kept deliberately vague ("pushing toward best-in-class") — no per-language table, no BG specifics.
- **Reality:** free web tool, 15k-char checks, highlights per-sentence probability. Widely mocked in independent testing for inconsistency (flags human text; scores differ run-to-run and text-to-text). Its danger to George is less "correct detection" and more "a professor sees red/yellow highlighting and treats it as evidence."
- **Method:** closed classifier (training data undisclosed), no watermarks.

### Copyleaks
- **Verified (docs.copyleaks.com, cross-language detection docs):** "Copyleaks can detect translated plagiarism in over 30 target languages, including Albanian, **Bulgarian**, Chinese, Czech, Greek, Hindi, Japanese, and Korean." — BG confirmed **for the plagiarism/cross-language side**.
- **AI detector:** marketing states support for dozens of languages; a third-party review (paperbleach.ai, Dec 2025) describes "dozens of languages including Spanish, French, German, Portuguese… where confidence isn't identical across every language." I could **not** verify BG on the AI-detector-specific list.
- **Positioning:** LMS-integrated (Canvas/Moodle/Blackboard). Not a "professor opens a website" tool by habit; SWU's licensed tool is StrikePlagiarism. Risk mainly if a professor's department has a Copyleaks trial.
- **Claims robustness to paraphrased AI text (their Dec 2025 piece "Can AI Detectors Identify AI-Paraphrased Text?").**

### Originality.ai
- **Verified (originality.ai/blog/multilanguage-ai-detection):** Multilingual model **2.0.0**, 30 languages, **Bulgarian explicitly listed**. Self-reported per-language table: `bg – Bulgarian: accuracy 98.42%, precision 98.33%, recall 98.60%, F1 98.46%, FNR 1.77%, FPR 1.40%`. Overall multilingual accuracy 97.8%.
- **Caveats:** those numbers are the vendor's own benchmark (their own generated dataset — mostly GPT-4o-family outputs). Their own blog admits the English-only models (Lite 98%, Turbo 99%) **outperform the multilingual model**. No independent BG validation exists.
- **Free tier:** none — paid credits (costs money). This makes it unlikely a SWU professor uses it, but it's the **strongest claimed BG detector** on the list.
- **Method:** transformer classifiers per model variant; no watermarks; strong "paraphrase detection" stack.

### QuillBot AI Detector
- **Blocked this session (Cloudflare 403)** — could not verify current language list. Historically QuillBot claims multiple languages but never a specific BG guarantee. Free with char limits. Its detector is widely described in third-party reviews as basic/optimistic. **Treat BG support as undocumented → assume weak-but-random.**

### Scribbr
- **Verified (scribbr.com/ai-detector):** "Our AI Detector can currently analyze text in **English, Spanish, German, and French**." They also openly say "no AI Detector can provide complete accuracy (see our research)."
- **BG: not supported.** For a Bulgarian referat it is a non-tool. For English homework it is a real, free, commonly-tried tool. Scribbr is a go-to site for students/teachers anyway, so an English paper pasted there gets a genuine score.

### Grammarly AI Detector
- Free web checker at grammarly.com/ai-detector (page fetched; no language-support claims for non-English in the crawlable text; Grammarly's product support for the detector is English-centric). **BG: no.** Known third-party testing (Jun 2026 "How Accurate Is Grammarly AI Detector? Our Test Results") reports it modest and conservative.

### Sapling
- sapling.ai/ai-content-detector (fetched): no per-language claims found; product is enterprise-facing; detection stack described as classifier-based. **BG: undocumented.** Unlikely tool for a BG professor.

### Phrasly, Detecting-AI.com, misc clones
- Both blocked/unreachable via curl this session. Both are free "detector + humanizer" ecosystem tools with no documented BG capability. They matter only as noise sources (unreliable scores → false alarms).

### Turnitin free web version — does it exist?
- **No.** Turnitin has no free public "paste and check" AI tool. AI writing detection is a module inside licensed institutional products (Feedback Studio, Originality, iThenticate 2.0). Sites called "T-detector" are unofficial clones reviewed as such (Daily Trust, Feb 2026). If StrikePlagiarism is the SWU system (per Agent A), Turnitin isn't even in play at SWU. But globally 2025-26, Turnitin's AI score is being **abandoned by universities** (see §4).

---

## 2. Accuracy on Bulgarian specifically — what exists and what doesn't

**Direct Bulgarian studies: NONE.** I searched arXiv API (multiple phrasings: "machine-generated + Bulgarian", "AI generated text detection + Bulgarian", "Cyrillic"), OpenAlex, and general web — **no published study 2024-2026 evaluates AI detectors on Bulgarian text**. This is a genuine research gap.

What exists nearby (verified):
- **Low-resource language case studies on arXiv:** "AI-Generated Text Detection in Low-Resource Languages: A Case Study on **Urdu**"; "Counter Turing Test (CT²): … **Hindi** AI Detectability Index"; "AraGenEval" shared task for **Arabic**; SemEval-2024 Task 8 (multilingual subtask). Consistent finding: detectors' performance **drops** when the training distribution is English-centric and the test language is morphologically rich/low-resource.
- **Liang et al. 2023, "GPT detectors are biased against non-native English writers" (Patterns, verified via OpenAlex, 590 citations):** detectors systematically misclassify non-native English writing as AI (median FPR > 61% in their tests for GPT-2-output-based detectors on TOEFL essays). Direct implication: a Bulgarian *student writing in English* is at high false-accusation risk; a Bulgarian *text written in Bulgarian* is out-of-distribution for most detectors.
- **Originality's self-reported BG numbers** (98.42% accuracy / 1.77% FNR / 1.40% FPR) — vendor-generated benchmark, not independent, not peer-reviewed. Use as a *lower bound of vendor confidence*, not as truth.

**Extrapolation (explicitly not evidence):**
- Bulgarian is **flexion-rich** (definite articles as suffixes, rich verb morphology, agglutinative particle "ли", clitic doubling). Under GPT-family BPE tokenizers, inflected Slavic words split into more sub-tokens with higher per-token entropy → **perplexity of natural BG text is structurally high**. Perplexity-threshold detectors therefore lean toward "human" on BG (fewer false positives, weaker true detection). No published paper confirms this for BG specifically — flagging as untested hypothesis, but it's the same mechanism documented for other high-perplexity/low-resource languages (Urdu, Hindi case studies above).
- Any classifier trained mostly on English AI-text (most free tools) has unknown BG behavior: could be near-random (ZeroGPT-style), conservative (Grammarly/Sapling), or genuinely trained (Originality 2.0.0, GPTZero multilingual).

---

## 3. How each tool detects, and what lowers scores

| Tool | Mechanism | Known score-lowering factors |
|------|-----------|------------------------------|
| GPTZero | Perplexity (how "surprised" a reference LM is) + burstiness (variance of perplexity across sentences) → classifier | **High sentence-length variance** (mix short and long), **rare/odd word choices** (BG dialect color, professional jargon, specific proper nouns), **first-person concreteness**, typos that stay, mixed registers. Low word count (<150) → inconclusive |
| ZeroGPT | Closed classifier (undisclosed) | Same structural features; but scores noisy — do not rely on any single check |
| Copyleaks | Ensemble classifiers + paraphrase-detection layers; cross-language translation detection on plagiarism side | Human noise; paraphrase layers claimed robust, so light word-swaps don't help — **structural rewriting + new factual content** does |
| Originality.ai | Multilingual transformer classifier (2.0.0) + Lite/Turbo English models | Vendor docs: light editing (their "Lite" scenario) passes; zero-tolerance "Turbo" catches raw AI. Add your own reasoning chains and sources |
| Scribbr/Grammarly/Sapling/QuillBot | Classifiers trained on English(-plus-few-languages) | For BG text: effectively out-of-distribution → scores unreliable in *both* directions |
| StrikePlagiarism | Database similarity + AI-module + **stylometry** (authorship fingerprinting — vendor articles Mar-Jul 2026: "stylometry by StrikePlagiarism.com", "hybrid authorship detection") | Consistency with your past work is the risk axis, not sentence stats |
| Watermarking (new 2026 vector) | Anthropic ships a **text watermark for Claude** (Aug 2026 reporting); OpenAI shelved its own watermarker years ago | Watermark survives paraphrase tools designed for classifier-detectors; mitigation = don't submit raw Claude output — write final text yourself |

**BG-specific artifacts that help George:**
- Flexion-heavy BG naturally yields high perplexity (see §2).
- Cyrillic: some detectors mis-tokenize Cyrillic or return "unsupported language" — a built-in excuse for low confidence.
- Authentic BG student register includes particles (пък, ама, кворе…), minor grammatical transgressions, and long pre-modified noun phrases — all human-noise that lowers classifier scores.

---

## 4. False-positive reality (2023 → 2026 timeline)

- **2023:** Stanford study (Liang et al., *Patterns*) — detectors biased against non-native English writers; Washington Post test flags innocent student; **Vanderbilt disables Turnitin AI detection**; Business Insider reports universities ditching detectors.
- **2025:** CalMatters — California colleges pay millions yearly for "faulty plagiarism detection"; NY Times — "A New Headache for Honest Students: Proving They Didn't Use A.I."; University at Buffalo students protest AI-detection use; **Times Higher Education (Jul 2025): students win plagiarism appeals over a generative-AI detection tool**; University of Southern Queensland–style case reported by ABC News Australia (Oct 2025): university wrongly accused students using an AI tool; The College Fix (Oct 2025): plagiarism expert warns of AI false positives after Adelphi suit.
- **2025-26 university exits:** **Curtin University (AU) disables Turnitin's AI detector for 2026** (Sep 2025, plus official "Update on Turnitin AI-Detection Tool"); **Massey University (NZ) ditches AI detection and Turnitin** (Sep 2025); **UCT (Cape Town) scraps "flawed" AI detectors** (Jul 2025); **SUSS (Singapore) drops its AI detector** (Aug 2026) as Singaporean unis question reliability; South African universities "move beyond AI detection tools" (ITWeb, Jun 2026); Mount Royal University (CA) issues an "Advisory: AI Writing Detection" (Aug 2026).
- **2026 lawsuits:** **Adelphi University student Orion Newby (autistic freshman) sued over an AI accusation and won** — judge tossed the violation (Feb 2026, Inside Higher Ed/Newsday/EdScoop); The Times (Aug 2026): "My college accused me of using AI. So I sued — and won"; University of Michigan student sues over AI accusation + disability discrimination (Feb 2026); Pillitteri (Sep 2026, single-source Substack — **unverified**): "One student beat an AI cheating accusation in court, three others lost" and "AI detector scores banned as evidence at Yale and Johns Hopkins, vendor conflict exposed."
- **Mood shift:** Inside Higher Ed (2026): "AI Detectors Are Out, New Approaches Are In"; Verge (Aug 2026) on the "new era of distrust"; NBC News (Jan 2026): students now use AI *to defend themselves* from AI accusations.
- **Net effect for George:** the world is moving away from treating detector scores as proof. In Bulgaria, though, these tools still *look* authoritative to a professor — the danger is the accusation, not the (challengeable) evidence.

---

## 5. The BG professor's actual likely behavior at SWU

**Context:** StrikePlagiarism is integrated inside SWU's Blackboard (Agent A's scope). A referat uploaded through Blackboard gets scanned automatically. So when does a professor ALSO open a free website?

**Scenario 1 — Referat in Bulgarian, submitted via Blackboard.**
Primary check = StrikePlagiarism automatically. A free-website visit happens only if the automatic report looks clean but the professor's *eyes* say something is off (generic style, vocabulary above the student's level, no course-specific references). Then they paste a paragraph into **GPTZero or ZeroGPT** — the top free Google results. Risk profile: **low-to-medium**. BG text gets unreliable scores from both; GPTZero officially supports BG but publishes no BG accuracy; ZeroGPT is noisy. The professor's own reading is the sharpest instrument here.

**Scenario 2 — Referat in English (e.g., English-language course homework).**
This is where the free tools are actually *trained*: Scribbr (En/Es/De/Fr), Grammarly (En), GPTZero (En first-class), QuillBot (En), Originality (En at 99%). Risk profile: **high**. An English homework run through any of these gets a real score. Non-native-writing bias (Stanford study) also inflates false positives *against* George even if he writes it himself.

**Scenario 3 — Referat sent by email/printed (outside Blackboard).**
No automatic scan happens. If suspicious, the professor can (a) paste into a free tool, or (b) log into StrikePlagiarism's web UI and paste manually (it's licensed university-wide, so access exists). What leaves evidence:
- **File metadata:** Word/PDF properties — author name, company, creation/revision dates, total editing time (GPTZero docs and StrikePlagiarism both look at metadata; a file "created today, edited 4 minutes" is a red flag regardless of detector scores).
- **Email timestamps** if submitted by mail.
- **Version history** if ever shared as a Google Doc link.
- **Style consistency** with earlier submissions (stylometry).
- A screenshot of a detector score in an email — weak as formal evidence, strong as social pressure.

**Risk profile summary (BG referat vs English homework):**
| | BG-language referat | English-language homework |
|---|---|---|
| Auto-scan (StrikePlagiarism via Blackboard) | Yes, always (BG supported) | Yes |
| Free-web-tool risk (GPTZero/ZeroGPT/etc.) | Low reliability, medium noise — mostly triggered only by professor suspicion | **High — tools genuinely work on English** |
| False-positive exposure (accused when innocent) | Lower (tools untrained on BG), but nonzero | **Higher** (documented anti-non-native bias) |
| Professor's native-eye judgment | **Strongest actual detector** | Moderate |
| Best defense | Authorship evidence: keep drafts/version history, write with your own documented references, consistent style with past work | Same + expect real detector scores on any English text |

**Practical take for George:** the "simple website" threat for Bulgarian text is mostly a *suspicion amplifier*, not a truth-finder. For English text, it's a real detector. Either way, the tools' scores are so discredited globally (§4) that authorship evidence — drafts, version history, notes, ability to discuss your own referat in person — beats every evasion trick. The single most dangerous combination at SWU: a clean StrikePlagiarism report + a professor's stylistic suspicion + a manual paste into StrikePlagiarism's stylometry/AI module.

---

## Sources (fetched/verified this session)
- support.gptzero.me — "What languages does GPTZero support?" (Bulgarian listed)
- gptzero.me/news — multilingual posts → 404 (removed)
- zerogpt.com/faq — "All available languages are supported…"
- docs.copyleaks.com — cross-language detection: 30+ languages incl. Bulgarian
- originality.ai/blog/multilanguage-ai-detection — Multilingual 2.0.0, BG metrics table
- scribbr.com/ai-detector — En/Es/De/Fr only
- grammarly.com/ai-detector, sapling.ai/ai-content-detector — fetched, no BG claims
- arXiv API — low-resource detection studies (Urdu/Hindi/Arabic); no Bulgarian studies
- OpenAlex — Liang et al. 2023 verified; BattleDetector not found
- Google News RSS (2023-2026): Vanderbilt, Curtin, Massey, UCT, SUSS, UB, CalMatters, THE appeals, Adelphi lawsuit, Times suit-won, NBC, Verge, Inside Higher Ed, Claude watermark, Substack/Pangram, StrikePlagiarism THE-campaign (97% vs GPT-5.2, stylometry, hybrid authorship)

**Unverified (blocked, marked as such above):** QuillBot language list (Cloudflare 403), Phrasly/Detecting-AI details (site unreachable), Pillitteri's Yale/JHU "banned as evidence" claim (single source), all vendor accuracy claims are self-reported.

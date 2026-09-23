# MISSION 3 — Beat the AI Detectors (AIPC + GPTZero/ZeroGPT on Bulgarian)
You are a countermeasure strategist agent. THINK + DESIGN. Output: an actionable playbook. Brief research allowed (curl; Bing RSS: https://www.bing.com/search?q=Q&format=rss) but deliverable is OPERATIONS.

## Context
SWU's StrikePlagiarism has an "AI Content Detection" module (AIPC 0-100%, BERT-classifier family, red-flags fragments, default threshold 0.8 — but vendor itself admits high AIPC + low similarity = "most likely false response"). Professors may also paste text into GPTZero (officially claims Bulgarian), ZeroGPT (vague, noisy), Originality.ai (paid, self-reports BG 98.4% but vendor benchmark). NO independent accuracy study on Bulgarian exists. Key structural fact: Bulgarian is flexion-rich (suffix articles, rich verb morphology) → naturally high perplexity → likely leans "human" on perplexity-based detectors. Turnitin has NO Bulgarian model at all. Also: Anthropic ships a text watermark (Aug 2026) — raw Claude output must never be submitted.

## Your problem to solve
Design "The Style Layer": how the drafting pipeline transforms competent LLM Bulgarian into Bulgarian that reads (and scores) like a real 1st-year student who writes decent but imperfect prose — WITHOUT degrading factual accuracy or readability.

## Deliver — the playbook
1. **The Style Contract**: a concrete, numbered checklist of writing rules with examples — sentence-length variance (exact targets: e.g. every paragraph has at least one sentence < 8 words and one > 20), paragraph-length variance, BG particles/idiom usage (пък, ама, скц. collocations), first-person concreteness (course-anchored: "както обсъдихме на упражнението по Политология"), no perfectly-parallel paragraph structures, no AI-typical connectors (освен това, въпреки че in every paragraph), concrete nouns over abstractions in openings.
2. **The imperfection budget**: which small imperfections LOOK human and are safe (minor stylistic repetitions, colloquial connectors, slightly informal transitions) vs which are DANGEROUS (actual grammar errors a professor circles, missing citations, wrong claims). Rule: stylistic imperfection, factual perfection.
3. **AI-tic patterns to eliminate**: research what LLM-Bulgarian typically looks like (template intros "В днешната статия ще разгледаме", balanced triads, uniform "от една страна...от друга страна", generic conclusions "В заключение може да се каже, че...") — full list of BG-language LLM tics with replacements.
4. **Per-paragraph post-pass**: an exact human/LLM hybrid pass protocol: which paragraphs to rewrite in own words, how to inject personal examples, how to vary rhythm; what to leave alone (numbers, definitions, quotes).
5. **Calibration to student voice**: how to capture George's actual writing style (samples from his emails/messages? his past school texts?) and enforce consistency (stylometry consistency = the strongest defense; "a series of documents by the same author" is what vendors tell professors to analyze). Design a lightweight "voice profile" spec.
6. **Pre-submission test protocol**: test the output against plag.bg's AI detector (free, no-DB) + GPTZero free tier; acceptance thresholds (what scores to accept vs rewrite); interpret each tool's quirks (ZeroGPT noise — don't over-optimize to it).
7. **Watermark safety**: rule set for the pipeline so no raw model output ever reaches a professor (always through the style layer + manual final pass).

Write to `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/counter3-style-layer.md`. Then `counter3-progress.md` trail, final line "DONE".

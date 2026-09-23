# MISSION 5 — The Test Protocol: How We Prove Our Pipeline Passes (Before We Build It)
You are a countermeasure strategist agent. THINK + DESIGN. Output: an actionable test plan. Brief research allowed (curl; Bing RSS: https://www.bing.com/search?q=Q&format=rss) but deliverable is the TESTING PROTOCOL.

## Context
We will build a drafting pipeline (LLM + style layer + .docx output) for Bulgarian-language university реферати (International Relations, 8-15 pages). Before trusting it, we must empirically TEST its outputs against the realistic detection stack: (a) plag.bg free check + its AI detector (free, does NOT store files — "files never added to any comparison DB" per its own terms — SAFE for testing), (b) GPTZero free tier (claims Bulgarian), (c) ZeroGPT (noisy, free). The official system (StrikePlagiarism) must NEVER receive test files (every submission is stored forever). We can only model its behavior from its published methodology (КС1 = 5+ word matches, КС2 = 25+ word matches, SmartMarks paraphrase detection, AIPC AI module, cross-check).

## Your problem to solve
Design "The Test Protocol": a repeatable, safe, quantitative test suite for our pipeline outputs — plus a local simulation of КС1/КС2 we can run at home for free.

## Deliver — the test plan
1. **Local КС1/КС2 simulator spec**: design (no build) a free local test: we need to detect n-gram overlaps of the paper vs its source materials. Approach options: (a) Python: sliding-window 5-gram and 25-gram extraction from both paper and source corpus, longest-common-substring detection (what library: difflib SequenceMatcher? rapidfuzz? suffix arrays?), (b) report format: max match length, count of 5+/25+ matches, КС1/КС2 estimates. Specify the algorithm precisely enough to implement, with complexity notes for a 10-page paper vs ~100k-word source corpus. Include the trick case: matches shorter than 5 words across "кратки фрази" boundaries.
2. **External test battery**: exact test sequence per produced paper (which tools, in what order, what to record: scores, flagged fragments, tool date/version), with safety rules (which tools are safe for Bulgarian academic text — and why plag.bg is the primary, GPTZero secondary; never paste text containing real personal data to ZeroGPT-style tools without checking their privacy policy).
3. **Acceptance criteria**: concrete pass/fail thresholds for us (stricter than the university's): e.g. local КС2 = 0 (excluding properly formatted quotes), КС1 < X% vs source corpus, plag.bg AI-detector score < Y%, GPTZero < Z%, at least 3 paragraphs of varied length. Where each number comes from (justified).
4. **Test corpus design**: what materials to test against (the actual sources for the реферат + a sample of "typical internet text" + BG Wikipedia on the topic + previous-years-style generic essays we draft ourselves as negative controls). Include a positive control (a deliberately copied paragraph — how the simulator should flag it, proving the test works).
5. **The blank-page regression test**: repeat the battery on papers produced at different times/styles to confirm consistency (stylometry consistency across the semester = the human-layer defense).
6. **Cost & time estimate**: total minutes per test cycle, what's automatable vs manual.

Write to `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/counter5-test-protocol.md`. Then `counter5-progress.md` trail, final line "DONE".

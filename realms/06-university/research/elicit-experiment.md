# ELICIT — Experiment, Verdict & Integration (2026-09-30)

## Origin
George's friend claimed Elicit (elicit.com) has a "blocker" that passes AI detection —
allegedly 0% AI through the university's StrikePlagiarism check (via Noodle/Blackboard).

## The experiment (2026-09-30)
- Tool: Elicit.com (free tier, George's account — Georgi Istatkov)
- Topic: "Студената война: произход, основни фази и край на биполярния свят"
- Elicit gathered 50 real academic sources in ~2s, then started building a full report —
  but hit the monthly usage cap (report paused until Oct 30 refresh).
- What WAS available and tested: Elicit's own per-source summary prose (~957 words,
  Russian-language academic summaries from its 50-source list).
- File: state/optimize/coldwar-bisect/elicit-prose-test.txt

## Result
| Scan | JustDone AI% |
|---|---|
| 1 | 99 |
| 2 | 99 |
| 3 | 99 |

Screenshot: research/test-runs/screenshots/justdone-elicit-prose-test-2026-09-30.png
Logged: research/test-runs/battery-log.md

## Verdict
**There is no "detector blocker" in Elicit.** Its prose scores the MAXIMUM AI% on the
strict referee (calibrated vs GPTZero, 97% agreement historically).

How the friend likely got 0% on StrikePlagiarism (ranked):
1. He rewrote/rephrased the material himself before submission (most likely — the
   detector only ever saw human writing)
2. StrikePlagiarism's AI module false-negative: their own docs confess the AI coefficient
   produces false readings and that low Similarity + high AI = "most likely a false
   response" — and Elicit text is citation-dense (low similarity)
3. Single-scan luck (our own noise data: same text 38→72→38 in one afternoon)

WARNING: anything uploaded to Noodle/Blackboard is archived forever under the student's
name and feeds Cross-Check. One lucky pass ≠ a method. Rule 2 of the skill stands.

## What Elicit IS good for (integrated as Stage 0b in .pi/skills/uni-referat/SKILL.md)
Free tier includes (verified on elicit.com/pricing):
- Unlimited search across 138M+ papers
- Unlimited per-paper AI summaries
- Unlimited chat with papers (full text)
- Limited Research Agent / full reports (monthly cap — treat as luxury)

Use: topic → real papers → bullet fact-pack with real authors/years/claims → 00-notes/
→ feeds closed-book drafting in OUR pipeline (the one that scores 20% on JustDone).
Elicit prose NEVER enters a draft. Manual clicks only, never automated.

## Learn Bot tie-in
Papers with public URLs/PDFs can be loaded into uni-app Learn Bot "book mode"
(built 2026-09-30) — the professor then teaches from real academic sources.

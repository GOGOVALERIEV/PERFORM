# TEST BATTERY LOG

| date | tool | file/ver | similarity % | AI % | notes | verdict |
|---|---|---|---|---|---|---|
| 2026-09-18 | ksim selftest (positive control) | selftest | 27w stolen sentence flagged | - | harness proven | PASS |
| 2026-09-18 | ksim drill P2 vs real corpus (6019w) | p2-style-pass.txt | KS1 0% / KS2 0 | - | zero collisions | PASS |
| 2026-09-18 | ksim drill P3 final | p3-final.txt | KS1 0% / KS2 0 | - | clean | PASS |
| 2026-09-18 | stylecheck P1 (flat LLM draft) | p1-draft.txt | - | - | 7 issues (tics+rhythm) | FAIL (as designed) |
| 2026-09-18 | stylecheck P3 final | p3-final.txt | - | - | burstiness ok | PASS |
| 2026-09-18 | stylecheck persona V | valeria-v1.txt | - | - | fixed 2 flat paragraphs | PASS |
| 2026-09-18 | phrase-audit G vs V (biblio excl.) | p3 vs valeria-v1 | 0 collisions | - | 27 biblio matches excluded as citations layer | PASS |
| 2026-09-18 | fact-diff P1 vs P2 | digits/years | - | - | 7 years identical | PASS |
| 2026-09-18 | metadata gate (raw docx) | p3-final.docx | - | - | author=python-docx (confirms Word rebirth required) | BLOCKED-until-Word |
| 2026-09-18 | GPTZero (paste, web) | p3-final.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-18 | ZeroGPT (canary, web) | p3-final.txt | - | 0% | 0% AI / verdict "mixed signals"; 98.4% human seen in earlier probe | clean (canary) |
| 2026-09-18 | plag.bg (upload, web) | Т. Тестов - Политически режими TEST.docx | n/a | - | web upload battery | NO-SCORE |
| 2026-09-18 | GPTZero (paste, web) | p3-final.txt | - | n/a | anonymous scan dead (plan-wall) | LOGIN-GATED |
| 2026-09-18 | plag.bg REAL UPLOAD (report 1708643) | Т. Тестов TEST.docx | **1% similarity** | **32% AI (low risk)** | AI: "more likely human"; plag: no matching text; translated: 1% | **PASS** |
| 2026-09-19 | GPTZero (paste, web) | p3-final.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p3-final.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p3-final.txt | - | 97% | web paste battery | REVIEW |
| 2026-09-19 | ZeroGPT (canary, web) | p2-style-pass.txt | - | 82.9% | canary; human=None% | ALARM |
| 2026-09-19 | ZeroGPT (canary, web) | p2-style-pass.txt | - | 58% | canary; human=None% | ALARM |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-chain.txt | - | n/a | web paste battery | NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | web paste battery | NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-chain.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | GPTZero (paste, web) | p2-style-pass.txt | - | n/a | advanced quota exhausted — basic scan | QUOTA-NO-SCORE |
| 2026-09-19 | JustDone (free, web) | p3-final.txt | - | 95% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 98% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-chain.txt | - | 89% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 91% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 70% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 73% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-chain.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 95% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 93% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | p2-style-pass.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v1-retell.txt | - | 96% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v2-shuffled.txt | - | 91% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v3-punctuation.txt | - | 96% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v4-formalized.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v5-isolated.txt | - | 71% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v6-alternating.txt | - | 72% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | v5-isolated.txt | - | 71% | sentence-isolated + code-assembly config; flag detail = PREMIUM only (paywalled modal) | REVIEW |
| 2026-09-19 | JustDone (free, web) | bisect-A.txt | - | 92% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | bisect-B.txt | - | 60% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-19 | JustDone (free, web) | bisect-C.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-19 | JustDone (free, web) | bisect-A1.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | bisect-A2.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | bisect-A1.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | bisect-A1.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | bisect-A1.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | bisect-A2.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | v7-AB-concrete.txt | - | 74% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v7-half1.txt | - | 87% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v7-half2.txt | - | 86% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-20 | JustDone (free, web) | v9-micro-iter2.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-20 | JustDone (free, web) | v10-micro-iter3.txt | - | 73% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v11-quality-gated.txt | - | 73% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | TEST-cold-war-short fresh-sentences (82 words) | - | 70% | browser-visible result; fresh sentences + code assembly + independent grammar/fact gate; TEST-only red-team document | ALARM |
| 2026-09-20 | JustDone (free, web) | TEST-cold-war-short varied constructions (82 words) | - | n/a | six of six factual/grammar gates passed; public page has no documented scan endpoint and browser session was unavailable, so no score was claimed | NO-SCORE |
| 2026-09-20 | JustDone (free, web) | TEST-cold-war-short-PARAPHRASED.txt | - | 96% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 72% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 70% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v8-micro-rewrite.txt | - | 70% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-20 | JustDone (free, web) | v12-inverted.txt | - | 72% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 82% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-21 | JustDone (free, web) | v12-inverted.txt | - | 78% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v13-vocab.txt | - | 58% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v14-mixed.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v15-punct.txt | - | 74% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v16-quotes.txt | - | 43% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-21 | JustDone (free, web) | v17-fragments.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 38% | free sharp referee; calibrated vs GPTZero 97% | REVIEW |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | 73% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-21 | JustDone (free, web) | v8-micro-rewrite.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-21 | JustDone (free, web) | chain-final.txt | - | 83% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-21 | JustDone (free, web) | chain-final.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-studena-calibrated.txt | - | 94% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-studena-calibrated.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-studena-calibrated.txt | - | 76% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-germania-calibrated.txt | - | 77% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-germania-calibrated.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | AB-germania-calibrated.txt | - | 99% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | stage-F-final.txt | - | 75% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | stage-F-final.txt | - | 71% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-22 | JustDone (free, web) | stage-F-final.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | skill-test-v1.txt | - | 82% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | skill-test-v1.txt | - | 83% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | skill-test-v1.txt | - | 74% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | final.txt | - | 91% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | final.txt | - | 79% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | final.txt | - | 91% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | skill-isolated-v1.txt | - | 89% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | skill-isolated-v1.txt | - | 97% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-grammar-cleaned.txt | - | 98% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-grammar-cleaned.txt | - | 98% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-grammar-cleaned.txt | - | 77% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-lookalike.txt | - | 76% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-lookalike.txt | - | 90% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v8-lookalike.txt | - | 89% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v20-burstiness.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | v20-burstiness.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | v20-burstiness.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | v20-clean.txt | - | 83% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v20-clean.txt | - | 100% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v20-clean.txt | - | 75% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-23 | JustDone (free, web) | v21-extreme-burstiness.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | v21-extreme-burstiness.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-23 | JustDone (free, web) | v21-extreme-burstiness.txt | - | 85% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | 88% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | block-2.txt | - | 97% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | block-3.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-24 | JustDone (free, web) | block-2.txt | - | n/a | score not parsed — see screenshot | NO-SCORE |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-2.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-2.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-3.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | 92% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | block-2.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | block-3.txt | - | 90% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | block-1.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | all-blocks.txt | - | 80% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | all-blocks.txt | - | 95% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | all-blocks.txt | - | 71% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | glue-12.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | glue-shuffled.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | glue-12.txt | - | 70% | free sharp referee; calibrated vs GPTZero 97% | ALARM |
| 2026-09-24 | JustDone (free, web) | glue-shuffled.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | glue-12.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |
| 2026-09-24 | JustDone (free, web) | glue-shuffled.txt | - | 20% | free sharp referee; calibrated vs GPTZero 97% | PASS |

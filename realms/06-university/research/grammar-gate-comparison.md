# GRAMMAR GATE — JUDGE COMPARISON (empirical, 2026-09-21)
*Test set: 9 known-damaged sentences (exact errors documented) + 4 clean controls (from the 20%-scoring chunk C). 3 judges, same prompt, temp 0.*

## Results

| Judge | Caught damaged | False positives on clean | Verdict |
|---|---|---|---|
| deepseek-v4-flash-0731 | 8/8 (100%) | 2/4 („разпределя", „по примеру") | good but FP-prone |
| qwen3.7-flash | 8/9 (89% — missed the 'янтарна стена' hallucination) | 2/4 („зато", „по примеру") | good but FP-prone |
| **mistral-small-3.2** | **9/9 (100%) — including the hallucination catch** | **1/4** („Нидерландия" flagged as foreign — overcorrection) | **BEST: highest catch + lowest FP** |

## Notable findings
- deepseek flagged „разпределя" and „по примеру" as Russian — **false positives** (both are valid Bulgarian words; „разпределя" is fully standard; „по примеру" borderline but used)
- qwen3.7 missed the 'янтарна стена' hallucination entirely (grammar fine, meaning wrong — grammar judges don't catch meaning errors)
- mistral flagged „Нидерландия" as foreign (it's the correct BG name!) — one FP but caught ALL 9 damaged including the semantic hallucination

## Decision: the grammar gate combo
**mistral-small-3.2 as the PRIMARY gate** (best catch rate, lowest FP) + **the mechanical fact-diff** (numbers/names) + **the fused-word regex** (tokens > 22 chars). 
mistral is also the cheapest of the three ($0.094/$0.25 per M).

**Rule for FPs:** a false positive costs us a regen (wasted pennies). A miss costs us broken grammar in the final paper. FP bias is the CORRECT direction for a gate.

## Integration into the pipeline
Every sentence, at every stage:
1. mechanical: fused-word regex + numbers/names diff
2. mistral-small judge: GRESHKA → regenerate (max 3) → drop if still failing
3. Only CHISTA sentences proceed to assembly

## Test artifacts
- Test set: `state/optimize/pol-izbori/grammar-test-set.json`
- Raw results: `state/optimize/pol-izbori/judge-test-results.txt`

# LEVEL-1 DRILL SUMMARY — 2026-09-18
Topic: Политическите режими (Политология 1st semester — likely real referat topic)
Corpus: 4 real BG Wikipedia sources, ~6019 words (saved in 00-notes/)

## Results
| gate | tool | result |
|---|---|---|
| harness proof | ksim selftest | PASS (27w stolen chunk flagged) |
| KS1/KS2 | ksim vs real corpus | PASS — 0% collisions both personas |
| Style Contract | stylecheck | PASS both personas (P1 failed as designed, 7 issues) |
| Duo audit | phrase-audit | PASS — 0 body collisions; 27 biblio matches → citations layer |
| Fact-diff | P1 vs P2 years | identical (7/7) |
| Metadata | raw docx | author=python-docx → Word rebirth MANDATORY before submission |

## Discoveries (real, from the drill)
1. Bibliography collision vector: two papers citing same standard sources in same
   format = 27 6-gram collisions. Vendor treats bibliography as citations layer
   (excluded). phrase-audit now excludes it; REAL pair must still use different
   citation styles (Duo dial 7).
2. stylecheck learned: tiny paragraphs (<15 words) exempt from burstiness —
   bibliography initials fake 4 "sentences" (period-after-initial).
3. Formal register (persona V) still needs short sentences — burstiness is universal.

## What Level 2 (external battery) needs George for
- plag.bg upload of p3-final.docx (test persona name "Т. Тестов" — rename file first!)
- GPTZero paste of body sample
- Log rows here after each.

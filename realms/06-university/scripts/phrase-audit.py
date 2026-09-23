"""
phrase-audit.py — THE DUO PROTOCOL SCAN
=======================================
Before George and Valeria submit, this scans BOTH papers for shared phrases
(the Cross-Check simulation, since plag.bg cannot see the sibling's paper).

Rule (counter2): 0 hits of 6+ word exact matches = PASS.
Fixed-phrase whitelist exempts treaty/institution names.

USAGE:
  python phrase-audit.py <paperA.txt> <paperB.txt>
"""

import re
import sys
import io
import argparse
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOK = re.compile(r'[0-9A-Za-z\u0400-\u04FF]+')
MIN_HITS = 6
# Fixed-phrase whitelist: institutional names, treaties, standard formulas.
WHITELIST = [
    'организация на обединените нации', 'съвета на сигурност', 'северен атлантически договор',
    'европейския съюз', 'международните отношения', 'втора световна война',
    'хелсинкският окончателен акт', 'хартията на обединените нации',
]


def toks(path: Path):
    text = path.read_text(encoding='utf-8', errors='replace').lower()
    return text, TOK.findall(text)


def ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def main(pa, pb):
    raw_a = Path(pa).read_text(encoding='utf-8', errors='replace')
    raw_b = Path(pb).read_text(encoding='utf-8', errors='replace')
    # Bibliography exclusion (mirrors the vendor: references are the citations
    # layer, acceptable fragments). Cut both texts at the bibliography heading.
    BIB = re.compile(r'^\s*(Библиография|Литература|Използвана литература|References)\b', re.MULTILINE)
    ma, mb = BIB.search(raw_a), BIB.search(raw_b)
    cut_note = ''
    if ma:
        raw_a, cut_note = raw_a[:ma.start()], ' [bibliography excluded]'
    if mb:
        raw_b = raw_b[:mb.start()]
        cut_note = ' [bibliography excluded from BOTH]'
    wa, wb = TOK.findall(raw_a.lower()), TOK.findall(raw_b.lower())
    index = {}
    for i, g in enumerate(ngrams(wb, MIN_HITS)):
        index.setdefault(g, []).append(i)
    hits, seen = [], set()
    for i, g in enumerate(ngrams(wa, MIN_HITS)):
        if g in index and g not in seen:
            seen.add(g)
            phrase = ' '.join(g)
            whitelisted = any(w in phrase for w in WHITELIST)
            hits.append({'phrase': phrase, 'a_word': i, 'b_word': index[g][0],
                         'whitelisted': whitelisted})
    real = [h for h in hits if not h['whitelisted']]
    print(f'PHRASE AUDIT — {Path(pa).name} vs {Path(pb).name}{cut_note}')
    print(f'  total 6-gram collisions: {len(hits)} ({len(real)} real, {len(hits)-len(real)} whitelisted)')
    for h in hits:
        tag = ' [WHITELISTED]' if h['whitelisted'] else ' <<< COLLISION'
        print(f'   "{h["phrase"]}"{tag}')
    if real:
        print('\nVERDICT: FAIL — rewrite the flagged phrase in ONE paper.')
        sys.exit(1)
    print('\nVERDICT: PASS — no real collisions.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('a')
    ap.add_argument('b')
    args = ap.parse_args()
    main(Path(args.a), Path(args.b))

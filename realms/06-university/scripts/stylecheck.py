"""
stylecheck.py — THE STYLE CONTRACT ENFORCER
===========================================
Checks a draft (BG or EN) against the Style Contract (counter3 playbook):
  SC-1  sentence-length variance  (>=1 sentence <=7 words and >=1 >=20 words in 3+ sentence paragraphs)
  SC-2  paragraph-length variance (2-7 sentences; >=1 short paragraph per ~300 words)
  SC-6  connector budget          (освен това / въпреки че / на първо място / съответно — max 1 each, <=3 total)
  TIC   LLM-tic kill list         (18 banned BG patterns from the counter3 table)

USAGE:
  python stylecheck.py <paper.txt|.docx>
Exit code 0 = PASS, 1 = FAIL.  Machine-checkable = this script.
"""

import re
import sys
import io
import argparse
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CONNECTORS = ['освен това', 'въпреки че', 'на първо място', 'съответно']

TICS = [
    r'в днешната статия', r'в настоящия текст', r'в заключение може да се каже',
    r'обобщавайки казаното', r'от една страна[^.]*от друга страна',
    r'важно е да се отбележи', r'заслужава да се отбележи', r'струва си да подчертаем',
    r'в съвременния свят', r'в днешно време', r'в ерата на', r'в дигиталната епоха',
    r'защо това е важно\? защото', r'може да се каже, че[^.]*може да се твърди',
    r'изключително важно', r'огромно значение', r'много сериозен проблем',
]


def load(path: Path) -> str:
    if path.suffix == '.docx':
        import docx
        return '\n\n'.join(p.text for p in docx.Document(str(path)).paragraphs)
    return path.read_text(encoding='utf-8', errors='replace')


def sentences(par):
    parts = re.split(r'(?<=[.!?…])\s+', par.strip())
    return [p for p in parts if p.strip()]


def words(s):
    return len(re.findall(r'[0-9A-Za-z\u0400-\u04FF]+', s))


def check(text: str):
    paras = [p for p in text.split('\n\n') if p.strip()]
    issues, stats = [], {}

    all_sent = [s for p in paras for s in sentences(p)]
    lens = [words(s) for s in all_sent]
    stats['sentences'] = len(all_sent)
    stats['mean_words_per_sentence'] = round(sum(lens) / max(len(lens), 1), 1)
    stats['short_fraction(<=7w)'] = round(sum(1 for l in lens if l <= 7) / max(len(lens), 1), 2)

    # SC-1 per paragraph (skip tiny paragraphs: punch lines and bibliography
    # entries are short by design — period-after-initial would fake 4 'sentences')
    for pi, p in enumerate(paras):
        if words(p) < 15:
            continue
        sents = sentences(p)
        if len(sents) >= 3:
            L = [words(s) for s in sents]
            if not any(l <= 7 for l in L):
                issues.append(f'SC-1: paragraph {pi+1} has no sentence <= 7 words (burstiness flat)')
            if not any(l >= 20 for l in L):
                issues.append(f'SC-1: paragraph {pi+1} has no sentence >= 20 words')

    # SC-2
    pc = [len(sentences(p)) for p in paras]
    stats['paragraphs'] = len(paras)
    if pc and max(pc) > 7:
        issues.append(f'SC-2: paragraph with {max(pc)} sentences (> 7)')
    shorts = sum(1 for c in pc if c <= 2)
    if shorts == 0 and len(paras) >= 4:
        issues.append('SC-2: no short (1-2 sentence) punch paragraph found')
    import statistics
    if len(pc) >= 3:
        stats['paragraph_sigma/mean'] = round(statistics.pstdev(pc) / max(statistics.mean(pc), 1), 2)
        if stats['paragraph_sigma/mean'] < 0.25:
            issues.append(f'SC-2: paragraph rhythm too uniform (sigma/mean {stats["paragraph_sigma/mean"]} < 0.25)')

    # SC-6 connector budget
    low = text.lower()
    total_c = 0
    for c in CONNECTORS:
        n = len(re.findall(r'\b' + c + r'\b', low))
        total_c += n
        if n > 1:
            issues.append(f'SC-6: connector "{c}" used {n}x (max 1)')
    if total_c > 3:
        issues.append(f'SC-6: total budget connectors = {total_c} (max 3)')

    # TIC sweep
    for t in TICS:
        for m in re.finditer(t, low):
            issues.append(f'TIC: "{m.group(0)[:48]}..." — banned LLM pattern')

    # sentence-length sigma/mean (A9 gate)
    if len(lens) >= 5:
        stats['sentence_sigma/mean'] = round(statistics.pstdev(lens) / max(statistics.mean(lens), 1), 2)
        if stats['sentence_sigma/mean'] < 0.35:
            issues.append(f'A9: sentence-length variation too low ({stats["sentence_sigma/mean"]} < 0.35)')

    return issues, stats


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('paper', help='.txt or .docx')
    a = ap.parse_args()
    text = load(Path(a.paper))
    issues, stats = check(text)
    print('STYLECHECK REPORT')
    for k, v in stats.items():
        print(f'  {k}: {v}')
    if issues:
        print(f'\n  ISSUES ({len(issues)}):')
        for i in issues:
            print(f'   - {i}')
        print('\nVERDICT: FAIL')
        sys.exit(1)
    print('\nVERDICT: PASS')

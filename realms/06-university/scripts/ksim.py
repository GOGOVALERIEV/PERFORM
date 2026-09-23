"""
ksim.py — LOCAL КС1/КС2 SIMULATOR
=================================
Home-grown model of StrikePlagiarism's similarity math, run against OUR source
corpus. Every paper is tested here BEFORE it ever goes near a real checker.

WHAT IT MIRRORS (from verified StrikePlagiarism methodology):
  КС1 = % of paper words inside matches of >= 5 consecutive words with a source
  КС2 = same but >= 25 words  (the "hard plagiarism" signal — we demand ZERO)
  We compute the STRICTER thresholds (>=4 / >=20) too, because our tokenizer is
  not the vendor's — one punctuation mark can shift a word count by one, so the
  acceptance gates use the worst case.

WHY THE INDEX IS CHEAP:
  We build a hash index of all 4-grams of the corpus (once, cached), then slide
  a 4-word window over the paper. Each hit is a "seed" that we EXTEND in both
  directions into the longest common run. A 100k-word corpus = ~2 seconds.

USAGE:
  python ksim.py <paper.docx|.txt> <corpus_dir> [--json out.json]
  python ksim.py selftest           # runs the built-in positive-control test
"""

import argparse
import hashlib
import json
import re
import sys
import io
import time
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOKEN_RE = re.compile(r'[0-9A-Za-z\u0400-\u04FF]+')  # Latin + digits + Cyrillic

# Gates (acceptance criteria from the Counter-Plan)
GATE_KS2_MAX_NONQUOTE = 0        # A1: zero 25+ word matches outside quotes
GATE_KS1_COVERAGE_GE4 = 2.0      # A2: <= 2% of words in >=4-word matches
MIN_N = 4                        # index n-gram size (stricter gate)
GAP_MERGE = 3                    # gap-merge pass: matches <=3 tokens apart merge


def read_docx(path: Path) -> str:
    try:
        import docx  # python-docx
    except ImportError:
        raise SystemExit('python-docx not installed — pip install python-docx')
    d = docx.Document(str(path))
    return '\n\n'.join(p.text for p in d.paragraphs)


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='replace')


def load_paper(path: Path):
    text = read_docx(path) if path.suffix == '.docx' else read_text(path)
    return text


# ------------------------------------------------------------------ quoting
def quote_spans(text: str):
    """Find direct-quote character spans (BG „...“ / «...» / "...")."""
    spans = []
    for pattern in (r'„[^„“]{2,}?“', r'«[^«»]{2,}?»'):
        for m in re.finditer(pattern, text, flags=re.S):
            spans.append((m.start(), m.end()))
    return spans


def char_to_token_marks(text: str, spans):
    """Map quote char-spans to a boolean list per token (is-inside-quote)."""
    marks, pos = [], 0
    tokens = TOKEN_RE.finditer(text)
    for t in tokens:
        inside = any(s <= t.start() and t.end() <= e for s, e in spans)
        marks.append(inside)
        pos += 1
    return marks


# ------------------------------------------------------------------ matching
def build_index(corpus_files):
    """4-gram -> list of (file_id, token_pos). Also keeps token lists per file."""
    index, corpus_tokens = {}, {}
    for fid, (fname, text) in enumerate(corpus_files):
        toks = TOKEN_RE.findall(text.lower())
        corpus_tokens[fid] = (fname, toks)
        for i in range(len(toks) - MIN_N + 1):
            key = hash(tuple(toks[i:i + MIN_N]))
            index.setdefault(key, []).append((fid, i))
    return index, corpus_tokens


def maximal_matches(paper_toks, index, corpus_tokens):
    """Slide 4-word window over paper; extend hits; merge overlaps."""
    hits = []  # (pstart, length, fid, cstart)
    for p in range(len(paper_toks) - MIN_N + 1):
        key = hash(tuple(paper_toks[p:p + MIN_N]))
        for fid, c in index.get(key, []):
            corr_toks = corpus_tokens[fid][1]
            L = MIN_N
            while (p + L < len(paper_toks) and c + L < len(corr_toks)
                   and paper_toks[p + L] == corr_toks[c + L]):
                L += 1
            hits.append((p, L, fid, c))
    # merge overlaps on the paper axis (keep the longest per region)
    hits.sort(key=lambda h: (h[0], -h[1]))
    merged = []
    for h in hits:
        if merged and h[0] <= merged[-1][0] + merged[-1][1] - 1:
            prev = merged[-1]
            if h[0] + h[1] > prev[0] + prev[1]:
                merged[-1] = (prev[0], h[0] + h[1] - prev[0], h[2], 0)
        else:
            merged.append(list(h) if isinstance(h, tuple) else h)
    # gap-merge: two matches <=GAP tokens apart in the paper (same file) are
    # reported as one suspicious merged fragment — sub-threshold matches that
    # sit close together are how paraphrase systems stitch things.
    gap_merged, used = [], set()
    merged.sort(key=lambda h: h[0])
    for i, a in enumerate(merged):
        if i in used:
            continue
        for j in range(i + 1, len(merged)):
            b = merged[j]
            if j in used or b[2] != a[2]:
                continue
            if 0 < b[0] - (a[0] + a[1]) <= GAP_MERGE:
                gap_merged.append((a[0], b[0] + b[1] - a[0], a[2], a[3], True))
                used.add(j)
                break
        else:
            gap_merged.append(a)
    return gap_merged


def coverage(matches, total_words, min_len, quote_marks=None, want_quote=None):
    words = 0
    for m in matches:
        L = m[1]
        if L < min_len:
            continue
        if quote_marks is not None:
            is_q = any(quote_marks[m[0]:m[0] + L])
            if want_quote is not None and is_q != want_quote:
                continue
        words += L
    return round(100.0 * words / max(total_words, 1), 2)


def run(paper_path: Path, corpus_dir: Path):
    t0 = time.time()
    paper_text = load_paper(paper_path)
    paper_toks = [t.lower() for t in TOKEN_RE.findall(paper_text)]
    qmarks = char_to_token_marks(paper_text, quote_spans(paper_text))
    if len(qmarks) != len(paper_toks):
        qmarks = [False] * len(paper_toks)

    corpus_files = []
    for f in sorted(corpus_dir.rglob('*')):
        if f.suffix.lower() in ('.txt', '.docx', '.md') and f.is_file():
            corpus_files.append((f.name, read_docx(f) if f.suffix == '.docx' else read_text(f)))
    if not corpus_files:
        raise SystemExit(f'no corpus files found in {corpus_dir}')

    index, corpus_tokens = build_index(corpus_files)
    matches = maximal_matches(paper_toks, index, corpus_tokens)

    total = len(paper_toks)
    report = {
        'run_id': datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S'),
        'paper_file': str(paper_path),
        'paper_sha256': hashlib.sha256(paper_path.read_bytes()).hexdigest()[:16],
        'total_words': total,
        'corpus_files': [f for f, _ in corpus_files],
        'max_match_words': max([m[1] for m in matches], default=0),
        'ks1': {
            'ge4_pct_nonquote': coverage(matches, total, 4, qmarks, want_quote=False),
            'ge5_pct_nonquote': coverage(matches, total, 5, qmarks, want_quote=False),
            'count_ge4': sum(1 for m in matches if m[1] >= 4),
        },
        'ks2': {
            'ge20_count_total': sum(1 for m in matches if m[1] >= 20),
            'ge25_count_total': sum(1 for m in matches if m[1] >= 25),
            'ge25_count_nonquote': sum(1 for m in matches if m[1] >= 25 and not any(qmarks[m[0]:m[0]+m[1]])),
            'matches': [{'len': m[1], 'paper_word': m[0], 'file': corpus_tokens[m[2]][0],
                         'quote': any(qmarks[m[0]:m[0]+m[1]])}
                        for m in matches if m[1] >= 8],
        },
        'quote_pct': coverage(matches, total, 4, qmarks, want_quote=True),
        'gate_failures': [],
    }
    # ---- gates ----
    if report['ks2']['ge25_count_nonquote'] > GATE_KS2_MAX_NONQUOTE:
        report['gate_failures'].append('A1: КС2 non-quote > 0')
    if report['ks1']['ge4_pct_nonquote'] > GATE_KS1_COVERAGE_GE4:
        report['gate_failures'].append(f"A2: КС1(>=4) non-quote {report['ks1']['ge4_pct_nonquote']}% > {GATE_KS1_COVERAGE_GE4}%")
    report['verdict'] = 'PASS' if not report['gate_failures'] else 'FAIL'
    report['elapsed_sec'] = round(time.time() - t0, 2)
    return report


def selftest():
    """Positive control: a clean draft + a deliberately stolen 30-word sentence.
    The simulator MUST flag the stolen one. If it doesn't — all green results are void."""
    tmp = Path(__import__('tempfile').gettempdir()) / 'ksim_selftest'
    corpus = tmp / 'corpus'
    corpus.mkdir(parents=True, exist_ok=True)
    (corpus / 'source1.txt').write_text(
        '''Втората световна война промени европейския ред. Хелсинкският окончателен акт бе подписан
        на 1 август 1975 година от тридесет и пет държави, включително Съединените щати, Канада и
        всички европейски държави освен Албания и Андора, и постави началото на процеса на
        сближаването между Изтока и Запада в Европа. Според историците този документ имал
        огромно значение за по-късните промени.''', encoding='utf-8')
    paper = tmp / 'paper.txt'
    paper.write_text(
        '''Разпадът на СССР промени света. Много учени смятат, че договорите от този период имат
        специална роля. „Хелсинкският окончателен акт бе подписан на 1 август 1975 година от
        тридесет и пет държави, включително Съединените щати, Канада и всички европейски държави
        освен Албания и Андора“ — така се създаде новата дипломатическа рамка. Други смятат
        противоположното и това е интересно.''', encoding='utf-8')
    rep = run(paper, corpus)
    flagged = rep['ks2']['ge25_count_total'] + rep['ks2']['ge20_count_total']
    ok = flagged >= 1
    print(f"KSIM SELFTEST — positive control")
    print(f"  max match: {rep['max_match_words']} words | КС2(>=25 total): "
          f"{rep['ks2']['ge25_count_total']} | КС2(>=20 total): {rep['ks2']['ge20_count_total']}")
    for m in rep['ks2']['matches']:
        print(f"  match: {m['len']}w @ paper word {m['paper_word']} in {m['file']} quote={m['quote']}")
    print('  verdict:', 'WORKS — stolen sentence flagged' if ok else 'BROKEN — harness is void!')
    return ok


if __name__ == '__main__':
    if 'selftest' in sys.argv:
        ok = selftest()
        sys.exit(0 if ok else 1)
    ap = argparse.ArgumentParser()
    ap.add_argument('paper', help='paper .docx or .txt')
    ap.add_argument('corpus', help='corpus dir')
    ap.add_argument('--json', help='write JSON report here')
    a = ap.parse_args()
    rep = run(Path(a.paper), Path(a.corpus))
    print(json.dumps(rep, ensure_ascii=False, indent=1)[:4000])
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'-> saved {a.json}')
    print('VERDICT:', rep['verdict'], ('| FAIL: ' + '; '.join(rep['gate_failures'])) if rep['gate_failures'] else '')

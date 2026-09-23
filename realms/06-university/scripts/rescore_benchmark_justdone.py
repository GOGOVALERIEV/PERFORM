"""Rescore every benchmark paper with JustDone (free sharp referee)."""
import subprocess, sys, io
from pathlib import Path
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print = __import__('functools').partial(print, flush=True)

REALM = Path(__file__).resolve().parents[1]
BATCH = REALM / 'state' / 'benchmark' / 'batch1'
OUT = REALM / 'state' / 'benchmark' / 'justdone-scores.txt'

results = []
for paper_dir in sorted(BATCH.iterdir()):
    if not paper_dir.is_dir():
        continue
    final = paper_dir / 'p2-style-pass.txt'
    if not final.exists():
        final = paper_dir / 'p2-chain.txt'
    if not final.exists():
        print(f'{paper_dir.name}: no final file — skip')
        continue
    r = subprocess.run([sys.executable, str(REALM / 'scripts' / 'battery_justdone.py'), str(final), '--words', '300'],
                       capture_output=True, text=True, timeout=420, encoding='utf-8', errors='replace')
    m = __import__('re').search(r'JustDone AI%: (\d{1,3}(?:\.\d+)?)', r.stdout + r.stderr)
    score = m.group(1) if m else 'n/a'
    results.append((paper_dir.name, score))
    print(f'{paper_dir.name}: {score}%')

OUT.write_text('\n'.join(f'{n}\t{s}%' for n, s in results) + '\n', encoding='utf-8')
print('\n=== FINAL JUSTDONE STANDINGS (saved to', OUT, ') ===')
for n, s in sorted(results, key=lambda x: float(x[1]) if x[1] != 'n/a' else 999):
    print(f'  {s:>6}%  {n}')

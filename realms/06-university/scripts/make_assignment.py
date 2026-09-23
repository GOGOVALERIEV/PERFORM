"""
make_assignment.py — EVIDENCE-LAYER SCAFFOLDING (counter4 §3)
Creates the per-assignment folder structure that doubles as the authorship
evidence pack. Every item answers an oral-defense question later.

USAGE:
  python make_assignment.py "Политология" "referat-1-politicheski-rezhimi"
"""

import sys
import io
from datetime import date
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]

if len(sys.argv) != 3:
    raise SystemExit('usage: python make_assignment.py "<course>" "<assignment-slug>"')

course, slug = sys.argv[1], sys.argv[2]
base = REALM / 'courses' / course / slug
folders = ['00-notes', '02-versions', '03-selfcheck', '04-final', '05-submission']
for d in folders:
    (base / d).mkdir(parents=True, exist_ok=True)

outline = base / '01-outline.md'
if not outline.exists():
    outline.write_text(
        f'# OUTLINE — {slug}\n'
        f'course: {course}\n'
        f'date_created: {date.today().isoformat()}\n'
        f'thesis: (one sentence — my claim)\n\n'
        f'## Sections (thesis per section, source per section)\n'
        f'1. \n\n'
        f'## Dial settings (Duo protocol: which of the 8 I picked)\n'
        f'- thesis angle: \n- structure: \n- register: \n- case study: \n\n'
        f'## Limitations (3 bullets, for the oral defense)\n- \n',
        encoding='utf-8')

(battery := REALM / 'research' / 'test-runs').mkdir(parents=True, exist_ok=True)
log = battery / 'battery-log.md'
if not log.exists():
    log.write_text(
        '# TEST BATTERY LOG\n\n'
        '| date | tool | file/ver | similarity % | AI % | notes | verdict |\n'
        '|---|---|---|---|---|---|---|\n',
        encoding='utf-8')

print(f'created: {base}')
print(f'  00-notes/  01-outline.md  02-versions/  03-selfcheck/  04-final/  05-submission/')
print(f'battery log ready: {log}')
print('\nNEXT STEPS (counter4 §2):')
print(' 1. Draft versions go to 02-versions/ — each SAVED IN WORD (Real-Editor Rebirth)')
print(' 2. plag.bg report screenshot -> 03-selfcheck/')
print(' 3. ksim + stylecheck PASS before anything leaves the machine')
print(' 4. Final .docx -> Word -> Export PDF -> 04-final/ (PDF from Word, never print-to-PDF)')

"""
battery_zerogpt.py — ZeroGPT external battery (Level 2, CANARY)
===============================================================
The only detector that still scans WITHOUT an account (verified 2026-09-18).
Role per counter5: CANARY — noisy, never a gate. A pass here is weak comfort;
a fail here is a strong alarm (three tools agreeing = rewrite).

Extracts: AI % (gauge), human %, verdict line. Screenshot + battery log row.

USAGE:
  python battery_zerogpt.py <paper.txt|docx> [--words 400]
"""

import argparse
import io
import re
import sys
from datetime import date
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
LOG = REALM / 'research' / 'test-runs' / 'battery-log.md'
SHOTS = REALM / 'research' / 'test-runs' / 'screenshots'
SHOTS.mkdir(parents=True, exist_ok=True)
URL = 'https://www.zerogpt.com/'


def load_text(path: Path) -> str:
    if path.suffix == '.docx':
        import docx
        return '\n\n'.join(p.text for p in docx.Document(str(path)).paragraphs)
    return path.read_text(encoding='utf-8', errors='replace')


def log_row(file_name, ai_pct, note, verdict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text('| date | tool | file/ver | similarity % | AI % | notes | verdict |\n|---|---|---|---|---|---|---|\n', encoding='utf-8')
    LOG.open('a', encoding='utf-8').write(
        f'| {date.today()} | ZeroGPT (canary, web) | {file_name} | - | {ai_pct} | {note} | {verdict} |\n')


def run(text_path: Path, words: int):
    text = load_text(text_path)
    # cut bibliography before sampling (don't feed references to a detector)
    m = re.search(r'^\s*Библиография', text, re.MULTILINE)
    if m:
        text = text[:m.start()]
    sample = ' '.join(text.split()[:words])
    print(f'sampling {len(sample.split())} words from {text_path.name}')

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=False)
        pg = b.new_context(viewport={'width': 1400, 'height': 950}).new_page()
        pg.goto(URL, timeout=60000, wait_until='domcontentloaded')
        pg.wait_for_timeout(6000)
        ta = pg.query_selector('textarea')
        if not ta:
            raise SystemExit('no textarea — site changed, re-probe')
        ta.fill(sample)
        pg.wait_for_timeout(1500)
        clicked = False
        for el in pg.query_selector_all('button'):
            t = (el.inner_text() or '').strip().lower()
            if 'detect text' in t:
                el.click()
                clicked = True
                break
        if not clicked:
            raise SystemExit('no Detect Text button — site changed, re-probe')
        pg.wait_for_timeout(25000)
        body = pg.inner_text('body')

        # parse: gauge "X% AI GPT*" + verdict line
        ai_pct = None
        m = re.search(r'(\d{1,3}(?:\.\d+)?)\s*%\s*AI\s*GPT', body, re.IGNORECASE)
        if m:
            ai_pct = m.group(1)
        verdict_line = ''
        m2 = re.search(r'Your Text[^.]*\.', body, re.IGNORECASE)
        if m2:
            verdict_line = m2.group(0)[:90]
        human_pct = None
        m3 = re.search(r'(\d{1,3}(?:\.\d+)?)\s*%\s*human', body, re.IGNORECASE)
        if m3:
            human_pct = m3.group(1)
        shot = SHOTS / f'zerogpt-{text_path.stem}-{date.today()}.png'
        pg.screenshot(path=str(shot), full_page=False)
        b.close()

    print(f'AI GPT*: {ai_pct}% | human: {human_pct}% | verdict: {verdict_line}')
    print(f'screenshot: {shot}')
    # CANARY rules: no pass gate; alarm only if it screams AI
    if ai_pct is not None:
        v = 'ALARM' if float(ai_pct) >= 50 else 'clean (canary)'
        log_row(text_path.name, f'{ai_pct}%', f'canary; human={human_pct}%', v)
    else:
        log_row(text_path.name, 'n/a', 'score not parsed — check screenshot', 'NO-SCORE')
    return ai_pct, human_pct


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--words', type=int, default=400)
    a = ap.parse_args()
    run(Path(a.file), a.words)

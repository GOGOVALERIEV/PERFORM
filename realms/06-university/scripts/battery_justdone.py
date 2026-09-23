"""
battery_justdone.py — JustDone external battery (the FREE sharp referee)
=========================================================================
No login needed, verdict visible free, Bulgarian supported.
Calibrated: known-AI drill text scored 98% here vs 97% GPTZero (2026-09-19).
Role: PRIMARY AI% judge for the benchmark (GPTZero is quota-gated).

USAGE:
  python battery_justdone.py <paper.txt|docx> [--words 300]
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


def load_text(path):
    if path.suffix == '.docx':
        import docx
        return chr(10).join(p.text for p in docx.Document(str(path)).paragraphs)
    return path.read_text(encoding='utf-8', errors='replace')


def log_row(file_name, ai_pct, note, verdict):
    header = '| date | tool | file/ver | similarity % | AI % | notes | verdict |\n|---|---|---|---|---|---|---|\n'
    if not LOG.exists():
        LOG.write_text(header, encoding='utf-8')
    LOG.open('a', encoding='utf-8').write(
        f'| {date.today()} | JustDone (free, web) | {file_name} | - | {ai_pct} | {note} | {verdict} |\n')


def run(path, words):
    text = load_text(path)
    m = re.search(r'^\s*Библиография', text, re.MULTILINE)
    if m:
        text = text[:m.start()]
    sample = ' '.join(text.split()[:words])
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={'width': 1400, 'height': 1100})
        pg.goto('https://justdone.com/ai-detector', timeout=60000, wait_until='domcontentloaded')
        pg.wait_for_timeout(8000)
        try: pg.click('button:has-text("Reject All")', timeout=4000)
        except Exception: pass
        pg.click('[class*="input"], [class*="Input"]', timeout=10000)
        pg.keyboard.insert_text(sample)
        pg.wait_for_timeout(2500)
        pg.click('button:has-text("Check for AI Content")', timeout=8000)
        found = None
        for i in range(36):
            pg.wait_for_timeout(5000)
            try: pg.click('button:has-text("Reject All")', timeout=1200)
            except Exception: pass
            body = pg.inner_text('body')
            m = re.search(r'Your Text[^%]{0,200}?(\d{1,3}(?:\.\d+)?)\s*%\s*AI', body, re.IGNORECASE)
            m2 = re.search(r'(\d{1,3}(?:\.\d+)?)\s*%\s*AI\s*content', body, re.IGNORECASE)
            if m or m2:
                found = (m or m2).group(1)
                break
        shot = SHOTS / f'justdone-{path.stem}-{date.today()}.png'
        pg.screenshot(path=str(shot))
        b.close()
    print(f'JustDone AI%: {found}')
    print(f'screenshot: {shot}')
    if found:
        v = 'ALARM' if float(found) >= 50 else ('REVIEW' if float(found) >= 25 else 'PASS')
        log_row(path.name, f'{found}%', 'free sharp referee; calibrated vs GPTZero 97%', v)
    else:
        log_row(path.name, 'n/a', 'score not parsed — see screenshot', 'NO-SCORE')
    return found


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--words', type=int, default=300)
    a = ap.parse_args()
    run(Path(a.file), a.words)

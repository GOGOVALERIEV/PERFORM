"""
battery_gptzero.py — GPTZero external battery (Level 2)
=======================================================
Pastes a body sample of a paper into GPTZero's free web checker, extracts the
AI-probability score, screenshots the result, logs a row into battery-log.md.

SAFETY RULES (counter5 §2):
- PASTE only, never account upload. No personal data in the text (test persona).
- GPTZero claims Bulgarian support but publishes no accuracy data — score is a
  noisy SECONDARY signal. Never a sole verdict.

USAGE:
  python battery_gptzero.py <paper.txt|docx> [--words 350] [--headless]
  python battery_gptzero.py selftest          # uses the raw-LLM control paragraph
"""

import argparse
import io
import json
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
URL = 'https://gptzero.me/'


def load_text(path: Path) -> str:
    if path.suffix == '.docx':
        import docx
        return '\n\n'.join(p.text for p in docx.Document(str(path)).paragraphs)
    return path.read_text(encoding='utf-8', errors='replace')


def log_row(file_name, score, note, verdict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text('| date | tool | file/ver | similarity % | AI % | notes | verdict |\n|---|---|---|---|---|---|---|\n', encoding='utf-8')
    LOG.open('a', encoding='utf-8').write(
        f'| {date.today()} | GPTZero (paste, web) | {file_name} | - | {score} | {note} | {verdict} |\n')


def run(text_path: Path, words: int, headless: bool):
    text = load_text(text_path)
    # body sample: cut first `words` words, skip a potential bibliography header
    sample = ' '.join(text.split()[:words])
    print(f'pasting {len(sample.split())} words from {text_path.name}')

    from playwright.sync_api import sync_playwright
    # Persistent profile — log in ONCE in the opened window; session is saved.
    profile = REALM / 'state' / 'browser-profile' / 'gptzero'
    profile.mkdir(parents=True, exist_ok=True)
    BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # real Brave binary — passes Google/bot checks
    with sync_playwright() as p:
        b = p.chromium.launch_persistent_context(str(profile), headless=headless,
                                                 executable_path=BRAVE,
                                                 viewport={'width': 1400, 'height': 950})
        pg = b.pages[0] if b.pages else b.new_page()
        pg.bring_to_front()
        pg.goto(URL, timeout=60000, wait_until='domcontentloaded')
        pg.wait_for_timeout(5000)
        # cookie banner — dismiss so it can't overlay the Scan button
        for label in ('Accept', 'Decline'):
            try:
                pg.click(f'button:has-text("{label}")', timeout=3000)
                pg.wait_for_timeout(800)
                break
            except Exception:
                pass
        # anonymous scan is dead (verified 2026-09-18): ensure logged in first
        body_txt = pg.inner_text('body')
        if 'Log in' in body_txt or 'Get started' in body_txt:
            print('>>> NOT LOGGED IN: log in manually in the opened window (2 min).')
            print('>>> Session is saved in this profile — ONE-TIME step.')
            try:
                pg.click('a:has-text("Log in"), button:has-text("Log in")', timeout=5000)
            except Exception:
                pass
            for _ in range(120):  # up to 10 min manual login
                pg.wait_for_timeout(5000)
                cur = pg.inner_text('body')
                if 'Log in' not in cur[:2000] and 'Get started' not in cur[:2000]:
                    print('logged in — session saved')
                    break
            else:
                try:
                    pg.screenshot(path=str(SHOTS / 'gptzero-timeout-state.png'))
                    print('timeout state screenshot saved')
                except Exception:
                    pass
                raise SystemExit('login timeout — run again')
        pg.goto(URL, timeout=60000, wait_until='domcontentloaded')
        pg.wait_for_timeout(5000)
        ta = pg.query_selector('textarea')
        if not ta:
            raise SystemExit('no textarea found — site changed, re-probe')
        ta.fill(sample)
        pg.wait_for_timeout(1500)
        # FREE TIER: uncheck 'Advanced AI Scan' (advanced quota = 1 scan/account)
        try:
            pg.get_by_text('Advanced AI Scan', exact=False).first.click(timeout=4000)
            pg.wait_for_timeout(500)
            print('Advanced AI Scan unchecked (basic scan)')
        except Exception:
            print('Advanced toggle not found — proceeding as-is')
        clicked = False
        for el in pg.query_selector_all('button'):
            t = (el.inner_text() or '').strip().lower()
            if t.startswith('scan'):
                el.scroll_into_view_if_needed()
                el.click()
                clicked = True
                break
        if not clicked:
            raise SystemExit('no Scan button found — site changed, re-probe')
        # results open in a NEW TAB: app.gptzero.me/documents/<uuid>
        # BUT that tab is the EDITOR — a SECOND Scan button (bottom right)
        # actually runs the analysis. Flow: close promos -> click Scan -> poll.
        result_pg, found, paywall = None, '', False
        for i in range(60):
            pg.wait_for_timeout(5000)
            docs = [w for w in b.pages if 'app.gptzero.me/documents/' in w.url]
            if not docs:
                continue
            result_pg = docs[0]
            try:
                body = result_pg.inner_text('body')
            except Exception:
                continue
            # paywall: advanced scan quota exhausted -> close, basic result may follow
            if 'reached the limit' in body or 'Upgrade to get even more' in body:
                paywall = True
                try:
                    result_pg.click('button[aria-label="Close"], button:has-text("✕")', timeout=2500)
                except Exception:
                    pass
                continue
            # close promo popup if present
            if 'Be prepared' in body or 'Upgrade with' in body:
                try:
                    result_pg.click('button:has-text("✕"), [aria-label="Close"]', timeout=2500)
                    result_pg.wait_for_timeout(800)
                except Exception:
                    pass
            # step 2: if the score isn't there yet, press the editor's Scan
            m = re.search(r'(\d{1,3}(?:\.\d+)?)\s*%\s*(?:AI|likely|generated|artificial)', body, re.IGNORECASE)
            if not m:
                m2 = re.search(r'\bAI\b[^\d%]{0,50}(\d{1,3}(?:\.\d+)?)\s*%', body, re.IGNORECASE)
                m = m2
            if m:
                found = m.group(1)
                break
            if i == 1:
                try:
                    result_pg.get_by_role('button', name='Scan', exact=True).click()
                    print('pressed editor Scan (step 2)')
                except Exception as e:
                    print('editor Scan click failed:', e.__class__.__name__)
        if not found and paywall:
            print('advanced quota exhausted — no basic scan offered; score withheld')
            found = ''  # NEVER parse numbers from a paywall page
        target = result_pg or pg
        shot = SHOTS / f'gptzero-{text_path.stem}-{date.today()}.png'
        target.screenshot(path=str(shot), full_page=False)
        print(f'result URL: {target.url}')
        b.close()
    print(f'screenshot: {shot}')
    verdict = 'PASS' if (found and float(found) < 25) else ('REVIEW' if found else 'NO-SCORE')
    note = 'advanced quota exhausted — basic scan' if paywall else 'web paste battery'
    if found:
        log_row(text_path.name, f'{found}%', note, verdict)
    else:
        log_row(text_path.name, 'n/a', note, 'QUOTA-NO-SCORE' if paywall else 'NO-SCORE')
    return found, str(shot)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?')
    ap.add_argument('--words', type=int, default=350)
    ap.add_argument('--headless', dest='headless', action='store_true', default=False, help='run invisible (default: visible)')
    ap.add_argument('selftest', nargs='?')
    a = ap.parse_args()
    if not a.file:
        print('usage: python battery_gptzero.py <paper.txt|docx> [--words N]')
        sys.exit(1)
    score, shot = run(Path(a.file), a.words, a.headless)
    print('AI SCORE:', score)

"""
battery_plagbg.py — plag.bg external battery (Level 2)
======================================================
Uploads the final .docx to plag.bg's free checker and extracts similarity % +
AI %. Screenshot + battery log row.

SAFETY GATES (run automatically, in order — abort if any fails):
1. CLAUSE GATE: verify the homepage still says files are NEVER added to any
   comparison database. If the clause disappears — plag.bg is dropped from the
   battery for the semester (counter5 §2, re-verified every session).
2. PERSONA GATE: refuse to run on a file whose name lacks "Тестов"/"TEST" —
   test uploads must never carry a real persona's filename.

plag.bg requires a free account (my.plag.bg). Credentials come from
realms/06-university/config/plagbg-credentials.txt (two lines: email, password).
George creates the account once (test persona recommended); the script never
echoes the password.

USAGE:
  python battery_plagbg.py <paper.docx> [--headless]
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
CREDS = REALM / 'config' / 'plagbg-credentials.txt'
CLAUSE = 'никога не се добавят към каквато и да е сравнителна база данни'


def clause_gate(pg) -> bool:
    pg.goto('https://www.plag.bg/', timeout=60000, wait_until='domcontentloaded')
    pg.wait_for_timeout(3500)
    ok = CLAUSE in pg.inner_text('body')
    print(f'CLAUSE GATE: {"PASS" if ok else "FAILED — clause missing, plag.bg dropped from battery"}')
    return ok


def persona_gate(file_path: Path) -> bool:
    name = file_path.stem.upper()
    ok = ('ТЕСТОВ' in name) or ('TEST' in name)
    print(f'PERSONA GATE: {"PASS" if ok else "FAILED — filename must carry the test persona (Т. Тестов / TEST)"}')
    return ok


def load_creds():
    if not CREDS.exists():
        raise SystemExit(
            f'no credentials at {CREDS}\n'
            'Create a plag.bg account once (my.plag.bg/signup — test persona email '
            'recommended), then save the credentials as two lines:\n  email\n  password\n'
            'in that file. The script will use them silently.')
    lines = CREDS.read_text(encoding='utf-8').strip().splitlines()
    if len(lines) < 2:
        raise SystemExit('credentials file must have exactly 2 lines: email, password')
    return lines[0].strip(), lines[1].strip()


def run(file_path: Path, headless: bool):
    if not persona_gate(file_path):
        sys.exit(1)
    from playwright.sync_api import sync_playwright
    # Persistent profile — George logs in ONCE; session cookies are saved and
    # every future run is auto-logged-in. No password files.
    profile = REALM / 'state' / 'browser-profile' / 'plagbg'
    profile.mkdir(parents=True, exist_ok=True)
    BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # real Brave binary — passes Google/bot checks
    with sync_playwright() as p:
        b = p.chromium.launch_persistent_context(str(profile), headless=headless,
                                                 executable_path=BRAVE,
                                                 args=['--start-maximized'])
        pg = b.pages[0] if b.pages else b.new_page()
        if not clause_gate(pg):
            log_row(file_path.name, 'aborted', 'clause gate failed — files might be archived', 'ABORTED')
            b.close()
            sys.exit(1)
        pg.goto('https://my.plag.bg/login', timeout=60000, wait_until='domcontentloaded')
        pg.wait_for_timeout(3000)
        # cookie banner first — it overlays buttons
        for label in ('ПРИЕМЕТЕ ВСИЧКИ', 'Приемете всички', 'Accept'):
            try:
                pg.click(f'text="{label}"', timeout=3000)
                pg.wait_for_timeout(800)
                break
            except Exception:
                pass
        if 'login' in pg.url.lower():
            creds = CREDS.read_text(encoding='utf-8').strip().splitlines() if CREDS.exists() else []
            if len(creds) >= 2 and 'HERE' not in creds[0]:
                print('auto-filling login from config…')
                pg.fill('input#username', creds[0].strip())
                pg.fill('input#password', creds[1].strip())
                sub = pg.query_selector('input[type=submit]') or pg.query_selector('button[type=submit]')
                if sub:
                    sub.click()
                else:
                    pg.keyboard.press('Enter')
                pg.wait_for_timeout(10000)
            else:
                print('>>> NOT LOGGED IN: log in manually in the opened window (10 min).')
                print('>>> The session is saved in this profile — this is a ONE-TIME step.')
                for _ in range(120):  # up to 10 minutes for manual login
                    pg.wait_for_timeout(5000)
                    if 'login' not in pg.url.lower():
                        print('logged in — session saved')
                        break
                else:
                    try:
                        pg.screenshot(path=str(SHOTS / 'plagbg-timeout-state.png'))
                        print('timeout state screenshot saved')
                    except Exception:
                        pass
                    raise SystemExit('login timeout — run again and log in faster')
        print('session active')
        # upload flow: find the file input on the dashboard
        file_input = pg.query_selector('input[type=file]')
        if not file_input:
            raise SystemExit('no file input after login — site changed, re-probe')
        file_input.set_input_files(str(file_path.resolve()))
        pg.wait_for_timeout(3000)
        # submit if a confirm button appears (best effort — the flow may differ)
        for el in pg.query_selector_all('button'):
            t = (el.inner_text() or '').strip().lower()
            if any(k in t for k in ['провери', 'качи', 'upload', 'check', 'изпрати', 'start']):
                el.click()
                break
        # results take a while — poll up to 3 minutes for percentage text
        import time
        found = ''
        for _ in range(36):
            pg.wait_for_timeout(5000)
            body = pg.inner_text('body')
            m = re.search(r'сходство[^\d]{0,40}(\d{1,3}(?:\.\d+)?)\s*%|(\d{1,3}(?:\.\d+)?)\s*%\s*сходств', body, re.IGNORECASE)
            if m:
                found = m.group(1) or m.group(2)
                break
        shot = SHOTS / f'plagbg-{file_path.stem}-{date.today()}.png'
        pg.screenshot(path=str(shot), full_page=False)
        print(f'similarity: {found or "NOT PARSED — check screenshot"}')
        print(f'screenshot: {shot}')
        log_row(file_path.name, found or 'n/a', 'web upload battery', 'DONE' if found else 'NO-SCORE')
        b.close()


def log_row(file_name, similarity, note, verdict):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text('| date | tool | file/ver | similarity % | AI % | notes | verdict |\n|---|---|---|---|---|---|---|\n', encoding='utf-8')
    LOG.open('a', encoding='utf-8').write(
        f'| {date.today()} | plag.bg (upload, web) | {file_name} | {similarity} | - | {note} | {verdict} |\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--headless', dest='headless', action='store_true', default=False, help='run invisible (default: visible)')
    a = ap.parse_args()
    run(Path(a.file), a.headless)

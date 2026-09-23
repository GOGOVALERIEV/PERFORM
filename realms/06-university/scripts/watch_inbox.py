"""
UNIVERSITY INBOX WATCHER — Module 1 of the University System
============================================================
The front door of the pipeline. Scans Gmail for university-related
emails (teacher tasks, deadlines, attachments), scores them by
relevance, parses deadlines, and saves a clean task list to state/.

WHAT IT DOES (the loop):
  1. Ask Gmail: "give me every email from the last N days"
  2. For each email, pull: who sent it, subject, snippet, attachments
  3. SCORE it — the more university words/teachers/courses it hits,
     the more likely it's a real task (like a spam filter in reverse)
  4. Find DATES in the text (deadline candidates: 25.10, 1.12.2026...)
  5. Save everything to state/inbox-tasks.json + remember what we
     already saw (state/seen-ids.json) so reruns only show NEW emails

USAGE:
  python watch_inbox.py               # scan last 14 days, new emails only
  python watch_inbox.py --days 90     # scan last 90 days
  python watch_inbox.py --all         # ignore memory, rescore everything
  python watch_inbox.py --min 1       # lower the relevance bar (show weak hits)

WHY SCORING INSTEAD OF A HARD FILTER?
  Teachers email from personal accounts (gmail, abv.bg) — we can't
  just filter "is from swu.bg". A score catches the personal email
  that says "Здравейте, домашното по Политология е до 15.10..." while
  ignoring random newsletters. This is the same idea anti-spam uses,
  but pointed the other way.
"""

import argparse
import json
import re
import sys
import io
import time
from datetime import datetime, timezone
from pathlib import Path

# Windows console safety: force UTF-8 so Cyrillic never crashes printing.
# (Under pythonw the streams are None — same guard as google_helper.)
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr is not None and (getattr(sys.stderr, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Make PERFORM/scripts importable — google_helper lives there and auto-finds config/.
PERFORM_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PERFORM_ROOT / 'scripts'))
from google_helper import get_gmail  # noqa: E402

# ---------------------------------------------------------------------------
# Folder layout — everything this module writes lives inside its own realm.
# ---------------------------------------------------------------------------
REALM = Path(__file__).resolve().parents[1]
STATE_DIR = REALM / 'state'
SEEN_FILE = STATE_DIR / 'seen-ids.json'
TASKS_FILE = STATE_DIR / 'inbox-tasks.json'

# ---------------------------------------------------------------------------
# THE WATCHLIST — knowledge distilled from the official schedule
# (realms/06-university/research/university-research.md).
# When a teacher changes or a new subject appears in 2nd semester,
# this is the ONE place to update.
# ---------------------------------------------------------------------------
TEACHERS = [
    'Георгиева', 'Попов', 'Тюлеков', 'Кочев',
    'Хаджипетрова', 'Лачова', 'Стоилова', 'Лалев',
]

COURSES = [
    'английски език', 'политология',
    'история на международните отношения',
    'глобализъм', 'френски език',
    'политическа история на европа',
]

# Words that mean "this is an action item", weighted by how strongly they
# signal a TASK (not just university chatter). Higher = louder signal.
TASK_KEYWORDS = {
    'домашно': 3, 'домашната': 3, ' homework': 3,
    'реферат': 3, 'есе': 2, 'доклад': 3,
    'презентация': 3, 'presentation': 3,
    'изпит': 3, 'сесия': 2, 'колоквиум': 3,
    'тест': 2, 'контролно': 3,
    'дедлайн': 3, 'deadline': 3, 'срок': 2,
    'задача': 2, 'задание': 3, 'курсова': 3,
    'оценяване': 2, 'оценка': 2, 'точки': 1,
    'задължително': 2, 'пишете': 2, 'подгответе': 3,
    'изпратете': 3, 'качете': 3, 'предайте': 3,
}

# Dates like 25.10 / 1.12.2026 / 05-01 / 25/10/26 — BG convention day first.
# After matching we VALIDATE: day 1-31, month 1-12. Otherwise prices like
# "48.90" sneak in as fake 'dates'.
DATE_RE = re.compile(r'\b(\d{1,2})\s*([./-])\s*(\d{1,2})(?:\s*[./-]\s*(\d{2,4}))?\b')
# "до 15.10", "крайна дата", "до X.Y" — a deadline marker right before a date.
DEADLINE_HINT_RE = re.compile(r'(до|крайн\w+|дедлайн|deadline|срок)\s*[:\-]?\s*\d{1,2}\s*[./-]', re.IGNORECASE)


def gmail_get(service, **kwargs):
    """
    Fetch one message from Gmail, politely.
    APIs rate-limit bursts (Gmail: quota per minute per user), so we:
      1. sleep a little between EVERY request (throttle),
      2. on a 403/429 'slow down' error, back off exponentially
         (1s → 2s → 4s → 8s) and try again — the classic politeness dance.
    """
    delay = 1.0
    for attempt in range(5):
        time.sleep(0.15)  # throttle: ~6-7 requests/sec max
        try:
            return service.users().messages().get(**kwargs).execute()
        except Exception as e:
            if '403' in str(e) or '429' in str(e):
                print(f'      rate-limited, backing off {delay:.0f}s...')
                time.sleep(delay)
                delay *= 2
            else:
                raise
    raise RuntimeError('Gmail kept rate-limiting us — try again later')


# Pre-built word-boundary patterns — one regex per keyword so that short
# words like 'есе' only match as WHOLE words (\b = word boundary).
TASK_PATTERNS = [
    (re.compile(r'\b' + re.escape(w.strip()) + r'\b', re.IGNORECASE), weight)
    for w, weight in TASK_KEYWORDS.items()
]


def load_json(path: Path, default):
    """Read a JSON file, or return the default if it doesn't exist yet."""
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return default


def msg_headers(payload):
    """Flatten the Gmail payload's header list into a simple dict."""
    return {h['name'].lower(): h['value'] for h in payload.get('headers', [])}


def walk_text_parts(payload):
    """
    Gmail 'full' format returns a tree of MIME parts. This walks it and
    returns (plain_text, attachments). We only decode plain text —
    HTML bodies carry the same words and this keeps things simple.
    """
    text, attachments = [], []

    def walk(part):
        mime = part.get('mimeType', '')
        if 'attachment' in part:  # attachmentId present = real file
            attachments.append({
                'filename': part.get('filename', ''),
                'id': part['body'].get('attachmentId', ''),
                'size': part['body'].get('size', 0),
            })
        elif mime == 'text/plain':
            data = part.get('body', {}).get('data', '')
            if data:
                # Gmail sends base64url-encoded bodies — this decodes them.
                text.append(__import__('base64').urlsafe_b64decode(data).decode('utf-8', errors='replace'))
        for child in part.get('parts', []):
            walk(child)

    walk(payload)
    return '\n'.join(text), attachments


def score_email(sender, subject, snippet, body):
    """
    Return (score, matched_signals). Score = how 'university-task-like'
    this email is. Signals explain WHY it scored — so the report shows
    its reasoning instead of a magic number.
    """
    haystack = f'{sender} {subject} {snippet} {body}'.lower()
    signals = []
    score = 0

    for teacher in TEACHERS:
        if teacher.lower() in haystack:
            score += 5
            signals.append(f'teacher:{teacher}')
    for course in COURSES:
        if course in haystack:
            score += 3
            signals.append(f'course:{course}')
    for pattern, weight in TASK_PATTERNS:
        if pattern.search(haystack):
            score += weight
            signals.append(f'task:{pattern.pattern[2:-2]}')
    if 'swu.bg' in sender.lower() or '@swu' in sender.lower():
        score += 4
        signals.append('domain:swu.bg')

    return score, signals


def find_deadlines(text):
    """
    Find date-like strings; mark ones near a deadline word as 'strong'.
    Weak = any date (might be a lecture date, exam date, whatever).
    Strong = date right after 'до/дедлайн/срок/deadline' → almost
    certainly THE deadline.
    """
    found = []
    for m in DATE_RE.finditer(text):
        day, month = int(m.group(1)), int(m.group(3))
        if not (1 <= day <= 31 and 1 <= month <= 12):
            continue  # not a real calendar date (e.g. '48.90' from a price)
        date_str = m.group(0)
        is_strong = bool(DEADLINE_HINT_RE.search(text[max(0, m.start() - 30):m.end() + 5]))
        found.append({'date': date_str, 'strong': is_strong})
    return found


def scan(days=14, min_score=4, rescan_all=False):
    """Main loop: query Gmail → score → dedupe → save → report."""
    service = get_gmail()
    seen = load_json(SEEN_FILE, {})          # {message_id: date_first_seen}
    tasks = load_json(TASKS_FILE, [])        # list of task dicts

    known_ids = {t['id'] for t in tasks}
    query = f'newer_than:{days}d'
    print(f'=== UNIVERSITY INBOX WATCHER ===')
    print(f'Query: "{query}" | min score: {min_score} | known tasks: {len(tasks)}')

    resp = service.users().messages().list(
        userId='me', q=query, maxResults=200).execute()
    messages = resp.get('messages', [])
    print(f'Emails found: {len(messages)}')

    new_tasks, new_hits = [], 0
    for msg in messages:
        mid = msg['id']
        # Re-scan everything with --all; otherwise skip mails we already scored.
        if not rescan_all and mid in seen:
            continue
        full = gmail_get(service, userId='me', id=mid, format='full')
        headers = msg_headers(full['payload'])
        body, attachments = walk_text_parts(full['payload'])
        sender = headers.get('from', '')
        subject = headers.get('subject', '(no subject)')
        snippet = full.get('snippet', '')

        score, signals = score_email(sender, subject, snippet, body)
        seen[mid] = datetime.now(timezone.utc).isoformat()

        if score >= min_score:
            new_hits += 1
            deadlines = find_deadlines(f'{subject} {snippet} {body[:3000]}')
            task = {
                'id': mid,
                'score': score,
                'from': sender,
                'subject': subject,
                'date': headers.get('date', ''),
                'signals': signals[:12],
                'deadlines': deadlines[:6],
                'attachments': [a['filename'] for a in attachments],
                'attachment_ids': [a['id'] for a in attachments],
                'snippet': snippet[:300],
            }
            new_tasks.append(task)
            if mid not in known_ids:
                tasks.append(task)

        # Save progress incrementally — a crash halfway doesn't lose memory.
        SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        SEEN_FILE.write_text(
            json.dumps(seen, ensure_ascii=False, indent=1), encoding='utf-8')

    TASKS_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=1), encoding='utf-8')

    # ----- Report ------------------------------------------------------
    print(f'\nRelevant emails (score >= {min_score}): {new_hits}')
    if new_tasks:
        for t in sorted(new_tasks, key=lambda x: -x['score']):
            dl = ', '.join(d['date'] + ('*' if d['strong'] else '')
                           for d in t['deadlines']) or '—'
            att = f' | files: {", ".join(t["attachments"])}' if t['attachments'] else ''
            print(f'\n[{t["score"]:3d}] {t["subject"]}')
            print(f'      from: {t["from"]}')
            print(f'      deadlines: {dl}{att}')
            print(f'      why: {", ".join(t["signals"][:6])}')
    else:
        print('Nothing above threshold. (Normal before the semester starts.)')
    print(f'\nTask list: {TASKS_FILE} ({len(tasks)} total)')
    return new_tasks


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='University inbox watcher')
    ap.add_argument('--days', type=int, default=14, help='how far back to scan')
    ap.add_argument('--min', type=int, default=4, help='minimum relevance score')
    ap.add_argument('--all', action='store_true', help='rescan already-seen emails')
    args = ap.parse_args()
    scan(days=args.days, min_score=args.min, rescan_all=args.all)

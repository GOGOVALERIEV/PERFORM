# Agent 3 — Infrastructure & Systems Research (SWU Blagoevgrad / Windows stack)

**Date of research:** 17 Sep 2026
**Method:** live HTTP probing of swu.bg infrastructure (DNS via Google DoH, direct page fetches, Microsoft identity endpoints, PyPI JSON API, Todoist API docs). Everything marked **[VERIFIED]** was confirmed live during this session. Everything marked **[UNVERIFIED]** could not be confirmed and must be tested on the ground (with George's credentials).

---

## Q1. SWU student portal & email

### 1.1 The real system map — "SUUNI" does NOT exist at SWU

**[VERIFIED — DNS]** `suni.swu.bg` returns **NXDOMAIN** (Status 3 from Google DNS). There is no system called SUUNI at SWU. SUUNI-style name confusion comes from other Bulgarian universities (Sofia University's system family etc.). SWU's actual stack, all confirmed live:

| System | URL | What it is | Tech (observed) |
|---|---|---|---|
| **WEB-Студент** | `https://stud.swu.bg/WebStudent/` | Student self-service: student status, schedules, dorm/scholarship applications, links | ASP.NET MVC (bundled CSS/JS, Bootstrap, jQuery) |
| **АИС** | `https://ais.swu.bg` → redirects to `/Account/Login?ReturnUrl=%2F` | "Академична информационна система" — the internal academic IS | ASP.NET (IIS/8.5, ASP.NET forms auth with `__RequestVerificationToken`, UserName/Password/RememberMe) |
| **tt.swu.bg** | `http://tt.swu.bg` ("PublicSchedules — Югозападен университет") | **Public** lecture & exam timetables: by course group, by lecturer, by room | ASP.NET MVC; exam views sit behind login (`/Exam` → 302 to `/Account/Login`) |
| **moodle.swu.bg** | `moodle.swu.bg` → IP `194.141.86.51` | DNS record exists **[VERIFIED]**; **unreachable from George's current network (TCP/443 timeouts) [VERIFIED timeout]** — likely university-VPN/LAN-only or geo-fenced. Treat Moodle as *existing but access-restricted*. |
| Student email | `https://portal.microsoftonline.com` (link on swu.bg) | **Microsoft 365** — see below |  |
| Staff email | `https://mail.swu.bg/` (self-hosted on `194.141.86.3`, mail.swu.bg is a CNAME to ns.swu.bg) | staff only | MX: `10 mail.swu.bg`; SPF `v=spf1 ip4:194.141.86.3/32 ip4:217.26.219.11 -all` |

**[VERIFIED — Microsoft identity]** Querying `https://login.microsoftonline.com/common/userrealm?user=test@swu.bg&api-version=1.0` returns:
`{"account_type":"Managed","domain_name":"swu.bg","cloud_instance_name":"microsoftonline.com",...}`
→ `swu.bg` **is a managed Microsoft 365 tenant domain**. Student mailboxes are M365 accounts on the swu.bg tenant. (The exact student UPN format — `name@swu.bg` vs `name@student.swu.bg` — **[UNVERIFIED]**; the tenant answers "Managed" for all tested aliases because they share the domain_name field. George can confirm his own address from Outlook on the web in 5 seconds.)

### 1.2 Exam signup — how it actually works at SWU

**[VERIFIED — official pages, fetched live]**

- The **official procedure "ДОПУСКАНЕ ДО ИЗПИТНА СЕСИЯ"** (swu.bg → Студенти → Учебни процедури и срокове → /79-lproctbgc/79-sessionbgart) says admission to an exam session is certified **with a stamp and signature in the student book (студентска книжка)** by the "Студентско състояние" inspector, conditioned on: (a) fulfilled course obligations for the semester, (b) "заверен семестър" (semester validated by the Faculty Council decision).
- **Enrollment in a semester** (procedure /71-highercoursebgart): done **by the group leader (отговорник на групата)**, or exceptionally individually *with the physical student book*. Condition: validated previous semester + paid semester fee (deadline for regular students: **up to 15 days after the start of classes**; for дистанционно/задочно: by end of the in-person classes).
- The public timetable app (`tt.swu.bg`) exposes **"Изпити по курсове / по преподаватели"** but the exam views sit behind login (`/Exam` → login redirect) **[VERIFIED]**.

**Implication for the automation system:** at SWU there is **no online self-service exam registration to automate** (unlike, e.g., Sofia University's SU/FAKT). The "exam signup" step is *physical/administrative* (stamp in the student book). What the system CAN and should automate:
1. **Watch** `tt.swu.bg` public pages for exam dates for George's courses and push them to Google Calendar.
2. **Task pipeline**: create "go sign the student book at Учебен отдел" tasks (office hours **[VERIFIED]: Mon–Fri 10:00–12:00 and 13:00–14:00**, per-faculty inspectors listed on the adservice page with phone/email/cabinet numbers).
3. Track Moodle course pages per subject (for upload deadlines of реферати) — once access from his network is sorted.

### 1.3 Student email forwarding to Gmail

Path: **Microsoft 365 Outlook on the web → Settings → Mail → Forwarding**. Two options:

1. **Native M365 forwarding** (`outlook.office.com` → ⚙ → Mail → Forwarding → enable, set George's Gmail, optionally keep a copy). **[UNVERIFIED at SWU]** — many university tenants *disable* user-level forwarding (anti-exfiltration policy). If the toggle is greyed out, use option 2.
2. **Gmail-side pull**: Gmail → ⚙ → Accounts → "Check mail from other accounts" (POP3) with `outlook.office365.com:995`, George's university creds + app password. This works even if forwarding is blocked, as long as POP is enabled on the mailbox (tenant-level setting; **[UNVERIFIED]** for SWU).

**Recommended wiring for the watcher:** keep the current Gmail watcher as the single inbox, feed it via (1) or (2). Do NOT try IMAP-polling M365 in Python — MS is deprecating basic auth; if you ever need programmatic access use MSAL (`msal` 1.38.0, current on PyPI as of 2026-08) + Graph API, which is heavy for this use case.

**M365 tenant extras George gets free:** 1 TB OneDrive, Office desktop/web apps — useful for the humanizer/referat workflow (or ignore it and stay in the Google stack).

### 1.4 Academic calendar 2026/27 — full official data [VERIFIED]

Fetched live from `https://www.swu.bg/bg/studentsbg/accalendarbg/78-studentscat/2348-2026-2027` ("Календарен график", last updated 02 Jun 2026). **Редовно обучение** (full-time, George's track):

| Period | Duration | Dates |
|---|---|---|
| Winter semester classes | 15 weeks | **17.09.2026 – 08.01.2027** |
| Vacation | 2 weeks | 24.12.2026 – 03.01.2027 |
| Winter exam session | 3 weeks | **11.01.2027 – 29.01.2027** |
| Winter resit (поправителна) session | 1 week | 01.02.2027 – 05.02.2027 |
| Summer semester classes | 15 weeks | **08.02.2027 – 21.05.2027** |
| Summer exam session | 3 weeks | **25.05.2027 – 08.06.2027** |
| Summer resit session | 1 week | 09.06.2027 – 16.06.2027 |
| Extra liquidation session (4th year) | 1 week | 17.06.2027 – 23.06.2027 |
| Annual liquidation session | 1 week | 23.08.2027 – 27.08.2027 |

Also on the same page: задочно (part-time) tracks, state exam windows (preliminary 28.06–09.07.2027, regular 30.08–10.09.2027, resit 24.01–04.02.2028), and note #5: **all official national holidays are days off regardless of sessions**. Previous years' graphs (2025/26, 2024/25…) are at `/bg/studentsbg/accalendarbg/78-studentscat/2044-2025-2026` etc.

**There is no ICS feed from SWU** — the calendar is an HTML page (button-links to article pages, not PDF). Our system must scrape/parse this page once per year and generate events itself. The dates above are ready to hard-code for 2026/27.

---

## Q2. Email-to-task systems

### 2.1 Rule-based vs LLM extraction

- **Rule-based** (what the inbox watcher does): deterministic, free, zero-latency, but brittle to professor phrasing ("до 15-ти", "следващия четвъртък", "предайте през Moodle"). Fine for *triage* (which course, which sender).
- **LLM extraction**: one structured-JSON call over the email body. Best practice in 2026 is a **hybrid**: cheap rules decide *whether* it's a task email; one LLM call extracts the payload; a validator enforces the schema; low-confidence fields fall back to George in a chat prompt.

### 2.2 Recommended schema (modeled on Todoist REST v2 — verified live against developer.todoist.com)

Todoist's task model is the industry reference for planner apps: `content`, `description`, `project_id`, `section_id`, `parent_id`, `labels[]`, `priority` (1–4, **1 is highest**), `due_string`/`due_date`/`due_datetime` (+ human language parsing "next Thursday"). A school planner is exactly this plus a course dimension. Recommended JSON our LLM step should emit:

```json
{
  "type": "assignment",              // assignment | exam | signup | admin | info
  "course": "Международни отношения",
  "title": "Реферат: ...",
  "deadline": "2026-11-15T18:00:00+02:00",
  "deadline_is_date_only": false,
  "deliverable": "docx 8-12 стр.",
  "format": "docx",                  // docx | pdf | pptx | moodle-upload | paper
  "where": "Moodle",                 // Moodle | email | paper | email+moodle
  "priority": 1,                     // Todoist convention: 1=highest
  "status": "todo",                  // todo | doing | blocked | submitted | graded
  "source_message_id": "<gmail-id>",
  "confidence": 0.92,
  "needs_human_check": false
}
```

Notes: store `status` machine-side (Todoist has labels but not status; keep the file-based pipeline as source of truth); keep `confidence` and route <0.75 to a "confirm with George" step. This mirrors how school-planner apps (e.g., myHomework/Todoist education workflows) model assignments: **course + due + priority + deliverable**.

---

## Q3. Scheduling integration

### 3.1 Reality check [VERIFIED]

SWU publishes **no ICS feed**. Everything must be self-generated into Google Calendar (already working via API). Build a once-a-year script: parse the календарен график page → push semester boundaries as all-day events. The 2026/27 dates in §1.4 are the payload.

### 3.2 Even/odd week (нечетна/четна) handling

Bulgarian universities commonly schedule labs on "нечетни седмици" (odd calendar weeks). ICS has no native "week parity" concept, but **`RRULE FREQ=WEEKLY;INTERVAL=2`** with a fixed **anchor date** is the standard trick — the anchor date *is* the parity. Two concrete forms:

**Every 2nd Thursday, anchored on the first occurrence** (RFC 5545):
```
DTSTART;TZID=Europe/Sofia:20261001T100000        ← first odd-week Thursday, 10:00
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TH;WKST=MO;UNTIL=20270108T235959Z
```
- `WKST=MO` matters: with `INTERVAL=2` the week-start defines which "week bins" the recurrence falls into. For a plain every-2nd-week event `WKST=MO` (ISO Monday start, matching BG convention) is correct.
- `UNTIL` uses UTC (Z suffix) even when DTSTART has a TZID — that's per RFC 5545 §3.3.10.
- Caveat: `INTERVAL=2` counts *occurrence-to-occurrence*, so if the anchor week is semester week 1, the event lands on weeks 1,3,5… If a professor says "starts from week 2", just set DTSTART to the week-2 date; don't try to encode parity numbers.

**Multiple disjoint blocks** (weeks 1–7 and 9–15 with a break): don't try UNTIL gymnastics — generate two separate VEVENTs with different DTSTART/UNTIL. This is exactly what Google Calendar does when you edit a single instance of a biweekly series, and it's the least fragile approach for scripts.

**Concrete for George, winter semester 2026/27:** classes run 17.09.2026 (Thu) – 08.01.2027. Semester week 1 = week of Mon 14.09. Even/odd parity: ISO week number — e.g., ISO week 39 (Sep 21–27) is odd week #3 of the semester… simplest reliable rule: odd-week = `iso_week % 2 == parity_of(iso_week_of(sep_14_2026))`. Compute once, anchor DTSTARTs accordingly.

### 3.3 Exam sessions

Push the 3 sessions (11.01–29.01, 25.05–08.06, resits) as all-day events + per-exam events from `tt.swu.bg` when George's course schedules appear. Clockify seeding already exists — tag exam-prep blocks with the course name.

---

## Q4. Windows automation stack (Windows 11, Python 3.12)

### 4.1 Running the watcher — recommended pattern

For a **daily scan** (email→task pipeline), **Task Scheduler is the right tool** — not startup folder, not an always-on daemon:

- **Task Scheduler** [VERIFIED syntax from `schtasks /create /?` on this machine]: `schtasks /Create /SC DAILY /ST 08:30 /TN "SWU\InboxScan" /TR "\"C:\...\venv\Scripts\pythonw.exe\" \"C:\...\watcher.py\"" /F`. Triggers: DAILY/WEEKLY/MINUTE/ONLOGON/ONEVENT. Use `ONLOGON` *plus* DAILY for resilience (catches "laptop was off at 08:30"). Set "Start only on AC power" off and "Run whether user is logged on" only if storing a password is acceptable — otherwise "Run only when user is logged on".
- **Startup folder** (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` [VERIFIED path on this machine]): good only for long-running watchers (continuous IMAP-ish polling), with a .vbs launcher to hide the console.
- **Always-on background python**: only needed if the watcher must be *real-time*. A Gmail API poll every 15 min via Task Scheduler (`/SC MINUTE /MO 15`) is simpler and survives reboots/updates better than a daemon.

**Existing project pattern stays:** `.vbs` launcher → `pythonw.exe` (no console) → script. `pythonw.exe` confirmed at `C:\Users\User\AppData\Local\Programs\Python\Python312\pythonw.exe` **[VERIFIED on this machine]**.

### 4.2 Toast notifications — which library in 2026

**[VERIFIED against PyPI JSON API, live]**

| Library | Latest | Released | Verdict |
|---|---|---|---|
| **win11toast** | 0.36.3 | **2026-01-17** | ✅ actively maintained, wraps WinRT toast, supports buttons/callbacks |
| winotify | 1.1.0 | 2022-02-07 | ⚠️ works, unmaintained 4+ years; fine for fire-and-forget toasts |

Use **win11toast** for the task pipeline ("New assignment from prof. X — due Nov 15"), keep winotify only if win11toast's WinRT dependency misbehaves.

### 4.3 Orchestration notes

- One Task Scheduler task per pipeline stage (scan → extract → notify), chained by state files — matches the project's existing state-file style, easy to re-run manually.
- Log to a rolling file + a "last run" state file so a missed run is detectable (Task Scheduler GUI also exposes "Last Run Result: 0x0").
- Use absolute paths in /TR (quoting!), run under the user account, and prefer `pythonw.exe` to avoid console flashes.

---

## Q5. File pipeline & formats

### 5.1 docx generation — python-docx

**[VERIFIED PyPI]** `python-docx` 1.2.0 (2025-06-16), current and maintained. Capabilities: styles, fonts (name + size + bold/italic), `section.left_margin/right_margin/top_margin/bottom_margin`, page size A4, tables, images, headers/footers, page numbering fields. Good enough for full реферат generation.

### 5.2 BG academic formatting standards (оформление на реферат)

**Honest status:** there is **no single national ISO standard** for BG student papers; each university (often each lecturer/faculty) publishes its own guidelines. **[VERIFIED NEGATIVE]** SWU's site search for "реферат" / "оформяване" returns no university-wide formatting guideline — so **SWU norms are per-lecturer [UNVERIFIED — George must collect each professor's sheet into the knowledge base]**. The de-facto BG academic convention (consistent across BG university guidelines and методически указания found in the wild) is:

| Element | Standard BG practice |
|---|---|
| Paper / margins | A4; left **3 cm**, right **1.5 cm** (sometimes 1), top/bottom **2 cm** |
| Font | **Times New Roman 14** (referat/курсова работа; 12 for длинни tables/footnotes) — not 12 for body |
| Line spacing | **1.5 lines**; single for tables/captions |
| Alignment | Justified; first-line indent 1–1.25 cm |
| Page numbers | Bottom center or top right; title page counted but not numbered |
| Title page | University name (top), faculty/department, discipline, **topic in caps**, author + факултетен номер, lecturer's title+name, city + year (bottom center) |
| Structure | Увод → chapters → Заключение → Библиография (bibliography is a *separate last section* in BG tradition, not inline-only) |
| Volume | Referat typically 8–15 pages, курсова 15–30 (per-lecturer) |
| Citation | Usually author-year in text + alphabetical Библиография; **БДС ISO 690** is the official BG standard (Bulgarian Institute for Standardization adopted ISO 690 as БДС ISO 690:2005); APA is increasingly accepted but BG departments traditionally prefer ISO 690 / Bulgarian bibliographic style — **[UNVERIFIED for George's specific faculty: Философски факултет / IR program — get the lecturer's sheet]** |

**Implementation:** encode this as a default template profile in the referat builder, with per-course overrides loaded from a `courses.json` (lecturer name → margin/font rules captured from their sheets).

### 5.3 PDF generation

**[VERIFIED PyPI]** `reportlab` 5.0.1 (2026-08-20 — major 5.x now) and `weasyprint` 70.0 (2026-09-08) both current. Recommendation: **WeasyPrint** for real documents (HTML/CSS → PDF, handles Cyrillic well via system fonts, easy styling for CVs/annexes); reportlab only for programmatic low-level PDFs. For "print the referat" needs, LibreOffice headless (`soffice --headless --convert-to pdf file.docx`) preserves the docx layout exactly — often the better path for academic docs.

### 5.4 pptx — python-pptx

**[VERIFIED PyPI]** `python-pptx` 1.0.2 (2024-08-07), stable, current. Key practices for BG academic presentations:
- **16:9**: set `prs.slide_width = Inches(13.333)`, `slide_height = Inches(7.5)`.
- Use slide **layouts from a master** (title, title+content, section header) rather than blank slides + textboxes — keeps theme consistency and lets the template carry fonts.
- BG fonts: Times New Roman 28–36pt titles / 20–24pt body, or Calibri if the lecturer is modern; Cyrillic is fully supported (it's just Unicode).
- Keep ≤ 6 bullet lines/slide; generate speaker notes in the notes pane (notes_slide.notes_text_frame) — pairs perfectly with the memory-trainer/simplifier goals.

### 5.5 Pipeline recommendation

docx (python-docx from a BG-standard template) → optional PDF (LibreOffice headless) → submit via Moodle (human-in-the-loop, see Q6) or email. Keep every artifact in the course folder + log to Clockify.

---

## Q6. Security & anti-detection of the whole system

### 6.1 Risk model for touching university systems

| Action | Risk | Verdict |
|---|---|---|
| Reading public pages (swu.bg, tt.swu.bg public schedules) | Negligible — public info, few requests/day | ✅ automate freely, but throttle (1 req/2–5 s, cache pages) |
| Scraping tt.swu.bg exam pages behind login | Low — but it's George's real account acting | ⚠️ automate reading only; use Playwright with persistent profile, human-initiated login |
| Auto-submitting anything (Moodle uploads, assignments) | **High** — academic-integrity exposure + account flags | ❌ **never fully automated**. System prepares the file + opens the page; **George clicks upload** |
| Programmatic login to ais.swu.bg / stud.swu.bg (ASP.NET forms + `__RequestVerificationToken` [VERIFIED]) | Medium — failed logins lock accounts; anti-bot risk low but real | ⚠️ if ever needed: Playwright, saved session, ≤1 login/session, never retry in a loop |
| Email automation via Google API | Zero risk to university (it's our own Gmail + M365 forwarding) | ✅ |

### 6.2 Behavioral best practices

1. **Rate**: human cadence — a student checks the portal a few times a day, not every 5 minutes. Poll tt.swu.bg 2–4×/day max, randomized offsets.
2. **Sessions**: reuse cookies/session state; do not re-login each poll. Logins are the loudest action.
3. **User-Agent**: when using Playwright, keep the real Edge UA (project rule: Edge for university/Meta work), don't strip headers — look like Edge on Win11, because it *is* Edge on Win11.
4. **Human-in-the-loop for submissions**: the one irreversible, reputation-bearing action (uploading a referat to Moodle) stays manual. The system's job: prepare file, open the correct Moodle page in Edge, pre-fill nothing that requires his account, toast him "review & submit".
5. **Account safety**: 2FA on the M365 account; app password for POP if used; never store the university password in plaintext — if Playwright needs it, use Windows Credential Manager (Python `keyring`) or the browser's own saved-password profile.
6. **Data hygiene**: emails contain lecturer personal data (GDPR-adjacent) — keep the pipeline state files inside the local PERFORM folder, don't sync raw emails to third-party services beyond Google's existing processing.

### 6.3 What "automation" should mean here (architecture principle)

The university-facing layer is **read-only + human-in-the-loop**. Everything heavy (drafting, formatting, scheduling, reminders, memory training) happens **on George's machine against his own files** — that's where the leverage is, and it's undetectable because it never touches university servers.

---

## Sources

**Fetched live during this session (17 Sep 2026):**
- https://www.swu.bg/bg/ (homepage; server Apache/2.4.56, PHP 8.2.4)
- https://www.swu.bg/bg/studentsbg (student hub; links: stud.swu.bg/WebStudent/, portal.microsoftonline.com, mail.swu.bg, ais.swu.bg)
- https://www.swu.bg/bg/studentsbg/accalendarbg + /78-studentscat/2348-2026-2027 (full календарен график 2026/27, updated 02 Jun 2026)
- https://www.swu.bg/bg/studentsbg/trproceduresbg (procedure list) + /79-lproctbgc/79-sessionbgart (ДОПУСКАНЕ ДО ИЗПИТНА СЕСИЯ) + /71-highercoursebgart, /72-summerenrollmentbgart (enrollment by group leader)
- https://www.swu.bg/bg/studentsbg/adservicebg (Учебен отдел inspectors, office hours Mon–Fri 10–12, 13–14)
- https://stud.swu.bg/WebStudent/ (WEB-Студент ЮЗУ, ASP.NET MVC; links to tt.swu.bg)
- https://ais.swu.bg/Account/Login (АИС, IIS 8.5, ASP.NET auth with __RequestVerificationToken)
- http://tt.swu.bg (+ /Schedule/StudentSchedule; /Exam → login-gated)
- DNS (Google DoH): suni.swu.bg = NXDOMAIN; moodle.swu.bg = 194.141.86.51 (TCP timeouts from George's network); swu.bg MX=10 mail.swu.bg; SPF=ip4:194.141.86.3/32 ip4:217.26.219.11
- https://login.microsoftonline.com/common/userrealm?user=test@swu.bg → Managed M365 tenant
- PyPI JSON API: win11toast 0.36.3 (2026-01-17), winotify 1.1.0 (2022-02-07), python-docx 1.2.0 (2025-06-16), python-pptx 1.0.2 (2024-08-07), reportlab 5.0.1 (2026-08-20), weasyprint 70.0 (2026-09-08), playwright 1.63.0, icalendar 7.3.0, msal 1.38.0
- https://developer.todoist.com/rest/v2/ (task schema: priority 1–4 with 1=highest, due_string, labels, project_id)

**Local machine verification:** `schtasks /create /?` output; pythonw.exe at Python312 path; Startup folder path.

**Unverified items (need ground truth from George):** exact student UPN/email format on the M365 tenant; whether M365 user-level forwarding is enabled at SWU; whether POP is enabled; Moodle reachability from campus/home network and per-course Moodle usage; per-lecturer formatting sheets ( margins/font/citation) for Философски факултет — no university-wide standard found on swu.bg.

**Failed approaches (documented so nobody repeats them):** Bing/DuckDuckGo HTML endpoints return garbage/captcha to curl (Hebrew/Chinese results for BG queries); SWU site's own search returns no formatting guidelines; /tmp path breaks Git-Bash Python scripts on Windows (use real paths).

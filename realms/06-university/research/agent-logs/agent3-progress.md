# Agent 3 — Progress Trail (Infrastructure & Systems)

- Read mission; created research workspace `_tmp/` for scrape artifacts (deleted after).
- DNS recon (Google DoH): `suni.swu.bg` = NXDOMAIN → "SUUNI" doesn't exist at SWU; `moodle.swu.bg` resolves (194.141.86.51) but TCP times out from this network; `swu.bg` MX/SPF → self-hosted staff mail.
- Fetched & parsed swu.bg student pages: students hub, academic calendar, study procedures (exam-session admission = stamp in student book), admin service (inspector office hours), state exams page.
- Probed live: `stud.swu.bg/WebStudent/` (ASP.NET MVC "WEB-Студент ЮЗУ"), `ais.swu.bg` (АИС login, IIS/ASP.NET + RequestVerificationToken), `tt.swu.bg` (public schedules; /Exam login-gated).
- Verified via Microsoft userrealm endpoint: swu.bg = managed Microsoft 365 tenant (student mail = M365).
- Extracted FULL official SWU academic calendar 2026/2027 (all session dates) — ready to hard-code into calendar script.
- Checked tooling versions live on PyPI: win11toast 0.36.3 (2026, maintained) vs winotify 1.1.0 (2022, stale); python-docx 1.2.0, python-pptx 1.0.2, reportlab 5.0.1, weasyprint 70.0, msal 1.38.0.
- Pulled Todoist REST v2 task schema from live docs → used as reference model for the email→task JSON schema (priority 1 = highest).
- Verified local machine: schtasks syntax, pythonw.exe path, Startup folder path.
- BG formatting standards: verified NEGATIVE — no university-wide guideline on swu.bg (search returned nothing); documented de-facto BG norms (TNR 14, 1.5 spacing, 3/1.5/2 margins, БДС ISO 690 citation) with per-lecturer caveat.
- Bing/DDG scraping attempts failed (bot garbage) — documented as failed approach; relied on primary sources instead.
- Wrote full report: `agent3-infra.md` (6 questions, verified/unverified marking, sources).
DONE

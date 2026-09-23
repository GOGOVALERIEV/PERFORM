# MISSION: Agent 3 — Infrastructure & Systems Research
You are a research agent. RESEARCH ONLY. You write ONE final report file and a brief in this folder. Do NOT build any scripts. Do NOT modify any files except the two files listed at the end.

## Context (read this first)
Our user (George) is a 1st-year IR student at SWU Blagoevgrad, Bulgaria. We are building his university automation system inside an existing Windows machine + PERFORM structure. Existing working infrastructure: Google APIs (Gmail/Docs/Sheets/Calendar) via service token, Clockify, GitHub. Machine: Windows 11, Python 3.12, Task Scheduler available. He has a girlfriend (Valeria) studying the same program — files flow between them via Telegram.

The system being built: inbox watcher (done), task pipeline (email→task→execution→submission), humanizer, redoer, presentation builder, simplifier, memory trainer.

## Your Research Questions (answer ALL, deeply)
1. **SWU student portal & email**: What systems does SWU Blagoevgrad actually use in 2026: SUUNI/suni.swu.bg? (student records, grades, exams registration) — how does exam signup work there? Is there Moodle (moodle.swu.bg or similar)? What is student email (Microsoft 365? Google Workspace?) — and can it auto-forward to George's Gmail (which our watcher already scans)? Forwarding setup specifics.
2. **Email-to-task systems**: patterns for converting emails to structured tasks: rule-based parsing (what we have) vs LLM-extraction of (task, course, deadline, deliverable, format) JSON. Research best-practice schemas for academic task tracking. Look at how tools like folotask/school planner apps model assignments (due dates, priority, status, course).
3. **Scheduling integration**: We already push events to Google Calendar + Clockify seeding. Research best patterns for academic-term calendars: Bulgarian academic calendar ICS feeds, SWU exam sessions as calendar events, even/odd week handling (нечетна/четна) — how do calendar tools handle biweekly recurring events (RRULE FREQ=WEEKLY;INTERVAL=2 with WKST; recursion with BYDAY)? Concrete RRULE syntax for "every 2nd Thursday".
4. **Windows automation stack**: For a Windows 11 machine: Task Scheduler vs startup folder vs always-on background python; running the watcher periodically (daily scan) — best pattern. pythonw + vbs launcher patterns (already used in this project). Notifications: Windows toast notifications from Python (win11toast / winotify) — which is maintained in 2026?
5. **File pipeline & formats**: .docx generation for реферати (python-docx: fonts Times New Roman 12/14, margins per BG standards — what ARE the BG academic formatting standards? title page conventions?), PDF generation (reportlab/weasyprint), .pptx via python-pptx (templates, master slides, 16:9, BG fonts). BG academic norms for оформление (margins, spacing, citation style: Bulgarian academy standard — APA/BG-themed?)
6. **Security & anti-detection of the whole system**: How much should automation touch university systems directly? Risks of bot-like behavior on SUUNI/Moodle (session patterns, rate of requests). Best practice: human-in-the-loop for submissions, browser automation only when needed (Playwright already installed) — risk model.

## Rules
- Use web search/fetch extensively. Verify with multiple sources where possible.
- If something can't be verified, SAY SO — mark it as "unverified" rather than guessing.
- Be concrete: name tools, versions, prices, URLs.

## Deliverables (write EXACTly these two files, nothing else)
1. `C:/Users/User/Desktop remaining/agent3-infra.md` — NO! Write to: `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/agent3-infra.md` — full report, English, structured by the 6 questions, "Sources" at the end.
2. Same folder, `agent3-progress.md` — brief trail. Final line: "DONE".

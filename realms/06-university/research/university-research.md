# SWU University Research — Lectures, System, Automation Potential
Researched: 2026-09-16 · Source: https://tt.swu.bg/Schedule/ViewStudentSchedule/9/1 (official timetable)

---

## 1. The Schedule (Winter Semester 2026/2027, period 17.09.2026 – 08.01.2027)

Program: **Международни отношения, бакалавър — Първи курс (редовно)**
Room numbers: building + room (6310 = floor 6 room 310 style). "поток" = whole stream attends.

| Day | Hours | Subject | Type | Room | Teacher |
|---|---|---|---|---|---|
| **Понеделник** | 09:30–12:30 | Английски език | упражнения (3h) | 6302 | доц. д-р Гергана Георгиева |
| **Понеделник** | 13:30–16:30 | Политология | лекции (3h) | 1208 | доц. д-р Николай Попов |
| **Вторник** | 09:30–13:30 | История на международните отношения | лекции (4h) | 6310 | доц. д-р Димитър Тюлеков |
| **Вторник** | 14:30–15:30 | Политология | упражнения (1h) | 6309 | гл. ас. д-р Йосиф Кочев |
| **Сряда** | 08:30–10:30 | Глобализъм, наука, технологии | лекции (2h) | 6310 | гл. ас. д-р Мария Хаджипетрова-Лачова |
| **Сряда** | 10:30–12:30 | Френски език | упражнения (2h) | 6310 | гл. ас. д-р Мария Хаджипетрова-Лачова |
| **Четвъртък** | 08:30–12:30 | Политическа история на Европа и САЩ | лекции (4h) | 6311 | гл. ас. д-р Вероника Стоилова |
| **Четвъртък** | 12:30–13:30 | Политическа история на Европа и САЩ | упражнения (1h) | 6304 | гл. ас. д-р Вероника Стоилова |
| **Четвъртък** | 14:30–16:30 | История на МО | упражнения (2h) — **нечетни седмици only** | 6310 | х.преп. Мартин Лалев |

**ПЕТЪК И СЪБОТА = СВОБОДНИ. ZERO CLASSES.** (Big win — those are the work/client days.)

### Date rules (critical)
- The "История на МО" Thursday 14:30–16:30 exercise happens ONLY on odd weeks:
  17.09; 01.10; 15.10; 29.10; 12.11; 26.11; 10.12.2026
- Even/odd weeks (зимен семестър): starts 14.09.2026 as НЕЧЕТНА, then alternates.
  четна weeks: 21.09, 05.10, 19.10, 02.11, 16.11, 30.11, 14.12, 28.12.2026

### Weekly hour load
- Lectures (лекции): 4+3+2+4 = **13 h/week**
- Exercises (упражнения): 3+1+2+1+2(+2 odd weeks) = **9–11 h/week**
- **Total: ~22–24 h/week on campus.** That leaves ~40+ workable hours for copywriting/AI/client work.

### Action item found in the schedule note
Sport enrollment at the Sport Complex: **14–25 September 2026, 09:00–17:00** (for 2026/2027).
Every student must pick a sport that fits their schedule. George must go once in that window.

### Machine-readable export
https://tt.swu.bg/Schedule/DownloadTimetable/18498 → Excel-compatible HTML table (vnd.ms-excel).
Saved copy: PERFORM/output/swu_timetable_download. Scraping is trivial — no login needed, no JS.

---

## 2. How the Study Process Works (Bulgaria / SWU specifics)

**Semester rhythm (typical BG public university, SWU follows it):**
1. **Зимен семестър** (winter): mid-September → ~mid-January. 15 teaching weeks, then exam session.
2. **Сесия** (exam session): Jan. Two windows — редовна (regular) and поправителна (retake/correction) — usually 3 weeks + 2 weeks.
3. **Летен семестър** (summer): ~08.02.2027 → mid-May, then сесия again June.
4. Grading scale: 2.00 (fail) – 6.00 (excellent). Pass ≥ 3.00. Exams are usually written, oral, or both.
5. **Attendance:** In BG, "упражнения" (exercises/seminars) are where attendance is TAKEN and points are given
   (presentations, homework, colloquiums). Lectures (лекции) are often technically mandatory but in practice
   attendance is rarely enforced — the professor can require it, but scores usually come from exercises.
6. **ECTS credits:** each subject carries credits (typically 4–6 ECTS); you need ~30/semester, 240 total for a BA.
7. **What actually decides your score (typical formula):**
   - Текущо оценяване (current score): attendance, homework, presentation, colloquium — often 30–50%
   - Изпит (exam) — the rest. Many teachers give syllabus rules ("оценяване по точки") in week 1.

**Teacher task channels (the pipeline to automate):** BG universities announce tasks via:
- Email (Gmail/university mail) — letters, requirements, PDF attachments
- Moodle or the university's own portal (SWU uses a university information system; tt.swu.bg is only timetables)
- Telegram/Facebook groups per course (very common in BG)
- Verbally in class → this is the one that must reach the system manually (one-line braindump)

---

## 3. The Five Future Modules — Feasibility Read (research only, nothing built)

| Module | What it does | Feasibility | Notes |
|---|---|---|---|
| 1. Inbox watcher | Gmail → detect teacher task → extract requirements (deadline, format, length) | HIGH | Gmail API already working in PERFORM. Filter by sender keywords. |
| 2. Humanizer | Rewrites own/AI text so AI-detectors miss | MEDIUM | Detector bypass = layered paraphrase + human-noise. Old detectors (originality.ai, Turnitin AI) are unreliable anyway — big false-positive scandals. Will iterate with tests. |
| 3. Redoer | Valeria's work (Telegram) → transformed variant for George | HIGH | Telegram API + LLM rewrite + different structure. Same pipeline as Humanizer. |
| 4. Presentation builder | Data → slide deck (structure + content) | HIGH | python-pptx already installed; "make_presentation.py" exists in old project-test as proof. |
| 5. Simplifier | Book/assignment → shortest learnable brief that makes you look like you read it | HIGH | LLM strength. Structure: 1-page essence → key arguments → names/dates/terms → likely exam questions. |
| 6. Memory trainer | Terminology drills from Simplifier output | HIGH | Spaced-repetition flashcards (Anki-style) generated from the brief. |

**Where lectures fit George's strategy:** lectures = lowest value per hour (slides get distributed or can be
recovered). Exercises = where the score is earned (attendance, presentations, homework). So the smart play:
skip-or-drop-in on lectures (recover via Simplifier), NEVER miss exercises. English/French are graded on
participation — those two need physical presence.

---

## 4. Open Questions (need George's answers before building)
1. Does George have the SWU university email + portal login (for Moodle/Moodle-like announcements)?
2. Is there a course Telegram group(s) — and is Valeria in them?
3. Which subjects' teachers announced attendance rules / point systems yet?
4. Confirm: schedule weeks start 14.09.2026 — actual start date for George's 1st year?

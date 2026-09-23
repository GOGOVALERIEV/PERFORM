---
name: swu-schedule
description: George's university schedule — SWU "Neofit Rilski" Blagoevgrad, Международни отношения (International Relations), BA, 1st course, full-time. Use when planning any day: the machine must respect these as FIXED WALLS. Auto-fetch source: tt.swu.bg public timetable.
---

# SWU — ЮЗУ "Неофит Рилски", Blagoevgrad

- **Program:** Международни отношения (International Relations) — бакалавър, редовно
- **Faculty:** Правно-исторически факултет (facultyId=2)
- **Speciality ID:** 9, **Course:** 1
- **Live source:** https://tt.swu.bg/Schedule/ViewStudentSchedule/9/1
- **Semester period:** 17.09.2026 → 08.01.2027
- **Parser:** `PERFORM/state/parse_swu.py` (run against saved HTML; refetch with curl)

## Weekly Schedule (Semester Winter 2026/27)

| Day | Time | Subject | Type | Room | Teacher |
|-----|------|---------|------|------|---------|
| **Mon** | 9:30–12:30 | Английски език | упражнения (3h) | 6302 | доц. д-р Гергана Георгиева |
| **Mon** | 13:30–16:30 | Политология | лекции (3h, поток with Право + Публична администрация) | 1208 | доц. д-р Николай Попов |
| **Tue** | 9:30–13:30 | История на международните отношения | лекции (4h) | 6310 | доц. д-р Димитър Тюлеков |
| **Tue** | 14:30–15:30 | Политология | упражнения (1h) | 6309 | гл. ас. д-р Йосиф Кочев |
| **Wed** | 8:30–10:30 | Глобализъм, наука, технологии | лекции (2h) | 6310 | гл. ас. д-р Мария Хаджипетрова-Лачова |
| **Wed** | 10:30–12:30 | Френски език | упражнения (2h) | 6310 | гл. ас. д-р Мария Хаджипетрова-Лачова |
| **Thu** | 8:30–12:30 | Политическа история на Европа и САЩ | лекции (4h) | 6311 | гл. ас. д-р Вероника Стоилова |
| **Thu** | 12:30–13:30 | Политическа история на Европа и САЩ | упражнения (1h) | 6304 | гл. ас. д-р Вероника Стоилова |
| **Thu** | 14:30–16:30 | История на международните отношения | упражнения (2h, BY DATES) | 6310 | х.преп. Мартин Лалев |

### Thursday exercise dates (История на МО, упражнения 14:30–16:30)
**17.09 · 01.10 · 15.10 · 29.10 · 12.11 · 26.11 · 10.12.2026**

## Machine Rules
1. These blocks are FIXED WALLS — the Tony Stark machine schedules around them, never through them.
2. Monday is the longest day (9:30–16:30). Deep work that day: evening only.
3. Thursday exercise sessions (14:30–16:30) happen ONLY on the dates listed above — other Thursdays end at 13:30.
4. When a real day differs from this grid (professor cancels, George finishes early), George states reality in chat → machine rebuilds from the real clock.

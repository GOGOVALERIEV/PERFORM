# DRAFTING PROMPTS — The Pipeline's Prompt Library
*Built from counter1 (similarity) + counter3 (style). Inject voice-profile + course + topic into each. Raw LLM output is RADIOACTIVE — it never leaves the work folder without the style pass + manual rewrite.*

## P0 — Outline (LLM-assisted, NOT submitted)
```
Ти си асистент по [ДИСЦИПЛИНА]. Тема: [ТЕМА]. Изисквания на преподавателя: [ИЗИСКВАНИЯ].
Източници, които ще ползвам: [СПИСЪК].
Направи ОЧЕРТАНИЕ (не текст!): 4-7 секции, за всяка — каква ТЕЗА ще защитя в нея,
кой източник я подкрепя, и какво остава за заключението. Без готови изречения —
само точки с тези. Не използвай фрази от източниците буквално.
```

## P1 — Body drafting (closed-book)
```
Ето очертанието и бележките ми по тема [ТЕМА]:
[ОЧЕРТАНИЕ]
[БЕЛЕЖКИ — ФРАГМЕНТИ САМО: дати, имена, факти; НЯМА готови изречения]

Напиши чернова на тялото (без увод и без заключение) на български, като:
1. Пишеш ОТ БЕЛЕЖКИТЕ, от паметта — не пресъздаваш изречения от източниците. Ако не
   помниш точно формулировка, напиши факта с твои думи.
2. Следваш тона на този глас: [ИНЖЕКТИРАЙ voice-profile.yaml — любимите частици,
   типични начала, списъка за избягване].
3. Не използваш нито една фраза от списъка за избягване.
4. Всяко определение се пренаписва със собствени думи + цитиране: "както поставя
   Иванов (2021), ...". Пряка цитата само ако я маркирам с „...“.
5. Дълги редове от факти (дати, договори) вграждаш в собствено изречение с теза —
   не ги оставяй самостоятелни.
```

## P2 — Tic sweep + rhythm pass (can be a smaller/faster model)
```
Ето чернова на български. Направи ИЗЧИСТВАНЕ, не презаписване:
1. Намери и премахни изкуствено-еднаквия ритъм: раздели/слей изречения, така че
   всеки параграф с 3+ изречения да има поне едно кратко (до 7 думи) и поне едно
   дълго (20+ думи). Параграфите да са неравни (2-7 изречения).
2. Замени шаблонните фрази: [СИСЪКЪТА ЗА ИЗБЯГВАНЕ]. Без добавяне на нови факти.
3. Добави 1 курс-котва (напр. "както обсъдихме на упражнението") и 1 лично
   наблюдение — мястото им да е естествено.
НЕ променяй числа, дати, имена, цитати. Върни целия текст.
```

## P3 — Fact-diff check (supervisor runs script, not an LLM)
`python scripts/ksim.py <final> <corpus>` + manual diff of digits/names between P1 output and P2 output.

## P4 — Human pass (George, mandatory)
- Hand-write the intro + conclusion from the outline (SC-11)
- Read every ARG paragraph; retype any paragraph that doesn't sound like you
- Open the final file in Word, skim, save (Real-Editor Rebirth — honest metadata)

## Notes
- Never submit raw P1/P2 output. The pipeline ends at P4.
- Never paste the same text into the chat session that drafted it "to check AI-ness" — testing happens in ksim/plag.bg/GPTZero only.

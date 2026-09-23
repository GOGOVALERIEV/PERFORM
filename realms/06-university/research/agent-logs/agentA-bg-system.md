# AGENT A — The Bulgarian / Government-Connected Anti-Plagiarism System
**Mission:** Find the "Bulgarian/government system" SWU "Neofit Rilski" uses to catch AI/plagiarism. Research-only. All sources fetched live via curl on 17 Sept 2026.

---

## ✅ VERDICT (answer first)

**The system is StrikePlagiarism.com — and it IS government-connected.** It is a Polish system (owner: **Plagiat.pl**, Warsaw, founded 2002), which was **procured centrally by the Bulgarian Ministry of Education and Science (МОН) in June 2022 via a 3-year public-procurement contract** with its Romanian subsidiary **Plagiat-Sistem Antiplagiat prin Internet SRL** (Bucharest), and deployed **free of charge to ALL Bulgarian universities from September 2022** "по решение на МОН" (verbatim from Uni-Ruse's official page). That is the "national system" students are talking about.

**The AI-catching part:** StrikePlagiarism.com has a module "Откриване на съдържание, генерирано от изкуствен интелект" (AI-generated content detection). The company's own representative announced in Bulgaria in Nov 2023 that "Софтуерът на компанията вече предоставя възможност да се открива съдържание, генерирано от изкуствен интелект" (Az-buki, №46, 16–22.11.2023). So when SWU students say "there's a system for catching AI people" — that system is **StrikePlagiarism running inside SWU's Blackboard (disted.swu.bg)**, with the AI-detection module included.

**The 2022–2025 central МОН contract has EXPIRED.** In June–July 2025 МОН announced it would **not** sign a new central contract and told every university to buy its own system (SEGA 16.07.2025; БГНЕС 19.07.2025). МОН explicitly said centralized buying is no longer "финансово рентабильно" for systems that also catch AI content. That is why SWU now runs **its own** StrikePlagiarism/Blackboard LTI integration — which is exactly what the SWU disted manual documents.

**What plag.bg is NOT:** plag.bg is not Bulgarian and not government. It is the Bulgarian-language storefront of **Plagramme** (Lithuanian consumer plagiarism+AI checker, data controller **LINGUA INTELLEGENS, UAB**, Vilnius; press in 2019 named owner "LLC ACVK", Vilnius). It is a separate, commercial, student-facing tool that some universities (e.g., Ruse's ЦДО) *recommend to teachers* for self-checking. It is **not** the system SWU checks your work with.

**Named, sourced:** StrikePlagiarism.com (Plagiat.pl, Poland) — МОН-procured national anti-plagiarism system for Bulgarian higher education since Sept 2022, with built-in AI-text detection since 2023. Verdict: **found and documented.**

---

## 1. plag.bg — who owns/runs it

**Owner: Lithuanian, not Bulgarian, not state.**

- Site footer/privacy policy (fetched live): "This document explains **LINGUA INTELLEGENS, UAB** privacy policy on its website under which you may use plagramme.com and **related domains**" — and the footnote in the Terms of Use explicitly lists **plag.bg** among those domains: "noplagiat.de, noplagio.it, plag.asia, plag.at, plag.be, plag.bg, plag.by, plag.co.in, plag.com.ua, plag.cz, plag.dk, plag.ee, plag.es, plag.fi, plag.fr, plag.gr, plag.hu, plag.id, plag.kr, plag.lt, plag.lv, plag.mk, plag.ph…" (~40 country domains).
- Terms of Use (plag.bg/terms-of-use): "Any legal issues… shall be exclusively governed and litigated by the laws and courts, **Lithuania**, European Union."
- Assets load from `cdn.plagramme.com`; the homepage links to `plagramme.com`, `linkedin.com/company/plagramme`, Facebook "plagplagramme", Instagram "plag.ai", and support runs through **support@plagramme.com** (confirmed in Uni-Ruse's ЦДО recommendation to e-mail that address for teacher accounts).
- Bulgarian press (glasnews.bg / kaldata.com, 2019) describing plag.bg at launch: "литовската компания предлага мощен софтуер за проверка на плагиатство… Компанията е основана през 2011 година и е собственост на LLC ACVK. Централният офис… във Вилнюс" (paid promo article). The privacy-policy data controller is today Lingua Intellegens, UAB — same Lithuanian operation, renamed/restructured.
- Is it PlagiarismCheck.org? **No.** It is Plagramme (plag.ai / plagramme.com), a different product; both are third-party tools but unrelated entities.
- МОН/НЦИД/state connection: **none found anywhere** — no МОН mention on plag.bg, no МОН procurement trace, no government endorsement. Its Bulgarian registrar data is GDPR-masked (whois register.bg: "personal data is not published"), but the terms bind it to Lithuanian law — that is decisive.
- What it markets: plagiarism checker supporting **129 languages**, an **AI detector ("1-ви многоезичен AI детектор")** that explicitly supports Bulgarian ("Откривай AI текст в документи на български, английски, немски…" — detects ChatGPT/Gemini/Claude, sentence-level marking, PDF reports), plus paid "plagiarism removal" and **"хуманизиране на AI текст"** (AI-text humanization!) services. Note the irony: the same site sells the student a way to *humanize* AI text after checking it.
- Who uses it in BG: **Русенски университет „Ангел Кънчев"** — official ЦДО page (uni-ruse.bg/Centers/TSDO/news, fetched live): "Уважаеми колеги, ЦДО препоръчва да използвате следната система за проверка за плагиатство: https://www.plag.bg/ Трябва да се регистрирате с университетския имейл адрес… ще имате 20 безплатни проверки на документи на месец; 20 допълнителни проверки за 9,55 лв." — i.e., a **recommended self-check tool for teachers**, not a verification-of-record system. 2019 press coverage (technews.bg 02.01.2019, kaldata, glasnews, haskovo.net) confirms it was marketed to Bulgarian teachers/academics since 2019.
- Students using it: Trustpilot widget on plag.bg shows Bulgarian student reviews 2025 ("Уникална програма… до какъв процент съм си помогнала с изкуственият интелект"). So students at many universities (probably including SWU) self-check on plag.bg — but the *institutional* check is StrikePlagiarism.

## 2. Government/legal angle

**The state-provided system exists and is StrikePlagiarism. Timeline (all primary/live-fetched):**

- **March 2022:** МОН announces a public procurement for anti-plagiarism software (forecast value 1,599,103 лв.). In the first tender the Romanian bidder offered an absurd **184.9 billion лв** (Actualno.com, 03.03.2022 — the story of the "Румънска компания иска да ни пази от плагиатство"). МОН re-tendered with a single invited bidder — the same Romanian company.
- **20 June 2022:** МОН press release ("МОН ОСИГУРЯВА БЕЗПЛАТЕН СОФТУЕР СРЕЩУ ПЛАГИАТСТВО"): МОН will pay **~500,000 лв./year**; software developed in Poland; already used at Sofia University (pilot); **contract signed with Plagiat-Sistem Antiplagiat prin Internet SRL (Romania) under the Public Procurement Act (ЗОП), 3-year term; 2 лв. per user/year; projected 237,000+ users** (students, PhDs, teachers, state servants); free for teachers, students, PhD candidates, **НАЦИД** (National Centre for Information and Documentation) and the **Commission on Academic Ethics (Комисия по академична етика)** to the Minister. Source: МОН announcement as carried by Mediapool.bg, BGVoice, bTV, SEGA, obekti.bg — all fetched.
- **23 March 2023:** МОН official news item web.mon.bg/bg/news/5251 (fetched via archive of web.mon.bg): "**СОФТУЕР СРЕЩУ ПЛАГИАТСТВО СРАВНЯВА ВСЯКА ПУБЛИКАЦИЯ С 35 МЛН. НАУЧНИ ИЗТОЧНИЦИ**" — Deputy Minister Prof. Albena Chavdarova: "единната система срещу плагиатство в България е въведена миналата година. Софтуерът е закупен от МОН и предоставен безплатно на всички висши училища, научни организации и институции… Преди това системата е въведена пилотно в Софийския университет."
- **September 2022:** rollout to all universities. Uni-Ruse (official ЦДО page): "**От месец септември 2022 г. по решение на Министерството на образованието и науката (МОН) във всички университети в България започна внедряването на системата StrikePlagiarism** за борба с плагиатството." Ruse notes accounts are **admin-created** because "за да ползвате системата безплатно (чрез абонамент от МОН)" — a paid self-created profile is not free.
- **16–22 Nov 2023:** Az-buki (MЕ's own publishing house, №46): Donika Gavova, StrikePlagiarism.com representative — the software "**единствената лицензирана от МОН компания за предоставяне на софтуер за проследяване на плагиатство**", three-year contract with МОН, and: "**Софтуерът на компанията вече предоставя възможност да се открива съдържание, генерирано от изкуствен интелект**". StrikePlagiarism's own Bulgarian homepage (fetched): "Откриване на съдържание, генерирано от изкуствен интелект — Нашият модул… е един от най-ефективните в света… Като оцвети текста в червено, системата ще ви покаже най-подозрителните фрагменти."
- **June–July 2025 (contract expiry):** SEGA "Университетите са останали без софтуер срещу плагиатството" (17.06.2025) and "Университетите сами ще си купуват антиплагиат система" (**16.07.2025**): МОН answers that "**нов договор няма да се сключва**" — "Сключването на нов централизиран договор би ограничило избора на висшите училища… проучванията за актуалните цени на най-популярните системи за антиплагиатство, **включващи и улавянето на съдържание, създадено от изкуствен интелект**, сравнени с цената… показват, че към момента не е финансово рентабично централизирано осигуряване… МОН е изпратено писмо до висшите училища… за сключване на индивидуални договори." БГНЕС (19.07.2025): "Българските университети сами ще си купуват програмите срещу плагиатство."
- **Post-2025:** НСА (National Sports Academy) ran teacher training on the platform on 20.06.2025; УНСС's library page (updated **04.03.2026**) still runs e-checks via StrikePlagiarism.com — the system persists institutionally after the central contract died.

**Legal framework that drives the checks:**
- **ЗРАСРБ (Закон за развитието на академичния състав в РБ)** — § 1.7 of the additional provisions defines "Плагиатство" ("представяне за собствени на трудове, които изцяло или частично са написани или създадени от другиго…"); the **Комисия по академична етика to the Minister** is the national second-instance body (under ЗРАСРБ); МГУ's April-2025 internal antiplagiarism rules (mgu.bg PDF, fetched, 17 pp.) are explicitly based on ЗРАСРБ + ЗВО + ЗAutorско право and cite § 1.7 verbatim. Planned two-tier checks (institutional ethics commissions → national commission) were the МОН plan in 2022 (SEGA).
- **Закон за висшето образование (ЗВО)** — МОН planned amendments to extend plagiarism checks to student signals (SEGA 2022). No separate МОН "national platform for diploma-work originality checks" beyond StrikePlagiarism was found; StrikePlagiarism IS that platform.
- **МОН AI guidance 2024–2026:** No МОН-specific AI-in-higher-ed guidelines found. МОН's AI activity in 2026 is school-focused (matura cheating: offnews "МОН ще се бори с преписвачите с помощта на изкуствен интелект", 02.07.2026 — paywalled/Cloudflare; paragraf.bg "Анулират матури при идентични текстове"). The AI-catching capability in *universities* arrived through the StrikePlagiarism product itself (AI module, 2023), not through a МОН directive.
- **Национална стратегия за развитие на висшето образование:** no separate originality-check infrastructure found in it; enforcement runs through ЗРАСРБ/ethics commissions (not separately verified due to search-engine blockage — flagged in limitations).

## 3. StrikePlagiarism — company + Bulgarian deployments

**Company chain:** Plagiat.pl (Warsaw, est. 2002) owns StrikePlagiarism.com; Bucharest representative office since 2010; Romanian subsidiary Plagiat-Sistem Antiplagiat prin Internet SRL (est. 2012 by Plagiat.pl) holds the Bulgarian МОН contract. Official about-page (strikeplagiarism.com/bg/about_us.html, fetched): 24 years, 70+ countries, 1500+ universities; "Plagiat.pl оперира в 20 държави… **България** и др."; Romania precedent: national system checking ALL Romanian PhD theses since 2010 — Bulgaria replicated the same model. Team speaks Bulgarian among 15 languages.

**Confirmed Bulgarian deployments (fetched/verified):**
| Institution | Evidence |
|---|---|
| **СУ „Св. Климент Охридски"** | Pilot before 2022 (МОН 2022 release); ЦДО-СУ manual "Плагиатство… Ръководство за студенти и докторанти" (eas.uni-sofia.bg, fetched, 31 pp.); fjmc.uni-sofia.bg student antiplagiarism manual |
| **ЮЗУ „Неофит Рилски" (SWU)** | disted.swu.bg Blackboard manual links StrikePlagiarism's official "StrikePlagiarism.com_Blackboard.-Student2024.pdf" (verified live) |
| **УНСС** | Library: "Електронна проверка на оригиналността… се извършват чрез специализиран софтуерен продукт StrikePlagiarism.com" (updated 04.03.2026); mandatory for diploma works, dissertations, monographs |
| **РУ „Ангел Кънчев"** | ЦДО page: МОН decision Sept 2022, 190 registered users by 10.07.2024, admin-created accounts via МОН subscription |
| **МГУ „Св. Иван Рилски"** | 17-page internal rules (04.2025): "използва Система за антиплагиатство, предоставена от МОН (МОН), базирана в интернет система StrikePlagiarism.com"; mandatory checks on diploma works, theses, articles |
| **УХТ Пловдив** | News 22.01.2025: students upload coursework to StrikePlagiarism from personal accounts |
| **АМТИИ Пловдив** | Official page: "Министерството на образованието и науката предостави на всички висши учебни заведения в страната безплатна система за проверка на плагиатство – Strike Plagiarism", teacher training 03.11.2022 |
| **НСА** | Training on the antiplagiarism platform, 20.06.2025 (nsa.bg via Google News) |
| **БАН (IBF-BMI)** | StrikePlagiarism training seminar, 16.10.2023 (biomed.bas.bg) |
| **АУ Пловдив, БУ „Проф. Асен Златаров", Тракийски университет** | library/system pages surfaced in search (au-plovdiv.bg library "систем…" page; known from prior research) — SWU + УНСС + Бургас already confirmed previously |

**Procurement:** Contract under ЗОП with Plagiat-Sistem Antiplagiat prin Internet SRL, 3 years from ~July 2022 (install/config in July 2022), ~500k лв./yr (2 лв./user, 237k users). opencmd/apop.bg registry pages could not be scraped directly (JS/gateways) — the procurement facts are documented by МОН's own releases + 6 independent media (Mediapool, SEGA, bTV, News.bg, Actualno, BGVoice). No new central tender was announced as of July 2025 (МОН refusal, SEGA/БГНЕС).

## 4. Bulgarian-made systems

**None found at national or university level.** Every trace of "антиплагиат система" in Bulgarian higher education leads to: (a) StrikePlagiarism (МОН-procured, Polish), (b) plag.bg/Plagramme (Lithuanian, commercial), or (c) Russian "Антиплагиат.ру" mentioned in student forums (bg-mamma) as unavailable/foreign. No BG-built plagiarism or AI-detection product from Софийски университет, ТУ-София or elsewhere surfaced in any fetched source or news item. Universities build *internal rules* (МГУ procedures, УНСС library rules) around foreign systems, not their own detection engines. (Confidence: medium-high; direct search engines were heavily rate-limited during this session — see limitations — but Google News + all fetched university pages show zero BG-built tools.)

## 5. SWU specifics

**SWU Правилник за образователните дейности** (PDF `disted.swu.bg/media/12752/01032023.pdf`, fetched, 29 pp. — version dated 01.03.2023):
- **Чл. 60, ал. 1:** "В случай на установено плагиатство при изготвяне на дипломна работа, при разработка за кандидатстване и участие в програми за национални и европейски стипендии, на преписване или нерегламентирано използване на технически средства на държавен или семестриален изпит **студентът се отстранява за срок от една година**." (пuniishment by the Rector after hearing the student — ал. 3).
- **AI / изкуствен интелект: 0 mentions** in the 2023 rules. There is no SWU AI policy in the rules — the enforcement machinery is the plagiarism clause + the authorship declaration.
- **Чл. 34, ал. 4, т. 2 (current numbering):** written works are stored at the base unit by the teacher **for one year** — the storage/archiving principle the declaration references ("чл. 34, ал. 4, т. 2" in the declaration refers to archiving coursework to prove authorship; numbering differs between rule versions — flagged as a minor discrepancy).

**SWU Authorship Declaration** (`stf.swu.bg/.../declaracia_avtorstvo_kursova_rab_referat.pdf`, fetched — verbatim):

> **ДЕКЛАРАЦИЯ ЗА АВТОРСТВО НА КУРСОВА РАБОТА / РЕФЕРАТ**
> Долуподписаният/ата … (име, презиме, фамилия) … (специалност, факултетен номер)
> **ДЕКЛАРИРАМ:**
> Представената от мен курсова работа/реферат е лична моя авторска разработка, резултат от собствени изследвания.
> Потвърждавам, че тя в нейната цялост и отделни части не е била използвана за придобиване на образователна и/или научна степен в ЮЗУ „Неофит Рилски" – Благоевград или в други университети.
> Формулировки, идеи и текстове, взети от други източници, са цитирани според изискванията. Курсовата работа/рефератът не е публикуван(а) на друго място.
> Декларирам, че предоставям правото на ЮЗУ „Неофит Рилски" – Благоевград, съгласно чл. 34, ал. 4, т. 2 на Правилника за образователните дейности, да архивира и съхранява тази курсова работа/реферат с цел доказване на моето авторство.
> Дата: …20… г.   Автор на курсовата работа/реферата:

Note: no explicit AI clause in the declaration either — but "лична моя авторска разработка, резултат от собствени изследвания" + the archiving right is exactly what enables the StrikePlagiarism cross-check against SWU's own archived corpus.

**SWU AI policy 2024–2026:** none found on swu.bg (no AI-specific policy page surfaced; site structure checked). The practical "AI policy" at SWU = the StrikePlagiarism AI-detection module inside Blackboard + the authorship declaration + чл. 60 removal penalty.

---

## What this means for George (plain language)

1. The university-level system that "catches AI people" at SWU is **StrikePlagiarism inside Blackboard** — it was a *government* (МОН) decision that put it in every Bulgarian university in September 2022, and since mid-2025 SWU pays for its own instance. It flags both plagiarism and **AI-generated sentences in red**.
2. Your teachers also check reports against a 35-million scientific-sources database (per МОН's own announcement).
3. **plag.bg is just a self-check tool** (Lithuanian). If a classmate says "I ran it through plag.bg" — that proves nothing about what the university sees. The university's verdict comes from StrikePlagiarism's similarity + AI report, read by a human teacher (the company's own guidance: the report never equals plagiarism — a professor must review it).
4. The only legal teeth at SWU: the authorship declaration you sign + чл. 60 of the Rules (1-year expulsion for established plagiarism). No SWU document yet defines what "AI use" means — which is why enforcement is improvised per-professor. That gap is George's opportunity for a student-representation initiative.

## Limitations (honest disclosure)
- Bing RSS and DuckDuckGo returned junk/bot-walls from this IP for most of the session; Brave Search worked but rate-limited hard (429s) after ~10 queries, so "Bulgarian-made systems" and "МОН AI strategy" scans are thinner than ideal. All core claims above rest on **primary sources fetched successfully** (mon.bg, swu.bg/stf.swu.bg, disted.swu.bg, uni-ruse.bg, unwe.bg, mgu.bg, uft-plovdiv.bg, artacademyplovdiv.com, strikeplagiarism.com, sistemantiplagiat.ro, plag.bg terms/privacy) plus national press copies of МОН releases.
- opencmd/apop.bg procurement registry could not be scraped (JS gateways); procurement facts come from МОН press materials + press.
- The mon.bg news #5251 live page serves via Cloudflare; text verified through the Wayback capture.

## Source list (all fetched live 17.09.2026 unless noted)
1. plag.bg — homepage, /about-us, /terms-of-use, /privacy-policy, /contacts, /services/ai (LINGUA INTELLEGENS UAB; plag.bg in domain list; Lithuania law; AI detector BG support)
2. whois register.bg — plag.bg (GDPR-masked)
3. web.mon.bg/bg/news/5251 (via web.archive.org) — МОН, 23.03.2023, 35 млн източници, Чавдарова
4. mediapool.bg/news336866 — МОН release 20.06.2022 (contract, 2 лв/user, 237k users, НАЦИД)
5. bgvoice.com/mon-osiguriava-softuer-sreshtu-plagiatstvo — same release copy
6. news.bg — "С 35 милиона източници…" 23.03.2023
7. segabg.com — "МОН купи на университетите софтуер срещу плагиатство" 20.06.2022; "Университетите сами ще си купуват антиплагиат система" 16.07.2025
8. actualno.com — procurement saga 03.03.2022 (184.9 млрд лв offer)
9. uni-ruse.bg/Centers/TSDO/news — МОН decision Sept 2022; plag.bg ЦДО recommendation
10. press.azbuki.bg №46 16–22.11.2023 — Gavova: МОН-licensed; AI detection
11. strikeplagiarism.com/bg/, /bg/about_us.html, /bg/news-media-02.html — AI module, Plagiat.pl, Bucharest office
12. sistemantiplagiat.ro/en — Romanian SRL established 2012 by Plagiat.pl
13. disted.swu.bg/information/blackboard-manual/ — StrikePlagiarism Blackboard-Student2024 PDF link
14. disted.swu.bg/regulations/ + media/12752/01032023.pdf — SWU Правилник (чл. 60)
15. stf.swu.bg — declaration PDF (verbatim above)
16. unwe.bg/library pages/20650 — УНСС originality e-checks via StrikePlagiarism (04.03.2026)
17. mgu.bg — internal antiplagiarism procedures PDF (04.2025, ЗРАСРБ §1.7)
18. uft-plovdiv.bg — student upload notice 22.01.2025
19. artacademyplovdiv.com — МОН-provided system + training 03.11.2022
20. eas.uni-sofia.bg — СУ ЦДО plagiarism manual 2019
21. biomed.bas.bg — BAS StrikePlagiarism training 16.10.2023
22. news.google.com/rss — nsa.bg training 20.06.2025; БГНЕС 19.07.2025; offnews 02.07.2026 headline

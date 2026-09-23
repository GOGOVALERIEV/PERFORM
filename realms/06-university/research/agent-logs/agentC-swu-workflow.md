# AGENT C — SWU's Actual Checking Workflow + The Safe Pipeline
*Research agent log · 2026 · Mission C: SWU / Blackboard / StrikePlagiarism mechanics & countermeasures*

---

## VERDICT — How checking actually works at SWU + the exact safe pipeline

**How it works.** SWU "Neofit Rilski" runs Blackboard Learn 9.1 at `disted.swu.bg` (Център за дистанционно обучение) with StrikePlagiarism.com (Polish vendor Plagiat.pl, Warsaw) integrated as an LTI tool. The integration is real and documented: SWU's own student Blackboard manual page ends with a direct link titled **"Ръководство за работа с инструмента StrikePlagiarism"** pointing to the official `StrikePlagiarism.com_Blackboard.-Student2024.pdf`, and the teacher manual links the Instructor 2024 PDF. StrikePlagiarism is also the **national system** provided to all Bulgarian universities by МОН (Ministry of Education) as SaaS — confirmed verbatim in Shumen University's internal rules ("предоставя от Министерството на образованието и науката чрез услугата SaaS: StrikePlagiarism.com").

**The machine layer.** When a professor creates a StrikePlagiarism assignment in Blackboard, each submission is checked against: (1) the internet, (2) the university's own document database (home DB — **every paper ever uploaded at SWU stays there**, so past years' papers on similar topics will match), (3) the Database Exchange Program (other universities' databases, cross-checked without revealing their content), and (4) RefBooks (~200M+ scientific texts). It also detects paraphrases (SmartMarks), text manipulation (Cyrillic/Latin letter swaps, hidden characters, micro-spaces), can run translated-translation matching (100+ language pairs), and — if the professor enables it — an **AI Content Detection module** that colors each fragment by AI-probability (green→red) and gives a per-document AI Content Probability Coefficient (AIPC, 0–100%).

**The human layer decides everything.** The report explicitly states (in both the official BG interpretation guide and Shumen's rules): *"Системата не посочва дали документът съдържа плагиатство"* — the system only informs; the lecturer reads the report, can **accept/exclude** fragments and sources (quote-exclusion button recalculates the coefficients), and then issues a final decision: Accept / Send for correction / Reject (Disqualify). Thresholds at Bulgarian universities that published them are generous, not paranoid: **Shumen University (ШУ): "high similarity" = КС1 > 50% AND КС2 > 5%**; StrikePlagiarism itself recommends NOT setting hard limits, only that КС2's word-count parameter be 2–25 words. At SWU specifically, there is **no published similarity threshold and no published AI-percentage rule** — the decision is fully at the professor's discretion (Учебен правилник чл. 34: текущ контрол; чл. 60: документална измама → отстраняване).

**AI detection is a flag for conversation, not a conviction.** Even StrikePlagiarism admits its AI module is probabilistic: "The coefficient is not a measure of the ratio of AI-generated text"; "If the author has a low Similarity Coefficient but a high AI Content Probability Coefficient, this is most likely a false response from the system"; they recommend analyzing *a series of documents by the same author* rather than a single submission. Their own BG interpretation guide says high coefficients "не бива автоматично да бъдат счетени за плагиатство". So a flagged paper does not auto-fail — it triggers a human look, and at BG universities the documented escalation is: professor requires re-doing the assignment (ШУ чл. 14), for final theses the decision goes to the scientific jury / state exam commission (ШУ чл. 15), and proven exam fraud at SWU is handled under чл. 60 of the Учебен правилник.

**The safe pipeline (one paragraph).** Write the paper from your own outline, draft by draft, in your own words, with real sources; quote sparingly and format every quote correctly (quotation marks + citation + bibliography entry — correctly formatted quotes go into a purple "quotes" layer and can be excluded by the lecturer, but only if they're properly formatted); keep sentences your own so no 25-word identical stretch (КС2) with any source exists; check yourself **before** submission on a tool that does NOT feed its database (plag.bg explicitly promises "Вашите файлове никога не се добавят към каквато и да е сравнителна база данни") — never on the official system twice, because the first submission is stored and cross-compared forever; if two classmates write related papers, expect them to trigger each other in Cross-Check, so agree on disjoint sources/angles and don't share sentence-level text; and keep your draft history (Google Docs versioning, notes) as your human evidence if AI is ever suspected. Quality and a clean report are the same move: original sentences, honest citations.

---

## 1. The two Blackboard manuals (dissected)

Both PDFs fetched and extracted (they are screenshot-based step manuals with short captions):

**Student manual** (`https://strikeplagiarism.com/en/assets/files/StrikePlagiarism.com_Blackboard.-Student2024.pdf`, 7 pages):
- Student logs in → picks the course from the course list → clicks content → selects an assignment → **submits the document**.
- After submission the document **status changes**. Once the teacher has checked and graded, the student can see the result **and view the report**.
- Report statuses visible to the student (right side of the screen): **Processed / Rejected / Accepted**.
- **Resubmission rule:** "If the document [is] rejected, the student can submit a new version of the paper but **only as many times as set by the supervisor during creating the assignment**." → resubmission is per-assignment, professor-configured, not guaranteed.
- Student then opens the **interactive report** to read the teacher's comments.

**Instructor manual** (`https://strikeplagiarism.com/en/assets/files/StrikePlagiarism.com_Blackboard.-Instructor2024.pdf`, 7 pages):
- Teacher logs in → selects course → chooses content → finds **StrikePlagiarism.com** (LTI tool) → enters Assignment title, instructions, grade, deadline → "Add an assignment".
- Once verification is over, the teacher opens the report **by clicking on the Similarity score**, grades inside the interactive report, and uses **Submit / Reject** buttons plus a score field.

**What the student does NOT see in Blackboard:** per the standalone system's documentation (knowledgebase), "The student does not have access to the interactive Similarity Report. The student cannot accept fragments or add comments. The student cannot add documents to the database." In practice the Blackboard LTI flow does surface a status + report link to the student after grading, but the *levers* (accepting fragments, excluding quotes, final verdict) are professor-only.

## 2. The StrikePlagiarism machine — full mechanics

### 2.1 Similarity coefficients (the numbers that matter)
From the knowledgebase and the official BG interpretation guide (`strikeplagiarism.com/bg/assets/files/Strikeplagiarism_com_BG_Univ_Similarity_Report_Interpretation.pdf`):

- **КС1 / SC1** — % of the document containing phrases of **5+ words** found in: the university home database, Database Exchange Program, RefBooks, or internet (legal-acts matches excluded). Measures "linguistic independence".
- **КС2 / SC2** — same databases, but phrases of **25+ words** (word-count configurable 2–25 by the university). This is the *serious-borrowing* number: long identical stretches can't be accidental.
- Quotes: "Системата ще приеме само заемки, които са цитирани правилно. Системата не изключва цитатите от другите коефициенти" — **properly formatted quotes are recognized but NOT auto-excluded**; the lecturer has a one-click "exclude quotes" button that recalculates the coefficients. So sloppy quotes stay counted; clean quotes get removed by a human who bothers.
- Template phrases, bibliography, and legal-act fragments are classified as citations/acceptable fragments.

### 2.2 What gets flagged and in which color (Similarity Report color code)
1. **Green** — fragments found in global internet resources
2. **Red** — fragments found in databases: the client's own DB **and other clients' databases** shared for cross-checking (two shades of red = multiple fragments from one source, order changed)
3. **Blue** — fragments of the currently selected source (everything recolors to blue when you click a source)
4. **Orange** — fragments found in **RefBooks** (the scientific repository)
5. **Blue background** — Legal Database matches (Wolters Kluwer legal acts)
6. **Yellow background** — characters from another alphabet (Cyrillic↔Latin lookalike swap detection)
7. **Purple background** — texts within quotation marks (correctly marked quotes)
Plus **SmartMarks (Paraphrases)** — lighter shade + underline on fragments that are *similar but not identical* (word-order changes, synonym swaps). Hovering shows the original source text.

### 2.3 Manipulation alerts (the system catches tricks)
Alerts list: **Characters from another alphabet** (e.g. Latin "c/e/r" swapped for Cyrillic "с/е/г"), **Spreads** (stretched letters faking spaces), **Micro spaces**, **Hidden characters** (white-colored text), **Paraphrases (SmartMarks)**. The guide is explicit that these are invisible on a printout but distort the analysis — and they're reported to the grader as an alerts section. **Conclusion: every classic "обход" trick is detected and itself looks worse than similarity.**

### 2.4 Databases — including BG student papers (Q4 answer)
From `strikeplagiarism.com/en/databases.html`:
- Internet (hundreds of millions of pages; "finds similarities even if the text has been translated or significantly changed")
- **Client database** (the university's own archive) and **between partner databases** via the **Database Exchange Program** — "without the ability to access the content of the text and reveal personal data"; the databases of clients include **"student papers, abstracts, term papers and other types of documents"**
- **RefBooks**: 200M+ texts — dissertations, monographs, publications, textbooks, 100+ languages, Scopus/WoS journals, arXiv, Paperity, Termedia
- Storage: GDPR, EU servers (Germany/France), ISO/IEC 27001:2022; documents saved in the DB are "protected against copying and disclosure"; accepted papers can be added to the DB on Accept.
- **So yes: BG student papers from previous years are in the comparison set** (SWU's own archive at minimum, plus every BG university that shares its DB through МОН's national deployment). A paper copied from a senior student's paper — or your own older paper — will match red.
- Russian-market analysis (anti-antiplagiat blog, 2022) adds: system memory holds 50M+ checked documents; Plagiat.pl operates in ~20 countries incl. Bulgaria; integration with Oxford/Cambridge/Springer aggregator Paperity.

### 2.5 Translated matching
Optional per-upload feature: the system machine-translates the document into a chosen language (100+ combinations), then checks the translation against databases/internet. Enabled by the **professor** at upload. A paper "translated" from a foreign source gets caught if the professor ticks this.

### 2.6 AI Content Detection module (Q2 answer)
Module name: **"AI Content Detection"** (section inside the Interactive Similarity Report; also marketed as "AI Content Indicator" / AIPC). Dedicated page: `strikeplagiarism.com/en/AI-detection.html`.

Claims:
- Detects text from "the latest AI models like GPT-5.4, GPT-5.1, GPT-5, GPT-4o, ChatGPT, Claude, Gemini, DeepSeek, Grok"
- **Method:** supervised learning, "several models, including a modified BERT model", trained on millions of AI vs. human texts; plus linguistic analysis (template phrasing, repeated phrases), statistical analysis (uniform sentence structure/length), ML classifiers
- **Languages:** "over 100 languages" (homepage says "30+ languages"; the BG homepage claims "един от най-ефективните в света"). No explicit Bulgarian claim in the language list we retrieved, but the listed set is broad and the module is offered to BG universities nationally.
- **Accuracy claims:** homepage: "98%+ accuracy with less than 1% false-positive rate"; the dedicated page: "**over 94% accuracy**" — internally inconsistent marketing numbers.
- **How it marks:** each fragment gets a probability 0–100% and a color in 5 ranges (green = minimal machine probability → red = maximum); overall **AI Content Probability Coefficient (AIPC)** = average. A slider (**default threshold 0.8 = 80% AIPC**) recomputes an "AI content Indicator" showing only fragments above the chosen level (60%, 80%...). Fragments can be filtered ("Show in text"), sorted high→low, and the AI report exports to PDF.
- **Crucial caveats in their own words:** "This section does not reflect the amount of text written by AI, but the probability of its use"; "If the author of a paper has a low Similarity Coefficient but a high AI Content Probability Coefficient, this is most likely a **false response** from the system, so the document should be analyzed in detail"; "we recommend that you pay attention to texts that exceed a 50% AIPC", but "if a text fragment has similarities found in any source but the AIPC exceeds 50%, it means the system does not respond correctly to this text fragment"; "no AI detection system is absolutely perfect"; they recommend analyzing **a series of documents by the same author**, not one submission; "the longer the text, the higher the detection reliability."
- **Independent tests 2024–2026:** we could not retrieve any independent evaluation specific to StrikePlagiarism's AI module (search engines heavily bot-blocked during this session — Bing RSS poisoned with unrelated results, Brave/Startpage/Mojeek/Ecosia/DDG all captcha/429 from this IP). General state of the field (widely documented): AI detectors including BERT-style classifiers have documented false-positive problems, especially for non-native-English authors and for human-edited AI text; vendor self-reported accuracy is not third-party-verified. **Treat the 94–98% claims as marketing until proven otherwise.**
- March 2, 2026 system update: new Similarity Report UI — "purely visual; calculation methodology unchanged; plagiarism and AI detection results are not affected."

### 2.7 Assignments, Cross-Check, and what the student sees
- Assignments module: professor creates assignment (title, description, due date, student e-mails or a join short-code), recommends uploading **all documents simultaneously**, then the batch is analyzed together and each report gains a **cross-check section** — "the system has checked if there have been any borrowings of text **between the student works**".
- **Cross-Check "does not influence the similarity coefficients"** — it's a separate side-report ("Show Comparison" shows two students' texts side by side, highlighted blue). So copying a classmate inflates nothing in КС1/КС2 *unless the classmate's paper is already in the home DB*, but the professor sees the pairwise match directly.
- Student in the standalone system: joins via short code, uploads, **cannot see the interactive report**, cannot accept fragments, cannot add to DB. (Blackboard LTI gives status + report visibility after grading, per the student manual.)
- Lecturer final decisions in the report: **Save changes / Disqualify-Reject / Send for correction / Accept (adds to database)**. Some institutions set blinking-icon threshold alerts on КС.

## 3. SWU ground truth (Q3)

- `disted.swu.bg` = SWU's Distance Learning Center (ЦДО) Blackboard. Student manual page (`/information/blackboard-manual/`) lists 16 Blackboard guide PDFs (assignments, secure assignment, grading, groups...) and **one external link: the StrikePlagiarism Student 2024 manual**. Teacher manual page (`/information/blackboard-manual-teacher/`) similarly links the **Instructor 2024 PDF** plus extra PDFs (progress monitoring, usage statistics). ⇒ the tool is presented as a **standard part of both the student and teacher toolchain**, not a hidden option.
- **Is it on EVERY assignment?** Not provable from public pages. Mechanics say it's **opt-in per assignment**: the professor must explicitly add the StrikePlagiarism LTI item and configure deadline/resubmissions/AI-check. However: (a) МОН funds the national license for all state universities, so cost is not a barrier; (b) SWU lists it in both core manuals; (c) BG practice (ШУ rules) makes checking **mandatory for diplome works/theses and optional-but-typical for course assignments**. Realistic reading: **diploma theses → always checked; semester assignments/реферати → professor's choice, and increasingly common.** Students should assume any uploaded assignment *can* be checked.
- The "Сигурно задание" (Secure Assignment) PDF on disted.swu.bg is a legacy Blackboard 9.1 SafeAssign-style guide (january 2013) — secure browser-locked assignments with submission logs; separate from StrikePlagiarism but shows SWU's long-standing anti-copy posture.
- **Учебен правилник** (`disted.swu.bg/media/1043/pravilnik_swu_16-04-2014.pdf`, 30 pp.): full-text search shows **zero occurrences of "плагиатство"** and zero of "авторство"/"честност". What it does contain:
  - **Чл. 34 /1/**: "Знанията и уменията на студентите… се проверяват и оценяват чрез **изпити и текущи оценки**, съгласно учебния план" — текущ контрол is the legal basis for all semester assignments; /7/: "През семестъра преподавателите провеждат **текущ контрол**… Формите на контрол се посочват в учебната програма… Оценките от текущия контрол се вписват в изпитния протокол и се отчитат при оформянето на окончателната оценка." → your semester paper grade legally flows into the final course grade.
  - **Чл. 60 /1/**: "При установена **документална измама** студентът се **отстранява за една учебна година**, а при по-тежки случаи – и окончателно, като се сезират съответните органи." → the SWU fraud clause (documented fraud at exam = 1-year removal; the plagiarism/AI case law at SWU runs through this + academic-ethics channels, since the 2014 правилник predates AI and has no explicit plagiarism article).
  - Задочно-education chapters: the professor "възлага разработване на **реферати, курсови работи**, задачи за самостоятелна работа, казуси" during присъствени периоди; students must "изпълнява възложените форми на текущ контрол (тестове, казуси и други) в съответствие с утвърдените срокове".
- **Чл. 34 of the "Правилник за образователните дейности" referenced in the declaration:** the text uploaded to us references a declaration citing чл. 34; the public Учебен правилник's чл. 34 (quoted above) is about текущ контрол, not plagiarism — so the declaration's чл. 34 anchor is either the same article (obligation to personally perform текущ контрол forms) or an article of a newer/other правилник not publicly retrievable at the cited path. Flag for verification against the PDF George actually signed.
- SWU normative-documents hub lives on the main site (`swu.bg`), not disted; direct .aspx paths 404'd (site restructured). A newer SWU-specific antiplagiarism instruction may exist behind the student portal (ais.swu.bg / stud.swu.bg) which requires login.

## 4. What actually makes a report look bad (Q4)

Ranked by how much it hurts, per the vendor's own interpretation guide + ШУ rules:
1. **Long identical stretches (КС2).** The guide: documents "съдържащи фрагменти, които надвишават КС2… особено ако са в горната часть на списъка" — if the longest-matches list is full of your text and the fragments are "дълги текстови фрагменти… разделени само от кратки фрази", that "предизвиква подозрение". Scattered 5-word coincidences = "случайни заемки" and get accepted.
2. **Red sources (databases)** — especially the **home database**: matching another student's past paper, a thesis, or your own earlier submission. Red beats green in the grader's eye because it means "someone at a university wrote this before you".
3. **Manipulation alerts.** Any alert (letter swaps, hidden chars, micro-spaces) converts "lazy student" into "intent to deceive" — the one thing that escalates to чл. 60 territory. Never touch these.
4. **Unformatted quotes.** Quotes are only protected if correctly formatted (quotation marks, reference, bibliography). The system marks proper quotes purple but **doesn't exclude them from the coefficients** — the lecturer must click. Wrong citation = plain similarity.
5. **Cross-Check match with a classmate.** Doesn't move КС1/КС2 but is shown pairwise — two similar papers in one batch are the easiest catch in the whole system.
6. **AI AIPC** — only if the professor enabled the module; a high AIPC with low similarity is, per the vendor itself, "most likely a false response", but it *will* be read by a human who may not be charitable.
7. **Translated plagiarism** — only if the professor enables translation checking; remember it's one toggle for them.

**Published BG thresholds found:** Шуменски университет "Епископ Константин Преславски", Вътрешни правила за използване на система за антиплагиатство, протокол РД-05-02/25.09.2024 — **"За висок процент на сходство се приема, когато КС1 надхвърля 50%, а КС2 надхвърля 5%, но тези стойности не посочват автоматично плагиатство."** Plus: чл. 8 — **students and PhD students may run a preliminary self-check of their own texts in the System**; чл. 14 — exceeding the thresholds in a semester assignment lets the professor **require the task to be redone**; чл. 15 — for theses/competitions the final call belongs to the научното жури / ДИК / редакционна колегия. No SWU-specific published threshold found (checked disted.swu.bg, swu.bg, and search — SWU relies on the 2014 правилник + professor discretion).

## 5. The safe pipeline (Q5)

### 5.1 Drafting
1. **Outline first, from the assignment brief.** List the 4–7 sections and what *you* will claim in each. The outline is the fingerprint of independent work; the report flags text, not structure.
2. **Write from the outline in your own words, source notes closed.** Read a source, close it, write the point from memory, then reopen to verify numbers and add the citation. Sentence-level copying happens when you write with the source open — so don't.
3. **Quote rarely and format perfectly.** Quotation marks + footnote/in-text reference + bibliography entry. Correctly formatted quotes land in the purple layer, recognizable and excludable. Quotes are also limited naturally: if you quote 30% of a paper, the *ideas* aren't yours and a human will notice regardless of the coefficient.
4. **Never reuse old papers** (yours or others') — the home DB and Cross-Check are exactly matched against them, red, with the original on file for the professor to open.
5. **Watch your own КС2-prone patterns:** definitions, laws, standard phrases ("Както вече споменах…"), discipline jargon chains — the guide warns these inflate coefficients; paraphrase them, shorten them, or quote them properly.

### 5.2 Pre-self-check
- **plag.bg** (Plag's BG self-check service): upload free, **"Вашите файлове никога не се добавят към каквато и да е сравнителна база данни и никога не се споделят с други проверяващи"** — safe, and it has its own **AI detector**, marks paraphrases orange / improper quotes purple / correct quotes green, 129 languages. Use it the day before submission: fix orange paraphrases, fix purple quotes, check AI-marked fragments and rewrite them in your own voice.
- Alternative: the official **free check tool** `check-paper-for-plagiarism.strikeplagiarism.com` (individual tokens; free demo checks are limited and — important — a StrikePlagiarism check stores the text in *their* ecosystem; an individual-account check is checked only against internet+RefBooks, not the university DB).
- **ШУ-style self-check inside the university system is officially allowed there** ("студентите и докторантите могат да осъществят предварителна (самостоятелна) проверка в Системата") — if SWU enables it, one self-check via the professor is legitimate; but as a default rule: **submit to the official system once, final.** Every extra run adds the text to comparisons.
- The other agents' simple web detectors (Quetext, etc.) are a weak proxy — they don't have the home DB or RefBooks, which is where SWU-dangerous matches actually live.

### 5.3 Cross-comparison with classmates (two students, related papers)
- If both submit to the same StrikePlagiarism assignment batch, **Cross-Check will show the overlap** side-by-side, even though the coefficients barely move. The professor clicks "Show Comparison" and sees both texts highlighted blue against each other.
- Also: whichever paper is uploaded first enters the pool; when the batch is analyzed together, both get compared mutually.
- **Countermeasure:** related topic ≠ shared sentences. Disjoint source lists (or at least disjoint *quote* choices), different structure, own examples. If you must discuss, discuss *ideas* — never trade text, not even "just one paragraph".
- If a classmate begs your old paper: it's in the DB anyway; lending it creates a red match against *you* months later with your name attached.

### 5.4 Worst case — professor manually suspects AI (BG procedure)
1. **The professor opens the AI Content Detection section** (if enabled) or just reads the paper and notices voice/style shifts. Per the vendor's guidance, a high AIPC alone is "not a measure of the amount of AI text" and professors are trained (МОН webinars) to treat it as a *signal for detailed analysis*.
2. **Разговор с преподавателя** — the realistic first step at course level: "защити работата си устно" — explain the structure, the sources, why you wrote it this way. ШУ чл. 14 gives the professor the right to **require the task to be redone** when similarity thresholds are exceeded; the same conversational route is the norm for AI suspicion.
3. **If it escalates** (thesis level or repeated): the report is exported to PDF and goes to the **катедра / научното жури / държавната изпитна комисия** (ШУ чл. 15) — at SWU the equivalent organs per Учебен правилник + академична етика; final theses decisions sit with the ДИК.
4. **Proven fraud:** SWУ чл. 60 /1/ — установена измама → **отстраняване за една учебна година**, worse cases → окончателно, with the case sent to the competent organs. For a semester paper the realistic spectrum is: re-do the assignment → grade 2 on it → in aggravated cases academic-ethics proceedings.
5. **Your defense is evidence of process:** version history (Google Docs/OneDrive), your notes and outline, ability to discuss every paragraph. The vendor itself tells graders to analyze "a series of documents written by the same author" — a student whose *other* work reads the same way, and who can defend the text orally, closes the conversation fast.

### 5.5 The pipeline on one screen
```
BRIEF → OUTLINE (own claims per section)
      → DRAFT from outline, sources closed, own sentences
      → quotes: few, formatted, in bibliography
      → SELF-CHECK on plag.bg (no-DB tool) + its AI detector
      → fix orange paraphrases / purple quotes / red-flag AI fragments
      → SUBMIT ONCE to Blackboard assignment (final version, .docx, clean formatting,
         no hidden chars, no letter swaps, nothing white-on-white)
      → if Rejected: professor-configured resubmission window — fix what the report says
      → KEEP: outline + drafts + version history (your human-proof)
```

---

## Sources (fetched live this session)
- `https://strikeplagiarism.com/en/assets/files/StrikePlagiarism.com_Blackboard.-Student2024.pdf` (7 pp., extracted)
- `https://strikeplagiarism.com/en/assets/files/StrikePlagiarism.com_Blackboard.-Instructor2024.pdf` (7 pp., extracted)
- `https://strikeplagiarism.com/en/` (homepage: AI claims, integrations, GDPR, ISO 27001)
- `https://strikeplagiarism.com/en/AI-detection.html` (module page: BERT, 94% claim, caveats, languages)
- `https://strikeplagiarism.com/en/databases.html` (DB exchange, RefBooks 200M+, EU storage)
- `https://strikeplagiarism.com/bg/` (BG homepage: Cross-Check, AI module red marking)
- `https://strikeplagiarism.com/bg/assets/files/Strikeplagiarism_com_BG_Univ_Similarity_Report_Interpretation.pdf` (16 pp. BG guide: КС1/КС2, colors, manipulation, interpretation rules)
- `https://knowledgebase.strikeplagiarism.com/the-system-from-a-to-z` (AIPC default 0.8, SmartMarks, cross-check, student rights, colors)
- `https://knowledgebase.strikeplagiarism.com/system-updates` (02.03.2026 UI update)
- `https://disted.swu.bg/information/blackboard-manual/` + `/blackboard-manual-teacher/` (SWU manuals + StrikePlagiarism links)
- `https://disted.swu.bg/media/1043/pravilnik_swu_16-04-2014.pdf` (Учебен правилник: чл. 34, чл. 60; no plagiarism article)
- `https://disted.swu.bg/media/16057/06сигурно-задание.pdf` (Secure assignment guide)
- `https://www.shu.bg/wp-content/uploads/file-manager-advanced/users/normativni-dokumenti/und/pravila-antiplagiat-25.09.2024.pdf` (ШУ thresholds КС1>50%, КС2>5%; self-check; escalation)
- `https://plag.bg/` (self-check tool, no-DB promise, AI detector, color scheme)
- `https://wiki.ut.ee/.../StrikePlagiarism` (University of Tartu: system overview)
- `https://ru.wikipedia.org/wiki/Strikeplagiarism.com` (company history, integrations)
- `https://xn----7sbbaar5acc1ard1a0beh.xn--p1ai/blog/strikeplagiarism-plagiat-kak-proverit-i-obojti` (market context, 50M archive, evasion tricks → all detected per §2.3)

**Research gaps (blocked by bot-walls, flag for a human with a browser):** independent 2024–2026 accuracy tests of StrikePlagiarism's AI module; SWU's own antiplagiarism instruction/threshold if one exists behind ais.swu.bg login; the exact declaration text referencing чл. 34; StrikePlagiarism /bg knowledgebase (Bulgarian-language student guides may exist beyond the EN ones).

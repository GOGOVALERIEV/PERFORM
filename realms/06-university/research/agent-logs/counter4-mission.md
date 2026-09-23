# MISSION 4 — Beat File Forensics: Metadata & Authorship Evidence
You are a countermeasure strategist agent. THINK + DESIGN. Output: an actionable playbook. Brief research allowed (curl; Bing RSS: https://www.bing.com/search?q=Q&format=rss) but deliverable is OPERATIONS.

## Context
When a professor manually suspects AI/copied work, file metadata is the cheapest forensic tool: .docx/.pptx/.pdf properties (Author, Last Modified By, Created, Modified, Total Editing Time, Application, Company), email timestamps, and version histories (Google Docs / OneDrive / Moodle logs). A file "created today, edited 4 minutes, Author: some-AI-tool" is a red flag regardless of any detector score. StrikePlagiarism's guide warns about manipulation alerts; professors are trained (МОН webinars) to analyze "a series of documents by the same author". The goal here is NOT forgery — it is producing documents whose metadata honestly reflects a real drafting process (because the pipeline will genuinely iterate drafts), plus building an authorship-evidence habit.

## Your problem to solve
Design "The Evidence Layer": rules so every submitted document's metadata and surrounding evidence tell a true story of genuine work.

## Deliver — the playbook
1. **Metadata field map**: exact list of forensic fields in .docx (docProps/core.xml + app.xml), .pptx, .pdf — what each says, what values look suspicious (Editing Time 0 min, Author mismatch vs the .py script name, Application = "python-docx"), and what natural values look like. Cite how python-docx/python-pptx set these by default.
2. **The honest-metadata workflow**: since the pipeline will genuinely go through multiple drafts (outline → draft → style pass → self-check fix → final), design it so saving iterations through a real editor (e.g., open each draft in Word/LibreOffice and save — which updates timestamps/editing time naturally) produces realistic metadata. Exact procedure per file format. What to never do (never fake timestamps — inconsistent metadata is worse than plain metadata; the goal is TRUTHFUL evidence of real process).
3. **Authorship evidence pack** (per assignment, stored in one folder): outline (dated), source notes, draft versions, self-check report (plag.bg), final file. What to keep, in what order, why each item helps in an oral defense. How Google Docs version history (if writing there) or local git history serves as tamper-proof evidence.
4. **The oral-defense checklist**: the 10 questions a professor asks ("защо избрахте тази структура", "какво е казаха Иванов (2023)", "обяснете този абзац") and how the evidence pack answers each. George must be able to discuss every paragraph — design the 15-minute pre-defense prep routine (read own outline → explain thesis per section → reconstruct 2 sources).
5. **Email submission hygiene**: if a professor collects by email — what the email metadata reveals, best practice (send from own Gmail, consistent name, attach .docx not links, subject format).

Write to `C:/Users/User/Desktop/PERFORM/realms/06-university/research/agent-logs/counter4-evidence-layer.md`. Then `counter4-progress.md` trail, final line "DONE".

"""
Build a big multi-TAB Google Doc teaching WW-2 + LFS:
  Tab 1: Big Picture
  Tab 2: How To Use WW-2
  Tab 3: How WW-2 Works (under the hood)
  Tab 4: The LFS System
  Tab 5: The Other Formats
  Tab 6: The Differences
  Tab 7: Reverse-Engineer Blueprint

Same tab-builder approach as the terms doc, with extra block types (h3, bullet, code).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_docs, get_drive

docs = get_docs()
drive = get_drive()
SHARE_EMAIL = 'marswasshere@gmail.com'


# ---------- request builders ----------
def para_style(tab_id, s, e, named):
    return {'updateParagraphStyle': {
        'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
        'paragraphStyle': {'namedStyleType': named}, 'fields': 'namedStyleType'}}


def text_style(tab_id, s, e, style, fields):
    return {'updateTextStyle': {
        'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
        'textStyle': style, 'fields': fields}}


def build_tab(tab_id, blocks):
    text = ''
    styles = []
    idx = 1
    for b in blocks:
        kind = b[0]
        if kind in ('title', 'h', 'h3'):
            line = b[1] + '\n'
            named = {'title': 'HEADING_1', 'h': 'HEADING_2', 'h3': 'HEADING_3'}[kind]
            styles.append(para_style(tab_id, idx, idx + len(line), named))
            text += line
            idx += len(line)
        elif kind == 'term':
            name, desc = b[1], b[2]
            line = name + ' — ' + desc + '\n'
            styles.append(text_style(tab_id, idx, idx + len(name), {'bold': True}, 'bold'))
            text += line
            idx += len(line)
        elif kind == 'bullet':
            line = '•  ' + b[1] + '\n'
            text += line
            idx += len(line)
        elif kind == 'code':
            line = b[1] + '\n'
            styles.append(text_style(tab_id, idx, idx + len(b[1]),
                                     {'weightedFontFamily': {'fontFamily': 'Courier New'}},
                                     'weightedFontFamily'))
            text += line
            idx += len(line)
        elif kind == 'note':
            line = b[1] + '\n'
            text += line
            idx += len(line)
    insert = {'insertText': {'text': text, 'location': {'index': 1, 'tabId': tab_id}}}
    return [insert] + styles


# ================= CONTENT =================

BIG_PICTURE = [
    ('title', 'WW-2 & LFS — THE BIG PICTURE'),
    ('note', 'Read this tab first. It fixes the one misunderstanding that makes everything else click.'),

    ('h', 'The one thing to get straight'),
    ('note', 'WW-2 is the FACTORY. LFS is ONE blueprint the factory builds from.'),
    ('note', 'They are not two rival systems — one lives inside the other. Asking "WW-2 vs LFS" is like asking "kitchen vs recipe". The kitchen (WW-2) can cook many recipes; LFS is one of them.'),
    ('note', 'So this guide teaches, in order: (1) the factory [WW-2], (2) one blueprint in full detail [LFS], (3) the other blueprints [the formats], (4) how LFS differs from those other blueprints — that last one is the comparison that actually means something.'),

    ('h', 'What WW-2 is'),
    ('note', 'An AI ad-script generation machine, nicknamed "Wonder Weapon". Boris built it. Its goal is to pump out around 1,000 direct-response ad scripts per day for health/wellness products (hair loss, joints, thyroid, menopause, etc.).'),
    ('note', 'You do not write ads by hand inside it. You hand it a code (a "task ID"), and the machine assembles and writes the ad for you, then checks its own work.'),

    ('h', 'The two Claudes (never confuse them)'),
    ('term', 'Claude Code', 'me — the engineer/teacher. I build, explain, and run the machine. I am talking to you right now.'),
    ('term', 'Claude API (Sonnet)', 'the factory worker INSIDE the machine. Every time the machine makes an ad, it calls this Claude to actually write the words. It never talks to you — it just produces scripts.'),
    ('note', 'Same brand, totally different jobs: one is the mechanic, one is the line worker.'),

    ('h', 'The 7 ideas that make the whole thing work'),
    ('bullet', 'Task ID = control panel: one short code decides product, format, angle, mechanism, everything.'),
    ('bullet', 'Format = template: the structure of an ad is stored separately from its content (LFS is one such template).'),
    ('bullet', 'Research = fuel: each product has files of archetypes, hotwords, and mechanisms the machine pulls from.'),
    ('bullet', 'Surgical context: it loads ONLY the few sections this exact ad needs (~800 tokens), not everything.'),
    ('bullet', 'Fresh process per ad: every ad is written in a brand-new Python process, so ads never pollute each other.'),
    ('bullet', 'Deterministic validation: a dumb, fast, no-AI checker enforces word counts, sections, forbidden words.'),
    ('bullet', 'Living quality gates: human corrections become permanent rules the machine obeys forever after.'),
]

USE_WW2 = [
    ('title', 'HOW TO USE WW-2'),
    ('note', 'The practical operator manual: setup, the control code, the commands, and the full workflow.'),

    ('h', 'Setup (one time)'),
    ('note', 'The machine needs an Anthropic API key in a .env file (so the factory-worker Claude can write), and per-product upload credentials.'),
    ('code', 'ww-2/.env                ->  ANTHROPIC_API_KEY=sk-ant-...'),
    ('code', 'products/{PRODUCT}/upload-config.json  ->  Google Docs + ClickUp + Meta keys'),

    ('h', 'The task ID — your control panel'),
    ('note', 'Everything starts with one code. This single string tells the machine exactly what to build:'),
    ('code', 'NOOR_LFS_ARC1_A1B2_M1_V001'),
    ('term', 'PRODUCT (NOOR)', 'which product. Maps to a folder in products/ with all its research.'),
    ('term', 'FORMAT (LFS)', 'which blueprint/template to use (LFS, YAPFEST, RVSL, OGVSL, DRPOV...).'),
    ('term', 'ARCHETYPE (ARC1)', 'which customer type — ARC1 to ARC5, defined per product (e.g. "the Velocity Hunter").'),
    ('term', 'ANGLE (A1B2)', 'two halves. A-point = the PAIN you enter through (A1 physical, A2 timing, A3 social). B-point = the DISCOVERY reframe (B1 science, B2 identity, B3 system-failure).'),
    ('term', 'MECHANISM (M1)', 'the unique reason the product works, copied verbatim from research (e.g. "The Thirsty Joints Trick").'),
    ('term', 'ROCK BOTTOM (optional)', 'the crisis-moment type — RBPUB, RBREL, RBPHOTO, RBSEARCH, RBEVENT. Inserted before the version if used.'),
    ('term', 'VERSION (V001)', 'iteration number. V002, V003... when you re-roll the same recipe.'),
    ('note', 'The machine accepts 6, 7, or 8-part IDs (older IDs also carried a HOOK type like RAGE; archetype now drives the hook).'),

    ('h', 'The commands you will actually use'),

    ('h3', 'generate — make one ad'),
    ('code', './tools/ww generate NOOR_LFS_ARC1_A1B2_M1_V001'),
    ('note', 'Writes a single script. Good for testing one recipe.'),

    ('h3', 'plan — build a batch recipe list automatically'),
    ('code', './tools/ww plan BATCH_001 -p NOOR -f lfs -a ARC1,ARC2 --angles A1B1,A2B3 -m M1'),
    ('note', 'Creates spec.json by mixing every archetype x angle x mechanism you list (a "cartesian product"). This is how you generate dozens of task IDs without typing them.'),

    ('h3', 'batch — make many ads in parallel'),
    ('code', './tools/ww batch BATCH_001 --workers 20'),
    ('note', 'Reads the spec.json, fires up to 20 ads at once (each in its own process), then auto-validates them all. This is the 1,000-ads/day engine.'),

    ('h3', 'validate — check an ad (no AI, instant)'),
    ('code', './tools/ww validate output/script.md --task-id NOOR_LFS_ARC1_A1B2_M1_V001'),

    ('h3', 'status — see how a batch did'),
    ('code', './tools/ww status BATCH_001'),

    ('h3', 'upload — push scripts to the team'),
    ('code', './tools/ww upload BATCH_001 --dry-run'),
    ('note', 'Creates Google Docs and ClickUp tasks for the creative team. Always --dry-run first to preview.'),

    ('h3', 'meta-upload — push creatives to Facebook/Instagram'),
    ('code', './tools/ww meta-upload BATCH_001 --dry-run'),
    ('note', 'Needs images + a headline in spec.json. Total creatives = copies x images.'),

    ('h3', 'visuals: storyboard / enrich / imagebatch'),
    ('note', 'storyboard turns a script into a shot-by-shot table; enrich appends a visual shopping-list + timeline; imagebatch generates the actual images (Gemini or fal.ai).'),

    ('h3', 'feedback: scan / learn'),
    ('note', 'scan watches the Meta Ad Library (what competitors run) into a database; learn turns a human correction into a permanent rule.'),
    ('code', './tools/ww learn "Product name must appear in the script body, not just the CTA"'),

    ('h', 'The end-to-end workflow'),
    ('bullet', '1. plan  -> build the recipe list (spec.json)'),
    ('bullet', '2. batch -> generate + auto-validate the scripts'),
    ('bullet', '3. review the outputs, re-roll failures (V002...)'),
    ('bullet', '4. storyboard / enrich / imagebatch -> add the visuals'),
    ('bullet', '5. upload -> hand to the creative team (Docs + ClickUp)'),
    ('bullet', '6. meta-upload -> launch the creatives'),
    ('bullet', '7. scan + learn -> feed performance + corrections back in'),
]

UNDER_HOOD = [
    ('title', 'HOW WW-2 WORKS (UNDER THE HOOD)'),
    ('note', 'What actually happens between "task ID" and "finished, checked ad". This is the part to truly understand if you want to build your own.'),

    ('h', 'The pipeline (task ID -> finished ad)'),
    ('bullet', '1. PARSE: split the task ID into its parts (product, format, archetype, angle, mechanism, rock bottom, version).'),
    ('bullet', '2. LOAD CONTEXT: open the product files and pull ONLY the needed sections (just ARC1, just A1, just B2, just M1...).'),
    ('bullet', '3. RENDER PROMPT: take the format template (formats/lfs/prompt.md), drop the loaded context into its {placeholders}, and attach the system prompt that teaches copywriting.'),
    ('bullet', '4. FRESH PROCESS: spawn a brand-new Python process for this one ad.'),
    ('bullet', '5. WRITE: call Claude API (Sonnet) with the system + task prompt. It returns an outline, then the full script.'),
    ('bullet', '6. SAVE + VALIDATE: strip the outline, save the .md file, and run the deterministic checker.'),

    ('h', 'Surgical context loading (the secret sauce)'),
    ('note', 'A product file might define 5 archetypes, 6 hotword sets, and 3 mechanisms. A naive system would dump ALL of it into the prompt — thousands of wasted tokens, and the AI gets confused by irrelevant material.'),
    ('note', 'WW-2 instead extracts ONLY the exact sections this task ID names: ARC1 alone, A1 alone, B2 alone, M1 alone. Roughly 800 tokens instead of 4,000. Cheaper, faster, and sharper writing because the worker sees only what matters.'),

    ('h', 'Fresh process per ad'),
    ('note', 'Each ad is generated in its own new Python process. Two reasons: (1) no "context erosion" — ad #50 is written with exactly the same clean slate as ad #1; (2) it lets the machine run many ads at once (20 parallel workers) without them interfering.'),

    ('h', 'Deterministic validation (no AI)'),
    ('note', 'After writing, a plain code checker (formats/{format}/validator.py + constants.json) verifies the hard rules — no AI involved, so it is instant and 100% consistent:'),
    ('bullet', 'word count within min/max'),
    ('bullet', 'character count under the Meta limit'),
    ('bullet', 'enough section dividers (========)'),
    ('bullet', 'no forbidden phrases ("In this video", "Let me tell you"...)'),
    ('bullet', 'CTA text + emojis correct'),
    ('bullet', 'P.S. close present (for LFS)'),

    ('h', 'Living quality gates'),
    ('note', 'Beyond the fixed format rules, there is a growing list of human-taught rules in AGENTS.md (QG-001, QG-002...). Example: "single avatar only — no second speakers." When a human spots a recurring mistake, they run ww learn "the rule" and it is appended; every future generation is then checked against it. The machine literally gets smarter from corrections.'),

    ('h', 'The folder structure (where everything lives)'),
    ('code', 'tools/      -> the CLI + all the Python (ww, generate.py, batch.py, context.py, validate.py)'),
    ('code', 'formats/    -> one folder per blueprint (lfs, yapfest, rvsl, ogvsl, drpov, vidmod...)'),
    ('code', 'products/   -> one folder per product, each with research/ (archetypes, hotwords, mechanisms)'),
    ('code', 'components/ -> shared pieces (dr-system.md system prompt, rock-bottom-types.md...)'),
    ('code', 'batches/    -> each batch: spec.json (the recipe list) + output/ (finished scripts) + report.json'),

    ('h', 'The RALF loop'),
    ('term', 'Research', 'gather raw material — Reddit scrapes, competitor scans, research files (archetypes/hotwords/mechanisms).'),
    ('term', 'Assemble', 'generate + validate scripts (generate/batch).'),
    ('term', 'Launch', 'push to team + Meta (upload/meta-upload).'),
    ('term', 'Feedback', 'scan performance + learn corrections, which feeds the next Research. The loop closes.'),
]

LFS = [
    ('title', 'THE LFS SYSTEM (Long Form Static)'),
    ('note', 'One specific blueprint inside WW-2 — studied in full so you can see how a format is actually built.'),

    ('h', 'What LFS is'),
    ('note', 'LFS = "Long Form Static". A 1,300-1,500 word first-person STATIC ad (text/image, NOT video) for Facebook/Instagram. The machine\'s own instruction puts it bluntly: "This is NOT marketing copy. This is a person venting to their best friend at 2am. Raw, visceral, embarrassing specifics they have not told anyone."'),

    ('h', 'When you use it'),
    ('note', 'For audiences who are already solution-aware or product-aware, when you want deep emotional identification ("that is EXACTLY me") in a wall of text people choose to read. It needs no actor and no camera — it is pure copy.'),

    ('h', 'The 11 sections (in order, with word targets)'),
    ('term', '1. SHOCK HOOK (40-60w)', 'the scroll-stopper. 2-3 lines that make them feel seen. Driven by the A-point.'),
    ('term', '2. PERSONAL PAIN SETUP (180-220w)', 'when it started and how it escalated.'),
    ('term', '3. GRAPHIC SYMPTOM BREAKDOWN (220-280w)', 'visceral, embarrassing detail using A-point hotwords — the "texture" that earns identification.'),
    ('term', '4. FAILED SOLUTIONS (180-220w)', 'everything tried (named products, dollar amounts, dismissive doctors). Ends on "Nothing worked."'),
    ('term', '5. ROCK BOTTOM MOMENT (180-220w)', 'one specific cinematic crisis scene (the rock-bottom type).'),
    ('term', '6. DISCOVERY + MECHANISM (280-350w)', 'the turn. Part A: discover WHY the problem exists (mechanism, verbatim, through the B-point lens). Part B: discover the product and map each ingredient to the mechanism.'),
    ('term', '7. TIMELINE OF RECOVERY (120-150w)', '4-6 checkpoints (Week 1, Month 1...) framed through the B-point.'),
    ('term', '8. VICTORY STATE (100-140w)', 'life now.'),
    ('term', '9. DIRECT READER ADDRESS (60-80w)', '"If you are reading this..." — validate and give hope.'),
    ('term', '10. PRODUCT CTA (40-60w)', 'emoji bullets, "Click LEARN MORE below", guarantee mentioned, no hard price.'),
    ('term', '11. P.S. CLOSE (30-50w)', 'final emotional punch.'),

    ('h', 'The 60 / 25 / 15 rule'),
    ('note', 'Spend 60% of words on PAIN (sections 1-5), 25% on DISCOVERY (6-8), 15% on FREEDOM (9-11). If you run long, cut from the back half — never sacrifice the pain. Identification is everything.'),

    ('h', 'The A/B point system (drives the angles)'),
    ('note', 'A-point = the pain you ENTER through: A1 physical/visible, A2 timing/age, A3 social. It powers the hook and symptom sections.'),
    ('note', 'B-point = the discovery REFRAME: B1 science/biology, B2 identity ("feel like myself again"), B3 system-failure (rage at doctors). It powers the discovery, timeline, and victory.'),

    ('h', 'Rock-bottom types'),
    ('term', 'RBPUB', 'public humiliation (a stranger notices).'),
    ('term', 'RBREL', 'relationship crisis (a partner pulls away).'),
    ('term', 'RBPHOTO', 'photo/mirror shock (does not recognise themselves).'),
    ('term', 'RBSEARCH', 'desperate 2am Google search.'),
    ('term', 'RBEVENT', 'a specific event ruined (wedding, vacation).'),

    ('h', 'Formatting rules (output goes straight into Meta)'),
    ('bullet', 'No section headers in the output (do not print "SHOCK HOOK").'),
    ('bullet', 'Use ======== dividers between major sections.'),
    ('bullet', 'No bold, no italics.'),
    ('bullet', 'Short paragraphs (1-3 sentences). Ellipses for trailing thoughts...'),
    ('bullet', 'ALL CAPS only for rare emphasis (NOT, NOTHING). Always use contractions.'),

    ('h', 'How to invoke it'),
    ('code', 'NOOR_LFS_ARC1_A1B1_M1_V001'),
    ('note', 'The "LFS" in slot 2 is what tells the machine to load formats/lfs/ (its prompt, constants, validator).'),

    ('h', 'A real hook (from an actual NOOR output)'),
    ('note', '"The morning I found a clump of hair on my pillow the size of a half-dollar coin, I did not tell my husband. I flushed it down the toilet and told myself it was stress."'),
]

OTHER_FORMATS = [
    ('title', 'THE OTHER FORMATS'),
    ('note', 'LFS is one of about eight blueprints. Knowing the others is what lets you choose the right tool — and it is the only way the "differences" make sense.'),

    ('term', 'Yapfest', 'a 1,500-2,000 word UGC VIDEO script (12 sections). Looks like a raw 7-10 min TikTok rant filmed in a kitchen. Same pain->discovery arc as LFS, but PERFORMED, with 4 hook options up top and an empty line between every sentence.'),
    ('term', 'RVSL (Rapid VSL)', 'a short (500-700w) MODULAR video front-end: 3-4 hooks + a lead + failed-solutions, which then attach to a pre-written "Master Body". Written in fragments; hotword must hit in the first sentence of every hook. Built for rapid reuse.'),
    ('term', 'OGVSL', 'a 750-900w (5-6 min) THIRD-person documentary-style video, classic 2018-style. A "60 Minutes" narrator tells a character\'s story with an expert and authority framing. First person only inside testimonials.'),
    ('term', 'DRPOV (Doctor POV)', 'a 1,300-1,500w first-person confession written AS A DOCTOR revealing what the medical system hides — 13 beats, heavy on data and a patient case study. Empirical, not just emotional.'),
    ('term', 'Freeform', 'a flexible 400-1,600w static ad where a custom briefing (not a fixed template) drives the whole structure. Used for one-off narratives that fit no template.'),
    ('term', 'RVSL-Concept', 'a variant of RVSL for concept-driven campaigns: uses 4 pre-written hooks verbatim from a brief, you only write the lead.'),
    ('term', 'VIDMOD', 'not one format but a library of 29 video frameworks built from modular blocks.'),

    ('h', 'VIDMOD\'s 29 frameworks (5 categories)'),
    ('bullet', 'UGC (13): first-person actor-to-camera (Problem-Solution, Unique Mechanism, X Reasons Why, Science & Studies, Personal Transformation, Docuseries...).'),
    ('bullet', 'NAR (5): no actor — text overlays / AI voiceover (Demo+Benefits, Old vs New, Emotional Story, Transformation, Product In Use).'),
    ('bullet', 'MASH (5): multi-testimonial compilations (Transformation Mashup, Social Proof Tsunami...).'),
    ('bullet', 'IFVSL (3): long in-feed VSLs, 1,800-3,500w (Civilian\'s Discovery, Guru\'s Discovery, Guthy-Renker style).'),
    ('bullet', 'VSLOP (3): short front-end hooks that drive clicks to a full VSL.'),

    ('h', 'At a glance'),
    ('term', 'LFS', 'static, 1,300-1,500w, first-person patient, solution/product-aware.'),
    ('term', 'Yapfest', 'video, 1,500-2,000w, first-person rant, unaware/problem-aware.'),
    ('term', 'RVSL', 'video front-end, 500-700w, fragments, problem-aware.'),
    ('term', 'OGVSL', 'video, 750-900w, third-person narrator, problem/solution-aware.'),
    ('term', 'DRPOV', 'static, 1,300-1,500w, first-person doctor, problem/solution-aware.'),
    ('term', 'Freeform', 'static, 400-1,600w, voice set by briefing, any stage.'),
]

DIFFERENCES = [
    ('title', 'THE DIFFERENCES'),

    ('h', 'WW-2 vs LFS — the mental-model fix'),
    ('note', 'This is the question you asked, so here is the honest answer: WW-2 and LFS are not the same KIND of thing, so they do not really "compete".'),
    ('note', 'WW-2 is the FACTORY — the code, the commands, the context-loading, the validation, the whole machine. LFS is ONE BLUEPRINT the factory can build (alongside Yapfest, RVSL, OGVSL, DRPOV...). Swapping "LFS" for "YAPFEST" in the task ID makes the SAME machine build a different ad. So the real difference is: WW-2 = how ads get made; LFS = what one particular ad looks like.'),

    ('h', 'LFS vs the other formats — the comparison that matters'),
    ('h3', 'LFS vs Yapfest'),
    ('note', 'Both are first-person 2am-confession arcs. The split: LFS is WRITTEN to be READ (static text, 1 hook, clean prose); Yapfest is SCRIPTED to be PERFORMED (video, 4 hooks, a line-break between every sentence). LFS suits more-aware readers; Yapfest grabs colder, scrolling viewers.'),
    ('h3', 'LFS vs RVSL'),
    ('note', 'LFS is a COMPLETE standalone ad (all 11 sections, its own CTA). RVSL is only a modular FRONT-END (hooks + lead + failed-solutions) that bolts onto a separate pre-written Master Body. LFS is long; RVSL is short and built for mixing-and-matching.'),
    ('h3', 'LFS vs OGVSL'),
    ('note', 'Point of view. LFS is FIRST-person and vulnerable ("this IS me"). OGVSL is THIRD-person and authoritative — a documentary narrator telling someone else\'s story ("this could be me"). LFS is longer and rawer; OGVSL is tighter and more "news report".'),
    ('h3', 'LFS vs DRPOV'),
    ('note', 'Who is talking. LFS is the PATIENT\'s emotional truth (no data, just lived experience). DRPOV is the DOCTOR\'s empirical truth (credentials, percentages, a case study). Same length, opposite kind of credibility.'),
    ('h3', 'LFS vs Freeform'),
    ('note', 'LFS is FORMULA-driven (every LFS shares the same 11-section skeleton — consistency). Freeform is BRIEFING-driven (structure invented per ad — flexibility). LFS for scale; Freeform for one-offs.'),

    ('h', 'The unifying principle'),
    ('note', 'Formats differ along five dials: medium (static vs video), voice/POV (patient / doctor / narrator), length, emotional intensity, and the audience awareness stage they suit. Picking a format = picking where you want those five dials set. That is the creative-strategist decision the machine cannot make for you.'),
]

BLUEPRINT = [
    ('title', 'REVERSE-ENGINEER BLUEPRINT'),
    ('note', 'The transferable principles. Internalise these ten and you can build a WW-2-style machine for ANY repetitive creative output — ads, emails, product descriptions, anything.'),

    ('term', '1. Task ID as control panel', 'compress every decision into one short, parseable code. The code IS the interface.'),
    ('term', '2. Separate structure from content', 'the format/template (the skeleton) lives apart from the product research (the flesh). Swap either independently.'),
    ('term', '3. Research as fuel, in files', 'store the raw selling material (archetypes, hotwords, mechanisms) as plain markdown the machine reads — not baked into code.'),
    ('term', '4. Surgical context loading', 'feed the AI ONLY the few sections this exact job needs. Less is sharper and cheaper.'),
    ('term', '5. Fresh process per unit', 'isolate every generation so jobs never contaminate each other and can run in parallel.'),
    ('term', '6. Deterministic validation', 'check the hard rules with plain code (word counts, banned words) — no AI, so it is instant and perfectly consistent.'),
    ('term', '7. Living quality gates', 'turn every human correction into a permanent, machine-enforced rule. The system compounds.'),
    ('term', '8. System prompt = the craft', 'a separate "teach the worker how to write" prompt (dr-system.md) carries the skill; the task prompt only carries the specifics.'),
    ('term', '9. Two-layer prompting', 'system layer = timeless craft; user layer = this one task. Reuse the first, vary the second.'),
    ('term', '10. Winners as examples', 'feed a couple of proven past winners as few-shot examples so the AI matches a known-good bar.'),

    ('h', 'Your move'),
    ('note', 'Boris is a copywriter, not an engineer — he almost certainly had AI write this code. His real edge is the COPYWRITING JUDGEMENT encoded in the templates and research. That is exactly the layer you are strong in. If you understand these ten principles, you can direct Claude Code to build your own machine, and pour YOUR copy judgement into the formats and research files. That is the reverse-engineering done.'),
]


# ================= EXECUTE =================
TITLE = 'WW-2 & LFS — Complete System Guide (How They Work, How To Use, The Differences)'
doc = docs.documents().create(body={'title': TITLE}).execute()
DOC_ID = doc['documentId']
print('Created doc: ' + DOC_ID)

# Fetch to get the default tab id
doc = docs.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
default_id = doc['tabs'][0]['tabProperties']['tabId']

# Rename default tab + create the other 6 tabs
setup = [
    {'updateDocumentTabProperties': {
        'tabProperties': {'tabId': default_id, 'title': '1. Big Picture'}, 'fields': 'title'}},
]
for name in ['2. Use WW-2', '3. How It Works', '4. The LFS System',
             '5. Other Formats', '6. The Differences', '7. Reverse-Engineer']:
    setup.append({'addDocumentTab': {'tabProperties': {'title': name}}})

res = docs.documents().batchUpdate(documentId=DOC_ID, body={'requests': setup}).execute()
new_ids = [r['addDocumentTab']['tabProperties']['tabId'] for r in res['replies'] if 'addDocumentTab' in r]

tab_plan = [
    (default_id, BIG_PICTURE),
    (new_ids[0], USE_WW2),
    (new_ids[1], UNDER_HOOD),
    (new_ids[2], LFS),
    (new_ids[3], OTHER_FORMATS),
    (new_ids[4], DIFFERENCES),
    (new_ids[5], BLUEPRINT),
]

for tab_id, blocks in tab_plan:
    reqs = build_tab(tab_id, blocks)
    docs.documents().batchUpdate(documentId=DOC_ID, body={'requests': reqs}).execute()
    print(f'  filled tab {tab_id} ({len(blocks)} blocks)')

# Share so it opens on either Google account
drive.permissions().create(
    fileId=DOC_ID,
    body={'type': 'user', 'role': 'writer', 'emailAddress': SHARE_EMAIL},
    sendNotificationEmail=False).execute()

print('\nDONE: https://docs.google.com/document/d/' + DOC_ID + '/edit')

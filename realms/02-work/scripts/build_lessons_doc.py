"""
Build the "AI Video Ads Course" Google Doc
==========================================
Takes the markdown lesson breakdowns in output/ai-video-lessons/breakdowns/
and builds ONE Google Doc with a tab per lesson (left-side sections).

Markdown supported: # ## ### headings, - bullets, 1. numbered lists,
**bold**, plain paragraphs. (No tables/code blocks — by design.)

Usage:
    python scripts/build_lessons_doc.py
"""
import sys, re, pathlib, time

sys.path.insert(0, 'C:/Users/User/Desktop/PERFORM/tools')
from google_helper import get_docs, get_drive

BREAKDOWNS = pathlib.Path('C:/Users/User/Desktop/PERFORM/output/ai-video-lessons/breakdowns')
PARENT_FOLDER = '176yVPhT_X3JPiDjgtfxe07GANkWeHdxh'  # course folder in Drive
DOC_TITLE = 'AI Video Ads Course — Full Breakdown (Frankie Shaw)'

# (markdown file, tab title) in tab order
TABS = [
    ('lesson_00_map.md', '00 — Course Map (read first)'),
    ('lesson_01.md',     '01 — V4 Update (core method)'),
    ('lesson_02.md',     '02 — Seedance 2 UGC Guide'),
    ('lesson_03.md',     '03 — V3 Update'),
    ('lesson_04.md',     '04 — Clip: Liver Hook'),
    ('lesson_05.md',     '05 — V5.1 (Kling 3 + Higgsfield)'),
    ('lesson_06.md',     '06 — Clip: Arthritis Hook'),
    ('lesson_07.md',     '07 — Module 1: Kie + Sora 2 Pro'),
    ('lesson_08.md',     '08 — V5 Animated Ads'),
    ('lesson_09.md',     '09 — AI UGC V3 (Kling era)'),
    ('lesson_10.md',     '10 — Clip: Outro'),
    ('lesson_11.md',     '11 — Omni / Google Flow'),
]

HEADING_MAP = {1: 'TITLE', 2: 'HEADING_1', 3: 'HEADING_2'}


def strip_bold(line):
    """Remove **markers**, return (clean_line, [(start, end) bold ranges])."""
    out, ranges, pos = [], [], 0
    for m in re.finditer(r'\*\*(.+?)\*\*', line):
        out.append(line[pos:m.start()])
        cur = sum(len(x) for x in out)
        out.append(m.group(1))
        ranges.append((cur, cur + len(m.group(1))))
        pos = m.end()
    out.append(line[pos:])
    return ''.join(out), ranges


def md_to_requests(md_text, tab_id):
    """Convert markdown to Google Docs batchUpdate requests for one tab."""
    text_parts = []          # final document text pieces
    headings = []            # (start, end, style)
    bold = []                # (start, end)
    lists = []               # (start, end, kind) contiguous blocks
    cursor = 1               # docs insert index (1-based)
    cur_list = None          # [start, end, kind] of open list block

    def close_list():
        nonlocal cur_list
        if cur_list:
            lists.append(tuple(cur_list))
            cur_list = None

    for raw in md_text.splitlines():
        # remove non-BMP chars (emoji) — they break index math (UTF-16)
        raw = ''.join(c for c in raw if ord(c) <= 0xFFFF)
        line = raw.strip()
        if not line:
            close_list()
            continue

        m_head = re.match(r'^(#{1,3})\s+(.*)$', line)
        m_bull = re.match(r'^[-*]\s+(.*)$', line)
        m_num = re.match(r'^\d+\.\s+(.*)$', line)

        if m_head:
            close_list()
            content, branges = strip_bold(m_head.group(2))
            style = HEADING_MAP[len(m_head.group(1))]
            headings.append((cursor, cursor + len(content), style))
        elif m_bull or m_num:
            kind = 'bullet' if m_bull else 'number'
            content, branges = strip_bold((m_bull or m_num).group(1))
            if cur_list and cur_list[2] == kind:
                cur_list[1] = cursor + len(content)
            else:
                close_list()
                cur_list = [cursor, cursor + len(content), kind]
        else:
            close_list()
            content, branges = strip_bold(line)

        for s, e in branges:
            bold.append((cursor + s, cursor + e))
        text_parts.append(content + '\n')
        cursor += len(content) + 1
    close_list()

    full_text = ''.join(text_parts)
    requests = [{'insertText': {'text': full_text,
                                'location': {'index': 1, 'tabId': tab_id}}}]
    for s, e, style in headings:
        requests.append({'updateParagraphStyle': {
            'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
            'paragraphStyle': {'namedStyleType': style},
            'fields': 'namedStyleType'}})
    for s, e, kind in lists:
        preset = ('BULLET_DISC_CIRCLE_SQUARE' if kind == 'bullet'
                  else 'NUMBERED_DECIMAL_ALPHA_ROMAN')
        requests.append({'createParagraphBullets': {
            'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
            'bulletPreset': preset}})
    for s, e in bold:
        requests.append({'updateTextStyle': {
            'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
            'textStyle': {'bold': True},
            'fields': 'bold'}})
    return requests


def main():
    docs = get_docs()
    drive = get_drive()
    log = []

    doc = docs.documents().create(body={'title': DOC_TITLE}).execute()
    doc_id = doc['documentId']
    log.append(f"Created doc: {doc_id}")

    # move next to the course materials in Drive
    try:
        drive.files().update(fileId=doc_id, addParents=PARENT_FOLDER,
                             fields='id,parents').execute()
        log.append("Moved into course folder")
    except Exception as e:
        log.append(f"Could not move to course folder (left in My Drive root): {e}")

    # rename the default first tab -> tab 0
    d = docs.documents().get(documentId=doc_id, includeTabsContent=True).execute()
    first_tab_id = d['tabs'][0]['tabProperties']['tabId']
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': [
        {'updateDocumentTabProperties': {
            'tabProperties': {'tabId': first_tab_id, 'title': TABS[0][1]},
            'fields': 'title'}}]}).execute()
    tab_ids = {TABS[0][1]: first_tab_id}

    # create remaining tabs
    for _, title in TABS[1:]:
        resp = docs.documents().batchUpdate(documentId=doc_id, body={'requests': [
            {'addDocumentTab': {'tabProperties': {'title': title}}}]}).execute()
        try:
            tab_ids[title] = resp['replies'][0]['addDocumentTab']['tabProperties']['tabId']
        except (KeyError, IndexError):
            d = docs.documents().get(documentId=doc_id, includeTabsContent=True).execute()
            for t in d['tabs']:
                if t['tabProperties']['title'] == title:
                    tab_ids[title] = t['tabProperties']['tabId']
        log.append(f"Tab created: {title}")
        time.sleep(0.5)

    # fill each tab
    for fname, title in TABS:
        md = (BREAKDOWNS / fname).read_text(encoding='utf-8')
        reqs = md_to_requests(md, tab_ids[title])
        docs.documents().batchUpdate(documentId=doc_id,
                                     body={'requests': reqs}).execute()
        log.append(f"Filled {title}: {len(reqs)} requests")
        time.sleep(0.5)

    log.append(f"\nDONE: https://docs.google.com/document/d/{doc_id}/edit")
    pathlib.Path('C:/tmp/build_doc_log.txt').write_text('\n'.join(log), encoding='utf-8')
    print("ALL DONE")


if __name__ == '__main__':
    main()

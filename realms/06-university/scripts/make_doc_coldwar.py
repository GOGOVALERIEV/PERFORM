"""
make_doc_coldwar.py — one Google Doc with the 3 scanned blocks, ready for George's human pass.
Blocks are inserted VERBATIM (char-for-char identical to what was scanned — touching them
would invalidate the 20% medians). Section labels tell George where his writing goes.
"""
import sys

sys.path.insert(0, 'C:/Users/User/Desktop/PERFORM/scripts')
from google_helper import get_docs, get_drive  # noqa: E402

REALM = 'C:/Users/User/Desktop/PERFORM/realms/06-university'
B = f'{REALM}/state/optimize/coldwar-bisect'
TITLE = 'CW REFERAT - blocks TEST (T.T.)'

blocks = []
for i in (1, 2, 3):
    blocks.append(open(f'{B}/block-{i}.txt', encoding='utf-8').read().strip())

docs = get_docs()
doc = docs.documents().create(body={'title': TITLE}).execute()
doc_id = doc['documentId']
print('doc created:', doc_id)

# Simple flat document: title + 3 labeled sections with the block text verbatim.
# Docs indices are computed sequentially on the default tab.
parts = []
parts.append(('TITLE', TITLE))
parts.append(('H2', 'INSTRUKCIYA (iztriy predi final)'))
parts.append(('P', '1. Blokovete sa verbatim kakvito gi skenirahme (20% mediana vseki). NE gi redaktirash vutreshnostta.'))
parts.append(('P', '2. Ti pishesh: po 1-2 izrecheniya prehod MEZHDU blokovete + vuvedenie + zaklyuchenie. Kratko, malko grapavo, tvoya glas.'))
parts.append(('P', '3. Zapetaykite lipsvashti pred "che/da/koeto" sa NAROCHNO. Ne gi poprawyay.'))
parts.append(('P', '4. Kato svarnish - kaji na Claude da skenira finala x3 (mediana).'))
for i, blk in enumerate(blocks, 1):
    parts.append(('H2', f'BLOK {i} (verbatim - ne pipat)'))
    parts.append(('P', blk))
    parts.append(('H2', f'>>> TVOYAT PREHOD {i} <<<' if i < 3 else '>>> TVOETO ZAKLYUCHENIE <<<'))

# Build full text + style runs
text = ''
styles = []  # (start, end, namedStyleType or bold)
for kind, content in parts:
    start = len(text) + 1  # docs index is 1-based
    text += content + '\n'
    end = start + len(content)
    if kind in ('TITLE', 'H2'):
        styles.append((start, end, kind))

requests = [{'insertText': {'location': {'index': 1}, 'text': text}}]
for start, end, kind in styles:
    if kind == 'TITLE':
        requests.append({'updateParagraphStyle': {'range': {'startIndex': start, 'endIndex': end},
                          'paragraphStyle': {'namedStyleType': 'TITLE'}, 'fields': 'namedStyleType'}})
    else:
        requests.append({'updateParagraphStyle': {'range': {'startIndex': start, 'endIndex': end},
                          'paragraphStyle': {'namedStyleType': 'HEADING_2'}, 'fields': 'namedStyleType'}})

docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
print('content inserted')

drive = get_drive()
drive.files().update(fileId=doc_id,
    body={'name': TITLE}).execute()

print('URL: https://docs.google.com/document/d/' + doc_id + '/edit')

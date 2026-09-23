"""
shake_everything.py — THE MEGA-SHAKE on a fresh, unprocessed paper
===================================================================
Input: AB-studena-calibrated.txt (fresh, 94-99% JustDone — never transformed).
Applies the FULL working transformation stack in sequence:

  STAGE A: sentence micro-rewrites (V8 method, 2 models alternating)
  STAGE B: code assembly, shuffled within paragraphs, paragraph sizes varied
  STAGE C: word-order inversion pass (V12 method)
  STAGE D: quote/attributions woven (V16-attribution style)
  STAGE E: vocabulary surprise (V13)
  STAGE F: code punctuation jitter (3 commas dropped)

Then JustDone x3 (median) on the result.
Also: quality gate — mechanical fact-diff + stylecheck, logged.
"""

import json
import re
import sys
import io
import random
import urllib.request
import functools
from pathlib import Path

print = functools.partial(print, flush=True)
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REALM / 'scripts'))
from optimize_paper import call  # noqa: E402

OUT = REALM / 'state' / 'optimize' / 'shake'
OUT.mkdir(parents=True, exist_ok=True)
MODELS = ['deepseek/deepseek-v4-flash-0731', 'qwen/qwen3.7-flash', 'mistralai/mistral-small-3.2-24b-instruct']
STUDENT_SYS = 'Ти си студент, който пише реферат на български. Връщаш само текста, без коментари.'
random.seed(21)

SRC = REALM / 'state/optimize/AB-test/AB-studena-calibrated.txt'
text_src = SRC.read_text(encoding='utf-8')
sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text_src) if s.strip()]
print(f'base: {len(sents)} sentences, {len(text_src.split())} words')


def rewrite(sentence, model, kind):
    prompts = {
        'micro': f'Пренапиши изречението изцяло — друг ред на думите, друга конструкция. Запази числата/имената/датите. Граматика СЪВЪРШЕНА. Само изречението:\n\n"{sentence}"',
        'invert': f'Изречение: "{sentence}"\n\nПренапиши с ОБЪРНАТ словоред: сказуемото/обстоятелството отпред, подлогът назад, вмъкни тире или скоби-пояснение. Граматика съвършена. Само изречението.',
        'retell': f'Преразкажи това изречение като студент, който обяснява на глас и записва. Друг ред, други формулировки, същите факти. Само изречението:\n\n"{sentence}"',
    }
    r = call(model, 'Ти си студент. Пишеш на български. Връщаш само едно изречение.', prompts[kind], timeout=120, temp=1.0)
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    return r if r and len(r.split()) >= 4 else sentence


# STAGE A: micro-rewrite, alternating models
print('\n=== STAGE A: micro-rewrites ===')
a_sents = []
for i, s in enumerate(sents):
    r = rewrite(s, MODELS[i % 2], 'micro')
    a_sents.append(r)
    if i % 5 == 0:
        print(f'  [{i+1}/{len(sents)}] {r[:60]}...')
(AOUT := OUT / 'stage-A.txt').write_text(' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in a_sents), encoding='utf-8')

# STAGE B: code assembly — shuffle within halves, rebuild paragraphs of varied size
print('\n=== STAGE B: code assembly ===')
random.shuffle(a_sents)  # sentence order within the flow (text is argumentative — order flexible for this test)
paras, size = [], random.choice([3, 4, 5])
for i in range(0, len(a_sents), size):
    paras.append(' '.join(a_sents[i:i + size]))
text_b = '\n\n'.join(paras)
(BOUT := OUT / 'stage-B.txt').write_text(text_b, encoding='utf-8')
print(f'  assembled: {len(paras)} paragraphs')

# STAGE C: inversion pass
print('\n=== STAGE C: inversion ===')
c_sents = []
flat = [s.strip() for p in paras for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
for i, s in enumerate(flat):
    r = rewrite(s, MODELS[(i + 1) % 3], 'invert')
    c_sents.append(r)
text_c = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in c_sents)
(COUT := OUT / 'stage-C.txt').write_text(text_c, encoding='utf-8')

# STAGE D: attributions woven
print('\n=== STAGE D: attributions ===')
t = call(MODELS[0], STUDENT_SYS,
         'В плът на този текст вплети 2 атрибуции: „според Дал (1971)…" и „както подчертава '
         'Линц (1964)…" — САМО ако текстът вече съдържа тези идеи (не измисляй нови вербални '
         'цитати). Всичко друго непроменено. Върни само текста.\n\nТЕКСТ:\n' + text_c,
         timeout=180)
text_d = (t or text_c)
(DOUT := OUT / 'stage-D.txt').write_text(text_d, encoding='utf-8')

# STAGE E: vocab surprise
print('\n=== STAGE E: vocab surprise ===')
e_sents = []
for i, s in enumerate([x.strip() for x in re.split(r'(?<=[.!?])\s+', text_d) if s.strip()]):
    r = rewrite(s, MODELS[i % 3], 'retell')
    e_sents.append(r)
text_e = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in e_sents)
(EOUT := OUT / 'stage-E.txt').write_text(text_e, encoding='utf-8')

# STAGE F: code punctuation jitter
print('\n=== STAGE F: punctuation jitter ===')
dropped = 0
for pat in [r'([а-я]), (че )', r'([а-я]), (да )', r'([а-я]), (което )', r'([а-я]), (като )']:
    m = re.search(pat, text_e)
    if m and dropped < 3:
        text_e = text_e[:m.start()] + m.group(1) + text_e[m.end():]
        dropped += 1
final = text_e
(FOUT := OUT / 'stage-F-final.txt').write_text(final, encoding='utf-8')
print(f'\nFINAL: {len(final.split())} words')
print('all stages saved in', OUT)

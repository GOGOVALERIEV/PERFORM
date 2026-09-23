"""
try_everything.py — THE FULL VARIANT BATTERY
=============================================
Base: v5-isolated.txt (71% JustDone, clean grammar, 25 sentences).
Every variant = a transformation of the base + JustDone score.
Also: V8 scanned 3x to measure the REFEREE'S OWN NOISE (critical baseline).

Variants:
  NOISE  : V8 text rescanned 3x (referee variance baseline)
  V12    : BG word-order inversion + parentheticals (per sentence, LLM)
  V13    : vocabulary surprise — rare/archaic BG words swapped in
  V14    : mixed register — half formal, half casual sentences
  V15    : punctuation-heavy style (dashes, semicolons, parentheses)
  V16    : quote-rich (short quotes woven in, properly marked)
  V17    : fragment chains ("Един проблем. Парите." style) throughout
  V18    : high-temperature regeneration of ALL sentences (temp 1.4)
  V19    : inversion + surprise COMBINED (V12+V13)

Scoring: JustDone free scan per variant (also 2nd scan on two variants for noise).
"""

import json
import re
import subprocess
import sys
import io
import urllib.request
import functools
from pathlib import Path

print = functools.partial(print, flush=True)
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
OUT = REALM / 'state' / 'optimize' / 'pol-izbori'
auth = json.loads(Path.home().joinpath('.pi/agent/auth.json').read_text(encoding='utf-8'))
KEY = auth['openrouter']['key']
DS = 'deepseek/deepseek-v4-flash-0731'
QW = 'qwen/qwen3.7-flash'


def call(model, system, prompt, timeout=150, temp=1.0):
    body = json.dumps({'model': model, 'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': prompt}], 'temperature': temp}).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    import time as _t
    for attempt in range(4):
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
            out = (resp.get('choices') or [{}])[0].get('message', {}).get('content', '').strip()
            return re.sub(r'\s+', ' ', out) if out else ''
        except Exception as e:
            wait = 5 * (2 ** attempt)
            print(f'    call fail ({model.split("/")[-1]}) attempt {attempt+1}: {e.__class__.__name__} — retry in {wait}s')
            _t.sleep(wait)
    return ''


def justdone(path, words=300):
    r = subprocess.run([sys.executable, str(REALM / 'scripts' / 'battery_justdone.py'),
                        str(path), '--words', str(words)],
                       capture_output=True, text=True, timeout=420,
                       encoding='utf-8', errors='replace')
    m = re.search(r'JustDone AI%: (\d{1,3}(?:\.\d+)?)', r.stdout + r.stderr)
    return float(m.group(1)) if m else None


def save(name, text):
    (OUT / f'{name}.txt').write_text(text, encoding='utf-8')


V5 = (OUT / 'v5-isolated.txt').read_text(encoding='utf-8')
SENTS = [s.strip() for s in re.split(r'(?<=[.!?])\s+', V5) if s.strip()]
V8_TEXT = (OUT / 'v8-micro-rewrite.txt').read_text(encoding='utf-8')
results = {}

# ---------- NOISE: referee variance on V8 ----------
print('=== NOISE: V8 scanned 3x (referee variance) ===')
noise = []
for i in range(3):
    s = justdone(OUT / 'v8-micro-rewrite.txt', words=300)
    noise.append(s)
    print(f'  scan {i+1}: {s}%')
results['NOISE_v8_3scans'] = noise
results['NOISE_range'] = (max(x for x in noise if x) - min(x for x in noise if x)) if all(noise) else None

# ---------- V12: word-order inversion ----------
print('=== V12: word-order inversion ===')
inv = []
for i, s in enumerate(SENTS):
    model = DS if i % 2 == 0 else QW
    r = call(model, 'Майстор на българския словоред. Връщаш само едно изречение.',
             f'Изречение: "{s}"\n\n'
             'Пренапиши с ОБЪРНАТ словоред: сказуемото или обстоятелството отпред, '
             'подлогът изместен назад, вмъкни тире-пояснение или скоби. Българската '
             'граматика позволява — използвай я. Числа/имена непокътнати. Само изречението.')
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    inv.append(r if r and len(r.split()) >= 5 else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in inv)
save('v12-inverted', t)
results['v12_inversion'] = justdone(OUT / 'v12-inverted.txt')
print(f'  V12: {results["v12_inversion"]}%')

# ---------- V13: vocabulary surprise ----------
print('=== V13: vocabulary surprise (rare/archaic words) ===')
sur = []
for i, s in enumerate(SENTS):
    model = QW if i % 2 == 0 else DS
    r = call(model, 'Лексикален майстор на български. Връщаш само едно изречение.',
             f'Изречение: "{s}"\n\n'
             'Замени 2-3 обикновени думи с РЯДКИ, книжовни или колоритни български '
             'думи/изрази (без да е смешно): "обстоятелство" вместо "факт", "за глава '
             'завъртя", "от друга страна — пак тя". Смисълът и фактите непокътнати. '
             'Само изречението.')
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    sur.append(r if r and len(r.split()) >= 5 else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in sur)
save('v13-vocab', t)
results['v13_vocab'] = justdone(OUT / 'v13-vocab.txt')
print(f'  V13: {results["v13_vocab"]}%')

# ---------- V14: mixed register ----------
print('=== V14: mixed register (formal/casual alternating) ===')
mix = []
for i, s in enumerate(SENTS):
    if i % 2 == 0:
        r = call(DS, 'Академичен редактор. Връщаш само едно изречение.',
                 f'Напиши това изречение ФОРМАЛНО и академично: "{s}" Само изречението.')
    else:
        r = call(QW, 'Студент, който пише небрежно но грамотно. Връщаш само едно изречение.',
                 f'Напиши това изречение НЕБРЕЖНО, разговорно, но грамотно: "{s}" Само изречението.')
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    mix.append(r if r and len(r.split()) >= 5 else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in mix)
save('v14-mixed', t)
results['v14_mixed'] = justdone(OUT / 'v14-mixed.txt')
print(f'  V14: {results["v14_mixed"]}%')

# ---------- V15: punctuation-heavy ----------
print('=== V15: punctuation-heavy (dashes, semicolons) ===')
t = V5
t = re.sub(r' — ', ' — ', t)
t = re.sub(r'([а-я]+) ([а-я]+), (което|като|че) ', r'\1 \2 — \3 ', t, count=4)
save('v15-punct', t)
results['v15_punct'] = justdone(OUT / 'v15-punct.txt')
print(f'  V15: {results["v15_punct"]}%')

# ---------- V16: quote-rich ----------
print('=== V16: quote-rich ===')
r = call(DS, 'Студент, който пише реферат с цитати. Връщаш само текста.',
         'Вземи този текст и вплети 3-4 КРАТКИ литературни/исторически цитата в кавички '
         '„така" с автор и година в скоби (измисли правдоподобни за темата — напр. '
         '„властта излиза от барутната дим" (популярна максима)). Дръж цитатите до 12 думи. '
         'Фактите и останалия текст почти непроменени.\n\nТЕКСТ:\n' + V5)
if r:
    save('v16-quotes', r)
    results['v16_quotes'] = justdone(OUT / 'v16-quotes.txt')
    print(f'  V16: {results["v16_quotes"]}%')
else:
    results['v16_quotes'] = 'n/a'

# ---------- V17: fragment chains ----------
print('=== V17: fragment chains ===')
frag = []
for i, s in enumerate(SENTS):
    r = call(QW if i % 2 == 0 else DS, 'Връщаш само едно изречение (или фрагмент-акцент).',
             f'Изречение: "{s}"\n\nПренапиши го така: започни с къс фрагмент-удар '
             f'("Един проблем. Парите." стил), после продължи със смисъла. Само фрагмента+изречението.')
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    frag.append(r if r else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in frag)
save('v17-fragments', t)
results['v17_fragments'] = justdone(OUT / 'v17-fragments.txt')
print(f'  V17: {results["v17_fragments"]}%')

# ---------- V18: high-temperature full regeneration ----------
print('=== V18: temp 1.4 regeneration of all sentences ===')
hot = []
for i, s in enumerate(SENTS):
    model = [DS, QW, 'mistralai/mistral-small-3.2-24b-instruct'][i % 3]
    r = call(model, 'Ти си студент, който пише свободно и малко хаотично, но грамотно. Само едно изречение.',
             f'Пренапиши това изречение НЕОЧАКВАНО: друг ред, друга енергия, изненадващ '
             f'избор на думи, но граматично чисто и фактите точни: "{s}" Само изречението.',
             temp=1.4)
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    hot.append(r if r and len(r.split()) >= 5 else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in hot)
save('v18-hot', t)
results['v18_hot'] = justdone(OUT / 'v18-hot.txt')
print(f'  V18: {results["v18_hot"]}%')

# ---------- V19: inversion + surprise combined ----------
print('=== V19: inversion + vocab surprise combined ===')
combo = []
for i, s in enumerate(inv):
    model = DS if i % 2 == 0 else QW
    r = call(model, 'Майстор на българската лексика и словоред. Само едно изречение.',
             f'Вземи това изречение (вече с обърнат словоред) и добави 2-3 РЯДКИ/колоритни '
             f'думи без да развалиш граматиката или фактите: "{s}" Само изречението.')
    r = re.sub(r'\s+', ' ', (r or '')).strip()
    combo.append(r if r and len(r.split()) >= 5 else s)
t = ' '.join(s if s.endswith('.') else s + '.' for s in combo)
save('v19-combo', t)
results['v19_combo'] = justdone(OUT / 'v19-combo.txt')
print(f'  V19: {results["v19_combo"]}%')

# ---------- summary ----------
print('\n================ FULL RESULTS ================')
print(f'referee noise on V8 (3 scans): {noise} -> range {results["NOISE_range"]}')
for k, v in results.items():
    if not k.startswith('NOISE'):
        print(f'  {k}: {v}%')
(OUT / 'try-everything-results.json').write_text(
    json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
print('saved:', OUT / 'try-everything-results.json')

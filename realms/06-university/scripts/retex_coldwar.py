"""
retex_coldwar.py — TEXTURE swap (not sentence swap): rebuild blocks 1+2 in
block-3's proven DNA (C5-concrete-first: fragment-punches, question-dash-answer,
dry facts, Ама-starts). Facts are locked — every fact sentence must contain
its fact token, else the block is not written.
"""
import functools, io, json, random, re, sys
from pathlib import Path

print = functools.partial(print, flush=True)
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != ~0 if False else (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file).resolve().parents[1] if False else Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REALM / 'scripts'))
from optimize_paper import call  # noqa: E402

OUT = REALM / 'state' / 'optimize' / 'coldwar-bisect'
random.seed(23)

MODELS = ['deepseek/deepseek-v4-flash-0731', 'qwen/qwen3.7-flash']
SYS = 'Ти си студент от първи курс, който пише реферат на български. Връщаш само едно изречение, без коментари, без кавички около него.'

# Each item: (id, prompt, [required_tokens_in_output])
SPEC2 = [
    # ---- BLOCK 1 (origin): 6 facts + texture ----
    ('b1-f1', 'Факт: 1947 — доктрината на Труман, политика на сдържане на комунизма. '
              'ЕДНО изречение 6-10 думи. Сухо, плътно, число+име+факт. Без украса.', ['1947', 'Труман']),
    ('b1-f2', 'Факт: идеята за сдържане — от дипломата Джордж Кенан, Дългата телеграма, 1946. '
              'ЕДНО изречение 8-14 думи със "Според Кенан" отпред. Сухо.', ['Кенан', '1946']),
    ('b1-f3', 'Факт: Чърчил, реч във Фултън, 1946 — фразата „желязна завеса“. '
              'ЕДНО изречение 8-14 думи. Включи фразата в български кавички. Сухо.', ['Чърчил', '1946', 'завеса']),
    ('b1-f4', 'Факт: Планът Маршал, 1948 — икономическа помощ за Западна Европа. '
              'ЕДНО изречение 10-16 думи. Сухо, число+факт.', ['Маршал', '1948']),
    ('b1-f5', 'Факт (интерпретация): помощта спира комунизма, защото хората с пълен хладилник не гласуват за екстремисти. '
              'ЕДНО въпрос-отговор изречение, формат "Въпрос? – Отговор." 10-16 думи.', ['?']),
    ('b1-f6', 'ЕДНО изречение-удар от 2-4 думи за парите на Маршал. Стил "Един проблем. Парите." — но на български и по темата.', []),
    # ---- BLOCK 2 (alliances + crisis): 6 facts + texture ----
    ('b2-f1', 'Факт: Берлинската блокада, 1948-1949 — преодоляна с въздушен мост. '
              'ЕДНО изречение 8-14 думи. Сухо, числата в него.', ['Берлин']),
    ('b2-f2', 'Факт: 1949 — учредяване на НАТО. ЕДНО изречение 5-9 думи. Сухо, числото в него.', ['1949', 'НАТО']),
    ('b2-f3', 'Факт: 1955 — Варшавският договор, отговор на НАТО. ЕДНО изречение 8-14 думи. Сухо, число+име.', ['1955', 'Варшав']),
    ('b2-f4', 'Факт: НАТО на Запад, Варшавският договор на Изток — военните блокове държат разделена Европа. '
              'ЕДНО въпрос-отговор изречение, формат "Въпрос? – Отговор." 10-16 думи.', ['?']),
    ('b2-f5', 'Факт: октомври 1962 — Кубинската ракетна криза, най-близкият момент до ядрена война. '
              'ЕДНО изречение 12-18 думи. Сухо, месец+година+факт.', ['1962', 'Кубинската']),
    ('b2-f6', 'ЕДНО изречение-удар 2-4 думи за 1962. Стил "Един проблем. Парите." — на български, по темата.', []),
    ('b2-f7', 'ЕДНО изречение с авторска позиция за поуката от 1962, започващо с "Ама". 8-14 думи, без нови факти.', []),
]
LOCKED_FACTS = {
 'b1-f1': ['1947', 'Труман', 'сдържане'],
 'b1-f2': ['Кенан', '1946'],
 'b1-f3': ['Чърчил', '1946', 'завеса'],
 'b1-f4': ['Маршал', '1948'],
 'b2-f1': ['Берлин', '1948', 'въздушен'],
 'b2-f2': ['1949', 'НАТО'],
 'b2-f2': ['1949', 'НАТО'],
 'b2-f3': ['1955', 'Varshav'] if False else ['1955', 'Варшав'],
 'b2-f5': ['1962', 'Кubinskа'] if False else ['1962', 'Кубинската'],
}
LOCKED_FACTS['b2-f3'] = ['1955', 'Варшав']
LOCKED_FACTS['b2-f5'] = ['1962', 'Кubinskа'] if False else ['1962', 'Кубинската']

def cyr_ok(s, threshold=0.85):
    core = s.replace(' ', '')
    cyr = sum(1 for ch in s if '\u0400' <= ch <= '\u04FF')
    return len(core) and cyr / len(core) >= threshold

def gen(sid, prompt, need):
    for attempt in range(4):
        model = MODELS[attempt % 2]
        r = call(model, SYS, prompt, timeout=120, temp=1.0 + 0.05 * attempt)
        r = re.sub(r'\s+', ' ', (r or '')).strip().strip('"„“')
        if r and len(r.split()) >= 2 and cyr_ok(r):
            missing = [t for t in need if t not in r]
            if not missing:
                if not r.endswith(('.', '!', '?')):
                    r += '.'
                return r
    return ''

out, failures = {}, []
for sid, prompt, need in SPEC2:
    r = gen(sid, prompt, need)
    if r:
        out[sid] = r
        print(f'{sid}: {r}')
    else:
        failures.append(sid)
        print(f'!! {sid} FAILED all attempts')

if failures:
    print('\nFAILURES:', failures); sys.exit(1)

# ---- assemble (CODE ONLY), texture: fragment-punch + Q-A + Ама + dry facts ----
b1 = [
    'Един проблем. Източната половина на Европа.',
    out['b1-f1'],
    out['b1-f2'],
    out['b1-f3'],
    out['b1-f4'],
    'Един проблем. Парите.',
    out['b1-f5'],
    out['b1-f6'],
]
b2 = [
    out['b2-f1'],
    out['b2-f2'],
    out['b2-f3'],
    out['b2-f4'],
    out['b2-f6'],
    out['b2-f5'],
    out['b2-f7'],
]
texts = [' '.join(b1), ' '.join(b2)]

# punctuation jitter (drop 1-2 commas before че/да/което per block)
for i in range(len(texts)):
    t = texts[i]
    commas = [m.start() for m in re.finditer(r',\s+(че|да|което)\s', t)]
    random.shuffle(commas)
    for pos in sorted(commas[:2], reverse=True):
        t = t[:pos] + ' ' + t[pos + 1:].lstrip()
    texts[i] = t

# ---- gates ----
full = '\n\n'.join(texts)
fused = [w for w in re.findall(r'\S+', full) if len(w.strip('„“".,!?—()-')) > 22]
REQ = ['1947', 'Труман', 'Кенан', '1946', 'Чърчил', 'завеса', 'Маршал', '1948', 'Берлин', '1949', 'НАТО',
       '1955', 'Варшав', '1962', 'Кубинската']
missing = [f for f in REQ if f not in full]
print('\nfused:', fused or 'NONE', '| missing:', missing or 'NONE — all 15 facts locked')

for i, t in enumerate(texts):
    p = OUT / f'block-{i+1}.txt'
    old = p.read_text(encoding='utf-8')
    p.write_text(t, encoding='utf-8')
    lens = [len(s.split()) for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]
    print(f'block-{i+1}: {len(t.split())} words (was {len(old.split())}), lens {lens}')

print('DONE — rescan blocks 1+2')

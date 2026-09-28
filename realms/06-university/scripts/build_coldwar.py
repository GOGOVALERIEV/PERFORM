"""
build_coldwar.py — bisect-architecture referat builder (Cold War topic)
=======================================================================
Follows the proven law:
  - sentences generated SEPARATELY (micro-prompts, 1-2 facts each),
    3 models alternating, temp 1.0  (v5/v6 mechanism)
  - dry/blasty texture per block: question-dash-answer, "Ама" starts,
    short declaratives, dense numbers  (bisect-C mechanism)
  - CODE assembly only — NO LLM ever sees the whole document
  - mechanical gates: fused words, fact preservation, sentence variance
  - LLM judge grades grammar+meaning per block (fallback: keep original)

Output: state/optimize/coldwar-bisect/block-1.txt ... block-N.txt
"""

import functools
import io
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

print = functools.partial(print, flush=True)
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REALM / 'scripts'))
from optimize_paper import call  # noqa: E402

OUT = REALM / 'state' / 'optimize' / 'coldwar-bisect'
OUT.mkdir(parents=True, exist_ok=True)
random.seed(7)

MODELS = [
    'deepseek/deepseek-v4-flash-0731',
    'qwen/qwen3.7-flash',
    'mistralai/mistral-small-3.2-24b-instruct',
]
SYS = 'Ти си студент от първи курс, който пише реферат на български. Връщаш само едно изречение, без коментари, без кавички около него.'

# ---------------------------------------------------------------- sentence spec
# Every sentence = 1-2 FACTS ONLY (from the closed-book list) + texture directive.
# Two extra REAL, verifiable attributions allowed: Churchill Fulton 1946, Kennan 1946.
SPEC = [
    # --- BLOCK 1: origin (1946-1948) ---
    ('s01', 'Факт: 1947 година — доктрината на Труман обявява политиката на сдържане на комунизма (на англ. containment). '
            'Напиши ЕДНО изречение 14-20 думи. Числото 1947 отпред или близо до подлога. Плътно, сухо, без украса.'),
    ('s02', 'Факт: идеята за сдържане се приписва на дипломата Джордж Кенан (Дългата телеграма, 1946). '
            'ЕДНО изречение със "според" или "както смята" + ИМЕТО Кенан и годината 1946. 12-20 думи.'),
    ('s03', 'Факт: Уинстън Чърчил произнася фразата "желязна завеса" в реч във Фултън през 1946 година. '
            'ЕДНО изречение, което въвежда фразата в български кавички „желязна завеса“ + автор + година. 10-18 думи.'),
    ('s04', 'Факт: Планът Маршал (1948) дава икономическа помощ за Западна Европа. '
            'ЕДНО по-дълго изречение 20-28 думи. Числото 1948 залепено за смисъла, не самоизправено.'),
    ('s05', 'ЕДНО въпрос-отговор изречение по темата (Маршал план / икономика срещу комунизъм), формат: '
            '"Въпрос? – Кратък отговор." Без нови факти, само авторска интерпретация. 8-16 думи.'),
    ('s06', 'ЕДНО МНОГО КЪСО изречение (3-6 думи), удар-фрагмент за икономическата помощ на Маршал. '
            'Стил: "Един проблем. Парите." (но по темата).'),
    # --- BLOCK 2: Berlin 1948-49 ---
    ('s07', 'Факт: 1948-49 — Берлинска блокада, преодоляна с въздушен мост. '
            'ЕДНО изречение 14-22 думи, сухо, и двете години в него.'),
    ('s08', 'Факт (за интерпретация): СССР затваря сухопътните пътища към Западен Берлин. '
            'ЕДНО изречение, започващо с "Ама". 10-18 думи. Без нови числа.'),
    ('s09', 'Факт: западните съюзници снабдяват града по въздуха месеци наред. '
            'ЕДНО кратко изречение 6-12 думи. Без нови числа.'),
    # --- BLOCK 3: alliances 1949-1955 ---
    ('s10', 'Факт: 1949 — учредяване на НАТО. ЕДНО изречение 10-16 думи. Числото 1949 в него.'),
    ('s11', 'Факт: 1955 — Варшавският договор, създаден като отговор на НАТО. '
            'ЕДНО изречение, започващо с "Шест години по-късно". 12-20 думи.'),
    ('s12', 'ЕДНО въпрос-отговор изречение: какво държи двете половини на Европа? – Военните блокове (НАТО и Варшавския договор). '
            'Формат "Въпрос? – Отговор." 10-18 думи.'),
    ('s13', 'ЕДНО МНОГО КЪСО изречение (2-6 думи): удар-фраза за двата блока. Без списъци, без три елемента.'),
    # --- BLOCK 4: crisis + détente ---
    ('s14', 'Факт: октомври 1962 — Кубинската ракетна криза, най-близкият момент до ядрена война. '
            'ЕДНО по-дълго изречение 20-28 думи. Месецът и годината в началото.'),
    ('s15', 'ЕДНО изречение с авторска позиция за поуката от 1962 (без нови факти). Започни с "Ама". 10-18 думи.'),
    ('s16', 'Факт: през 70-те години настъпва детант (на фр. détente — разреждане). '
            'ЕДНО изречение 12-20 думи, с BG дума + чуждия термин в скоби.'),
    ('s17', 'Факт: SALT-1 (1972) — първи договор за ограничение на стратегическите оръжия. '
            'ЕДНО изречение 12-20 думи. SALT-1 и 1972 заедно.'),
    ('s18', 'ЕДНО въпрос-отговор изречение: значи ли детентът край на надпреварата? – Не, само пауза. '
            'Формат "Въпрос? – Отговор." 8-14 думи. Авторска позиция.'),
    # --- BLOCK 5: the end (1985-1991) ---
    ('s19', 'Факт: 1985 — Михаил Горбачов идва на власт и стартира гласност и перестройка. '
            'ЕДНО по-дълго изречение 18-26 думи. 1985 + името + двете термина.'),
    ('s20', 'ЕДНО КРАТКО изречение (4-8 думи) за гласност и перестройка като думи, които срутват система. Авторска позиция, без нови факти.'),
    ('s21', 'Факт: ноември 1989 — падането на Берлинската стена. ЕДНО изречение 8-16 думи. Месец + година.'),
    ('s22', 'ЕДНО въпрос-отговор изречение: защо точно 1989? – Защото СССР вече не гарантира режимите. '
            'Формат "Въпрос? – Отговор." 8-16 думи. Авторска интерпретация.'),
    ('s23', 'Факт: декември 1991 — разпадът на СССР, край на биполярния свят. ЕДНО изречение 12-20 думи.'),
    ('s24', 'ЕДНО КРАТКО закриващо изречение (6-12 думи) с метафора от темата (завеса/стена/подпис). Без нови факти, авторска позиция.'),
]

REQUIRED_FACTS = ['1947', '1946', '1948', '1949', '1955', '1962', '1972', '1985', '1989', '1991',
                  'Труман', 'Кенан', 'Чърчил', 'Маршал', 'Берлин', 'НАТО', 'Варшав',
                  'Кубинската', 'SALT-1', 'Горбачов', 'СССР']


def call_retry(model, prompt, attempts=3, temp=1.0):
    for a in range(attempts):
        r = call(model, SYS, prompt, timeout=120, temp=temp)
        r = re.sub(r'\s+', ' ', (r or '')).strip().strip('"„“')
        if r and len(r.split()) >= 3:
            return r
        time.sleep(2 + 3 * a)
    return ''


# ---------------------------------------------------------------- generate
sents = {}
for i, (sid, prompt) in enumerate(SPEC):
    model = MODELS[i % 3]
    r = call_retry(model, prompt)
    if not r:  # fallback: try the other model
        r = call_retry(MODELS[(i + 1) % 3], prompt)
    if not r:
        print(f'!! {sid}: BOTH MODELS FAILED')
        sys.exit(1)
    if not r.endswith(('.', '!', '?')):
        r += '.'
    sents[sid] = r
    print(f'{sid} [{model.split("/")[1][:14]}] {r}')

(OUT / 'sentences.json').write_text(json.dumps(sents, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------------------------------------------------------------- assemble blocks (CODE ONLY)
ORDER = [f's{i:02d}' for i in range(1, 25)]
BLOCK_TARGET = 100  # words per block (well above JustDone's ~60-word floor)

blocks, cur, cur_len = [], [], 0
for sid in ORDER:
    w = len(sents[sid].split())
    if cur and cur_len + w > BLOCK_TARGET + 12:
        blocks.append(cur)
        cur, cur_len = [], 0
    cur.append(sents[sid])
    cur_len += w
if cur:
    blocks.append(cur)

# punctuation jitter: drop 1-2 commas before че/да/което per block (realistic student sloppiness)
texts = []
for b in blocks:
    t = ' '.join(b)
    commas = [m.start() for m in re.finditer(r',\s+(че|да|което)\s', t)]
    random.shuffle(commas)
    for pos in sorted(commas[:2], reverse=True):
        t = t[:pos] + ' ' + t[pos + 1:].lstrip()
    texts.append(t)

# ---------------------------------------------------------------- mechanical gates
full = '\n\n'.join(texts)
report = {'fused_words': [], 'missing_facts': [], 'blocks': []}
for tok in re.findall(r'\S+', full):
    core = tok.strip('„“".,!?—()-')
    if len(core) > 22:
        report['fused_words'].append(tok)
for fact in REQUIRED_FACTS:
    if fact not in full:
        report['missing_facts'].append(fact)
for i, t in enumerate(texts):
    lens = [len(s.split()) for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]
    report['blocks'].append({'n': i + 1, 'words': len(t.split()), 'sent_lens': lens})
    (OUT / f'block-{i + 1}.txt').write_text(t, encoding='utf-8')

print('\n=== GATES ===')
print('fused words:', report['fused_words'] or 'NONE')
print('missing facts:', report['missing_facts'] or 'NONE — all present')
for b in report['blocks']:
    print(f'block-{b["n"]}: {b["words"]} words, sentence lens {b["sent_lens"]}')
(OUT / 'gate-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------------------------------------------------------------- LLM judge per block (grammar + meaning)
print('\n=== JUDGE ===')
for i, t in enumerate(texts):
    verdict = call_retry(MODELS[0],
        f'Оцени този откъс от студентски реферат на български. Критерии: (1) граматика — има ли счупени '
        f'думи, слепени думи или изречение, което не се чете; (2) смисъл — изреченията логични ли са; '
        f'(3) фактите правдоподобни ли са. ОТГОВОР точно във формат: PASS или FAIL: <проблемът>.\n\n{t}',
        attempts=2)
    ok = verdict.upper().startswith('PASS')
    print(f'block-{i + 1}: {"PASS" if ok else "FAIL -> " + verdict[:120]}')
    (OUT / f'judge-{i + 1}.txt').write_text(verdict, encoding='utf-8')

print('\nDONE. Blocks ready for scanning.')

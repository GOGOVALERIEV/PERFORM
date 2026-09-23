"""
combinations.py — 5 COMBINATION CHAINS (proven pieces, different orders)
=========================================================================
Base: pol-izbori facts + v5 sentences. Each combo = a different order of the
proven mechanisms. Screened with 1 JustDone scan each; winner gets 3-scan median.

Usage: python combinations.py [--only C1,C3]
"""

import json
import re
import sys
import io
import random
import urllib.request
import concurrent.futures as cf
from pathlib import Path

print = functools.partial(print, flush=True) if (functools := __import__('functools')) else print
if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REALM / 'scripts'))
from optimize_paper import call, justdone  # noqa: E402

OUT = REALM / 'state' / 'optimize' / 'pol-izbori'
DS = 'deepseek/deepseek-v4-flash-0731'
QW = 'qwen/qwen3.7-flash'
GL = 'z-ai/glm-flash-latest'

BRIEF = json.loads((REALM / 'state' / 'benchmark' / 'batch1' / 'papers.json').read_text(encoding='utf-8'))['papers'][0]
FACTS = '\n'.join('- ' + f for f in BRIEF['facts'])
V5_SENTS = [s.strip() for s in re.split(r'(?<=[.!?])\s+',
            (OUT / 'v5-isolated.txt').read_text(encoding='utf-8')) if s.strip()]

STUDENT_SYS = 'Ти си студент, който пише реферат на български. Връщаш само текста, без коментари.'


def parallel_rewrite(sents, model, kind):
    """Rewrite each sentence in parallel with `model`, style per `kind`."""
    def one(i_s):
        i, s = i_s
        if kind == 'micro':
            p = (f'Пренапиши това изречение изцяло — друг ред на думите, друга конструкция, '
                 f'запази числата/имената/датите. Звучи като казано на глас и записано. '
                 f'Граматика СЪВЪРШЕНА. Върни само изречението:\n\n"{s}"')
        elif kind == 'invert':
            p = (f'Изречение: "{s}"\n\nПренапиши с ОБЪРНАТ словоред (сказуемото или '
                 f'обстоятелството отпред), вмъкни тире-пояснение или скоби. Граматика '
                 f'съвършена, числа/имена непокътнати. Само изречението.')
        elif kind == 'vocab':
            p = (f'Изречение: "{s}"\n\nЗамени 2-3 обикновени думи с РЯДКИ книжовни или '
                 f'колоритни български думи/изрази (без да е смешно). Фактите непокътнати. Само изречението.')
        elif kind == 'retell':
            p = (f'Преразкажи това изречение като студент, който обяснява на глас и е записал: '
                 f'друг ред, други формулировки, същият смисъл и факти. Само изречението:\n\n"{s}"')
        r = call(model, STUDENT_SYS, p, timeout=120, temp=1.0)
        r = re.sub(r'\s+', ' ', (r or '')).strip()
        return r if r and len(r.split()) >= 4 else s
    with cf.ThreadPoolExecutor(max_workers=5) as ex:
        return list(ex.map(one, enumerate(sents)))


def weave_attribution(text):
    """Weave 2 real attributions into existing claims (no invented quotes)."""
    return call(DS, STUDENT_SYS,
        'Вземи този текст и вплети 2 атрибуции на съществуващи твърдения: замените '
        '„съгласно дефиницията" тип пасажи с „според Дал (1971)…" и „както подчертава '
        'Линц (1964)…" САМО ако текстът вече твърди това — не измисляй нови вербални '
        'цитати, само приписвай съществуващи твърдения на техните автори. Всичко друго '
        'непроменено. Върни само текста.\n\nТЕКСТ:\n' + text, timeout=180)


def jitter(text):
    dropped = 0
    for pat in [r'([а-я]), (че )', r'([а-я]), (да )', r'([а-я]), (което )', r'([а-я]), (като )']:
        m = re.search(pat, text)
        if m and dropped < 3:
            text = text[:m.start()] + m.group(1) + text[m.end():]
            dropped += 1
    return text


def finish(name, text):
    text = jitter(text)
    (OUT / f'{name}.txt').write_text(text, encoding='utf-8')
    s = justdone(OUT / f'{name}.txt')
    print(f'  >>> {name}: {s}% JustDone')
    return s


def run():
    combos = {}

    # ---- C1: isolation -> micro-rewrite -> attributions -> jitter ----
    print('=== C1: my-final recipe ===')
    s = parallel_rewrite(V5_SENTS, DS, 'micro')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    t = call(DS, STUDENT_SYS,
             'Вплети 2 атрибуции (според Дал (1971)…, както подчертава Линц (1964)…) в '
             'съответните твърдения на този текст — те вече ги съдържат като смисъл. Само '
             'текст:\n\n' + text, timeout=180)
    combos['C1_final'] = finish('C1-final', t if t and len(t.split()) > 100 else text)

    # ---- C2: inversion -> micro-rewrite -> jitter ----
    print('=== C2: inversion-first ===')
    s = parallel_rewrite(V5_SENTS, DS, 'invert')
    s = parallel_rewrite(s, QW, 'micro')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    combos['C2_inversion_first'] = finish('C2-inversion-first', text)

    # ---- C3: vocab -> attributions -> micro-rewrite -> jitter ----
    print('=== C3: vocab-attr-rewrite ===')
    s = parallel_rewrite(V5_SENTS, GL, 'vocab')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    t = call(QW, STUDENT_SYS,
             'Вплети приписки (според Дал (1971)…, Линц (1964)…) където текстът говори за '
             'техните идеи. Само текст:\n\n' + text, timeout=180)
    s = parallel_rewrite([x.strip() for x in re.split(r'(?<=[.!?])\s+', (t or text)) if x.strip()], DS, 'micro')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    combos['C3_vocab_attr_rewrite'] = finish('C3-vocab-attr-rewrite', text)

    # ---- C4: three-model sandwich ----
    print('=== C4: three-model sandwich ===')
    s = parallel_rewrite(V5_SENTS, DS, 'retell')
    s = parallel_rewrite(s, QW, 'micro')
    s = parallel_rewrite(s, GL, 'retell')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    combos['C4_sandwich'] = finish('C4-sandwich', text)

    # ---- C5: concrete facts first -> isolation -> micro -> attr ----
    print('=== C5: concrete-facts-first ===')
    concrete = call(DS, STUDENT_SYS,
        'Превърни тези бележки в КОНКРЕТНИ мини-сценки: всяка бележка + пример с име, '
        'дада, държава или число. Същите факти, по-конкретно облечени. Върни само '
        'бележките (списък).\n\nБЕЛЕЖКИ:\n' + FACTS, timeout=180)
    sents_c = [re.sub(r'^-\s*', '', l).strip() for l in (concrete or FACTS).split('\n') if l.strip()]
    s = parallel_rewrite(sents_c, QW, 'retell')
    s = parallel_rewrite(s, DS, 'micro')
    text = ' '.join(x if x.endswith(('.', '!', '?')) else x + '.' for x in s)
    t = call(QW, STUDENT_SYS,
             'Вплети 2 приписки (Дал (1971), Линц (1964)) където пасва. Само текст:\n\n' + text,
             timeout=180)
    combos['C5_concrete_first'] = finish('C5-concrete-first', t if t and len(t.split()) > 100 else text)

    # ---- summary ----
    print('\n================ COMBO STANDINGS ================')
    for k, v in sorted(combos.items(), key=lambda x: (x[1] is None, x[1])):
        print(f'  {v:>6}%  {k}')
    (OUT / 'combinations-results.json').write_text(
        json.dumps(combos, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    random_seed = None
    import random
    random.seed(13)
    run()

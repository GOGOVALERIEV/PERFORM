"""
optimize_paper.py — SINGLE-PAPER OPTIMIZATION LOOP (George's design)
=====================================================================
The chain: facts -> RETELL (преразказ, not назубряне) -> synonym shuffler ->
punctuation imperfection pass -> JustDone test -> analyze flagged sentences ->
targeted rewrite -> retest. One paper, iterate until the free tests pass.

Every variant is saved to state/optimize/<paper>/ and scored on JustDone.
Cost per variant: ~$0.001-0.002 (paid-cheap models).
"""

import json
import re
import subprocess
import sys
import io
import urllib.request
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
OPT = REALM / 'state' / 'optimize'
BATCH = REALM / 'state' / 'benchmark' / 'batch1'


def call(model: str, system: str, prompt: str, timeout: int = 300, temp: float = 1.0) -> str:
    auth = json.loads(Path.home().joinpath('.pi/agent/auth.json').read_text(encoding='utf-8'))
    key = auth['openrouter']['key']
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}],
        'temperature': temp,
    }).encode('utf-8')
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        return (resp.get('choices') or [{}])[0].get('message', {}).get('content', '').strip()
    except Exception as e:
        print(f'  call failed: {e.__class__.__name__}: {str(e)[:120]}')
        return ''


def justdone(path: Path, words=300):
    r = subprocess.run([sys.executable, str(REALM / 'scripts' / 'battery_justdone.py'),
                        str(path), '--words', str(words)],
                       capture_output=True, text=True, timeout=420,
                       encoding='utf-8', errors='replace')
    m = re.search(r'JustDone AI%: (\d{1,3}(?:\.\d+)?)', r.stdout + r.stderr)
    return float(m.group(1)) if m else None


def main():
    paper_id = 'pol-izbori'
    base = json.loads((BATCH / 'papers.json').read_text(encoding='utf-8'))['papers'][0]
    out = OPT / paper_id
    out.mkdir(parents=True, exist_ok=True)
    facts = '\n'.join('- ' + f for f in base['facts'])
    DS = 'deepseek/deepseek-v4-flash-0731'
    QW = 'qwen/qwen3.7-flash'

    # ---- V1: RETELL framing (the key change) ----
    print('=== V1: retell framing ===')
    v1 = call(DS,
        'Ти си студент, който ПРЕРАЗКАЗВА прочетен материал за университетска разработка. '
        'Не пишеш есе и не съчиняваш — преразказваш със свои думи това, което си разбрал. '
        'Пишеш на български, естествено, като човек.',
        'Прочетох статия за изборните системи. Ето какво си записах от нея (бележки):\n'
        f'{facts}\n\n'
        'Преразкажи какво разбираш от материала — 450-500 думи, без списъци. Не следвай '
        'реда на бележките — редът трябва да е логиката на разказа. Кажи нещата така, '
        'сякаш ги обясняваш на състудент, но в по-академичен тон. Не цитирай точно — '
        'предавай смисъла.')
    (out / 'v1-retell.txt').write_text(v1, encoding='utf-8')
    print(f'  V1: {len(v1.split())} words')
    s1 = justdone(out / 'v1-retell.txt')
    print(f'  V1 JustDone: {s1}%')

    # ---- V2: synonym shuffler on V1 ----
    print('=== V2: synonym shuffler ===')
    v2 = call(QW,
        'Ти си лексикален редактор. Пишеш на български.',
        'Вземи този текст и замени колкото можеш повече думи с близки по смисъл (синоними), '
        'без да нарушиш точността на фактите и без да звучи неестествено. Също размести '
        'думите вътре в изреченията, където е възможно, и промени някои изречения от '
        'деятелен в страдателен залог или обратно. НЕ пипай числа, дати и имена. '
        'Върни само текста.\n\nТЕКСТ:\n' + v1)
    (out / 'v2-shuffled.txt').write_text(v2, encoding='utf-8')
    print(f'  V2: {len(v2.split())} words')
    s2 = justdone(out / 'v2-shuffled.txt')
    print(f'  V2 JustDone: {s2}%')

    # ---- V3: punctuation imperfection pass ----
    print('=== V3: punctuation imperfection ===')
    v3 = call(QW,
        'Ти си студент, който пише бързо преди срок. Пишеш на български.',
        'Вземи текста и въведи ДРЕБНИ, РЕАЛИСТИЧНИ грешки в пунктуацията — такива, които '
        'прави всеки студент: липсваща запетая пред "че" или "да" (само 2-3 пъти), '
        'излишна запетая тук-там, по една липсваща крайна точка в скоба. НЕ прави '
        'правописни грешки в думи. НЕ прекалива — 4-5 дребни неща на целия текст. '
        'НЕ пипай факти. Върни само текста.\n\nТЕКСТ:\n' + v2)
    (out / 'v3-punctuation.txt').write_text(v3, encoding='utf-8')
    print(f'  V3: {len(v3.split())} words')
    s3 = justdone(out / 'v3-punctuation.txt')
    print(f'  V3 JustDone: {s3}%')

    scores = {'v1_retell': s1, 'v2_shuffled': s2, 'v3_punctuation': s3}
    (out / 'scores.json').write_text(json.dumps(scores, indent=1), encoding='utf-8')
    print('\n=== SCORES SO FAR ===')
    for k, v in scores.items():
        print(f'  {k}: {v}%')


if __name__ == '__main__':
    main()

"""
run_benchmark.py — BATCH DRIVER
===============================
Runs N fresh papers end-to-end and builds the scoreboard.
Per paper: real Wikipedia corpus -> LLM draft (OpenRouter model) -> style sweep
(config-dependent) -> local gates (ksim, stylecheck) -> ZeroGPT + GPTZero.
plag.bg uploads happen separately after batch review (credit control).

MODELS: all free-tier unless config ends in '-paid-control'. Facts are closed-book
bullets (in papers.json) — the LLM never sees the corpus text, exactly like the
real pipeline.

USAGE:
  python run_benchmark.py --batch state/benchmark/batch1/papers.json           # all
  python run_benchmark.py --batch ... --only pol-izbori                        # one paper
  python run_benchmark.py --batch ... --skip-external                          # local gates only
"""

import functools
print = functools.partial(print, flush=True)
import argparse
import json
import re
import subprocess
import sys
import io
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
SCRIPTS = REALM / 'scripts'
BATCH = REALM / 'state' / 'benchmark' / 'batch1'
SCOREBOARD = REALM / 'state' / 'benchmark' / 'scoreboard.md'
PER_PAPER_TOKENS_IN = 6500
PER_PAPER_TOKENS_OUT = 7500

P1_PROMPT = '''Ти си студент по {course}, пишеш реферат на български (или английски, ако темата е на английски).
ТЕМА: {topic}
ФАКТИ, КОИТО ЗНАЕШ (пиши САМО от тях — не добавяй нови факти, числа или имена):
{facts}

Напиши тялото на реферата: 500-600 думи, 6-8 параграфа. Правила:
- Всички факти от списъка трябва да са вплетени в текста със собствени изречения
- Започвай параграфи с различни конструкции; никоя фамилия/число не измисляй
- Без увод-шаблони ("В днешната статия..."), без заключение-обобщение ("В заключение може да се каже")
- Без списъци с точки — само проза. Без заглавия — само параграфи, разделени с празен ред
- 1 цитат в кавички (кратък, до 15 думи) с автор и година от фактите, ако пасва
'''

P2_SWEEP = '''Ето чернова на реферат (текстът след това). Направи ИЗЧИСТВАНЕ на стила, не презаписване:
1. Увери се, че всеки параграф с 3+ изречения има поне едно КРАТКО изречение (до 7 думи) и поне едно ДЪЛГО (20+ думи) — разделяй и сливай изречения.
2. Параграфите да са неравни по дължина (2-7 изречения); поне един параграф да е 1-2 изречения (ударна линия).
3. Добави 2-3 естествени частици (пък, ама, тоест, все пак) — по една на параграф максимум, не повече.
4. Не променяй числа, дати, имена. Не добавяй нови факти.
5. Първото изречение на текста и последното пренапиши най-сильно — те се помнят.
Върни само чистия текст.

ТЕКСТ:
{text}
'''

P2_AGGRESSIVE = '''Ето чернова на реферат. Направи РЕДИМ-РЕСТАВРАЦИЯ — направи текста да звучи като истински студент, не като машина:
1. Прекъсвай монотонността: кратки удари (до 7 думи), дълги мисловни изречения (20+ думи), фрагменти-акценти ("Един проблем. Парите." — поне един такъв фрагмент в текста).
2. Вкарай разговорни свързки на средата на изречението: "пък", "ама на практика", "тоест", "излиза, че" — 4-5 за целия текст, по една на параграф.
3. Една нерезна лична забележка ("мисля, че", "ми се струва, че") и едно реторично мини-отклонение.
4. Параграфи с различна дължина — един с 6 изречения, друг с 2, друг с 4. Никакви два еднакви по ритъм.
5. НЕ пипай числа, дати, имена. НЕ добавяй факти.
Върни само чистия текст.

ТЕКСТ:
{text}
'''

P2_CHAIN = '''Ти си ДРУГИЯТ студент в курса — състудент, който пише собствена версия на същата тема от същите бележки.
Ето версията на колегата си. Пренапиши я като СВОЯ: различен порядък на изреченията, различни примери-изречения
(същите факти), друг ритъм, други свързки, различно начало и различен край. НИКАКВО изречение от колежката
версия не бива да оцелее дословно (5+ думи подред = провал). Запази всичките факти и точност.
Върни само своята версия.

ВЕРСИЯ НА КОЛЕГАТА:
{text}
'''


def fetch_corpus(topic, wiki_pages, out_dir: Path, lang='bg'):
    """Real Wikipedia extracts as the per-topic corpus."""
    out_dir.mkdir(parents=True, exist_ok=True)
    total = 0
    for title in wiki_pages:
        url = (f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts'
               f'&explaintext=1&format=json&titles={urllib.parse.quote(title)}')
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'benchmark/1.0'})
            page = next(iter(json.loads(urllib.request.urlopen(req, timeout=30).read())['query']['pages'].values()))
            text = page.get('extract', '')
            if text:
                text = re.sub(r'\n==+.+?==+\n', '\n\n', text)
                fn = out_dir / (title.replace(' ', '-').lower() + '.txt')
                fn.write_text(text, encoding='utf-8')
                total += len(text.split())
        except Exception as e:
            print(f'  corpus fetch failed for {title}: {e.__class__.__name__}')
    return total


def call_pi(model: str, prompt: str, timeout: int = 900) -> str:
    """
    Direct OpenRouter chat call (clean system prompt — pi's coding-assistant
    persona made models try to read folders instead of writing referats).
    Key lives in ~/.pi/agent/auth.json (never printed).
    """
    import base64
    auth = json.loads(Path.home().joinpath('.pi/agent/auth.json').read_text(encoding='utf-8'))
    key = auth['openrouter']['key']
    body = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'Ти си студент, който пише реферат за университетския си курс. ' 
             'Отговаряй САМО с текста на реферата — без комментарии, без markdown, без заглавия.'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.9,
    }).encode('utf-8')
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json',
                 'User-Agent': 'benchmark/1.0'})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        out = (resp.get('choices') or [{}])[0].get('message', {}).get('content', '').strip()
        out = re.sub(r'^```[a-z]*\n|```$', '', out, flags=re.M).strip()
        if not out:
            print(f'  OR({model}) empty: {json.dumps(resp)[:200]}')
        return out
    except Exception as e:
        msg = str(e)[:200]
        print(f'  OR({model}) failed: {e.__class__.__name__}: {msg}')
        return ''


def price_of(model: str):
    """Live OpenRouter pricing; returns (in, out) $/M tokens or None."""
    try:
        req = urllib.request.Request('https://openrouter.ai/api/v1/models', headers={'User-Agent': 'bench/1.0'})
        for m in json.loads(urllib.request.urlopen(req, timeout=30).read())['data']:
            if m['id'] == model:
                pr = m.get('pricing', {})
                return float(pr.get('prompt', 0)) * 1e6, float(pr.get('completion', 0)) * 1e6
    except Exception:
        pass
    return None


def run_paper(paper: dict, skip_external: bool):
    pid = paper['id']
    d = BATCH / pid
    d.mkdir(parents=True, exist_ok=True)
    print(f'\n=== {pid} | {paper["topic"][:50]} | {paper["config"]} ===')

    # 1. corpus
    wc = fetch_corpus(paper['topic'], paper['wiki'], d / 'corpus', paper.get('lang', 'bg'))
    print(f'  corpus: {wc} words')

    # 2. P1 draft (closed-book — corpus never enters the prompt)
    facts = '\n'.join('- ' + f for f in paper['facts'])
    p1 = call_pi(paper['draft_model'], P1_PROMPT.format(
        course=paper['course'], topic=paper['topic'], facts=facts))
    if not p1:
        return {'id': pid, 'error': 'draft failed'}
    (d / 'p1-draft.txt').write_text(p1, encoding='utf-8')
    w1 = len(p1.split())
    print(f'  P1 draft: {w1} words')

    # 3. P2 sweep per config
    sweep_model = paper['sweep_model']
    if paper['config'] == 'chain':
        sweep_prompt = P2_CHAIN.format(text=p1)
    elif paper['config'] == 'aggressive':
        sweep_prompt = P2_AGGRESSIVE.format(text=p1)
    else:
        sweep_prompt = P2_SWEEP.format(text=p1)
    p2 = call_pi(sweep_model, sweep_prompt)
    final = p2 if p2 else p1
    (d / ('p2-' + ('chain.txt' if paper['config'] == 'chain' else 'style-pass.txt'))).write_text(final, encoding='utf-8')
    print(f'  P2 sweep: {len(final.split())} words ({sweep_model})')

    # 4. local gates
    res = {'id': pid, 'config': paper['config'], 'models': f'{paper["draft_model"]} -> {sweep_model}',
           'words': len(final.split()), 'topic': paper['topic']}
    try:
        r = subprocess.run([sys.executable, str(SCRIPTS / 'ksim.py'), str(d / 'p2-style-pass.txt' if (d / 'p2-style-pass.txt').exists() else d / 'p2-chain.txt'), str(d / 'corpus'), '--json', str(d / 'ksim.json')],
                           capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace')
        j = json.loads(r.stdout[r.stdout.find('{'):r.stdout.rfind('}') + 1])
        res['ksim_ks1'] = j['ks1']['ge4_pct_nonquote']
        res['ksim_ks2'] = j['ks2']['ge25_count_nonquote']
        res['ksim_verdict'] = j['verdict']
    except Exception as e:
        res['ksim_verdict'] = f'ERROR {e.__class__.__name__}'
    try:
        r = subprocess.run([sys.executable, str(SCRIPTS / 'stylecheck.py'), str(d / ('p2-style-pass.txt' if (d / 'p2-style-pass.txt').exists() else 'p2-chain.txt'))],
                           capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        out = r.stdout
        n_issues = out.count(' - ') + out.count('\n   - ')
        res['stylecheck'] = 'PASS' if 'VERDICT: PASS' in out else f'FAIL({n_issues})'
    except Exception as e:
        res['stylecheck'] = f'ERROR {e.__class__.__name__}'

    # 5. external battery (headless — sessions are saved)
    if not skip_external:
        final_file = d / 'p2-style-pass.txt' if (d / 'p2-style-pass.txt').exists() else d / 'p2-chain.txt'
        try:
            r = subprocess.run([sys.executable, str(SCRIPTS / 'battery_zerogpt.py'), str(final_file), '--words', '350', '--headless'],
                               capture_output=True, text=True, timeout=300, encoding='utf-8', errors='replace')
            m = re.search(r'AI GPT\*: (\d{1,3}(?:\.\d+)?)%', r.stdout + r.stderr)
            res['zerogpt_ai'] = m.group(1) if m else 'n/a'
        except Exception as e:
            res['zerogpt_ai'] = f'ERR {e.__class__.__name__}'
        try:
            r = subprocess.run([sys.executable, str(SCRIPTS / 'battery_gptzero.py'), str(final_file), '--words', '350', '--headless'],
                               capture_output=True, text=True, timeout=600, encoding='utf-8', errors='replace')
            m = re.search(r'AI SCORE: (\d{1,3}(?:\.\d+)?)', r.stdout + r.stderr)
            res['gptzero_ai'] = m.group(1) if m else 'n/a'
        except Exception as e:
            res['gptzero_ai'] = f'ERR {e.__class__.__name__}'

    # 6. cost
    pr = price_of(paper['draft_model'])
    if pr and ':free' not in paper['draft_model']:
        res['cost_usd'] = round(PER_PAPER_TOKENS_IN / 1e6 * pr[0] + PER_PAPER_TOKENS_OUT / 1e6 * pr[1], 4)
    else:
        res['cost_usd'] = 0.0

    append_scoreboard(res)
    return res


def append_scoreboard(res):
    SCOREBOARD.parent.mkdir(parents=True, exist_ok=True)
    if not SCOREBOARD.exists():
        SCOREBOARD.write_text(
            '| paper | config | models | words | ksim KS2/KS1 | style | zerogpt AI% | gptzero AI% | cost $\n'
            '|---|---|---|---|---|---|---|---|---|\n', encoding='utf-8')
    ks = f'{res.get("ksim_ks2", "?")}/{res.get("ksim_ks1", "?")}'
    row = (f'| {res["id"]} | {res["config"]} | {res["models"][:60]} | {res.get("words","?")} | {ks} '
           f'| {res.get("stylecheck","?")} | {res.get("zerogpt_ai","-")} | {res.get("gptzero_ai","-")} | {res.get("cost_usd",0)} |\n')
    SCOREBOARD.open('a', encoding='utf-8').write(row)
    print(f'  SCOREBOARD ROW: {row.strip()[:120]}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', default=str(BATCH / 'papers.json'))
    ap.add_argument('--only', help='run a single paper id')
    ap.add_argument('--skip-external', action='store_true')
    a = ap.parse_args()
    papers = json.loads(Path(a.batch).read_text(encoding='utf-8'))['papers']
    scored = set()
    if SCOREBOARD.exists():
        scored = {line.split('|')[1].strip() for line in SCOREBOARD.read_text(encoding='utf-8').splitlines()
                  if line.startswith('|') and not line.startswith('| paper') and not line.startswith('|---')}
    todo = [p for p in papers if (not a.only or p['id'] == a.only) and p['id'] not in scored]
    if scored:
        print(f'skipping already scored: {sorted(scored)}')
    print(f'batch: {len(todo)} papers')
    for i, p in enumerate(todo, 1):
        print(f'\n[{i}/{len(todo)}]')
        try:
            run_paper(p, a.skip_external)
        except Exception as e:
            print(f'  PAPER {p["id"]} CRASHED: {e.__class__.__name__}: {str(e)[:200]}')
    print('\nBATCH DONE — scoreboard:', SCOREBOARD)

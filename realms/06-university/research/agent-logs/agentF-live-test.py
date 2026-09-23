"""
agentF-live-test.py — live OpenRouter test of the "cheap/fast 2026" class for
Bulgarian academic text, mirroring run_benchmark.py's call_pi conventions.
Measures: latency, tokens/sec, exact cost (usage-based), writing style stats.
"""
import json, re, time, urllib.request
from pathlib import Path

KEY = json.loads(Path.home().joinpath('.pi/agent/auth.json').read_text(encoding='utf-8'))['openrouter']['key']

SYS = ('Ти си студент, който пише реферат за университетския си курс. '
       'Отговаряй САМО с текста на реферата — без комментарии, без markdown, без заглавия.')

PROMPTS = {
 'tema1': '''ТЕМА: Управленческите решения в условия на неопределеност
ФАКТИ: (1) Х. Саймън — концепция на ограничената рационалност (1957). (2) Даниел Канеман и Амос Тверски — теория на перспективата, 1979. (3) Принцип на "достаточно доброто" решение (satisficing). (4) Роля на интуицията и евристики при кризисни решения.
Напиши тялото на реферата: 500-600 думи, 6-8 параграфа. Всички факти вплети със собствени изречения. Без увод-шаблони, без заключение-обобщение, без списъци. Само проза, параграфи разделени с празен ред.''',
 'tema2': '''ТЕМА: Дигиталната трансформация на малкия и средния бизнес в България
ФАКТИ: (1) Доклад на ЕК 2023 — индекс DESI, България 27-ма от 27 в ЕС. (2) Програма "Цифрова България 2030". (3) 40% на МСП не използват облачни услуги. (4) Е-фактурирание задължително от 2025 при B2B.
Напиши тялото на реферата: 500-600 думи, 6-8 параграфа. Всички факти вплети със собствени изречения. Без увод-шаблони, без заключение-обобщение, без списъци. Само проза, параграфи разделени с празен ред.''',
}

MODELS = [
    'inclusionai/ling-3.0-flash-vl:free',   # the 2026 cheap-fast class (InclusionAI/Ling)
    'inclusionai/ling-3.0-flash',           # same, paid tier, real cost
    'z-ai/glm-5.3-flashx',                  # Z.ai high-speed variant
    'deepseek/deepseek-v4-flash-0731',      # DeepSeek cheap flash
    'qwen/qwen3.7-flash',                   # Qwen cheap flash
]

# live price table  (model -> in/out $ per 1M token)
def price_table():
    out = {}
    req = urllib.request.Request('https://openrouter.ai/api/v1/models', headers={'User-Agent': 'agentF/1.0'})
    for m in json.loads(urllib.request.urlopen(req, timeout=30).read())['data']:
        out[m['id']] = (float(m['pricing']['prompt']), float(m['pricing']['completion']))
    return out

def call(model, prompt, sysmsg):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'system', 'content': sysmsg}, {'role': 'user', 'content': prompt}],
        'temperature': 0.9,
    }).encode('utf-8')
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json',
                 'User-Agent': 'agentF/1.0'})
    t0 = time.time()
    resp = json.loads(urllib.request.urlopen(req, timeout=300).read())
    dt = time.time() - t0
    ch = resp['choices'][0]
    msg = ch['message']
    content = (msg.get('content') or '').strip()
    usage = resp.get('usage', {})
    costs = resp.get('costs') or {}
    return content, dt, usage, costs

def style_stats(txt):
    words = re.findall(r'[А-Яа-яЀ-ӹA-Za-z0-9]+', txt)
    sents = [s for s in re.split(r'(?<=[.!?])\s+', txt) if len(s.strip()) > 1]
    slens = [len(re.findall(r'\s+', s)) + 1 for s in sents]
    n = len(words)
    ttr = (len(set(w.lower() for w in words)) / n) if n else 0
    ngrams = set(zip(words, words[1:], words[2:], words[3:]))
    rep4 = 1 - (len(ngrams) / max(1, n - 3))
    vac = (sum(1 for s in slens if s <= 7) / len(slens)) if slens else 0
    mean = (sum(slens) / len(slens)) if slens else 0
    sd = (sum((x - mean) ** 2 for x in slens) / len(slens)) ** .5 if slens else 0
    return dict(words=n, sents=len(slens), sent_avg=round(mean, 1), sent_sd=round(sd, 1),
                short_ratio=round(vac, 2), ttr=round(ttr, 3), rep4=round(rep4, 3))

def main():
    prices = price_table()
    report = []
    for topic, prompt in PROMPTS.items():
        for model in MODELS:
            try:
                txt, dt, usage, costs = call(model, prompt, SYS)
            except Exception as e:
                print(f'FAIL {model} / {topic}: {type(e).__name__}: {str(e)[:180]}')
                continue
            pin = usage.get('prompt_tokens', 0); pout = usage.get('completion_tokens', 0)
            pr = prices.get(model)
            cost = costs.get('total_cost') if isinstance(costs, dict) else None
            if cost is None and pr:
                cost = pin * pr[0] + pout * pr[1]
            tps = round(pout / dt, 1)
            stats = style_stats(txt)
            entry = dict(model=model, topic=topic, text=txt, lat_s=round(dt, 1), out_tok=pout,
                         tps=tps, cost_usd=round((cost or 0) * 1e6, 2) if cost else 0,  # micro-US$
                         cost_text=f'${cost:.7f}' if cost else 'free', **stats)
            report.append(entry)
            print(f"{model:<36} {topic:<6} {pout:>5} tok {tps:>6} tok/s  {entry['cost_text']:<12} "
                  f"sent_avg={stats['sent_avg']} sd={stats['sent_sd']} ttr={stats['ttr']} rep4={stats['rep4']}")
    Path('agentF-live-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    print('saved agentF-live-results.json')

main()
"""skill-v8-combined.py — SKILL generation + V8 transformations + GRAMMAR GATES on every sentence."""
import sys, io, re, json, subprocess, urllib.request, functools
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print = functools.partial(print, flush=True)
from pathlib import Path
auth = json.loads(Path.home().joinpath('.pi/agent/auth.json').read_text(encoding='utf-8'))
KEY = auth['openrouter']['key']
DS = 'deepseek/deepseek-v4-flash-0731'
QW = 'qwen/qwen3.7-flash'
JUDGE = 'mistralai/mistral-small-3.2-24b-instruct'
REALM = Path(__file__).resolve().parents[1]
OUT = REALM / 'state' / 'optimize' / 'skill-v8-combined'
OUT.mkdir(parents=True, exist_ok=True)

def call(model, system, prompt, timeout=150, temp=1.0):
    body = json.dumps({'model': model, 'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': prompt}], 'temperature': temp}).encode()
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=body,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        return (resp.get('choices') or [{}])[0].get('message', {}).get('content', '').strip()
    except Exception as e:
        print(f'    call fail: {e.__class__.__name__}')
        return ''

def grammar_gate(sentence):
    if re.search(r'\b[a-я]{22,}\b', sentence, re.IGNORECASE):
        return False
    r = call(JUDGE,
        'Ти си строг учител по български език. Отговаряш САМО: VERDICT: CHISTA или VERDICT: GRESHKA + до 5 думи защо.',
        f'Провери това изречение за ГРАМАТИЧЕСКИ грешки на български:\nслепени думи, руски думи, счупени форми, несъществуващи думи, халюцинации. Запетайки НЕ са грешки.\n\nИЗРЕЧЕНИЕ: "{sentence}"',
        timeout=60, temp=0.0)
    return 'CHISTA' in r.upper() and 'GRESHKA' not in r.upper()

facts = '''- 1947: доктрина на Труман — сдържане на комунизма
- План Маршал (1948): икономическа помощ за Западна Европа
- 1948-49: Берлинска блокада, преодоляна с въздушен мост
- 1949: учредяване на НАТО; 1955: Варшавският договор като отговор
- Октомври 1962: Кубинската ракетна криза — най-близкият момент до ядрена война
- 70-те: детант (разреждане), договори SALT-1 (1972)
- 1985: Горбачов — гласност и перестройка
- Ноември 1989: падането на Берлинската стена
- Декември 1991: разпад на СССР, край на биполярния свят'''

skill = Path('C:/Users/User/Desktop/PERFORM/uni/skill-how-humans-write.md').read_text(encoding='utf-8')
GENERATION_SYS = 'Ти си български студент, който пише реферат по международни отношения.\n\n' + skill + '\n\nТЕМА: Студената война: произход, основни фази и край на биполярния свят\n\nФАКТИ (използвай САМО тях):\n' + facts + '\n\nНАПИШИ: 450-550 думи, 6-7 параграфа проза. Върни само текста.'

# STAGE 1: GENERATE
print('=== STAGE 1: GENERATE with skill ===')
draft = call(DS, GENERATION_SYS, 'Напиши реферата сега.', timeout=300, temp=1.0)
draft = re.sub(r'^```[a-z]*\n|```$', '', draft, flags=re.M).strip()
(OUT / 'stage1-draft.txt').write_text(draft, encoding='utf-8')
print(f'  draft: {len(draft.split())} words')

# STAGE 2: GRAMMAR GATE on every sentence
print('\n=== STAGE 2: GRAMMAR GATE ===')
sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', draft) if s.strip()]
clean_sents = []
for i, s in enumerate(sents):
    ok = grammar_gate(s)
    tag = '✓' if ok else '✗'
    print(f'  [{i+1}/{len(sents)}] {tag} | {s[:55]}...')
    if ok:
        clean_sents.append(s)
    else:
        fix = call(DS, 'Ти си студент, който пише на СЪВЪРШЕН български. Връщаш само едно изречение.',
                   f'Пренапиши като ГОТОВО ЗА ПРЕДАВАНЕ — граматика перфектна:\n\n"{s}"', timeout=120, temp=0.8)
        fix = re.sub(r'\s+', ' ', fix).strip()
        if fix and grammar_gate(fix):
            clean_sents.append(fix)
            print(f'    -> FIXED')
        else:
            clean_sents.append(s)
            print(f'    -> keeping original')

print(f'\n  clean: {len(clean_sents)}/{len(sents)}')

# STAGE 3: MICRO-REWRITE with gates
print('\n=== STAGE 3: MICRO-REWRITE with gates ===')
final_sents = []
for i, s in enumerate(clean_sents):
    r = call(QW if i % 2 == 0 else DS,
        'Ти си студент. Пишеш на български. Връщаш само едно изречение.',
        f'Пренапиши — друг ред на думите, друга конструкция, запази числата/имената. Граматика СЪВЪРШЕНА:\n\n"{s}"',
        timeout=120, temp=1.0)
    r = re.sub(r'\s+', ' ', (r or s)).strip()
    if not r.endswith(('.', '!', '?')): r += '.'
    ok = grammar_gate(r)
    if ok:
        final_sents.append(r)
        print(f'  [{i+1}] ✓ {r[:55]}...')
    else:
        final_sents.append(s)
        print(f'  [{i+1}] kept original')

# STAGE 4: ASSEMBLE + JITTER
text_final = ' '.join(s if s.endswith(('.', '!', '?')) else s + '.' for s in final_sents)
dropped = 0
for pat in [r'([а-я]), (че )', r'([а-я]), (да )', r'([а-я]), (което )']:
    m = re.search(pat, text_final)
    if m and dropped < 3:
        text_final = text_final[:m.start()] + m.group(1) + text_final[m.end():]
        dropped += 1
(OUT / 'final.txt').write_text(text_final, encoding='utf-8')
print(f'\nFINAL: {len(text_final.split())} words, {dropped} jitters')

# STYLECHECK
r = subprocess.run([sys.executable, str(REALM / 'scripts' / 'stylecheck.py'), str(OUT / 'final.txt')],
    capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
print('\n=== STYLECHECK ===')
print(r.stdout[-400:])

# JUSTDONE x3
print('\n=== JUSTDONE ×3 ===')
scores = []
for i in range(3):
    r = subprocess.run([sys.executable, str(REALM / 'scripts' / 'battery_justdone.py'), str(OUT / 'final.txt'), '--words', '300'],
        capture_output=True, text=True, timeout=420, encoding='utf-8', errors='replace')
    m = re.search(r'JustDone AI%: (\d{1,3}(?:\.\d+)?)', r.stdout + r.stderr)
    s = m.group(1) if m else 'n/a'
    scores.append(s)
    print(f'  scan {i+1}: {s}%')
    import time; time.sleep(15)
print(f'\nMEDIAN: {sorted(scores)[1] if len(scores) == 3 and all(x.replace(".","").isdigit() for x in scores) else "n/a"}%')

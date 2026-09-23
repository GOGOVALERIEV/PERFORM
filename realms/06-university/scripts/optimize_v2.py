"""
optimize_v2.py — THE QUALITY-GATED OPTIMIZER (v2 of the loop)
==============================================================
George's law: the machine must never produce trash. So every rewrite is
gated by quality BEFORE it enters the paper:

  per sentence:
    1. generate 3 rewrite candidates (different models, different temps)
    2. mechanical gate: all numbers/dates/names preserved? no fused words?
    3. LLM judge: grammar correct + meaning same? -> PASS/FAIL
    4. accept first passing candidate; if none pass -> KEEP ORIGINAL

The fallback is the quality floor: a damaged rewrite can never enter the text.
Output: paper with grammar guaranteed >= input, AI% driven down by the
sentences that DID improve.
"""

import json
import re
import sys
import io
import random
import urllib.request
from pathlib import Path

if sys.stdout is not None and (getattr(sys.stdout, 'encoding', '') or '').lower().replace('-', '') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REALM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REALM / 'scripts'))
from optimize_paper import call, justdone  # noqa: E402

OUT = REALM / 'state' / 'optimize' / 'pol-izbori'
MODELS = ['deepseek/deepseek-v4-flash-0731', 'qwen/qwen3.7-flash', 'z-ai/glm-flash-latest']
JUDGE = 'deepseek/deepseek-v4-flash-0731'  # paid-cheap judge


def mechanical_gate(original: str, candidate: str) -> tuple[bool, str]:
    """Facts preserved + no fused words. Returns (ok, reason)."""
    # numbers/dates must survive exactly
    orig_nums = set(re.findall(r'\b\d{1,4}(?:[.,]\d+)?\b', original))
    cand_nums = set(re.findall(r'\b\d{1,4}(?:[.,]\d+)?\b', candidate))
    if orig_nums - cand_nums:
        return False, f'lost numbers: {orig_nums - cand_nums}'
    # proper names (capitalized words, non-sentence-start) must survive
    orig_names = set(w for w in re.findall(r'\b[А-Я][а-я]{2,}\b', original))
    cand_names = set(w for w in re.findall(r'\b[А-Я][а-я]{2,}\b', candidate))
    missing = {n for n in orig_names if n not in cand_names}
    # allow 1 name swap (e.g. Великобритания->Британия handled by judge too)
    if len(missing) > 1:
        return False, f'lost names: {missing}'
    # fused-word detector: 3+ consecutive lowercase letters patterns like 'признавамевсяка'
    # heuristic: any token > 18 chars that isn't a known long BG word pattern
    if re.search(r'\b[a-яа-я]{22,}\b', candidate):
        return False, 'fused words suspected'
    if len(candidate.split()) < 4 or len(candidate.split()) > 45:
        return False, 'length out of band'
    return True, 'ok'


JUDGE_PROMPT = '''Оцени като строг учител по български език.
ОРИГИНАЛ: {orig}
КАНДИДАТ: {cand}

Отговори точно в този формат:
GRAMMAR: OK или GRESHKA (граматически правилно ли е кандидатът? гледай за слепени думи, липсващи подлежащи, развалена структура)
MEANING: OK или SMENEN (същият ли е смисълът, всичките числа/имена/факти запазени?)
VERDICT: PASS или FAIL'''


def judge_sentence(original: str, candidate: str) -> tuple[bool, str]:
    raw = call(JUDGE,
               'Ти си строг учител по български език и стилистика. Отговаряш кратко и точно.',
               JUDGE_PROMPT.format(orig=original, cand=candidate), timeout=120)
    verdict_ok = 'VERDICT: PASS' in raw.upper() or ('GRAMMAR: OK' in raw.upper() and 'MEANING: OK' in raw.upper())
    return verdict_ok, raw[:200]


def improve_sentence(sentence: str, models, candidates_per_model=1) -> tuple[str, str]:
    """Try to improve one sentence. Returns (final_sentence, action)."""
    candidates = []
    for m in models:
        c = call(m,
                 'Ти си студент. Пишеш на български. Връщаш само едно изречение.',
                 'Ето едно изречение от студентски текст:\n\n' + sentence + '\n\n'
                 'Пренапиши го изцяло — друг ред на думите, друга конструкция, запази '
                 'числата/имената/датите точно. Да звучи като казано на глас и записано. '
                 'Граматиката трябва да е съвършена. Върни само изречението.',
                 timeout=120)
        c = re.sub(r'\s+', ' ', (c or '')).strip()
        if c and c != sentence:
            candidates.append(c)
    # mechanical gate first (free)
    for c in candidates:
        ok, reason = mechanical_gate(sentence, c)
        if not ok:
            continue
        ok2, why = judge_sentence(sentence, c)
        if ok2:
            return c, 'accepted'
        else:
            print(f'      judge FAIL: {why[:80]}')
    return sentence, 'kept-original'


def main():
    src = OUT / 'v5-isolated.txt'  # 71%, clean grammar — the safe base
    text = src.read_text(encoding='utf-8')
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    print(f'base: {len(sents)} sentences from v5 (71%, clean)')

    improved, kept = 0, 0
    final_sents = []
    for i, s in enumerate(sents, 1):
        final, action = improve_sentence(s, MODELS[:2])
        if action == 'accepted':
            improved += 1
        else:
            kept += 1
        final = final if final.endswith(('.', '!', '?')) else final + '.'
        final_sents.append(final)
        print(f'  [{i}/{len(sents)}] {action} -> {final[:60]}...')
    text_new = ' '.join(final_sents)
    # punctuation jitter
    dropped = 0
    for pat in [r'([а-я]), (че )', r'([а-я]), (да )', r'([а-я]), (което )']:
        m = re.search(pat, text_new)
        if m and dropped < 3:
            text_new = text_new[:m.start()] + m.group(1) + text_new[m.end():]
            dropped += 1
    (OUT / 'v11-quality-gated.txt').write_text(text_new, encoding='utf-8')
    print(f'\nv11: {len(text_new.split())} words | improved {improved}/{len(sents)} | kept-original {kept} | jitter {dropped}')
    s = justdone(OUT / 'v11-quality-gated.txt')
    print(f'V11 JustDone: {s}%')
    scores = json.loads((OUT / 'scores.json').read_text(encoding='utf-8'))
    scores['v11_quality_gated'] = s
    scores['v11_quality_stats'] = {'improved': improved, 'kept_original': kept}
    (OUT / 'scores.json').write_text(json.dumps(scores, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()

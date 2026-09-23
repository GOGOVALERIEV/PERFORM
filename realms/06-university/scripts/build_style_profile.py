"""build_style_profile.py — extract PDFs with pdfplumber + build the style profile."""
import sys, io, re, json, statistics, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
print = __import__('functools').partial(print, flush=True)
from pathlib import Path
import pdfplumber

REALM = Path(__file__).resolve().parents[1]
pdfs = sorted((REALM / 'state/style-corpus/pdfs').glob('*.pdf'))
corpus_dir = REALM / 'state/style-corpus/texts'
corpus_dir.mkdir(parents=True, exist_ok=True)

good_texts = []
for pdf in pdfs:
    txt_out = corpus_dir / (pdf.stem + '.txt')
    try:
        with pdfplumber.open(str(pdf)) as pf:
            text = ' '.join((p.extract_text() or '') for p in pf.pages)
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split()
        cyr = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
        if len(words) < 800 or cyr / max(len(text), 1) < 0.3:
            print(f'{pdf.name}: skipped ({len(words)} words, cyr {round(100*cyr/max(len(text),1))}%)')
            continue
        txt_out.write_text(text, encoding='utf-8')
        good_texts.append((pdf.stem, text))
        print(f'{pdf.name}: KEPT {len(words)} words')
    except Exception as e:
        print(f'{pdf.name}: ERROR {e.__class__.__name__}: {str(e)[:80]}')

print(f'\nre-extracted: {len(good_texts)} texts')

# ---- profile with artifact filtering ----
all_sents, connectors, first_words = [], collections.Counter(), collections.Counter()
total_words, word_freq = 0, collections.Counter()
CONNECTORS = ['обаче', 'но', 'така', 'ако', 'защото', 'докато', 'от друга страна',
              'в същото време', 'освен това', 'въпреки че', 'пък', 'тоест', 'с други думи',
              'следователно', 'поради това']

for stem, text in good_texts:
    total_words += len(text.split())
    sents = re.split(r'(?<=[.!?])\s+', text)
    for s in sents:
        w = s.split()
        if len(w) < 4 or len(w) > 80:
            continue
        cyr = sum(1 for c in s if '\u0400' <= c <= '\u04FF')
        if cyr < len(s) * 0.5:
            continue
        all_sents.append(s)
        low = s.lower()
        for c in CONNECTORS:
            if re.search(r'\b' + re.escape(c) + r'\b', low):
                connectors[c] += 1
        fw = re.findall(r'[а-яё]+', low)
        if fw:
            first_words[fw[0]] += 1
        for w in re.findall(r'[а-яё]{5,}', low):
            word_freq[w] += 1

lens = [len(s.split()) for s in all_sents]
mean, sd = statistics.mean(lens), statistics.stdev(lens)
profile = {
    'corpus': {'texts': len(good_texts), 'total_words': total_words, 'sentences': len(all_sents)},
    'sentence_stats': {
        'mean_words': round(mean, 1),
        'sd': round(sd, 1),
        'sigma_over_mean': round(sd / mean, 2),
        'pct_short_<=7w': round(100 * sum(1 for l in lens if l <= 7) / len(lens), 1),
        'pct_long_>=20w': round(100 * sum(1 for l in lens if l >= 20) / len(lens), 1),
        'p10': sorted(lens)[len(lens) // 10],
        'p50': sorted(lens)[len(lens) // 2],
        'p90': sorted(lens)[len(lens) * 9 // 10],
    },
    'connectors_per_1k_sentences': {c: round(1000 * n / len(all_sents), 1) for c, n in connectors.most_common(14)},
    'top_25_words': word_freq.most_common(25),
    'top_15_openers': first_words.most_common(15),
}
(REALM / 'state/style-corpus/style-profile.json').write_text(
    json.dumps(profile, ensure_ascii=False, indent=1), encoding='utf-8')
print('\n=== STYLE PROFILE ===')
print(json.dumps(profile, ensure_ascii=False, indent=1)[:2000])
print('\nDONE')

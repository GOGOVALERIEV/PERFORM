"""LANE 3c FINAL: bazar.bg - full listing extraction, <= 300 EUR filter."""
import re
from common import get

report = open("lane3c_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 3c: BAZAR.BG FINAL (budget <= 300 EUR)")
all_listings = []
for q in ["lenovo thinkpad", "dell latitude", "hp elitebook", "laptop i5 ssd"]:
    url = f"https://www.bazar.bg/obiavi?q={q.replace(' ', '%20')}&priceTo=300"
    try:
        r = get(url, timeout=30)
        log(f"\n== '{q}' -> {r.status_code} len {len(r.text)}")
        if r.status_code != 200: continue
        t = r.text
        blocks = re.findall(r'<a[^>]+href="(https://bazar\.bg/obiavi/[^"]+)"[^>]*>\s*<div class="title">(.*?)</a>', t, re.S)
        log("blocks:", len(blocks))
        for href, inner in blocks:
            title = re.search(r'<span class="title">\s*([^<]+)', inner)
            loc = re.search(r'<span class="location">([^<]*)', inner)
            date = re.search(r'<span class="date">([^<]*)', inner)
            price = re.search(r'<span class="price">([\d.,]+)', inner)
            if title:
                p = float(price.group(1).replace(",", ".")) if price else None
                item = dict(title=title.group(1).strip()[:130], loc=(loc.group(1).strip() if loc else "?"),
                            date=(date.group(1).strip() if date else "?"), price=p, url=href)
                all_listings.append(item)
                flag = " <<< TARGET" if p is not None and p <= 300 else ""
                log(f"  {p if p else '?':>7} EUR | {item['title'][:95]} | {item['loc']} | {item['date']}{flag}")
    except Exception as e:
        log(q, "ERR", str(e)[:80])

log("\n\n=== ALL <= 300 EUR, laptop-relevant, sorted ===")
import unicodedata
def is_laptop(x):
    tl = x["title"].lower()
    return any(k in tl for k in ["лаптоп", "laptop", "thinkpad", "latitude", "elitebook", "probook", "notebook", "ultrabook"])
good = [x for x in all_listings if x["price"] and x["price"] <= 300 and is_laptop(x)]
good.sort(key=lambda x: x["price"])
for x in good:
    log(f"{x['price']:7.2f} EUR | {x['title'][:110]} | {x['loc']} | {x['url'][:90]}")
log("\nTOTAL relevant <=300 EUR:", len(good))
report.close()

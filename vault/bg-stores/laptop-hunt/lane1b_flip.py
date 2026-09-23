"""LANE 1b: Flip.bg - find cheapest MacBook from sitemap, get real prices."""
import re
from common import get

report = open("lane1b_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

r = get("https://flip.bg/sitemap-laptop.xml", timeout=30)
locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
products = [l for l in locs if "/magazin/" in l]
log("total laptop product pages:", len(products))

# fetch sample of product pages, extract price + title
import random
sample = products[::max(1, len(products)//15)][:15]
log("\n== SAMPLED PRODUCT PRICES ==")
results = []
for u in sample:
    try:
        rr = get(u, timeout=25)
        t = rr.text
        title = re.search(r"<title>([^<]+)</title>", t)
        prices = re.findall(r'"price":"?([\d.]+)', t)
        if not prices:
            prices = re.findall(r'(\d{3,4}(?:[.,]\d\d)?)\s*лв', re.sub(r"<[^>]+>", " ", t))
        log(u.split("/laptop")[-1][:80], "|", (title.group(1)[:60] if title else "?"), "| prices:", sorted(set(prices))[:3])
        if prices:
            results.append((min(float(p.replace(",", ".")) for p in prices if p), u))
    except Exception as e:
        log(u, "ERR", str(e)[:60])

if results:
    results.sort()
    log("\nCHEAPEST SAMPLED:", results[0])
report.close()

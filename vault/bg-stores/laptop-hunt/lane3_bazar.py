"""LANE 3: bazar.bg + other BG marketplaces."""
import re
from common import get, jina

report = open("lane3_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 3: BAZAR.BG + ALTERNATIVES")
# probe bazar.bg laptop category
for url in ["https://www.bazar.bg/ads/laptops/", "https://www.bazar.bg/obiavi/kompyutri-i-periferiya/laptopi/",
            "https://www.bazar.bg/search?q=thinkpad"]:
    try:
        r = get(url, timeout=25)
        log(url, "->", r.status_code, "len", len(r.text))
        if r.status_code == 200 and len(r.text) > 5000:
            open("lane3_bazar_page.html", "w", encoding="utf-8").write(r.text)
            break
    except Exception as e:
        log(url, "ERR", e)

# search thinkpad/latitude/elitebook on bazar
for q in ["thinkpad", "latitude", "elitebook"]:
    try:
        r = get(f"https://www.bazar.bg/obiavi/q-{q}/laptopi", timeout=25)
        log(f"\n== bazar.bg q-{q} -> {r.status_code} len {len(r.text)}")
        if r.status_code == 200:
            # extract listing titles and prices
            t = re.sub(r"<script.*?</script>", "", r.text, flags=re.S)
            titles = re.findall(r'title="([^"]{15,120})"', t)
            prices = re.findall(r'(\d[\d\s.,]*)\s*лв', t)
            log("titles sample:", list(dict.fromkeys(titles))[:15])
            log("prices sample:", prices[:20])
    except Exception as e:
        log("bazar ERR", e)
report.close()

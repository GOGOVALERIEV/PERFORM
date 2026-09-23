"""LANE 3b: bazar.bg with CORRECT query format."""
import re
from common import get

report = open("lane3b_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 3b: BAZAR.BG (fixed URLs)")
for q in ["lenovo thinkpad", "dell latitude", "hp elitebook"]:
    url = f"https://www.bazar.bg/obiavi?q={q.replace(' ', '%20')}"
    try:
        r = get(url, timeout=30)
        log(f"\n== {q} -> {r.status_code} len {len(r.text)}")
        if r.status_code == 200:
            t = r.text
            # find listing blocks: title + price + link
            items = re.findall(r'<a[^>]+href="(https://www\.bazar\.bg/obiavi/[^"]+)"[^>]*title="([^"]{10,150})"', t)
            prices = re.findall(r'itemprop="price"[^>]*content="([\d.]+)"', t)
            if not prices:
                prices = re.findall(r'(\d{2,4}(?:[.,]\d\d)?)\s*лв', re.sub(r"<script.*?</script>", "", t, flags=re.S))
            log("listing links:", len(items))
            seen = set()
            for link, title in items:
                if link in seen: continue
                seen.add(link)
                log(f"  - {title.strip()[:100]} | {link[:100]}")
            log("prices on page:", sorted(set(prices))[:25])
            if items:
                open("lane3b_bazar_thinkpad.html", "w", encoding="utf-8").write(t)
    except Exception as e:
        log(q, "ERR", str(e)[:80])
report.close()

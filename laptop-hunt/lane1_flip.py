"""LANE 1: Flip.bg deep dive - ALL laptops, prices, what exists under 600 BGN."""
import re, json
from common import get, budget_bgn

report = open("lane1_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 1: FLIP.BG LAPTOP CATALOG")
log("budget in BGN:", round(budget_bgn()))
r = get("https://flip.bg/laptop/apple/", timeout=30)
html = r.text
objs = re.findall(r'\{[^{}]*"price"[^{}]*\}', html)
log("products found on /laptop/apple/:", len(objs))
rows = []
for o in objs:
    try:
        d = json.loads(o)
        if d.get("price") and d.get("title"):
            rows.append((float(d["price"]), d["title"]))
    except Exception:
        pass
rows.sort()
log("\n== ALL MACBOOKS ON FLIP.BG (price BGN | model) ==")
for p, t in rows:
    tag = " <== UNDER BUDGET" if p <= 600 else ""
    log(f"{p:8.2f} BGN ({p/1.95583:6.1f} EUR) | {t}{tag}")

# cheapest 3 product pages for details (grade, battery info)
log("\n== CHEAPEST LISTING DETAILS ==")
r2 = get("https://flip.bg/laptop/", timeout=30)
slugs = re.findall(r'"(/magazin/[^"]+)"', r2.text)
lap_slugs = [s for s in slugs if "laptopi" in s][:5]
for s in lap_slugs:
    try:
        rr = get("https://flip.bg" + s, timeout=30)
        txt = re.sub(r"<[^>]+>", " ", rr.text)
        txt = re.sub(r"\s+", " ", txt)
        m = re.search(r'(?:Гаранция|garanci[^ ]*)[^.]{0,120}', txt, re.I)
        price = re.findall(r'(\d[\d.,]+)\s*(?:лв|BGN)', txt)
        log(s, "| prices:", price[:4])
    except Exception as e:
        log(s, "ERR", e)
report.close()

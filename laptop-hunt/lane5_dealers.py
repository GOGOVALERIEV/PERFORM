"""LANE 5: BG refurbished laptop dealers - shops, prices, warranty."""
import re
from common import ddg, get, jina

report = open("lane5_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 5: BG REFURB DEALERS")
for q in ["рефърбиширани лаптопи магазин България", "used laptops Bulgaria shop thinkpad",
          "втора ръка лаптопи София магазин гаранция", "refurbished laptops Bulgaria онлайн магазин"]:
    log(f"\n== DDG: {q}")
    try:
        for href, txt in ddg(q):
            log(f"  - {txt[:100]} | {href[:130]}")
    except Exception as e:
        log("  ddg ERR", e)

# probe known candidate shops
for shop in ["https://laptop.bg/", "https://www.itplaza.bg/", "https://bolero.bg/", "https://www.pаcífic.com/"]:
    try:
        r = get(shop, timeout=20)
        log("probe", shop, "->", r.status_code, len(r.text))
    except Exception as e:
        log("probe", shop, "ERR", str(e)[:80])
report.close()

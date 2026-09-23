"""LANE 5b: BG dealers - scrape thinkpad-class laptops under 600 BGN."""
import re
from common import get

report = open("lane5b_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

SITES = {
    "technodream": [
        "https://technodream.bg/category/laptopi-lenovo-thinkpad-vtora-ruka",
        "https://technodream.bg/category/laptopi-vtora-ruka",
    ],
    "hop.bg": [
        "https://hop.bg/laptops-111",
        "https://hop.bg/en/laptops-111(filter=lenovo,brand=1)",
    ],
    "ardes": ["https://ardes.bg/upotrebyavani-laptopi/laptopi-vtora-upotreba"],
    "kvantservice": ["https://www.kvantservice.com/laptopi/lenovo/thinkpad/"],
    "outletpc": ["https://outletpc.bg/%D0%BB%D0%B0%D0%BF%D1%82%D0%BE%D0%BF%D0%B8-%D0%B2%D1%82%D0%BE%D1%80%D0%B0-%D1%83%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B0"],
}
for name, urls in SITES.items():
    log(f"\n===== {name} =====")
    for url in urls:
        try:
            r = get(url, timeout=30)
            log(url[:80], "->", r.status_code, "len", len(r.text))
            if r.status_code != 200 or len(r.text) < 3000:
                continue
            t = r.text
            # generic product extraction: titles + prices
            titles = re.findall(r'title="([^"]{20,140})"|>([^<>]{20,140}(?:ThinkPad|Latitude|EliteBook|ProBook)[^<>]{0,60}))', t, re.I)
            prices = re.findall(r'(?:price[^>]{0,60}?>|с листа|price-value[^>]*>)\s*([\d\s.,]{3,9})', t)
            if not prices:
                prices = re.findall(r'([\d]{2,4}(?:[.,]\d{2})?)\s*(?:лв|BGN|lv)', t)
            clean_titles = list(dict.fromkeys([(a or b).strip() for a, b in titles]))[:20]
            for ct in clean_titles:
                log("  T:", ct[:120])
            log("  prices:", sorted(set(prices))[:30])
            open(f"lane5b_{name}.html", "w", encoding="utf-8").write(t)
        except Exception as e:
            log(url[:80], "ERR", str(e)[:90])
report.close()

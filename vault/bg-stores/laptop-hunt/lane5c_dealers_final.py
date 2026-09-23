"""LANE 5c FINAL: dealer sites - save HTML then extract text+products."""
import re
from common import get

SITES = {
    "technodream_thinkpad": "https://technodream.bg/category/laptopi-lenovo-thinkpad-vtora-ruka",
    "technodream_all": "https://technodream.bg/category/laptopi-vtora-ruka",
    "hop_bg": "https://hop.bg/en/laptops-111(filter=lenovo,brand=1)",
    "ardes": "https://ardes.bg/upotrebyavani-laptopi/laptopi-vtora-upotreba",
    "kvantservice": "https://www.kvantservice.com/laptopi/lenovo/thinkpad/",
    "outletpc": "https://outletpc.bg/%D0%BB%D0%B0%D0%BF%D1%82%D0%BE%D0%BF%D0%B8-%D0%B2%D1%82%D0%BE%D1%80%D0%B0-%D1%83%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B0",
}
for name, url in SITES.items():
    try:
        r = get(url, timeout=40)
        fn = f"dl_{name}.html"
        open(fn, "w", encoding="utf-8").write(r.text)
        print(name, r.status_code, "saved", len(r.text))
    except Exception as e:
        print(name, "ERR", str(e)[:80])

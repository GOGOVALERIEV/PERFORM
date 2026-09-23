"""Verify top candidate product pages: real price, RAM, SSD, battery, warranty, grade."""
import re, html as H
from common import get

targets = [
    ("ARDES-L5320-88eur?", "https://ardes.bg/product/dell-latitude-5320-renoviran-produkt-80130040-547640"),
    ("ARDES-EB830G6-88eur?", "https://ardes.bg/product/hp-elitebook-830-g6-renoviran-produkt-80099111-224844"),
    ("OUTLETPC-T490-239", "https://outletpc.bg/lenovo-thinkpad-t490-38349"),
    ("OUTLETPC-X390-204", "https://outletpc.bg/lenovo-thinkpad-x390-46600"),
    ("OUTLETPC-T495-254", "https://outletpc.bg/lenovo-thinkpad-t495-44389"),
    ("HOP-T580-229", "https://hop.bg/en/laptops-111/laptop-lenovo-thinkpad-t580comma-i5-8350ucomma-16gbcomma-512-111(id=63548)"),
    ("KVANT-T490", "https://www.kvantservice.com/product/lenovo-thinkpad-t490-24393-id55000/"),
    ("KVANT-T480s", "https://www.kvantservice.com/product/lenovo-thinkpad-t480s-17255-id56308/"),
    ("KVANT-T590", "https://www.kvantservice.com/product/lenovo-thinkpad-t590-35995-id56017/"),
    ("KVANT-T490s", "https://www.kvantservice.com/product/lenovo-thinkpad-t490s-31942-id56331/"),
]
for name, url in targets:
    try:
        r = get(url, timeout=40)
        t = r.text
        print(f"\n===== {name} -> {r.status_code}")
        if r.status_code != 200:
            continue
        txt = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
        txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", txt)
        txt = H.unescape(re.sub(r"\s+", " ", txt))
        # price: first plausible price
        pr = re.findall(r'(\d[\d.,]{1,8})\s*(?:лв|€|BGN|EUR|lv)', txt[:6000])
        print("PRICE candidates:", pr[:8])
        # battery / warranty / grade keywords
        for kw in ["батери", "batter", "Wh", "гаранци", "garanci", "клас", " grade", "Grade"]:
            for m in re.finditer(kw, txt, re.I):
                seg = txt[max(0,m.start()-60):m.start()+110].strip()
                if re.search(r"\d|месеца|months|new|нова|A|B", seg):
                    print(f"  [{kw}]:", seg[:170])
                    break
    except Exception as e:
        print(name, "ERR", str(e)[:80])

"""FINAL PARSE: all 6 sources -> one clean EUR list 60-300 EUR, business laptops."""
import re, html as H, urllib.parse
from common import get

F = open("final_list.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=F)

ALL = []
def add(src, title, price, cur, url, extra=""):
    if not title or not price: return
    ALL.append(dict(src=src, title=H.unescape(re.sub(r"\s+", " ", title)).strip(),
                    price=float(price), cur=cur, url=url, extra=extra))

def pf(s):
    s = s.strip().replace(" ", "").replace("\xa0", "")
    if "," in s: s = s.replace(".", "").replace(",", ".")
    elif s.count(".") >= 2: s = s.replace(".", "")
    return float(s)

# ---- 1 BAZAR ----
log("### 1. BAZAR.BG")
for q in ["lenovo thinkpad", "dell latitude", "hp elitebook", "laptop i5 ssd"]:
    try:
        r = get(f"https://www.bazar.bg/obiavi?q={urllib.parse.quote(q)}&priceTo=300", timeout=30)
        if r.status_code != 200: continue
        t = r.text
        for c in t.split('<div class="title">')[1:]:
            mt = re.search(r'<span class="title">\s*([^<]+)', c)
            if not mt: continue
            head_end = max(0, t.find(c[:80]))
            hrefs = re.findall(r'href="(https://bazar\.bg/obiavi/[^"]+)"', t[max(0, head_end-3000):head_end])
            mp = re.search(r'<span class="price">([\d.,]+)', c)
            ml = re.search(r'<span class="location">([^<]*)', c)
            md = re.search(r'<span class="date">([^<]*)', c)
            title = H.unescape(mt.group(1)).strip()
            if not mp or not any(k in title.lower() for k in ["лаптоп", "laptop", "notebook"]): continue
            p = pf(mp.group(1))
            if p < 60 or p > 300: continue
            extra = f"{ml.group(1).strip() if ml else ''} | {md.group(1).strip() if md else ''}"
            add("bazar.bg", title, p, "EUR", hrefs[-1] if hrefs else "", extra)
    except Exception as e:
        log("bazar ERR", str(e)[:70])

# ---- 2 OUTLETPC ----
log("\n### 2. OUTLETPC.BG")
try:
    r = get("https://outletpc.bg/%D0%BB%D0%B0%D0%BF%D1%82%D0%BE%D0%BF%D0%B8-%D0%B2%D1%82%D0%BE%D1%80%D0%B0-%D1%83%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B0?limit=100", timeout=40)
    for b in r.text.split('class="product-thumb"')[1:]:
        mh = re.search(r'href="(https://outletpc\.bg/[^"]+)"', b)
        mt = re.search(r'title="([^"]{20,300})"', b)
        mp = re.search(r'class="price".{0,250}?([\d.,]+)\s*(лв|€|BGN|EUR)', b, re.S)
        if mp: add("outletpc.bg", mt.group(1) if mt else "", pf(mp.group(1)), mp.group(2), mh.group(1) if mh else "")
except Exception as e:
    log("outletpc ERR", str(e)[:70])

# ---- 3 ARDES ----
log("\n### 3. ARDES.BG")
ardes = ""
for u in ["https://ardes.bg/upotrebyavani-laptopi/laptopi-vtora-upotreba",
          "https://ardes.bg/upotrebyavani-laptopi/laptopi-vtora-upotreba/page/2"]:
    try:
        r = get(u, timeout=40)
        if r.status_code == 200: ardes += r.text
    except Exception as e:
        log("ardes ERR", u[-20:], str(e)[:60])
for tile in re.split(r'<div class="product" data-sku', ardes)[1:]:
    mh = re.search(r'href="(/product/[^"]+)"', tile)
    mt = re.search(r'title="\s*([^"]{15,250})"', tile)
    tile_clean = re.sub(r"<sup>", "", tile)
    mp = re.search(r'class="price".{0,300}?([\d.,]+)\s*(лв|€|BGN)', tile_clean, re.S)
    if mh and mp:
        add("ardes.bg", mt.group(1) if mt else mh.group(1), pf(mp.group(1)), mp.group(2),
            "https://ardes.bg" + mh.group(1))

# ---- 4 HOP ----
log("\n### 4. HOP.BG")
hop_urls = [
    "https://hop.bg/en/laptops-111" + urllib.parse.quote("(filter=up to 300 €,price=61)"),
    "https://hop.bg/en/laptops-111",
]
hop_raw = ""
for u in hop_urls:
    try:
        r = get(u, timeout=40)
        if r.status_code == 200: hop_raw += r.text
    except Exception as e:
        log("hop ERR", str(e)[:60])
chunks = re.split(r"location\.href='(https://hop\.bg/[^']+)'", hop_raw)
for i in range(1, len(chunks) - 1, 2):
    href, c = chunks[i], chunks[i+1]
    ma = re.search(r'alt="([^"]{15,250})"', c)
    mp = re.search(r'(\d+)(?:\.\s*<sup>(\d+)</sup>|([\d.,]+)?)\s*(€|лв|lv)', c)
    if ma and mp:
        whole = mp.group(1) + (("." + mp.group(2)) if mp.group(2) else (mp.group(3) or ""))
        add("hop.bg", ma.group(1), pf(whole), mp.group(4), href)

# ---- 5 TECHNODREAM ----
log("\n### 5. TECHNODREAM.BG")
tech_raw = ""
for u in ["https://technodream.bg/category/laptopi-vtora-ruka",
          "https://technodream.bg/category/laptopi-vtora-ruka?page=2",
          "https://technodream.bg/category/laptopi-lenovo-thinkpad-vtora-ruka",
          "https://technodream.bg/category/laptopi-dell-vtora-ruka",
          "https://technodream.bg/category/laptopi-hp-vtora-ruka"]:
    try:
        r = get(u, timeout=40)
        if r.status_code == 200: tech_raw += r.text
    except Exception as e:
        log("techno ERR", u[-25:], str(e)[:50])
for m in re.finditer(r'"type":"product","id":\d+,"parameter_id":\d+,"name":"([^"]{10,200})".{0,400}?"url":"https:\\?/\\?/technodream\.bg\\?/product\\?/([^"]+)".{0,1200}?"price":([\d.]+),"discount_price":"([\d.]*)","currency":"([A-Z]+)"', tech_raw, re.S):
    name, url, price, disc, cur = m.groups()
    p = float(disc) if disc else float(price)
    add("technodream.bg", name, p, cur, url.replace("\/", "/"))

# ---- 6 KVANTSERVICE ----
log("\n### 6. KVANTSERVICE.COM")
t = open("dl_kvantservice.html", encoding="utf-8").read()
for tile in re.split(r'data-product-id="\d+"', t)[1:]:
    mt = re.search(r'class="[^"]*slider_product_title[^"]*">([^<]{5,120})<', tile)
    if not mt: continue
    mh = re.search(r'data-link-href="(https://www\.kvantservice\.com/product/[^"]+)"', tile)
    ms = re.findall(r'<span class="ml_minus_5"[^>]*>([^<]+)</span>', tile)
    mp = re.search(r'([\d.,]+)\s*(лв|€|BGN)', tile)
    cond = "A" if "kvant_status_a" in tile else ("B" if "kvant_status_b" in tile else "?")
    if mt:
        add("kvantservice.com", mt.group(1), pf(mp.group(1)) if mp else None, mp.group(2) if mp else "?",
            mh.group(1) if mh else "", "спец:" + " | ".join(s.strip() for s in ms[:4]) + f" | клас:{cond}")

# ---------- MASTER ----------
log("\n\n================ FINAL MASTER (60-300 EUR) ================")
def to_eur(p, cur):
    return p / 1.95583 if cur in ("лв", "BGN") else p
BUS = re.compile(r"thinkpad|latitude|elitebook|probook|lifebook", re.I)
GEN = re.compile(r"лаптоп|laptop|notebook", re.I)
master = []
for a in ALL:
    if not BUS.search(a["title"]) and not (GEN.search(a["title"]) and a["src"] == "bazar.bg"):
        continue
    e = to_eur(a["price"], a["cur"])
    if not (60 <= e <= 300): continue
    a["eur"] = round(e, 2)
    master.append(a)
# dedupe by (src, title[:60])
seen = set(); uniq = []
for a in master:
    k = (a["src"], a["title"][:60])
    if k in seen: continue
    seen.add(k); uniq.append(a)
uniq.sort(key=lambda x: x["eur"])
for a in uniq:
    log(f"{a['eur']:7.2f} EUR | {a['src']:16} | {a['title'][:105]} | {a['extra'][:60]}")
    log(f"           {a['url'][:120]}")
log("\nTOTAL CANDIDATES:", len(uniq))
F.close()

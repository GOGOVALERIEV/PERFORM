"""HARVEST: pair products+prices on all dealers + bazar.bg. Output master list <= 300 EUR."""
import re, html as H
from common import get

out = open("master_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=out)

ALL = []  # dicts: source, title, price, currency, url


def pf(s):
    s = s.strip().replace(" ", "").replace(" ", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") >= 2:
        s = s.replace(".", "")
    return float(s)

def add(source, title, price, cur, url):
    if title and price:
        ALL.append(dict(source=source, title=H.unescape(re.sub(r'\s+', ' ', title)).strip(),
                        price=price, cur=cur, url=url))

# ---------- 1. BAZAR.BG ----------
log("########## 1. BAZAR.BG ##########")
for q in ["lenovo thinkpad", "dell latitude", "hp elitebook", "laptop i5 ssd"]:
    url = f"https://www.bazar.bg/obiavi?q={q.replace(' ', '%20')}&priceTo=300"
    try:
        r = get(url, timeout=30)
        if r.status_code != 200: continue
        t = r.text
        chunks = t.split('<div class="title">')
        for c in chunks[1:]:
            m_title = re.search(r'<span class="title">\s*([^<]+)', c)
            if not m_title: continue
            head = t[max(0, t.find(c[:100]) - 3000):t.find(c[:100])]
            hrefs = re.findall(r'href="(https://bazar\.bg/obiavi/[^"]+)"', head)
            href = hrefs[-1] if hrefs else ""
            m_loc = re.search(r'<span class="location">([^<]*)', c)
            m_date = re.search(r'<span class="date">([^<]*)', c)
            m_price = re.search(r'<span class="price">([\d.,]+)', c)
            title = H.unescape(m_title.group(1)).strip()
            if not any(k in title.lower() for k in ["лаптоп", "laptop", "notebook", "ултрабук"]): continue
            p = pf(m_price.group(1)) if m_price else None
            if p is None or p > 320: continue
            item = dict(source="bazar.bg", title=title[:120], price=p, cur="EUR", url=href,
                        extra=f"{m_loc.group(1).strip()} | {m_date.group(1).strip()}")
            ALL.append(item)
            log(f"  {p:7.2f} EUR | {title[:100]} | {item['extra']}")
    except Exception as e:
        log("bazar ERR", q, str(e)[:80])

# ---------- 2. OUTLETPC ----------
log("\n########## 2. OUTLETPC.BG ##########")
t = open("dl_outletpc.html", encoding="utf-8").read()
blocks = t.split('class="product-thumb"')
for b in blocks[1:]:
    m_href = re.search(r'href="(https://outletpc\.bg/[^"]+)"', b)
    m_title = re.search(r'title="([^"]{20,300})"', b)
    m_price = re.search(r'class="price".{0,200}?([\d.,]+)\s*(лв|€|BGN|EUR)', b, re.S)
    if m_price:
        add("outletpc.bg", m_title.group(1) if m_title else "", 
            pf(m_price.group(1)), m_price.group(2), m_href.group(1) if m_href else "")
for a in ALL:
    if a["source"] == "outletpc.bg":
        log(f"  {a['price']:8.2f} {a['cur']} | {a['title'][:105]}")

# pagination try: limit=100
try:
    r = get("https://outletpc.bg/%D0%BB%D0%B0%D0%BF%D1%82%D0%BE%D0%BF%D0%B8-%D0%B2%D1%82%D0%BE%D1%80%D0%B0-%D1%83%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B0?limit=100", timeout=40)
    n = r.text.count('class="product-thumb"')
    log("  page with limit=100 ->", r.status_code, "products:", n)
    if n > 40:
        open("dl_outletpc_full.html", "w", encoding="utf-8").write(r.text)
        blocks = r.text.split('class="product-thumb"')
        outletpc_full = []
        for b in blocks[1:]:
            m_href = re.search(r'href="(https://outletpc\.bg/[^"]+)"', b)
            m_title = re.search(r'title="([^"]{20,300})"', b)
            m_price = re.search(r'class="price".{0,200}?([\d.,]+)\s*(лв|€|BGN|EUR)', b, re.S)
            if m_price:
                outletpc_full.append(dict(source="outletpc.bg", 
                    title=H.unescape(m_title.group(1)) if m_title else "",
                    price=pf(m_price.group(1)), cur=m_price.group(2), url=m_href.group(1) if m_href else ""))
        ALL = [a for a in ALL if a["source"] != "outletpc.bg"] + outletpc_full
        log("  outletpc total products now:", len(outletpc_full))
except Exception as e:
    log("  outletpc pagination ERR", str(e)[:60])

# ---------- 3. ARDES ----------
log("\n########## 3. ARDES.BG ##########")
ardes_text = ""
for page in ["dl_ardes.html"]:
    ardes_text += open(page, encoding="utf-8").read()
try:
    r = get("https://ardes.bg/upotrebyavani-laptopi/laptopi-vtora-upotreba/page/2", timeout=40)
    log("  page2:", r.status_code, len(r.text))
    if r.status_code == 200: ardes_text += r.text
except Exception as e:
    log("  ardes page2 ERR", str(e)[:60])

# pair: each product block = <a href="/product/..." ...> ... title ... then price div
prod_chunks = re.split(r'href="(https://ardes\.bg/product/[^"]+)"', ardes_text)
for i in range(1, len(prod_chunks) - 1, 2):
    href, chunk = prod_chunks[i], prod_chunks[i+1]
    m_title = re.search(r'title="([^"]{15,300})"', chunk)
    m_price = re.search(r'class="price".{0,300}?([\d.,]+)\s*(лв|€|BGN|EUR)', chunk, re.S)
    if m_title and m_price:
        add("ardes.bg", m_title.group(1), pf(m_price.group(1)), m_price.group(2), href)
for a in [x for x in ALL if x["source"] == "ardes.bg"]:
    log(f"  {a['price']:8.2f} {a['cur']} | {a['title'][:105]} | {a['url'][:70]}")

# ---------- 4. HOP.BG ----------
log("\n########## 4. HOP.BG ##########")
import urllib.parse
hop_url = "https://hop.bg/en/laptops-111" + urllib.parse.quote("(filter=up to 300 €,price=61)")
try:
    r = get(hop_url, timeout=40)
    log("  <=300 EUR filter page:", r.status_code, len(r.text))
    if r.status_code == 200:
        open("dl_hop_300.html", "w", encoding="utf-8").write(r.text)
        blocks = re.split(r"location\.href='(https://hop\.bg/en/[^']+)'", r.text)
        for i in range(1, len(blocks) - 1, 2):
            href, chunk = blocks[i], blocks[i+1]
            m_alt = re.search(r'alt="([^"]{15,250})"', chunk)
            m_price = re.search(r'class="price".{0,300}?([\d.,]+)\s*(лв|€|BGN|EUR|lv)', chunk, re.S)
            if m_alt and m_price:
                add("hop.bg", m_alt.group(1), pf(m_price.group(1)), m_price.group(2), href)
except Exception as e:
    log("  hop ERR", str(e)[:80])
for a in [x for x in ALL if x["source"] == "hop.bg"]:
    log(f"  {a['price']:8.2f} {a['cur']} | {a['title'][:105]}")

# ---------- 5. TECHNODREAM ----------
log("\n########## 5. TECHNODREAM.BG ##########")
for fn in ["dl_technodream_thinkpad.html", "dl_technodream_all.html"]:
    t = open(fn, encoding="utf-8").read()
    chunks = re.split(r'href="(https://technodream\.bg/product/[^"]+)"', t)
    for i in range(1, len(chunks) - 1, 2):
        href, chunk = chunks[i], chunks[i+1]
        m_title = re.search(r'title="([^"]{10,250})"', chunk) or re.search(r'>([^<>]{10,180}(?:ThinkPad|LifeBook|Latitude|EliteBook)[^<>]{0,80})<', chunk)
        m_price = re.search(r'([\d.,]+)\s*(?:лв|€|BGN|EUR|lv)', chunk[:1500])
        if m_title:
            add("technodream.bg", m_title.group(1), pf(m_price.group(1)) if m_price else None, 
                "BGN?" if m_price else "?", href)
seen = set()
for a in [x for x in ALL if x["source"] == "technodream.bg"]:
    k = a["title"][:50]
    if k in seen: continue
    seen.add(k)
    log(f"  {a['price']} {a['cur']} | {a['title'][:105]}")

# ---------- 6. KVANTSERVICE ----------
log("\n########## 6. KVANTSERVICE.COM ##########")
t = open("dl_kvantservice.html", encoding="utf-8").read()
chunks = re.split(r'href="(https://www\.kvantservice\.com/product/[^"]+)"', t)
for i in range(1, len(chunks) - 1, 2):
    href, chunk = chunks[i], chunks[i+1]
    m_title = re.search(r'title="([^"]{10,200})"', chunk) or re.search(r'>([^<>]{10,150}ThinkPad[^<>]{0,80})<', chunk)
    m_price = re.search(r'([\d.,]+)\s*(?:лв|€|BGN|EUR|lv)', chunk[:1200])
    if m_title and "ThinkPad" in (m_title.group(1) or ""):
        add("kvantservice.com", m_title.group(1), pf(m_price.group(1)) if m_price else None,
            "BGN?" if m_price else "?", href)
seen = set()
for a in [x for x in ALL if x["source"] == "kvantservice.com"]:
    k = a["url"]
    if k in seen: continue
    seen.add(k)
for a in [x for x in ALL if x["source"] == "kvantservice.com"]:
    k = a["url"]
    if k in seen: continue
    seen.add(k)
    log(f"  {a['price']} {a['cur']} | {a['title'][:105]} | {a['url'][:80]}")

log("\n\n================= MASTER LIST: ALL <= 300 EUR =================")
def to_eur(p, cur):
    if cur in ("BGN", "BGN?"): return p / 1.95583
    return p
master = []
for a in ALL:
    if not a["price"]: continue
    e = to_eur(a["price"], a["cur"])
    if e <= 300 and re.search(r"thinkpad|latitude|elitebook|probook|laptop|notebook|lifebook", a["title"], re.I):
        a["eur"] = e
        master.append(a)
master.sort(key=lambda x: x["eur"])
for a in master:
    log(f"{a['eur']:7.2f} EUR ({a['price']:.2f} {a['cur']}) | {a['source']:16} | {a['title'][:100]}")
    log(f"          {a.get('url','')[:120]}  {a.get('extra','')}")
log("\nTOTAL:", len(master))

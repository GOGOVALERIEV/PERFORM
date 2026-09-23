import requests, re

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
BASE = "https://flip.bg"

# 1. sitemap probe
for sm in ["sitemap.xml", "sitemap-laptop.xml", "sitemap_index.xml"]:
    try:
        r = requests.get(f"{BASE}/{sm}", headers=UA, timeout=20)
        print(sm, r.status_code, len(r.text))
        if r.status_code == 200 and "<loc>" in r.text:
            locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
            lap = [l for l in locs if "laptop" in l.lower()]
            print("  total locs:", len(locs), "laptop locs:", len(lap))
            for l in lap[:15]: print("   ", l)
    except Exception as e:
        print(sm, "ERR", e)

# 2. probe brand pages directly
for brand in ["lenovo", "hp", "dell", "asus", "apple"]:
    r = requests.get(f"{BASE}/laptop/{brand}/", headers=UA, timeout=20)
    t = r.text
    n = len(re.findall(r'"price"', t))
    print(brand, r.status_code, "len", len(t), "price objs:", n)

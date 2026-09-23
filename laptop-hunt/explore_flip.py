import requests, re

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
BASE = "https://flip.bg"

r = requests.get(BASE + "/laptop/", headers=UA, timeout=30)
html = r.text
print("status", r.status_code, "len", len(html))

objs = re.findall(r'\{[^{}]*"price"[^{}]*\}', html)
print("price objs:", len(objs))
for o in objs[:3]:
    print(o[:500])
    print("---")

slugs = set(re.findall(r'/(laptop(?:\/|/)[a-zA-Z0-9\-_/]+)', html))
print("slugs:", list(slugs)[:40])

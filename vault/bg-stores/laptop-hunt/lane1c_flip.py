"""LANE 1c: Flip.bg - real price of cheapest MacBooks (known magazin URLs)."""
import re
from common import get
urls = [
    "https://flip.bg/magazin/apple/laptopi-apple-macbook-12-2017-i3-1-2-ghz-8-gb-hd-graphics-615-256gb-space-gray/75268583/",
    "https://flip.bg/magazin/apple/laptopi-apple-macbook-12-2017-i5-1-3-ghz-8-gb-hd-graphics-615-512gb-space-gray/75268591/",
]
for u in urls:
    try:
        r = get(u, timeout=30)
        t = r.text
        title = re.search(r"<title>([^<]+)</title>", t)
        prices = re.findall(r'"price":"?([\d.]+)', t)
        prices2 = re.findall(r'(\d{3,4}(?:[.,]\d{2})?)\s*лв', re.sub(r"<[^>]+>", " ", t))
        print(u.split("/")[-3][:50], "|", title.group(1)[:70] if title else "?")
        print("   json prices:", sorted(set(prices))[:5], "| лв matches:", sorted(set(prices2))[:5])
    except Exception as e:
        print(u[:60], "ERR", str(e)[:60])

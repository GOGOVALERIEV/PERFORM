"""LANE 2b: OLX listings via Bing search (site:olx.bg)."""
import re, urllib.parse
from common import get

report = open("lane2b_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 2b: OLX VIA BING")
queries = [
    'site:olx.bg thinkpad втора ръка',
    'site:olx.bg dell latitude laptop',
    'site:olx.bg hp elitebook laptop',
]
listing_urls = set()
for q in queries:
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&count=30"
    try:
        r = get(url, timeout=30)
        log("\n== bing:", q, "->", r.status_code, "len", len(r.text))
        links = re.findall(r'<a[^>]+href="(https://www\.olx\.bg/d/[^"]+)"', r.text)
        titles = re.findall(r'<h2><a[^>]*>(.*?)</a>', r.text, re.S)
        for h, t in zip(links, titles):
            t = re.sub(r"<[^>]+>", "", t).strip()
            log("  -", t[:110])
            log("    ", h[:130])
            listing_urls.add(h)
        # also grab olx.bg/d/ links generically
        links2 = re.findall(r'href="(https://www\.olx\.bg/d/[^"]+)"', r.text)
        listing_urls.update(links2)
    except Exception as e:
        log("bing ERR", e)

log("\n== TRY DIRECT FETCH OF 2 LISTING PAGES ==")
for u in list(listing_urls)[:2]:
    try:
        rr = get(u, timeout=25)
        log(u[:100], "->", rr.status_code, "len", len(rr.text))
        if rr.status_code == 200:
            txt = re.sub(r"<[^>]+>", " ", rr.text)
            txt = re.sub(r"\s+", " ", txt)
            m = re.findall(r'(\d{2,4}) лв', txt)
            log("  prices found:", m[:6])
    except Exception as e:
        log(u[:100], "ERR", str(e)[:80])
report.close()

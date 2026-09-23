"""Parse saved dealer HTML files into clean product lists."""
import re, glob, html as H

out = open("lane5c_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=out)

def clean(t):
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = H.unescape(t)
    return t

KEY = re.compile(r"thinkpad|latitude|elitebook|probook", re.I)
for fn in sorted(glob.glob("dl_*.html")):
    log("\n\n########", fn, "########")
    raw = open(fn, encoding="utf-8").read()
    t = clean(raw)
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    # collect product-name-ish lines
    names = []
    for l in lines:
        if KEY.search(l) and 8 < len(l) < 160:
            names.append(l)
    seen = set(); uniq = []
    for n in names:
        k = n[:60]
        if k not in seen: seen.add(k); uniq.append(n)
    for n in uniq[:40]:
        log("  NAME:", n[:140])
    # prices
    prices = re.findall(r'(\d{2,4}(?:[.,]\d{2})?)\s*(?:лв|BGN|EUR|€)', t)
    nums = sorted(set(float(p.replace(",", ".")) for p in prices))
    log("  ALL PRICES (BGN/EUR mixed):", [x for x in nums if 50 <= x <= 9000][:60])
    # product links
    links = re.findall(r'href="(https?://[^"]*(?:product|laptop|obiavi|p/|item)[^"]*)"', raw)
    log("  LINKS:", list(dict.fromkeys(links))[:15])
out.close()

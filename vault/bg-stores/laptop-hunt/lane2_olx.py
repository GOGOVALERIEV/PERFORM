"""LANE 2: OLX.bg workaround hunt - jina proxy + API variants."""
import re, json
from common import get, jina

report = open("lane2_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 2: OLX.BG WORKAROUNDS")
queries = ["thinkpad", "dell-latitude", "hp-elitebook", "laptop"]
for q in queries:
    url = f"https://www.olx.bg/ads/q-{q}/?search%5Bfilter_float_price%3Ato%5D=600&search%5Bdist%5D=0"
    log(f"\n===== OLX query: {q} =====")
    try:
        r = jina(url)
        log("jina status:", r.status_code, "len:", len(r.text))
        text = r.text
        # jina returns markdown; extract title+price lines
        lines = [l for l in text.split("\n") if any(x in l for x in ["лв", "BGN", "lv"]) or re.search(r"ThinkPad|Latitude|EliteBook|ProBook|T4|T5|X2|L1|E5|E7", l, re.I)]
        for l in lines[:40]:
            log(l.strip()[:220])
    except Exception as e:
        log("jina ERR", e)

# try olx api variants directly
log("\n===== DIRECT API VARIANTS =====")
variants = [
    "https://www.olx.bg/api/v1/offers/?query=thinkpad&limit=10",
    "https://api.olx.bg/v1/offers/?query=thinkpad",
    "https://www.olx.bg/api/v1/offers/?query=thinkpad&limit=10",
]
for v in variants:
    try:
        r = get(v, timeout=20)
        log(v[:60], "->", r.status_code, r.text[:120].replace("\n", " "))
    except Exception as e:
        log(v[:60], "ERR", e)
report.close()

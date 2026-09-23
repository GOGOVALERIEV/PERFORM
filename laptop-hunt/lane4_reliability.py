"""LANE 4: reliability research - which used business laptops last longest."""
from common import ddg, jina
import re

report = open("lane4_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 4: RELIABILITY RESEARCH")
queries = ["most reliable used business laptop thinkpad vs dell latitude vs hp elitebook",
           "best used laptop under 300 euros thinkpad t480 t490",
           "thinkpad models to avoid used buying guide"]
for q in queries:
    log(f"\n== DDG: {q}")
    try:
        for href, txt in ddg(q):
            log(f"  - {txt[:100]} | {href[:120]}")
    except Exception as e:
        log("  ddg ERR", e)

# fetch 2 best articles via jina
for url in ["https://r.jina.ai/https://www.zdnet.com/article/best-refurbished-laptop/",
            "https://r.jina.ai/https://laptopmedia.com/best-laptops/"]:
    try:
        r = jina(url.replace("https://r.jina.ai/", ""), timeout=40)
        log("\n== fetched:", url, r.status_code, "len", len(r.text))
        log(r.text[:1500])
    except Exception as e:
        log("fetch ERR", e)
report.close()

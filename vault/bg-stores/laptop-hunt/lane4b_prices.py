"""LANE 4b: real used prices - pcprice.watch guide + reddit thread."""
import re
from common import get, jina

report = open("lane4b_report.txt", "w", encoding="utf-8")
def log(*a): print(*a); print(*a, file=report)

log("LANE 4b: REAL USED MARKET PRICES")
for name, url in [
    ("pcprice.watch guide", "https://www.pcprice.watch/guides/used-thinkpad-buyers-guide-2026"),
    ("reddit t480 under 300", "https://www.reddit.com/r/thinkpad/comments/185pufe/is_a_used_t480_the_best_laptop_you_can_buy_under/"),
]:
    log("\n=====", name)
    try:
        r = jina(url, timeout=50)
        log("status:", r.status_code, "len:", len(r.text))
        if r.status_code == 200:
            text = r.text
            # keep lines with model numbers or prices
            keep = [l for l in text.split("\n") if re.search(r"T4[7-9]0|T14|X1|X2[78]0|L4[8-9]0|E4[89]0|E1[45]|Latitude 74|Latitude 54|EliteBook 84|EliteBook 64|\$\d+|€\d+", l)]
            for l in keep[:60]:
                log("  ", l.strip()[:200])
        else:
            log(r.text[:300])
    except Exception as e:
        log("ERR", str(e)[:100])
report.close()

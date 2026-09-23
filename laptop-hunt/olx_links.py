import re, time
from playwright.sync_api import sync_playwright

QUERIES = ["lenovo-thinkpad", "dell-latitude", "hp-elitebook"]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0 Safari/537.36", locale="bg-BG")
    pg = ctx.new_page()
    for q in QUERIES:
        url = f"https://www.olx.bg/ads/q-{q}/?search%5Bfilter_float_price%3Ato%5D=600"
        try:
            pg.goto(url, timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            try: pg.locator("#onetrust-accept-btn-handler").first.click(timeout=2500)
            except Exception: pass
            time.sleep(1.5)
            pairs = pg.eval_on_selector_all("a[data-cy='l-card']",
                "els => els.map(e => ({href: e.href, text: (e.innerText||'').slice(0,300)}))")
            print(f"\n##### {q} -> {len(pairs)} cards")
            for x in pairs:
                t = x["text"].replace("\n", " | ")
                print(t[:200])
                print("   ", x["href"])
        except Exception as e:
            print(q, "ERR", str(e)[:80])
    b.close()

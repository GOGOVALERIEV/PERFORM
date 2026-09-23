"""OLX.bg via Playwright (real browser, beats CloudFront bot-block)."""
import re, time, json
from playwright.sync_api import sync_playwright

QUERIES = ["lenovo thinkpad", "dell latitude", "hp elitebook"]
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900},
        locale="bg-BG",
    )
    page = ctx.new_page()
    for q in QUERIES:
        url = f"https://www.olx.bg/ads/q-{q.replace(' ', '-')}/?search%5Bfilter_float_price%3Ato%5D=600"
        print(f"\n##### {q} -> {url}")
        try:
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            # dismiss cookie banner if present
            for sel in ["button:has-text('Приемам')", "button:has-text('Accept')", "#onetrust-accept-btn-handler"]:
                try:
                    page.locator(sel).first.click(timeout=2500)
                    break
                except Exception:
                    pass
            time.sleep(2)
            # cards
            cards = page.locator('[data-cy="l-card"], a[data-testid="ad-card-container"]')
            n = cards.count()
            print("cards:", n)
            if n == 0:
                html = page.content()
                print("page title:", page.title())
                open(f"olx_debug_{q.split()[0]}.html", "w", encoding="utf-8").write(html)
                continue
            for i in range(min(n, 25)):
                c = cards.nth(i)
                try:
                    title = c.locator("h4, h6, [data-testid='ad-title']").first.inner_text(timeout=2000).strip()
                except Exception:
                    title = ""
                try:
                    price = c.locator('[data-testid="ad-price"], h3').first.inner_text(timeout=2000).strip()
                except Exception:
                    price = ""
                try:
                    href = c.get_attribute("href") or ""
                    if href.startswith("/"): href = "https://www.olx.bg" + href
                except Exception:
                    href = ""
                try:
                    loc = c.locator('[data-testid="location-date"]').first.inner_text(timeout=1500).strip()
                except Exception:
                    loc = ""
                if title:
                    results.append(dict(q=q, title=title, price=price, loc=loc, url=href))
                    print(f"  {price[:15]:>12} | {title[:80]} | {loc[:40]}")
        except Exception as e:
            print("ERR", str(e)[:100])
    browser.close()

with open("olx_results.txt", "w", encoding="utf-8") as f:
    for r in results:
        f.write(f"{r['price']} | {r['title']} | {r['loc']} | {r['url']}\n")
print("\nTOTAL:", len(results))

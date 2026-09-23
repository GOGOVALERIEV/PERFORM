"""OLX whiteboard scan -> cards {title,url,price,location}, filtered Blagoevgrad."""
import re, time, json
from playwright.sync_api import sync_playwright

SEARCHES = ["бяла даска", "дъска за рисуване маркер", "whiteboard"]
cards = {}
seen = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        viewport={"width": 1366, "height": 900}, locale="bg-BG",
    )
    page = ctx.new_page()
    for q in SEARCHES:
        url = f"https://www.olx.bg/obiavi/q-{q.replace(' ', '-')}/?currency=EUR"
        print(f"##### {q}")
        try:
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)
            for sel in ["#onetrust-accept-btn-handler", "button:has-text('Приемам')"]:
                try: page.locator(sel).first.click(timeout=2000)
                except Exception: pass
            time.sleep(1)
            cards_el = page.locator('div[data-cy="l-card"]')
            n = cards_el.count()
            print(" cards:", n)
            for i in range(min(n, 40)):
                c = cards_el.nth(i)
                try:
                    title = c.locator("h4").first.inner_text(timeout=1500).strip()
                    link = c.locator("a").first.get_attribute("href", timeout=1500)
                    if link and not link.startswith("http"): link = "https://www.olx.bg" + link
                    price = ""
                    try: price = c.locator('p[data-testid="ad-price"]').first.inner_text(timeout=1000).strip()
                    except Exception: pass
                    loc = ""
                    try:
                        loc = c.locator('p[data-testid="ad-card-location"]').first.inner_text(timeout=1000).strip()
                    except Exception:
                        try: loc = c.locator("p").nth(2).inner_text(timeout=800).strip()
                        except Exception: pass
                    key = (link or "").split("?")[0]
                    if key and key not in seen:
                        seen.add(key)
                        cards[key] = {"title": title, "url": link, "price": price, "location": loc}
                except Exception:
                    continue
        except Exception as e:
            print(" ERR", str(e)[:120])

allc = list(cards.values())
json.dump(allc, open(r"C:/Users/User/Desktop/PERFORM/vault/olx/2026-09-22_boards_fresh.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nTOTAL:", len(allc))
print("\n== BLAGOEVGRAD ==")
for c in allc:
    if "лагоев" in c["location"]:
        print(c["price"], "|", c["title"][:60], "|", c["location"], "|", c["url"][:80])
print("\n== ALL (first 25) ==")
for c in allc[:25]:
    print(c["price"], "|", c["title"][:55], "|", c["location"])

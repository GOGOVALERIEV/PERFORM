# deal-radar

Daily discount radar for George (student, Blagoevgrad, tight budget).
Trigger: "deals", "deal radar", "какво има ново", "check deals", or part of morning routine.

## THE SYSTEM

- Code: `C:\Users\User\Desktop\project-test\tools\deal-radar\`
- Data: `C:\Users\User\Desktop\project-test\output\deals\` (one JSON per day: YYYY-MM-DD.json)
- Budget context: George is a student; food deals matter most, then dorm/everyday stuff.

## STORES (all physically in Blagoevgrad, OSM-verified 17 Sep 2026)
1. Lidl (food, Mon+Thu promos) — collector: NOT BUILT (JS-locked; needs headed Playwright + network capture)
2. Billa (food, Wed-Tue promos) — collector: CRACKED (collect_billa.py). Method:
   publitas slug from billa.bg brochure page -> <slug>.json HTML shell contains direct
   PDF URL -> download -> pages are IMAGES (no text layer) -> extract page images to
   output/deals/billa_pages/ -> VISION-READ for prices (works, proven 17 Sep).
3. Kaufland (food+home, Thu promos) — collector: CRACKED (collect_kaufland.py v2).
   Same Schwarz API as Lidl! IDs discovered from broshuri.html
   (leaflets.kaufland.com/bg-BG/<ID>/); API gives OCR names+%+page images.
   NOTE: also yields NEXT-week flyer IDs (BG39 = coming week) - future-proofing gold.
4. Metro (wholesale, needs Metro card) — CRACKED: headed Playwright discovers brochure
   IDs (catalogues.metro.bg/food-NNNN), Publitas PDF has TEXT LAYER -> coordinate
   parser (collect_metro.py + inline parser) = 63 priced deals
5. dm (drugstore) — CRACKED (collect_dm.py): Playwright captures products.dm.de
   tiles API -> 35 products. Real domain: dm-drogeriemarkt.bg (dm.bg does NOT exist)
6. Lilly (pharmacy) — CRACKED (collect_lilly.py): HTML direct from aptekililly.bg
   /selection/all-promo-offers (lilly.bg redirects to the pharma giant - wrong site)
7. Technopolis (electronics) — CRACKED (collect_technopolis.py): HTML direct from
   /bg/c/weekly-offers (te-product-box tiles, prices in HTML)
8. JYSK (home/dorm) — collector: page images via iPaper (collect_jysk.py, 25 pages
   saved to output/deals/jysk_pages/) -> prices via vision_ocr (run: python vision_ocr.py <folder> jysk)
9. Office 1 (student supplies) — CRACKED (collect_office1.py): HTML direct, 1904 deals!
10. eMAG (online everything) — CRACKED (collect_emag.py): sapi.emag.bg recommendations
    API, filters real discounts, 42+ deals, supports pagination

NOT in Blagoevgrad (DO NOT add): T-Market, Fantastico, Profi, Fordo, Piccadilly, Zora.

## MORNING FLOW (when triggered)
1. Check `output/deals/` for today's JSON.
   - If missing or stale (>24h): run available collectors (see below), refresh.
   - If collectors are all missing/broken: SAY SO honestly, do not invent deals.
2. Load the JSON, dedupe, sort: food first, then discount % descending.
3. Present as a tight table: Store | Product | Price (old -> new) | % | valid until.
4. Max ~15 lines unless George asks for more.
5. End with 1 line: "Best move today: <single best deal + where>."

## ON-DEMAND FLOW ("check X", "ko e s evtin olio", "check beer prices")
1. Search today's collected data for X (fuzzy match, BG + EN).
2. If not found in data: offer to run a live hunt (open store sites with Playwright headed mode).
3. Present: which store has it cheapest, price history if known.

## COLLECTOR STATUS: 10/10 STORES CRACKED (19 Sep 2026)
### LIDL - collect_lidl.py
- Method: Schwarz leaflets API -> https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier=ID
- Flyer ID auto-discovered from https://www.lidl.bg/c/broshura/s10020060 (slug like 21-09-27-09-353775, pick the one covering today)
- API gives: pages with OCR keyWords (product names + discount %) + page image URLs
- EXACT PRICES: download page images (imgproxy.leaflets.schwarz URLs from the JSON)
  and READ THEM WITH VISION (assistant reads the image file) - this is the price oracle. No OCR lib needed.
- Output: output/deals/lidl_YYYY-MM-DD.json (deals + deals_vision_read)
### Billa / Kaufland / rest - NOT BUILT
- Billa: Publitas leaflet (view.publitas.com/billa-bulgaria/...) - JSON endpoint returns HTML
  shell; headless viewer blocked. Next try: Publitas PDF download inside viewer, or headed Playwright.
- Kaufland: SPA. Try the same Schwarz-style API discovery via headed Playwright network capture
  (Kaufland is also Schwarz Group - endpoints.leaflets.schwarz may serve them too! Try it first.)
- Dead-ends (do not retry): plain requests on promo pages, Publitas .json with/without
  Accept header, headless Playwright on Publitas viewer.
- Reference Playwright+network-capture pattern: tools/deal-radar/crack_lidl2.py

## RULES
- Never present invented/fabricated deals. Missing data = say "no data yet".
- Always note validity dates and "needs Metro card" for Metro.
- eMAG deals: check shipping to Blagoevgrad.

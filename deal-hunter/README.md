# Deal Hunter

Low-cost personal-shopping discovery for Bulgaria. It does not use an LLM, paid search API, proxy, or bulk marketplace scraper.

## Run it

```powershell
node deal-hunter/hunt.js "external SSD 1TB" --budget-bgn 200 --verify 8
```

## Normal use: just ask in Codex

Deal Hunter is also a project skill. In this chat, say what you want in ordinary language, including the limits that matter: budget, new/used, pickup versus delivery, country, brand, urgency, and whether risky offers should be visible. The skill makes a small collection run, adds browser-visible OLX/Temu/Alibaba cards when those sites permit normal browsing, then gives a final comparison in chat.

Example: `Find a new external 1TB SSD under 220 BGN. Delivery is fine, local is a bonus, and show every risky offer too.`

The skill does not make purchases, log in, send sellers messages, or solve CAPTCHAs. Browser-only sources are read only when their normal page is available.

The script uses public store search pages where adapters exist (eMAG, Technopolis, Ardes, AliExpress), then falls back to a small number of Bing `site:` searches for other configured sources. It opens only the top few links, extracting public product metadata where available. Results are cached locally for 24 hours under `output/cache/`.

Useful variants:

```powershell
# Known link: no search at all
node deal-hunter/hunt.js --url "https://www.example.com/product-page"

# Only places where an SSD is sensible to buy
node deal-hunter/hunt.js "Samsung T7 Shield 1TB" --budget-bgn 190 --sources emag,technopolis,technomarket,ozone,amazon_de

# Re-fetch pages instead of using the 24-hour cache
node deal-hunter/hunt.js "external SSD 1TB" --fresh

# The short, natural-language version (still no model/API use)
node deal-hunter/ask.js "find a cheap reliable external SSD under 220 BGN"

# Include all recent browser-read marketplace cards (OLX, Temu, Alibaba)
node deal-hunter/hunt.js "external SSD" --include-browser

# Verify configuration only: does not open any website
node deal-hunter/ask.js "find a cheap external SSD under 220 BGN" --dry-run
```

## What it deliberately does not do

- It does not hammer, bypass, or attempt to defeat bot protections on Temu, Alibaba, AliExpress, Amazon, or any other marketplace.
- It does not call a model to gather links. Model review can happen later, only after the report has narrowed the list.
- It does not pretend the visible price is delivered cost. Confirm shipping, VAT, stock, and return conditions at checkout.

## Reliability logic

`config/sources.json` is the human-editable starting trust map. A local retailer scores more highly than a marketplace. Page-level signals such as a warranty, return policy, and official seller wording can raise the score. For storage devices, low-trust marketplaces and implausible capacity/price combinations are flagged because fake capacity is a real failure mode. Nothing is silently excluded: high-risk deals remain in the report with a visible risk level and the exact reason.

The score is a prioritization tool, not proof that a seller is safe.

## Local stores, OLX, and price memory

Every verified offer is retained in `output/offer-history.json` with first/last-seen dates and a small price history. A report therefore tells us whether a deal is new and gives us the raw material to spot a real price drop later.

Retail sources distinguish ordinary online delivery from a Blagoevgrad pickup possibility. A pickup label means **check the exact product page/branch stock**; it never means that an item is definitely on the shelf.

OLX is browser-only because it blocks raw collectors. A browser reader gathers visible title, price, condition, date, and location, then `olx-import.js` prioritizes `гр. Благоевград` and nearby towns. Include the latest (under 24 hours old) browser collection in a combined report with `--include-olx`. OLX/private offers are always labelled separately from retailer offers and carry an inspect-before-paying warning.

`olx-import.js` is the safe boundary between a browser reader and the local system. It takes a JSON array of visible browser cards (`title`, `url`, `text`), extracts price/location/condition, boosts Blagoevgrad and nearby towns, and flags implausibly cheap high-capacity storage:

```powershell
node deal-hunter/olx-import.js olx-cards.json --query "външен SSD"
```

It writes `output/olx-latest.json`. No OLX login, saved search, message, or payment action is performed.

Temu and Alibaba are configured as browser-only lanes: their public HTTP pages returned verification/CAPTCHA screens in testing. The system can rank browser-read cards when supplied, but will not bypass a site's access controls.

For those lanes, import browser-visible cards with the generic importer, then run the combined hunt:

```powershell
node deal-hunter/browser-import.js temu temu-cards.json --query "external SSD"
node deal-hunter/browser-import.js alibaba alibaba-cards.json --query "external SSD"
node deal-hunter/hunt.js "external SSD" --include-browser
```

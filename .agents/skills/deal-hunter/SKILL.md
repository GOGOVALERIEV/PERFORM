---
name: deal-hunter
description: Find and compare physical-product deals for personal shopping in Bulgaria, including local retailers, OLX, and Chinese marketplaces. Use when the user asks to find, compare, hunt, or evaluate a product deal.
---

Use the project at `C:/Users/User/Desktop/PERFORM/deal-hunter` as one Deal Hunter system. The user speaks normally; do not require a terminal command or a dashboard.

## Interpret the request

Extract the product, essential specifications, budget, new/used preference, location/delivery preference, acceptable sources, urgency, and brand requirements. If a detail is absent, make a reasonable assumption and state it in the final answer only if it materially affected the ranking.

The user wants all offers shown. Never remove an offer just because it is dangerous, implausibly cheap, used, private, wholesale, or low trust. Mark its risk and explain why.

## Collect efficiently

Run the local collector with a small scope first: normally `--max-links 12 --verify 6`, reduced further for a quick answer. Use the source list in `deal-hunter/config/sources.json`.

For OLX, Temu, and Alibaba, use normal browser access only when needed. Do not bypass CAPTCHA, verification, rate limits, or logins. Read only visible search cards. Save visible `{title, url, text}` cards to a temporary JSON file under `deal-hunter/output/`, import OLX through `olx-import.js`, and import Temu/Alibaba through `browser-import.js`. Then rerun `hunt.js` with `--include-browser` so all lanes share one report.

Do not make purchases, message sellers, enter personal data, or log in.

## Answer the shopping request

Read the generated report and make the final judgment against the user's stated priorities. Give a short ranked answer with delivered-price caveats, source/seller facts, local availability when known, and clear risk warnings. Include dangerous offers in their own labelled section or within the ranked list; the user decides whether to buy.

Use `--dry-run` only for configuration/tests. It must not be presented as live shopping results.

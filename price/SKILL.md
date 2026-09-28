# Price — Expense Butler

Log every buy in 1 second from Telegram. No thinking required.

## Notebook & Logs
- `purchases.json` — every buy: date, amount (BGN), what. Never delete it.
- `logs/YYYY-MM-DD.txt` — daily log, one file per day. George writes numbers (electricity, water, food, wifi, phone) as he discovers them. Empty = unknown, never guess.
- `month-budget.json` — the plan: 1500/month. rent 160, bills 100, food 300, else 100.

## Morning Routine Hook
- Tony Stark (Step 4.5) reads the logs + ledger every morning and shows: spent / 1500 / left.
- Data first, discussion second. No data = one gentle reminder, never nagging.

## Daily Use (via the Telegram bridge bot)
- `buy 25 food` → logged instantly, replies with this month's total.
- `bought 12.50 kebab` → same thing. Comma decimals work (1,20).
- `/price` → this month: every buy + total.
- No number in the message (e.g. "thinking of buying a laptop") → goes to pi as a normal chat.

## How it works
- The fast path lives inside `01-productivity/telegram-bridge/bot.mjs` (search for "PRICE").
- It writes straight to the ledger — pi is not involved, so it's instant.
- Messages sent while the PC is asleep wait on Telegram's servers (up to ~24h)
  and get logged when the bridge starts again.

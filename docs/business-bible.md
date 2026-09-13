# How The Whole Thing Actually Works
### From "I have a product idea" to "money lands in my bank account" — the real plumbing

This is the document for the stuff everyone is ashamed to ask: where pages live, how
card payments physically work, who is allowed to pay you, how ad accounts get made,
and what order to do everything in. No Shopify. Claude Code automates every buildable part.

---

## 1. The Map: every online business is the same 5 blocks

Every funnel, every brand, every affiliate campaign — it's always these five blocks
connected by links:

```
PRODUCT  →  PAGES  →  PAYMENTS  →  TRAFFIC  →  TRACKING
(what you  (where you  (how money   (how people  (how you know
 sell)      sell it)    moves)       arrive)      what's working)
```

If you ever feel lost, ask: "which block am I in right now?" Everything in this doc
fits into one of those five.

---

## 2. Internet plumbing — what a website ACTUALLY is

**A website is just files sitting on a computer that never turns off.**
That's it. An advertorial is an HTML file. A landing page is an HTML file.
Claude Code writes HTML files all day. The only question is which always-on
computer they sit on.

The three pieces:

1. **Domain** — the address (`menopausereset.com`). You rent it for ~$10/year from a
   registrar (Cloudflare or Namecheap — Cloudflare is cheapest, no upsell games).
2. **Hosting** — the always-on computer holding your files. For our stack:
   **Cloudflare Pages** or **Vercel** — both have free tiers that are genuinely free
   forever for sites like ours, both deploy straight from a GitHub repo. Claude Code
   pushes to GitHub → 30 seconds later the page is live on the internet. That IS the
   "posting" you were asking about.
3. **DNS** — the phone book that connects the domain name to the hosting computer.
   You set it once in the registrar dashboard ("point menopausereset.com to
   Cloudflare Pages") and never think about it again.

**The workflow with Claude Code:**
```
You: "Claude, build the advertorial from this copy"
 → Claude writes advertorial.html in a git repo
 → git push
 → Cloudflare Pages auto-deploys
 → live at menopausereset.com/article in under a minute
 → that URL goes into the ad
```
No page builder. No Shopify. No monthly fee. Total cost: the domain.

**The brutal truth about "how do people see it":** they don't. A new website is
invisible. Google won't send you traffic for months/years (SEO is a slow different
game). Nobody stumbles onto it. **In DR, 100% of your visitors are BOUGHT with ads.**
The website is a store built in the desert — the ads are the only road to it.
That's why ad skills (your skills) are the business.

---

## 3. Payments — how card details actually work

**Rule #1: you never touch card numbers. Ever.** Handling raw card data requires
bank-level security certification (called PCI compliance). Nobody does it themselves —
everyone uses a **payment processor**.

### How a purchase physically flows
```
Buyer clicks "Buy Now" on YOUR page
 → browser goes to a CHECKOUT page hosted by the processor (looks like yours, isn't)
 → buyer types card details INTO THE PROCESSOR's page (never touches your server)
 → processor talks to the card networks (Visa/Mastercard), takes the money
 → money sits in your processor account
 → processor pays out to your business bank account every few days
 → processor pings YOUR system: "sale happened!" (this ping is called a WEBHOOK)
 → your Claude-built script catches the webhook → emails the buyer the book
```

### Your two options as a digital-product seller

**Option A — Stripe (the developer standard)**
- Fee: ~2.9% + €0.30 per sale. Available in Bulgaria.
- You create a "product" and a "checkout link" via Stripe's API (Claude Code can
  literally create products and payment links with a script).
- **Catch:** Stripe requires a legal entity + bank account + ID verification (KYC)
  BEFORE you can take money. And YOU are responsible for charging EU customers VAT
  — which for digital products means charging each EU country's own VAT rate and
  filing for it (OSS scheme). Your accountant handles it, but it's real admin.

**Option B — Merchant of Record / MoR (Paddle, Lemon Squeezy, Gumroad)**
- Fee: ~5% + payment fees (roughly double Stripe).
- THEY are legally the seller — they handle ALL the VAT/sales-tax mess in every
  country, they handle refunds/chargebacks, they deliver the file automatically.
- You can start as an individual on some of them — before the firm even exists.

**Honest recommendation (not yes-man advice):** start with a Merchant of Record for
the first product. The extra ~3% fee is the cheapest accountant you'll ever hire,
and you can be selling THIS WEEK. Switch to Stripe when you're doing thousands/month
and the fee difference is real money. "Automate everything with Claude Code" does NOT
mean build your own checkout — payments is the one block where you plug into someone
else's fortress. We automate AROUND it (product creation, webhooks, delivery, reporting)
via their APIs.

### Delivering the book
Digital delivery = an automatic email with a download link after purchase.
MoR platforms do it built-in. With Stripe, Claude builds a tiny webhook script:
"purchase event received → send email with the PDF link." One file of code.

---

## 4. The firm — when and what (Bulgaria)

You need a legal entity for: a Stripe account, a business bank account, signing
affiliate network agreements at scale, and not having tax problems.

- **The standard BG move: ЕООД** (single-owner limited company). Minimum capital is
  symbolic (2 лв). Registration via a lawyer/accountant costs a few hundred leva and
  takes about a week. You get an **ЕИК** (company ID number).
- **In BG an accountant is effectively mandatory** (monthly filings) — roughly
  100–250 лв/month. Get the accountant BEFORE registering; they usually handle the
  registration too, and they'll advise on VAT registration (required past 100k лв
  revenue/12mo, or earlier for EU digital sales — ask them about OSS).
- **Business bank account** — opened after registration with the ЕИК. This is where
  Stripe/Paddle/affiliate networks send payouts.
- **Order of operations:** you do NOT need the firm on day 1. Build the product and
  funnel first (costs ~$10), validate that ads can sell it, THEN register when money
  starts flowing — or immediately if you go the Stripe route (Stripe needs the entity).
- ⚠️ I'm not a lawyer or accountant — the above is the standard pattern; confirm the
  details with a BG accountant.

---

## 5. Ad accounts — making your own from zero

### Meta (your home turf)
1. A real, aged personal Facebook profile (yours).
2. Go to **business.facebook.com** → create a **Business Manager/Portfolio** (your own
   "JF Market", but it's George's).
3. Inside the BM, create: a **Facebook Page** (the identity ads run from), an
   **Ad Account** (the wallet — add your card), and a **Pixel/Dataset** (goes on your pages).
4. **Business verification** (upload company docs) unlocks higher limits and trust.

**The warm-up reality nobody tells beginners:** fresh ad accounts are fragile.
Meta's automated systems ban new accounts for things established accounts get away
with. Start at $10–20/day, run squeaky-clean ads for the first weeks, never log in
from weird devices/VPNs, and expect a small spending limit that grows with history.
Getting banned in week 1 is a beginner rite of passage — avoid it by being boring
at first. (And per your own rule: Meta only in Edge.)

### Google Ads (since you asked how it works)
Google is a DIFFERENT animal than Meta:
- **Meta = demand CREATION.** People are scrolling, not shopping. You interrupt them
  with a hook and create desire. Creative (the ad) is everything.
- **Google Search = demand CAPTURE.** People type "how to stop menopause weight gain"
  — they're ALREADY looking. You bid on **keywords**, your text ad shows in the
  results, you pay per click (**PPC**). The targeting is the search itself.
- Setup: ads.google.com → account → campaign → choose keywords → write text ads →
  set budget → add billing. No "page" or BM needed — simpler than Meta.
- Google also has **YouTube ads** (video, Meta-like) and **Performance Max** (their
  "trust the machine" version of ASC).

**Honest recommendation:** ignore Google for now. One channel, mastered, beats two
channels half-learned — and your skills, your job, and Boris's machine are all Meta.
Google Search becomes interesting later to capture people who saw your Meta ad and
googled the product name.

---

## 6. The two business models, wired end-to-end

### Model A — Affiliate (selling OTHER people's products)
```
Your Meta ad → your advertorial (hosted by YOU, Cloudflare Pages)
            → affiliate link → THEIR landing page → THEIR checkout
            → network tracks the sale → commission credited to you
            → network pays out (bank transfer / Payoneer / Wise), usually weekly or
              biweekly, often with a ~$50-100 minimum threshold
```
- You sign up at an **affiliate network** (ClickBank, Digistore24, BuyGoods,
  MaxBounty…) — free, sometimes requires approval/an interview for the good offers.
- You get a unique **affiliate link** with your ID baked in; their system tracks
  which sales came from you (**S2S/postback tracking** in the fancy setups).
- You own ONLY: the ad + the advertorial (your "pre-lander"). They own product,
  LP, checkout, delivery, support.
- Commissions on digital DR offers: often 50–75% of the sale.
- **The catch:** zero control. Offer dies, you're dead. Their LP converts badly,
  your ROAS eats it. And Meta is hostile to sketchy affiliate angles — compliance
  discipline matters double.

### Model B — Own product (the book)
```
Your Meta ad → your advertorial → your LP → MoR/Stripe checkout
            → webhook → buyer gets the PDF by email
            → upsell page ("the workout video course, $29?")
            → payout to your bank every few days
```
- You own EVERYTHING: ~90%+ margin (a PDF has no COGS), the customer email list
  (back-end gold — email flows, next products), full control of the funnel.
- You also own every problem: refunds, support emails, compliance, VAT.

**The classic path (and probably yours):** start affiliate to learn the traffic game
with someone else's funnel doing the converting — then build your own product once
you've SEEN what converts. Or run both: your book as the affiliate-style funnel you
fully own.

---

## 7. ZERO → FIRST SALE: the exact assembly order (own-book example)

Say it's the menopause book. Here is the whole checklist, in order:

1. **Offer first, book second.** Decide the promise, the angle, the price ($17–37 is
   the classic info-book zone), the bonuses. THEN we write the book with Claude.
   (You're the copywriter — you know the offer matters more than the product.)
   ⚠️ Niche warning: menopause/"get your ex back"/fitness are health-and-relationship
   claim MINEFIELDS on Meta. Compliance-clean copy from day 1 or the new ad account dies.
2. **Buy the domain** (~$10, Cloudflare). 10 minutes.
3. **Claude builds the pages**: advertorial + landing page + thank-you page as HTML
   in a GitHub repo → deployed free on Cloudflare Pages → live on your domain.
4. **Payments**: create the product on a Merchant of Record (Paddle/Gumroad/
   Lemon Squeezy) → get the checkout link → Claude wires every Buy button to it.
   Delivery is automatic (they email the PDF).
5. **Tracking**: create the Meta Pixel in your BM → Claude installs it on all pages
   (+ CAPI via the MoR/Stripe webhook when we get fancier).
6. **Ad account**: BM → Page → ad account → card → business verification when the
   firm exists. Warm it up gently.
7. **Ads**: generate with the WW-2-style machine → upload (manually at first, via
   Meta API once your own account is healthy) → ad's Website URL = the advertorial.
8. **Launch small**: $20–50/day. Watch the chain you already know:
   hook rate → CTR → CVR → AOV. Each metric tells you which block leaks.
9. **The firm + accountant**: register the ЕООД when money flows (or before, if
   going Stripe). Bank account → payouts land there.
10. **Iterate forever**: kill losers, scale winners, new hooks weekly, build the
    email list, add an upsell. That's the RALF loop applied to your own money.

**Total startup cost: ~$10 domain + ad budget.** Everything else in the stack is free.
The ad budget is the real investment — assume the first $300–1000 is tuition, not profit.

---

## 8. What Claude Code automates vs what it can't

| Block | Claude Code CAN automate | Humans/reality required |
|---|---|---|
| Product | Research, write, format the book (PDF/EPUB) | Your offer judgment |
| Pages | Write HTML/CSS, deploy, A/B variants, edits in seconds | — |
| Payments | Create products/links via API, webhook delivery script, refund reports | KYC/ID verification, bank account, firm |
| Traffic | Generate ads (WW-2), upload via Meta API, naming, batching | Ad account creation, warm-up, ban appeals, judgment on what to scale |
| Tracking | Pixel install, pull metrics via API into Sheets, daily P&L report, kill-criteria alerts | Deciding what the numbers MEAN |

The pattern: **everything made of files and API calls = automated. Everything made
of trust, identity, and law (banks, KYC, Meta's trust score, the firm) = you, once,
manually.** Build the manual things slowly and carefully — they're the foundation
the automation stands on.

---

## 9. The vocabulary of this doc (quick reference)

- **Registrar** — where you rent domains (Cloudflare, Namecheap)
- **DNS** — phone book pointing domain → host
- **Static site** — plain HTML files, no database; what LPs/advertorials are; free to host
- **Deploy** — push files live to the internet
- **Payment processor** — Stripe etc.; the only one allowed to touch cards
- **Merchant of Record (MoR)** — processor that is legally the seller and eats the tax admin (Paddle, Gumroad, Lemon Squeezy)
- **Checkout** — the page where the card gets typed (hosted by processor, not you)
- **Webhook** — "something happened" ping from one system to another (sale → send book)
- **KYC** — "Know Your Customer," the ID-verification banks/processors require
- **Payout** — processor → your bank, every few days
- **PPC** — pay-per-click (the Google Search model)
- **Affiliate network** — marketplace of offers + the tracking + the payouts (ClickBank, Digistore24)
- **Pre-lander** — your page between the ad and the merchant's page (usually an advertorial)
- **Postback / S2S** — server-to-server conversion tracking used in affiliate marketing
- **OSS / VAT MOSS** — the EU scheme for paying VAT on digital sales across countries (accountant word)
- **ЕООД / ЕИК** — BG single-owner Ltd / its company ID number

---

## 10. The confusion-killer: advertorial = TSL = VSL = the SAME page

These are NOT different things you choose between or put in different places.
They are the **same landing page wearing different costumes.** The landing page is
just "the page someone lands on after clicking the ad, where you sell them." Its
*style* has names:

| Costume | What the page is made of |
|---|---|
| **Advertorial** | written like an article ("I tried this for 30 days…"), story-first |
| **TSL** (Text Sales Letter) | one long written pitch: headline → story → offer → buy button |
| **VSL** (Video Sales Letter) | mostly a video, buy button underneath |
| **PDP** | normal product page: image, price, "add to cart" |

- "Is the LP a TSL?" → the LP *can be* a TSL. The TSL **IS** the landing page, not a
  separate thing somewhere else.
- "Where do people see the TSL?" → same as any landing page: they click the ad, they
  land on it. The ad is the only road.
- You pick ONE costume per funnel and test it against another costume.

**Where money goes to get people to see it:** the AD. You pay Meta in Ads Manager,
Meta shows the ad, the ad links to your page. The page is free to host — the ad budget
is the "money to be seen." Nothing else costs money to get traffic.

## 11. The bans / multiple-accounts / proxy world (and why you don't need it yet)

Real thing, you heard right — but it exists for ONE reason: surviving while running ads
that **break Meta's rules** (aggressive health/relationship claims, grey affiliate
offers). Those accounts get banned constantly, so aggressive buyers run many identities
at once:

- **Aged accounts** bought from sellers — old FB profiles look more trustworthy than fresh ones.
- **Antidetect browser** (Octo Browser, GoLogin, Dolphin Anty, Multilogin) — runs each
  account in its own sealed browser identity so Meta can't see they're all one person/PC.
- **Proxies** — give each account its own IP so they look like different people. Three types:
  1. **Datacenter** — cheapest, Meta spots it instantly. *(the one that doesn't work)*
  2. **Residential** — real home IPs, good.
  3. **Mobile (4G/LTE)** — the BEST (the "phone" one). Thousands of real phone users
     share one mobile IP, so Meta can't ban it without hitting innocent people — too
     trusted to block.

  → 3 types, 2 usable, mobile is king.

**Honest part (not yes-man):** this whole world is a costly, constant cat-and-mouse arms
race (proxies + accounts + browser subscriptions, monthly) and a full skill of its own.
For YOUR plan — your own clean book funnel — you need **none of it.** One legit account,
kept healthy, doesn't get banned because you're not breaking rules. The 10-ad-account
guys are aggressive affiliates fighting Meta daily — a harder, riskier game than the one
you're starting. If a new account gets banned: appeal via Meta's review form; if that
fails, that's when people rebuild a fresh BM. Step one is just not triggering it: start
small, compliant copy, no wild claims.

## 12. Monthly running cost (excluding profit tax)

- Domain: ~$1/mo (≈$10/year)  •  Hosting: $0 (free tier)  •  Processor: $0 fixed (% per sale only)
- **BG accountant: ~100–250 лв/mo — your biggest fixed cost** (only once the firm exists)
- → **~100–250 лв/mo fixed** after the firm; **~$1/mo** before it.
- Everything else is **ad budget = fuel, not cost** (you spend to make more back).
  Budget ~$300–1000 as tuition — first ads usually lose while you learn what converts.

---

*Created Jun 12, 2026. Companion doc: industry-terms-cheatsheet.md (the vocabulary).*
*Not legal/tax advice — confirm firm + VAT details with a Bulgarian accountant.*

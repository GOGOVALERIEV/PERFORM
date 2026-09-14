# Meta + Ecom + DR Terms Cheatsheet

The vocabulary of the job. Organized by topic. If someone uses a term on Slack and you
don't know it — it's probably in here.

---

## 1. Meta Ads structure (the "Russian dolls")

Meta organizes everything in 3 layers, each inside the previous one:

| Term | What it is | Decided at this level |
|---|---|---|
| **Campaign** | The top box | Objective (sales, leads, traffic) + budget type |
| **Ad Set** | Middle box, lives inside a campaign | Audience, placements, budget, schedule, optimization event |
| **Ad** | The actual creative people see | The video/image + copy + headline + link |

- **BM / Business Manager** — the company account that owns everything (yours: JF Market).
- **Ad Account** — the wallet inside the BM that spend comes out of (yours: jf1).
- **Page** — the Facebook/IG identity the ads run "from."
- **Pixel** — a snippet of code on the website that reports back to Meta: "this person bought." It's Meta's eyes on the store.
- **CAPI (Conversions API)** — same job as the pixel but server-to-server. More reliable since iOS 14 broke tracking. Usually run together with the pixel.
- **Placements** — WHERE the ad shows: FB feed, IG feed, Reels, Stories, Audience Network. "Advantage+ placements" = let Meta choose.
- **Dark post** — an ad that never appears on the page's organic feed. Almost all ads are dark posts.
- **Post ID ad** — running multiple ad sets pointing at ONE existing post so all likes/comments accumulate on it (social proof stacking).

## 2. Budget & optimization terms

- **CBO (Campaign Budget Optimization)** — budget set at campaign level, Meta distributes it across ad sets automatically. Now officially called "Advantage Campaign Budget."
- **ABO (Ad set Budget Optimization)** — budget set per ad set, you control distribution manually. Common for testing.
- **ASC / Advantage+ Shopping Campaign** — Meta's "trust the machine" campaign type: minimal targeting controls, Meta does everything. Very common for scaling.
- **Learning phase** — the first ~50 conversions per ad set per week, when Meta is still figuring out who to show it to. Performance is unstable here. Big edits reset it ("re-enters learning").
- **Optimization event** — what you tell Meta to optimize for (usually Purchase).
- **Attribution window** — how long after a click/view Meta takes credit for a sale. Standard: 7-day click, 1-day view.
- **Frequency** — average times one person has seen the ad. High frequency (3+) = audience getting tired.
- **Auction** — every ad impression is a real-time bid against other advertisers. You're not buying "spots," you're bidding.
- **Bid cap / cost cap** — manual limits on what you'll pay per result. Advanced; most accounts run "lowest cost" (no cap).

## 3. Targeting terms

- **Broad** — no interests, no lookalikes, just age/gender/country. Dominant strategy now; Meta's algorithm finds buyers itself.
- **Interest targeting** — targeting by declared interests ("hair care," "yoga"). Old-school, fading.
- **Lookalike (LAL / LLA)** — Meta finds people similar to a source list (e.g. your buyers). "1% LAL" = the closest 1% of the country.
- **Custom audience** — a list YOU define: site visitors, video viewers, customer emails.
- **Retargeting / remarketing** — ads aimed at people who already engaged (visited site, added to cart, watched 75% of video).
- **Prospecting / cold traffic** — people who've never heard of you. Where most budget goes.
- **TOF / MOF / BOF** — Top/Middle/Bottom of Funnel. Cold strangers / aware but undecided / almost-buyers.
- **Exclusions** — audiences you DON'T show ads to (e.g. exclude past buyers from prospecting).

## 4. Metrics (the scoreboard)

### Money metrics
- **Spend** — what you paid Meta.
- **ROAS (Return On Ad Spend)** — revenue ÷ spend. ROAS 3 = every $1 in ads brings $3 in sales. THE headline number.
- **Breakeven ROAS** — the ROAS where you make $0 profit after product costs. If margins are 50%, breakeven ROAS is 2.
- **CPA (Cost Per Acquisition)** — spend ÷ purchases. What one customer costs you. Also said as "cost per purchase."
- **CPL** — Cost Per Lead (for lead-gen funnels).
- **AOV (Average Order Value)** — revenue ÷ orders. Upsells exist to raise this.
- **LTV (Lifetime Value)** — total revenue one customer brings over time (repeat orders, subscriptions).
- **CAC (Customer Acquisition Cost)** — basically CPA, the term ecom founders use. The famous health check: **LTV > 3× CAC**.

### Traffic metrics
- **Impressions** — times the ad was shown (one person can count many times).
- **Reach** — unique people who saw it.
- **CPM (Cost Per Mille)** — cost per 1,000 impressions. The "rent" of the auction. US ecom: often $10–40.
- **CPC** — cost per click.
- **CTR (Click-Through Rate)** — clicks ÷ impressions. 1%+ is generally decent for ecom. "Link CTR" counts only clicks to the website (the one that matters).

### Creative/video metrics
- **Hook rate** — 3-second video views ÷ impressions. Did the first 3 seconds stop the scroll? Good: 30%+.
- **Hold rate** — ThruPlays (15s) ÷ 3-second views. Did people who stopped keep watching?
- **Thumbstop** — slang for the same idea: the moment a thumb stops scrolling.
- **VVR / video view rate, avg watch time, 25/50/75/100% video plays** — deeper retention metrics.
- **CVR (Conversion Rate)** — purchases ÷ landing page visitors. A SITE metric, not an ad metric. Tells you if the funnel (not the ad) is the problem.

### Diagnosis logic everyone uses
- Bad hook rate → fix the first 3 seconds.
- Good CTR but bad CVR → ad is fine, landing page/offer is the problem.
- Good ROAS that decays + rising frequency → creative fatigue, need new ads.

## 5. Ecom / funnel terms

- **Funnel** — the full path from ad → page → checkout → upsells. "The funnel" often means everything after the click.
- **Landing page (LP)** — the page the ad sends people to. Built to do ONE thing.
- **PDP (Product Detail Page)** — a standard product page on the store.
- **Advertorial** — a landing page disguised as an article ("I tried this for 30 days..."). Classic DR bridge between ad and offer. **Listicle** — the "Top 5 reasons" version.
- **Offer** — not the product; the DEAL: product + price + bonuses + guarantee + urgency. DR people say "the offer matters more than the product."
- **Front end / back end** — the first purchase (often barely profitable) vs everything sold after (where profit lives).
- **Upsell** — offer shown after purchase ("add 2 more bottles 40% off"). **Downsell** — cheaper offer if they decline. **Cross-sell** — related product. **Order bump** — small checkbox add-on ON the checkout page. **OTO (One-Time Offer)** — "only available right now" upsell page.
- **Bundle** — multiple units sold as one package (3-bottle pack). Raises AOV.
- **Subscription / continuity** — recurring billing. **Churn** — % of subscribers who cancel per month.
- **Cart abandonment** — added to cart, didn't buy. Recovered with email/SMS flows.
- **ATC (Add To Cart), IC (Initiate Checkout)** — funnel events the pixel tracks before Purchase.
- **COGS (Cost Of Goods Sold)** — what the product costs you to make/ship. **Margin** — what's left after COGS.
- **3PL** — third-party logistics; the warehouse that ships your orders. **Fulfillment** — getting the order to the customer.
- **Dropshipping** — selling without holding inventory; supplier ships directly. **White label / private label** — putting your brand on a generic manufactured product (most supplement/cosmetic DR brands, including hair products).
- **MER (Marketing Efficiency Ratio)** — total revenue ÷ total ad spend across ALL channels. The "blended ROAS" founders trust more than Meta's numbers.
- **Klaviyo** — the standard ecom email/SMS platform. **Flows** — automated email sequences (abandoned cart, post-purchase).

## 6. Direct Response (DR) copywriting terms

- **DR (Direct Response)** — advertising designed to make people act NOW (buy, click, sign up) — measurable. Opposite of **brand advertising** (Nike vibes, unmeasurable).
- **Hook** — the first 1–3 seconds/first line. Its only job: stop the scroll. Most-discussed element in any creative team.
- **Angle** — the strategic "way in" to selling the product. Same hair product: "postpartum hair loss" angle vs "aging hair" angle vs "stress shedding" angle. (The A in your WW-2 task IDs.)
- **Mechanism / unique mechanism** — the REASON the product works, framed as new/different: "it's not your shampoo, it's your blocked follicles — this unblocks them." Gives a skeptical buyer NEW hope. (The M in your task IDs.)
- **Big idea** — one dramatic, novel concept the whole ad hangs on. Bigger than an angle.
- **Avatar** — the specific imagined customer ("Sarah, 45, noticed her part widening"). You write to ONE person.
- **Pain point** — the specific problem that keeps the avatar up at night.
- **PAS** — Problem → Agitate → Solution. The most-used ad copy formula.
- **AIDA** — Attention → Interest → Desire → Action. The classic one.
- **Lead** (copywriting meaning!) — the OPENING section of a sales message, after the hook. Confusing because "lead" also means a potential customer — context tells you which.
- **Body** — the middle: proof, mechanism, story. **Close** — the end: offer + CTA.
- **CTA (Call To Action)** — the instruction: "Tap Shop Now." Every DR ad has exactly one.
- **USP** — Unique Selling Proposition; the one thing only you can claim.
- **Social proof** — evidence other people bought and loved it: reviews, testimonials, "10,000 sold."
- **Awareness levels** (Eugene Schwartz — the DR bible *Breakthrough Advertising*): Unaware → Problem-aware → Solution-aware → Product-aware → Most aware. The level decides what your hook talks about.
- **Market sophistication** — how many similar claims the market has already heard. Sophisticated markets need new mechanisms, not bigger promises.
- **Objection handling** — answering "yeah but..." inside the copy before the buyer thinks it.
- **Scarcity / urgency** — limited stock / limited time. Overused, still works.
- **Risk reversal / guarantee** — "90-day money back" — moving the risk from buyer to seller.
- **Claims / compliance** — what you're legally allowed to say. Health/beauty (like Noor Hair) is heavily policed: no "cures," "regrows," disease claims. Getting this wrong = ad rejected or **account banned**.
- **Swipe file** — a copywriter's saved collection of great ads to steal structure from.

## 7. Creative production terms

- **Creative** — the asset itself (the video/image). "We need new creatives" = new ads.
- **UGC (User-Generated Content)** — ads that look like a normal person filmed them on a phone. Dominant ecom format. Usually made by paid **UGC creators**, not real customers.
- **Talking head** — one person speaking to camera.
- **B-roll** — the supporting footage cut over the voiceover (hands using product, before/after shots).
- **VO (voiceover)**, **AI VO** — narration; increasingly AI-generated.
- **VSL (Video Sales Letter)** — a LONG sales video (5–40 min), often on the landing page, not the ad. **TSL** — text version (long-form sales page).
- **Static** — an image ad (vs video).
- **Mashup** — an ad stitched from clips of multiple existing videos/creators.
- **Storyboard** — the shot-by-shot written plan for a video before it's made (your WW-2 machine generates these).
- **Hook variation** — same ad body, different first 3 seconds. Cheapest way to multiply tests.
- **Iteration** — a new version of a winning ad with one element changed.
- **Native** — content that blends into the platform (looks like a regular Reel, not an ad).
- **Whitelisting / creator licensing** — running ads FROM an influencer's own account/handle for trust.

## 8. Testing & scaling terms

- **Creative testing** — the systematic process: launch batches of new ads, kill losers, scale winners. The core loop of the whole job.
- **Winner / winning ad** — an ad that hits the performance targets (e.g. above breakeven ROAS at meaningful spend).
- **Kill criteria** — pre-agreed rules for shutting an ad off ("kill if no purchase by $50 spend").
- **Fatigue** — a winner's performance decaying because the audience has seen it too much.
- **Vertical scaling** — raising budget on what's working. The "20% rule": raise gradually to avoid resetting learning.
- **Horizontal scaling** — duplicating winners into new ad sets/audiences/campaigns/geos.
- **Surf scaling** — aggressively raising budgets when performance is hot, cutting when cold.
- **Testing campaign vs scaling campaign** — common account structure: a sandbox where ads prove themselves, and a big-budget campaign where proven winners live.
- **DCT (Dynamic Creative Testing)** — Meta auto-mixes your headlines/videos/texts into combinations. Being replaced by **Flexible ads**.
- **Incrementality** — did the ads CAUSE the sales, or would they have happened anyway? The deepest measurement question.
- **Post-purchase survey (PPS)** — "How did you hear about us?" at checkout — used to check Meta's numbers (tools: KnoCommerce, Fairing).

## 9. Job titles you'll hear

- **Media buyer** — runs the ads inside Ads Manager: budgets, launches, kills, scaling. (Badar's world.)
- **Creative strategist** — decides WHAT ads to make: angles, hooks, briefs, analyzing why ads win. (Boris's world — and where you're heading.)
- **Copywriter** — writes the words. **Editor** — cuts the videos.
- **DTC (Direct-To-Consumer)** — brands selling straight to customers online (vs retail). The whole world you work in is "DTC ecom."

---

*Created Jun 12, 2026 — Session: terminology training.*

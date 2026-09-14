"""
Rebuild the EXISTING terms Google Doc into 3 real TABS (Раздели):
  Tab 1: Meta / Facebook / General
  Tab 2: Ecom
  Tab 3: Direct Response (copywriting)

George's rule: "add a section" = add a TAB inside the SAME doc, never a new doc.

How it works (plain English):
- A Google Doc can hold multiple TABS, like browser tabs but inside one document.
- The Docs API lets us: create a tab (addDocumentTab), rename it, delete old text
  (deleteContentRange), insert new text (insertText), and style it (bold, headings).
- We build each tab's text as ONE big string, tracking the position (index) of every
  line as we go, so afterwards we can tell Google "make THIS range bold / a heading."
- Google counts position by characters; every newline is 1 character. We avoid emojis
  (which count as 2) so Python's len() matches Google's counting exactly.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_docs

DOC_ID = '18VONtKuBvMH0V_LZ1UUJ9cER81T3PCZ15j4NR4Mau3E'  # existing terms doc

docs = get_docs()


# ---------- request builders ----------
def para_style(tab_id, s, e, named):
    return {'updateParagraphStyle': {
        'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
        'paragraphStyle': {'namedStyleType': named},
        'fields': 'namedStyleType'}}


def bold(tab_id, s, e):
    return {'updateTextStyle': {
        'range': {'startIndex': s, 'endIndex': e, 'tabId': tab_id},
        'textStyle': {'bold': True}, 'fields': 'bold'}}


def build_tab(tab_id, blocks):
    """blocks: list of tuples. Returns list of API requests for ONE tab."""
    text = ''
    styles = []
    idx = 1  # first insertable index in a tab body
    for b in blocks:
        kind = b[0]
        if kind in ('title', 'h'):
            line = b[1] + '\n'
            named = 'HEADING_1' if kind == 'title' else 'HEADING_2'
            styles.append(para_style(tab_id, idx, idx + len(line), named))
            text += line
            idx += len(line)
        elif kind == 'term':
            name, desc = b[1], b[2]
            line = name + ' — ' + desc + '\n'
            styles.append(bold(tab_id, idx, idx + len(name)))
            text += line
            idx += len(line)
        elif kind == 'note':
            line = b[1] + '\n'
            text += line
            idx += len(line)
    insert = {'insertText': {'text': text, 'location': {'index': 1, 'tabId': tab_id}}}
    return [insert] + styles


# ---------- CONTENT ----------

META = [
    ('title', 'META / FACEBOOK & GENERAL'),
    ('note', 'Everything about running ads on the platform: structure, money, audiences, the scoreboard, testing, and the account-survival world.'),

    ('h', 'The structure (Russian dolls)'),
    ('term', 'Campaign', 'the top box. You set the GOAL here (sales, leads, traffic) and sometimes the budget. Everything else lives inside it.'),
    ('term', 'Ad Set', 'the middle box. This is WHERE you set the audience, the placements, the schedule, and the optimisation event. Most "settings" decisions happen here.'),
    ('term', 'Ad', 'the actual thing people see: the video or image + the text + the headline + the link.'),
    ('term', 'Business Manager (BM) / Portfolio', 'the company account that owns everything — Pages, ad accounts, pixels. Yours at work is JF Market.'),
    ('term', 'Ad Account', 'the wallet inside the BM that the money is spent from (yours: jf1). A BM can hold several.'),
    ('term', 'Page', 'the Facebook/Instagram identity the ads appear to come from.'),
    ('term', 'Pixel', 'a tiny piece of code on your website that reports back to Meta what people did ("viewed", "added to cart", "bought"). It is Meta\'s eyes on your store.'),
    ('term', 'CAPI (Conversions API)', 'the same reporting as the pixel but sent server-to-server instead of from the browser. More reliable since iPhones broke browser tracking. Usually run alongside the pixel.'),
    ('term', 'Dataset', 'the newer name for the pixel + CAPI bundled together as one source of events.'),
    ('term', 'Placements', 'WHERE the ad shows: Facebook feed, Instagram feed, Reels, Stories, Marketplace, Audience Network.'),
    ('term', 'Advantage+ placements', 'letting Meta automatically choose the placements for you instead of picking them by hand. The usual default.'),
    ('term', 'Dark post', 'an ad that never appears on the Page\'s normal timeline. Almost all ads are dark posts so the feed is not spammed.'),
    ('term', 'Existing-post / Post-ID ad', 'pointing several ad sets at ONE post so all the likes and comments pile up on the same post (stacking social proof).'),

    ('h', 'Budget & optimisation'),
    ('term', 'CBO / Advantage Campaign Budget', 'budget set at the CAMPAIGN level; Meta decides how to split it across the ad sets automatically.'),
    ('term', 'ABO (Ad set Budget Optimisation)', 'budget set per AD SET; you control how much each one gets. Common for clean testing.'),
    ('term', 'ASC / Advantage+ Shopping Campaign', 'Meta\'s "trust the machine" campaign type — almost no manual targeting, Meta does nearly everything. Very common for scaling.'),
    ('term', 'Lowest cost', 'the default bidding: "spend my budget and get me the most results you can." No price cap.'),
    ('term', 'Cost cap / Bid cap', 'manual limits telling Meta the most you will pay per result. Advanced; most accounts skip it.'),
    ('term', 'Optimisation event', 'the action you tell Meta to chase. For a store it is almost always Purchase.'),
    ('term', 'Learning phase', 'the first ~50 conversions of a new ad set, while Meta is still figuring out who to show it to. Performance is jumpy here, and big edits restart it.'),
    ('term', 'Learning limited', 'a warning that an ad set is not getting enough conversions to ever finish learning — usually budget too low or audience too small.'),
    ('term', 'Attribution window', 'how long after a click or view Meta is allowed to claim credit for a sale. Standard today: 7-day click, 1-day view.'),
    ('term', 'Auction', 'every single ad slot is a live bid against other advertisers. You are not buying fixed spots — you are winning auctions.'),
    ('term', 'Spending limit', 'a cap (daily or account-level) on how much can be spent. New accounts start with a low one that grows with trust.'),

    ('h', 'Targeting'),
    ('term', 'Broad', 'no interests, no lists — just age / gender / country. The dominant strategy now because Meta\'s algorithm finds the buyers itself.'),
    ('term', 'Interest targeting', 'choosing people by declared interests ("hair care", "yoga"). Old-school and fading.'),
    ('term', 'Lookalike (LAL / LLA)', 'Meta builds an audience of people similar to a source list (e.g. your buyers). "1% lookalike" = the closest 1% of the country.'),
    ('term', 'Custom audience', 'a list YOU define: past site visitors, video viewers, your customer emails.'),
    ('term', 'Retargeting / remarketing', 'ads aimed at people who already engaged — visited the site, added to cart, watched most of a video.'),
    ('term', 'Prospecting / cold traffic', 'people who have never heard of you. Where most of the budget goes.'),
    ('term', 'TOF / MOF / BOF', 'Top / Middle / Bottom of Funnel — cold strangers / aware but undecided / almost-buyers.'),
    ('term', 'Exclusions', 'audiences you deliberately DON\'T show ads to (e.g. hide past buyers from cold campaigns).'),

    ('h', 'The scoreboard — money metrics'),
    ('term', 'Spend', 'what you paid Meta. The simplest number.'),
    ('term', 'ROAS (Return On Ad Spend)', 'revenue divided by spend. ROAS 3 = every $1 of ads brought back $3 of sales. The headline number.'),
    ('term', 'Breakeven ROAS', 'the ROAS where profit is exactly $0 after product costs. If your margin is 50%, breakeven is ROAS 2 — below that you lose money even with "good" sales.'),
    ('term', 'CPA / Cost per purchase', 'spend divided by purchases — what one customer cost you to get.'),
    ('term', 'CPL', 'Cost Per Lead, for funnels that collect a sign-up before a sale.'),
    ('term', 'AOV (Average Order Value)', 'revenue divided by number of orders. Upsells and bundles exist to push this up.'),
    ('term', 'LTV (Lifetime Value)', 'total money one customer brings over time — repeat orders, subscriptions, back-end products.'),
    ('term', 'CAC (Customer Acquisition Cost)', 'basically CPA, the word founders use. The classic health check is LTV greater than 3x CAC.'),
    ('term', 'MER (Marketing Efficiency Ratio)', 'TOTAL revenue divided by TOTAL ad spend across all channels — the "blended" number founders trust more than Meta\'s self-reported ROAS.'),

    ('h', 'The scoreboard — traffic metrics'),
    ('term', 'Impressions', 'how many times the ad was shown. One person can count many times.'),
    ('term', 'Reach', 'how many UNIQUE people saw it.'),
    ('term', 'Frequency', 'average times one person has seen the ad (impressions / reach). Climbing past ~3 means the audience is getting tired.'),
    ('term', 'CPM (Cost Per Mille)', 'cost per 1,000 impressions — the "rent" of the auction. US ecom is often $10-40.'),
    ('term', 'CPC (Cost Per Click)', 'what you pay per click.'),
    ('term', 'Landing page views', 'people who clicked AND the page actually finished loading. Lower than link clicks because some people bounce before the page loads (slow page = lost money).'),

    ('h', 'The CTRs (there are several — do not mix them up)'),
    ('note', 'CTR means Click-Through Rate = clicks divided by impressions. But "clicks" can mean different things, so Meta reports more than one CTR:'),
    ('term', 'CTR (all)', 'ANY click divided by impressions — counts likes, comments, shares, clicking the image to enlarge it, clicking "See more" to expand the text, clicking the Page name. A big, mostly-vanity number.'),
    ('term', 'CTR (link click-through rate)', 'only clicks on the actual link. Better, but can still include clicks that stay inside Facebook.'),
    ('term', 'Outbound CTR', 'only clicks that actually LEAVE Facebook and land on your website. This is the one that matters for a funnel.'),
    ('term', 'The "See more" expansion', 'when ad text is long Facebook hides the rest behind "See more"; clicking to expand it counts as a click in CTR (all) but is NOT a visit to your site.'),
    ('note', 'Read: a big gap between CTR (all) and link/outbound CTR means people engage with the post but will not click through — the hook grabs them, the click-promise does not.'),

    ('h', 'The scoreboard — video / creative metrics'),
    ('term', 'Hook rate', '3-second video views divided by impressions — did the first 3 seconds stop the scroll? Good is roughly 30%+.'),
    ('term', 'Hold rate', 'ThruPlays (15s) divided by 3-second views — of the people who stopped, how many kept watching?'),
    ('term', 'ThruPlay', 'Meta counting a video as "watched" at 15 seconds (or to the end if shorter).'),
    ('term', '3-second video plays', 'the count behind hook rate — people who watched at least 3 seconds.'),
    ('term', 'Thumbstop', 'slang for the same idea as hook rate: the moment a thumb stops scrolling.'),
    ('term', 'Video plays 25/50/75/100%', 'how far through the video people got — a retention curve showing where they drop off.'),
    ('term', 'Average watch time', 'the average seconds watched. Long watch time on a long video is a strong buying signal.'),
    ('term', 'CVR (Conversion Rate)', 'purchases divided by landing-page visitors. This is a PAGE metric, not an ad metric — it tells you if the funnel (not the ad) is the problem.'),

    ('h', 'Diagnosis logic (sound senior instantly)'),
    ('note', 'Bad hook rate -> fix the first 3 seconds.'),
    ('note', 'Good CTR but bad CVR -> the ad is fine; the landing page or offer is the problem.'),
    ('note', 'Good ROAS that slowly dies + rising frequency -> creative fatigue; make new ads.'),
    ('note', 'High CPM -> either a tired audience, a low-quality ad score, or an expensive auction (season/competition).'),

    ('h', 'Testing & scaling'),
    ('term', 'Creative testing', 'the core loop of the whole job: launch batches of new ads, kill the losers, scale the winners.'),
    ('term', 'Winner', 'an ad that beats the target (e.g. above breakeven ROAS at meaningful spend).'),
    ('term', 'Kill criteria', 'rules agreed in advance for switching an ad off ("kill it if no purchase by $50 spend").'),
    ('term', 'Fatigue', 'a winner decaying because the audience has now seen it too many times.'),
    ('term', 'Vertical scaling', 'raising the budget on something that works. The "20% rule" = raise gradually so you do not reset the learning phase.'),
    ('term', 'Horizontal scaling', 'duplicating a winner into new ad sets, audiences, or countries instead of just raising its budget.'),
    ('term', 'Surf scaling', 'aggressively pushing budget up while performance is hot and pulling back when it cools.'),
    ('term', 'Testing vs scaling campaign', 'a common setup: a sandbox campaign where ads prove themselves, and a big-budget campaign where proven winners live.'),
    ('term', 'DCT / Flexible ads', 'Meta auto-mixing your headlines, videos and texts into combinations to find the best mix.'),
    ('term', 'Incrementality', 'the deepest question: did the ads actually CAUSE the sales, or would they have happened anyway?'),
    ('term', 'Post-purchase survey (PPS)', 'a "How did you hear about us?" question at checkout, used to sanity-check Meta\'s numbers.'),

    ('h', 'Account survival (the grey-hat world — you do NOT need this for a clean funnel)'),
    ('note', 'This whole world exists to survive running ads that break Meta\'s rules. For a clean, compliant book funnel you run ONE healthy account and need none of it.'),
    ('term', 'Aged accounts', 'older Facebook profiles bought from sellers — they look more trustworthy to Meta than brand-new ones.'),
    ('term', 'Antidetect browser', 'tools like Octo Browser, GoLogin, Dolphin Anty, Multilogin that run each account in its own sealed identity so Meta cannot see they are all one person on one PC.'),
    ('term', 'Proxy', 'a middle-man IP address so each account looks like a different person in a different place.'),
    ('term', 'Datacenter proxy', 'cheapest, from server farms — Meta spots and blocks these almost instantly. (The type that does NOT work.)'),
    ('term', 'Residential proxy', 'real home internet IPs — trusted, works well.'),
    ('term', 'Mobile proxy (4G/LTE)', 'the best. Thousands of real phone users share one mobile IP, so Meta cannot ban it without hitting innocent people — "too trusted to block." The "phone" proxy.'),
    ('term', 'Ban + appeal', 'when an account is shut off you submit Meta\'s review form to appeal; if it fails, people rebuild on a fresh BM. Best move is never triggering it: start small, compliant copy.'),

    ('h', 'Who does what (job titles)'),
    ('term', 'Media buyer', 'runs the ads inside Ads Manager — budgets, launches, kills, scaling. (Badar\'s world.)'),
    ('term', 'Creative strategist', 'decides WHAT ads to make — angles, hooks, briefs, and analysing why ads win. (Boris\'s world, and where you are heading.)'),
    ('term', 'Copywriter', 'writes the words. Editor cuts the videos.'),
    ('term', 'DTC (Direct-To-Consumer)', 'brands selling straight to customers online instead of through shops. The whole world you work in.'),
]

ECOM = [
    ('title', 'ECOM (the store + the funnel + the money plumbing)'),
    ('note', 'How the selling machine is physically built and how the money actually moves.'),

    ('h', 'The funnel & pages'),
    ('term', 'Funnel', 'the whole path from ad -> page -> checkout -> upsells. A funnel is just a chain of web pages where each page has ONE exit: the next page.'),
    ('term', 'Landing page (LP)', 'the page the ad sends people to — the actual selling page. Built to do ONE thing, with no menu or distractions.'),
    ('term', 'PDP (Product Detail Page)', 'a normal product page: image, price, "add to cart".'),
    ('term', 'Advertorial', 'a landing page disguised as an article ("I tried this for 30 days..."). It warms up cold, skeptical traffic before the pitch.'),
    ('term', 'Listicle', 'the "Top 5 reasons..." version of an advertorial.'),
    ('term', 'Pre-lander', 'any warm-up page (usually an advertorial) sitting between the ad and the real sales page.'),
    ('note', 'Note: advertorial, TSL and VSL are the SAME landing page wearing different clothes — see the DR tab.'),

    ('h', 'The offer & raising order value'),
    ('term', 'Offer', 'not the product — the DEAL: product + price + bonuses + guarantee + urgency. DR people say the offer matters more than the product.'),
    ('term', 'Front end vs back end', 'the first purchase (often barely profitable) vs everything sold after it (where the real profit lives).'),
    ('term', 'Upsell', 'an offer shown right after purchase ("add 2 more bottles, 40% off").'),
    ('term', 'Downsell', 'a cheaper offer shown if they decline the upsell.'),
    ('term', 'Cross-sell', 'a related product offered alongside ("people also buy...").'),
    ('term', 'Order bump', 'a small checkbox add-on ON the checkout page itself ("+ add gift wrap for $5").'),
    ('term', 'OTO (One-Time Offer)', 'an "only available right now" upsell page that disappears if you leave.'),
    ('term', 'Bundle', 'several units sold as one package (a 3-bottle pack) to raise the order value.'),
    ('term', 'Subscription / continuity', 'recurring billing — the customer is charged every month automatically.'),
    ('term', 'Churn', 'the percentage of subscribers who cancel each month.'),

    ('h', 'Tracking events & costs'),
    ('term', 'ATC (Add To Cart)', 'the funnel event when someone adds the product to their cart.'),
    ('term', 'IC (Initiate Checkout)', 'the event when someone starts the checkout but has not paid yet.'),
    ('term', 'Cart abandonment', 'added to cart or started checkout but did not buy — recovered later with email/SMS.'),
    ('term', 'COGS (Cost Of Goods Sold)', 'what the product costs you to make and ship.'),
    ('term', 'Margin', 'what is left after COGS — the room you have to spend on ads and still profit. A PDF/book has ~90%+ margin.'),

    ('h', 'Fulfilment & sourcing'),
    ('term', '3PL (Third-Party Logistics)', 'the outside warehouse that stores and ships your orders for you.'),
    ('term', 'Fulfilment', 'the whole job of getting the ordered product to the customer.'),
    ('term', 'Dropshipping', 'selling without holding stock — the supplier ships directly to the customer when an order comes in.'),
    ('term', 'White label / private label', 'putting your brand on a generic factory-made product. Most supplement and beauty DR brands (including hair products) work this way.'),

    ('h', 'Email / retention tools'),
    ('term', 'Klaviyo', 'the standard ecom email + SMS platform.'),
    ('term', 'Flows', 'automated email/SMS sequences that fire on a trigger (abandoned cart, post-purchase, win-back).'),

    ('h', 'The money plumbing (how card payments actually work)'),
    ('note', 'You NEVER touch raw card numbers — that needs bank-level certification. Everyone plugs into a processor instead.'),
    ('term', 'Payment processor', 'the company allowed to handle cards (Stripe, etc.). It takes the money and pays you out.'),
    ('term', 'Checkout', 'the page where the card is actually typed in — hosted by the processor, not by you. This is the page that takes the payment.'),
    ('term', 'Merchant of Record (MoR)', 'a processor that is LEGALLY the seller (Paddle, Lemon Squeezy, Gumroad). They handle all the VAT/tax mess, refunds, and file delivery. Higher fee (~5-10%) but far less admin — best for a first digital product.'),
    ('term', 'Webhook', 'a "something happened" ping from one system to another. Example: processor pings your script "sale completed!" -> your script emails the buyer the book.'),
    ('term', 'KYC (Know Your Customer)', 'the ID + business verification banks and processors require before they will pay you.'),
    ('term', 'Payout', 'the processor sending your money to your bank account, usually every few days.'),

    ('h', 'Hosting (where the pages physically live)'),
    ('term', 'Domain', 'the web address you rent (~$10/year) from a registrar like Cloudflare or Namecheap.'),
    ('term', 'Hosting', 'the always-on computer holding your page files. Cloudflare Pages / Vercel are free for sites like ours.'),
    ('term', 'Static site', 'plain HTML files with no database — exactly what a landing page or advertorial is. Free and instant to host.'),
    ('term', 'Deploy', 'pushing your files live to the internet. With Claude: write the HTML -> git push -> live in under a minute.'),
]

DR = [
    ('title', 'DIRECT RESPONSE (the copywriting craft)'),
    ('note', 'The words and ideas that make people act NOW. Your home turf.'),

    ('h', 'The foundations'),
    ('term', 'DR (Direct Response)', 'advertising built to make people act immediately (buy, click, sign up) and measure it. The opposite of brand advertising (Nike vibes, unmeasurable).'),
    ('term', 'Brand advertising', 'ads meant to build a feeling/awareness over time, not to be measured by direct sales. Not what you do.'),

    ('h', 'The big strategic words (your mentor speaks in these)'),
    ('term', 'Concept', 'the core IDEA of an ad — the one sentence that makes it a distinct ad. Same hair product: "postpartum moms losing hair in clumps" vs "it is not your shampoo, it is your follicles" are two different concepts. When a top strategist says "20 concepts a week" they mean 20 genuinely different ideas/angles tested per week — elite output.'),
    ('term', 'Angle', 'the strategic doorway into the sale — which problem/desire you enter through. Same product can be sold on the postpartum angle, the ageing angle, or the stress angle. (The "A" in your WW-2 task IDs.)'),
    ('term', 'Mechanism / unique mechanism', 'the REASON the product works, framed as new and different ("it is not your shampoo, it is blocked follicles — this unblocks them"). It gives a skeptical buyer fresh hope. (The "M" in your task IDs.)'),
    ('term', 'Big idea', 'one dramatic, novel concept the whole ad hangs on — bigger than a single angle.'),
    ('term', 'Avatar', 'the one specific imagined customer you write to ("Sarah, 45, noticed her part widening").'),
    ('term', 'Pain point', 'the exact problem that keeps the avatar up at night.'),

    ('h', 'The anatomy of an ad / sales message'),
    ('term', 'Hook', 'the first 1-3 seconds or first line. Its only job is to stop the scroll. The most-discussed element in any creative team.'),
    ('term', 'Lead (copywriting meaning)', 'the OPENING section of the message, just after the hook — where you pull the reader in. Careful: "lead" also means a potential customer; context tells you which.'),
    ('term', 'Body', 'the middle — proof, mechanism, story, demonstration.'),
    ('term', 'Close', 'the end — the offer plus the call to action.'),
    ('term', 'CTA (Call To Action)', 'the single clear instruction: "Tap Shop Now." Every DR ad has exactly one.'),
    ('term', 'USP (Unique Selling Proposition)', 'the one thing only you can honestly claim.'),
    ('term', 'Social proof', 'evidence other people bought and loved it — reviews, testimonials, "10,000 sold".'),

    ('h', 'The frameworks & theory'),
    ('term', 'PAS', 'Problem -> Agitate -> Solution. The most-used short-copy formula.'),
    ('term', 'AIDA', 'Attention -> Interest -> Desire -> Action. The classic structure.'),
    ('term', 'Awareness levels', 'from Eugene Schwartz\'s book Breakthrough Advertising (the DR bible): Unaware -> Problem-aware -> Solution-aware -> Product-aware -> Most-aware. The avatar\'s level decides what the hook can say.'),
    ('term', 'Market sophistication', 'how many similar claims the market has already heard. Tired/sophisticated markets need a NEW mechanism, not a louder promise.'),
    ('term', 'Objection handling', 'answering the reader\'s "yeah, but..." inside the copy before they consciously think it.'),
    ('term', 'Scarcity / urgency', 'limited stock / limited time. Overused, still works.'),
    ('term', 'Risk reversal / guarantee', 'moving the risk from buyer to seller ("90-day money back"). Removes the reason to say no.'),
    ('term', 'Claims / compliance', 'what you are legally allowed to say. Health, beauty and money niches are policed hard — no "cures", "regrows", or disease claims. Getting this wrong gets ads rejected or the account banned.'),
    ('term', 'Swipe file', 'a copywriter\'s saved collection of great ads to study and borrow structure from.'),

    ('h', 'The unit words (concept vs iteration vs format)'),
    ('term', 'Concept', 'the IDEA (see above). The big unit.'),
    ('term', 'Iteration', 'a new VERSION of a winning concept with one element changed. The medium unit.'),
    ('term', 'Hook variation', 'the same ad body with only a different first 3 seconds. The cheapest, smallest unit — the fastest way to multiply tests.'),
    ('term', 'Format', 'the COSTUME the creative wears (UGC, static, VSL, advertorial...). See the formats list below.'),

    ('h', 'Formats (the costumes)'),
    ('term', 'UGC (User-Generated Content)', 'an ad that looks like a normal person filmed it on their phone. The dominant ecom format — usually made by paid creators, not real customers.'),
    ('term', 'Talking head', 'one person speaking straight to camera.'),
    ('term', 'B-roll', 'the supporting footage cut over a voiceover (hands using the product, before/after shots).'),
    ('term', 'VO / AI VO', 'voiceover narration; increasingly AI-generated.'),
    ('term', 'Static', 'an image ad (as opposed to video).'),
    ('term', 'VSL (Video Sales Letter)', 'a long sales video (5-40 min), usually ON the landing page, not the ad itself. For pricier or complex products.'),
    ('term', 'TSL (Text Sales Letter)', 'the text version of a VSL — a long written sales page. The TSL IS the landing page, just made of text.'),
    ('term', 'Mashup', 'an ad stitched together from clips of several existing videos or creators.'),
    ('term', 'Storyboard', 'the shot-by-shot written plan for a video before it is filmed (what your WW-2 machine generates).'),
    ('term', 'Native', 'content built to blend into the platform — looks like a normal Reel, not an ad.'),
    ('term', 'Whitelisting / creator licensing', 'running ads FROM an influencer\'s own handle for extra trust.'),
    ('note', 'Your WW-2 machine has its own named formats (LFS, RVSL, Yapfest, etc.) and ~29 video frameworks — those are house names for specific format+structure combos.'),

    ('h', 'Getting paid (the business side)'),
    ('term', 'Performance deal', 'getting paid on RESULTS instead of a flat fee — e.g. a retainer plus a percentage of ad spend or profit. Real example George heard: $10k/month + 5% of ad spend. This is how top strategists earn big: paid for the outcome, not the hours.'),
    ('term', 'Retainer', 'a fixed monthly fee for ongoing work (e.g. writing X ads/month).'),
    ('term', 'Rev-share', 'taking a cut of the revenue or profit you help generate, on top of or instead of a fee.'),
]


# ---------- EXECUTE ----------
# 1) Fetch doc, find the default tab, measure its content length.
doc = docs.documents().get(documentId=DOC_ID, includeTabsContent=True).execute()
tabs = doc.get('tabs', [])
print(f'Doc currently has {len(tabs)} tab(s).')
default = tabs[0]
default_id = default['tabProperties']['tabId']
body = default['documentTab']['body']['content']
end_index = body[-1]['endIndex']  # last index; final newline lives just before this

# 2) Clear default tab, rename it, and create the two other tabs — one batch.
setup_requests = []
if end_index - 1 > 1:
    setup_requests.append({'deleteContentRange': {
        'range': {'startIndex': 1, 'endIndex': end_index - 1, 'tabId': default_id}}})
setup_requests.append({'updateDocumentTabProperties': {
    'tabProperties': {'tabId': default_id, 'title': 'Meta · Facebook · General'},
    'fields': 'title'}})
setup_requests.append({'addDocumentTab': {'tabProperties': {'title': 'Ecom'}}})
setup_requests.append({'addDocumentTab': {'tabProperties': {'title': 'Direct Response'}}})

res = docs.documents().batchUpdate(documentId=DOC_ID, body={'requests': setup_requests}).execute()

# Pull the two new tab IDs from the replies (the addDocumentTab replies, in order).
new_tab_ids = [r['addDocumentTab']['tabProperties']['tabId']
               for r in res['replies'] if 'addDocumentTab' in r]
ecom_id, dr_id = new_tab_ids[0], new_tab_ids[1]
print(f'Tabs ready: Meta={default_id}, Ecom={ecom_id}, DR={dr_id}')

# 3) Fill each tab (separate batch each, so index math stays isolated per tab).
for label, tab_id, blocks in [('Meta', default_id, META), ('Ecom', ecom_id, ECOM), ('DR', dr_id, DR)]:
    reqs = build_tab(tab_id, blocks)
    docs.documents().batchUpdate(documentId=DOC_ID, body={'requests': reqs}).execute()
    terms = sum(1 for b in blocks if b[0] == 'term')
    print(f'  {label} tab filled: {terms} terms')

print('\nDONE: https://docs.google.com/document/d/' + DOC_ID + '/edit')

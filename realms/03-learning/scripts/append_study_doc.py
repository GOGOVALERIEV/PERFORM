import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_docs

DOC_ID = "1aLnQSBEmAD7__GA-KZ_BAPz2lyJ-mIjV0XU3bw4mUW4"

NEW_CONTENT = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION 3 — DEEPER CLARIFICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: Why would anyone use Post-ID / existing-post stacking instead of just running money on the ad?
A: Social proof is a massive trust signal. An ad with 2,400 comments looks completely different from the same ad with 10 comments. When you scale a winner across 5 ad sets WITHOUT stacking, each ad set builds separate social proof (maybe 400 comments each). With stacking, all 5 point to one post and you get 2,000 comments in one place. Same spend, same ads, but one version looks huge and trusted. People glance at the comment count before deciding if it's real. That is why people do it.

Q: Attribution window — where do I actually see this in Ads Manager?
A: Two places:
1. When setting up a campaign, inside the Ad Set settings under the "Conversion" section — you pick the window that Meta uses to count conversions for that campaign.
2. In the results table, top right: Columns → Customize columns → attribution dropdown. The purchase count and ROAS in your table literally change depending on which window you select.
Most important rule: keep the same window across all campaigns so your comparisons are honest. If Campaign A uses 7-day click and Campaign B uses 28-day click, the data is lying to you.

Q: Exclusions — how do you actually set them up step by step?
A: Ad Set level → Audience section → Exclusions field → click Add → select a Custom Audience.
You need to create that Custom Audience first: Audiences menu → Create audience → Custom audience → Website → select "Purchase" event → last 180 days → save. Then it shows up in exclusions. Done. Your cold traffic campaign will not waste spend on people who already bought.

Q: CPL is for SaaS / MRR businesses?
A: CPL is for any business where there is a step between ad and sale — SaaS, coaching, info products, insurance, real estate, webinars. MRR (Monthly Recurring Revenue) is a completely separate metric measuring how much a subscription business earns per month. CPL = efficiency of getting leads. MRR = total monthly revenue from subscribers. A SaaS company tracks both but they measure completely different things.

Q: PPS — what does it tell me statistically and what is the next step?
A: The survey gives you a percentage breakdown of where buyers say they came from. Example: 100 customers answer — 35 say Facebook ad, 30 say word of mouth, 20 say Google, 15 don’t remember. Meanwhile Meta claims credit for 70 of those 100 sales. The gap (Meta says 70, customers say 35) shows Meta is overcounting by 2x.
Next step: stop using Meta’s ROAS as your main number. Switch to MER (total revenue ÷ total ad spend across ALL channels). If Meta says ROAS 4 but the survey shows Meta only accounts for 35% of real buyers, your actual Meta contribution is probably ROAS ~1.4. You’d make completely different budget decisions knowing that.

Q: White label vs dropshipping — is white label just dropshipping brands?
A: No, different axes entirely.
Dropshipping = a FULFILLMENT model. No inventory. Customer orders → supplier ships directly. You never touch the product.
White label = a BRANDING model. Factory makes the product, you put your brand on it. You usually DO hold inventory (or use a 3PL). You are a real brand.
Private label = same as white label but the factory made the formula specifically for you — more exclusive, more expensive to set up.
Noor Hair = almost certainly white or private label + 3PL. They own the brand, ordered bulk inventory, a warehouse ships it. That is NOT dropshipping. Dropshipping is the beginner model. White label + 3PL is the established brand model.

Q: In a UGC ad, is the B-roll the effects and clips the editor adds?
A: Yes exactly. A-roll = the creator talking to camera. B-roll = everything the editor layers in: product close-ups, text overlays, before/after images, ingredient visuals, branded animations. The brand usually provides a B-roll package (a folder of product shots and clips) and the editor cuts them in over the creator’s voiceover. Sometimes the editor sources B-roll themselves.

Q: What is the difference between a TSL and a Landing Page?
A: TSL IS a type of landing page. Landing page = the category. Inside that category there are types:
- VSL landing page: video does all the selling, minimal text
- TSL landing page: long-form text IS the sales pitch, reads like a long article but every sentence sells
- Advertorial landing page: disguised as a news/blog article, warms up reader before the pitch
When someone says "landing page" they mean whichever type. When they say "TSL" they mean specifically the long-form text version.

Q: Is a storyboard for editors?
A: For editors AND creators. The storyboard tells UGC creators exactly what shots to film (shot 1: woman looking at hair in mirror, shot 2: product close-up, etc.) and tells editors how to cut it together and what B-roll to source. The WW-2 machine generates storyboards so creators and editors just execute the plan — no guessing.

Q: Are native ads just statics that look like something a real person would post?
A: Native is about how the ad LOOKS, not whether it is video or image. A native ad can be either:
- Native static: looks like a casual screenshot or text-on-photo a real person shared, not a polished brand visual
- Native video: looks like a casual phone recording, not a produced ad
The opposite of native is a polished, clearly-branded creative. Native works for cold product-unaware audiences because it bypasses ad blindness — people don’t instantly recognize it as an ad and scroll past. For people who already know the brand, polished branded ads are fine.

Q: Page type examples — real ones:
A:
Product page (PDP): Any Shopify product page with navigation, images, description, reviews, add-to-cart. Example: Noor Hair’s own product page.
Advertorial: https://deyga.in/blogs/news/i-tried-this-hair-growth-trio-for-30-days-here-s-what-no-one-tells-you — looks like a blog article, every sentence sells.
Landing Page (LP): https://drinkag1.com/dailyhealthdrink — no navigation, one product, one CTA repeated, social proof, guarantee.
TSL: Sit behind paid funnels — best way to find one is to click a supplement brand ad on Facebook and see where it takes you. Gundry MD and similar supplement brands run them.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPDATED QUESTIONS FOR BORIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Dark posts: does he use Post-ID / existing-post stacking? When and how does he set it up?
- ASC: when does he turn it on, what budget, what proven ads does he feed into it?
- Where does he buy proxies — which specific services does he trust (residential vs 4G)?
- Where does he source Facebook accounts — which vendors are trustworthy vs scams?
- For his own offer: does he have a cart abandonment email system? What does the sequence look like?
- What is in his portfolio and can George see it?
"""

docs = get_docs()

doc = docs.documents().get(documentId=DOC_ID).execute()
body = doc.get('body', {})
content = body.get('content', [])
end_index = content[-1].get('endIndex', 1) - 1

requests = [{
    'insertText': {
        'location': {'index': end_index},
        'text': NEW_CONTENT
    }
}]

result = docs.documents().batchUpdate(
    documentId=DOC_ID,
    body={'requests': requests}
).execute()

print("Done. Doc updated successfully.")

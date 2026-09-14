"""
Creates the Product Finding step-by-step Google Doc.
"""
import pickle, os
from googleapiclient.discovery import build

token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'google-token.pickle')
with open(token_path, 'rb') as f:
    creds = pickle.load(f)
docs = build('docs', 'v1', credentials=creds)

doc = docs.documents().create(body={'title': 'HOW TO FIND PRODUCTS — Step by Step'}).execute()
doc_id = doc['documentId']
print(f"Created: {doc_id}")

sections = []
def title(t): sections.append(('TITLE', t))
def sub(t): sections.append(('SUBTITLE', t))
def h1(t): sections.append(('HEADING_1', t))
def h2(t): sections.append(('HEADING_2', t))
def h3(t): sections.append(('HEADING_3', t))
def p(t): sections.append(('NORMAL_TEXT', t))

title("HOW TO FIND PRODUCTS — Step by Step")
sub("From Zakaria's Course (Product Finding Section) + George's Notes")
p("This is a DO THIS THEN THAT document. Follow it in order.")
p("")

h1("THE RULE BEFORE YOU START")
p("Don't copy from other people without knowing wtf you are doing.\nDon't over-complicate it.\nPeople don't buy the product — they buy the OUTCOME the product provides.")
p("")

h1("WHAT MAKES A GOOD PRODUCT")
p("""Before you search, know what you're looking for:

1. Big avatar — a LOT of people have this problem (millions, not hundreds)
2. A lot of archetypes — many sub-groups within that avatar (more archetypes = more angles = more ads)
3. Big desire — how badly do they want this fixed? (mental pain + physical pain)
4. Big problems — how much does this fuck up their life?
5. Magnitude of desire — more pain + bigger dream = more willing to pay
6. Mental pain sells HARDER than physical pain — "I feel embarrassed" beats "my hair is thin"
7. The product actually works — "if you bring products that don't solve it but market like they do, you'll make money, but it's up to your morals. You should not do that."
8. Not too sophisticated — can you actually enter this market? Or is it dominated by huge brands?
9. You search for UNITED STATES market — that's where the money is""")
p("")

h1("3 METHODS TO FIND PRODUCTS")
p("Do one, two, or all three. They all lead to the same place: a product worth selling.")
p("")

h2("METHOD 1: Facebook Ad Library (Best Method)")
p("""WHERE: facebook.com/ads/library
COUNTRY: United States

STEP 1: Type keywords related to problems (not product names)
Examples: "hair loss", "back pain", "acne scars", "beard growth", "teeth whitening"

STEP 2: Look at the ads that come up
For each ad, ask yourself:
- What PRODUCT are they selling?
- What AVATAR are they targeting? (who is in the ad? who is it talking to?)
- What ARCHETYPE/ANGLE are they using? (what specific pain point? what emotional hook?)
- How are they SCALING it? (lots of ad variations = they're spending money = it's working)
- What is the DESIRE they're selling? (not the product — the outcome)

STEP 3: Check the competitors
When you find a good product, search for OTHER brands selling the same thing.
- How many competitors are there?
- Are they doing a good job or bad job?
- Is there room for YOU? (better angles, untapped archetypes, better understanding of the avatar)

STEP 4: Evaluate the product
- Is the desire big enough? (magnitude of the problem)
- Is the market too sophisticated for you right now?
- Can you actually sell this and compete?

STEP 5: Add to your spreadsheet (see bottom of this doc)""")
p("")

h2("METHOD 2: Alibaba / Direct Product Search")
p("""WHERE: alibaba.com, aliexpress.com, or similar supplier sites

STEP 1: Browse or search for product categories
Look at what's available — supplements, gadgets, beauty tools, health devices, etc.

STEP 2: When you find something interesting, ASK:
- What problem does this solve?
- WHO has this problem? (avatar)
- How big is the desire?
- Are people already selling this on Facebook? (check Ad Library)

This is the "product-first" approach — you find the product, THEN check if the market exists.
It works but it's backwards compared to Method 3.""")
p("")

h2("METHOD 3: Problem-First Research (Reddit)")
p("""WHERE: Reddit (or any forum where people complain about problems)

This is the OPPOSITE of Method 2. Instead of finding products and looking for problems, you find PROBLEMS and then find products that solve them.

STEP 1: Go to Reddit
Search for subreddits where people complain about problems.
Examples: r/hairloss, r/backpain, r/acne, r/PCOS, r/skincare

STEP 2: Read what people say
- Some communities talk about the problem but don't know solutions (problem-aware = easy to sell to)
- Others actively discuss products (product-aware = need different approach)
- Note the solutions people mention — even home remedies tell you what ingredients/angles work

STEP 3: Find products that solve what they're complaining about
- Search for supplements, devices, tools that address the specific root cause
- Check if brands already sell to this audience (Facebook Ad Library)

STEP 4: Evaluate using the same criteria
- Big avatar? Big desire? Big pain? Not too sophisticated? Can you compete?

STEP 5: Add to your spreadsheet

WHY THIS METHOD IS POWERFUL:
- You find problems that have HIGH DESIRE built in
- You hear the exact language your customers use (becomes your ad copy)
- You might find avatars nobody is targeting yet (blue ocean)
- Boris's machine (research.py) automates the Reddit scraping part of this""")
p("")

h2("METHOD 4: Spy Tools (Ask Boris)")
p("""Zakaria mentioned package spy tools that you can get from people to find winning products.

YOU DON'T KNOW WHAT THESE ARE YET.
Ask Boris what spy tools he uses and how.
(This is still pending — add to Boris questions)""")
p("")

h1("AFTER YOU FIND A PRODUCT — THE CHECKLIST")
p("""For EVERY product you find, answer these questions:

THE AVATAR:
[ ] Who has this problem? (be specific — not "women" but "women 30+ with PCOS hair loss")
[ ] How many archetypes can you find? (more = better)
[ ] What awareness stage are they in? (problem-aware and solution-aware = easiest to sell to)

THE DESIRE:
[ ] How big is the mental pain? (embarrassment, depression, insecurity, relationships)
[ ] How big is the physical pain? (symptoms, daily discomfort)
[ ] What is the dream outcome they want? (not "less hair loss" but "feel beautiful and confident again")

THE COMPETITION:
[ ] How many competitors in Facebook Ad Library?
[ ] Are they doing a good job or bad job?
[ ] Can you beat them with better understanding of the avatar?
[ ] Is the market too sophisticated for you right now?

THE PRODUCT:
[ ] Does it actually work?
[ ] Can you source it? (Alibaba, white label, create your own)
[ ] What's the price point people are willing to pay? (check Amazon reviews)
[ ] Can you ship to US?

THE OFFER:
[ ] Don't just discount — bundle stuff
[ ] Create offers that feel like a deal (derma roller + caffeine shampoo as free gift)
[ ] Understand that the OFFER is what closes the sale, not just the product

DECISION: Yes / No / Maybe (need more research)""")
p("")

h1("THE SPREADSHEET")
p("""Make a spreadsheet to track every product you evaluate. Columns:

Product Name | Problem It Solves | Avatar | # of Archetypes | Desire Level (1-10) | Competition Level (Low/Med/High) | Can They Pay? | Sophistication | Facebook Ads Running? | Decision

Fill this in for every product you consider. Don't keep it in your head — write it down.""")
p("")

h1("GEORGE'S NOTES (Raw — From the Course)")
p("""These are your own words, unchanged:

- basically dont copy from the other people without knowing wtf you are doing
- when i am finding a product i should look for a big avatar with a lot of archetypes with big desire and big problems if not acting
- and this is just from me like just dont over complicate it
- so we come back to people buy things for the fix of their problems people dont buy the product but the outcome that the product provides
- so first comes the magnitude of desire
- so thats another thing from me like if i have a product that is for hair loss which people would suffer the most from it woman what woman and then when we kinda figure this out we need to find a winning archetype and then after this is done we are gonna test a lot of angles for this and basically when are done we find new archetypes and make iterations on the existing winning archetypes thats the game and the we make more fires in which we put more fire
- and like the problems that i have to think about is mental pain and physical pain
- how big is that pain
- and then what is the outcome how big is the desire
- about the research like we just have to know in what stage they are mostly in problem aware but sometimes we could target people that are in problem unaware both are great then if the company grows and we have a lot of winning archetypes and people have seen us then we could do most aware and product aware
- but from what we know is a lot easier to sell to the aware stages there is already build in desire for the fix
- archetype is the question - for what do the person want the solution for 1 for 2 for 3 for everything he doesent or just because why not give me the dopamine
- the big thing in this course is that i will know how to make advertorials
- ok big thing how to find untapped products - this i need a clarification from boris""")
p("")

h1("KEY INSIGHTS FROM THE COURSE")
p("""- Authentic content wins — real people showing real results converts way better than polished ads. A girl documenting her hair loss journey with a red light device beats a studio ad.
- Understand the desire BEHIND the problem — men don't just want a beard, they want to look masculine and feel confident. Women don't just want eyebrows, they want to feel beautiful. Sell the emotion, not the product.
- Health niche = risky — regulations can change, you need products that actually work. Be careful until you know what you're doing.
- The sophistication thing matters less if you're selling in Bulgaria since Trump fucked shit up (your note — consider this when evaluating markets)""")
p("")

h1("STILL NEED TO FIGURE OUT")
p("""- [ ] Ask Boris: what spy tools does he use to find products?
- [ ] Ask Boris: how to find untapped products?
- [ ] Ask Boris: what's his process for picking which product to work on next?""")

# ============================================================
# BUILD THE DOC
# ============================================================
full_text = ""
format_ranges = []
for style, text in sections:
    start = len(full_text) + 1
    full_text += text + "\n"
    end = len(full_text) + 1
    format_ranges.append((start, end - 1, style))

requests = [{"insertText": {"location": {"index": 1}, "text": full_text}}]

for start, end, style in format_ranges:
    if style in ("TITLE", "SUBTITLE", "HEADING_1", "HEADING_2", "HEADING_3", "NORMAL_TEXT"):
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {"namedStyleType": style},
                "fields": "namedStyleType"
            }
        })

chunk_size = 50
for i in range(0, len(requests), chunk_size):
    chunk = requests[i:i+chunk_size]
    docs.documents().batchUpdate(documentId=doc_id, body={"requests": chunk}).execute()
    print(f"  Batch {i//chunk_size + 1} done")

print(f"\nhttps://docs.google.com/document/d/{doc_id}/edit")

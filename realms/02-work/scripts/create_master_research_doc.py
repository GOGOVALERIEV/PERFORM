"""
Creates the Master Market Research Google Doc.
Combines: Zakaria's course notes + transcripts + ww-2 machine knowledge.
"""
import pickle
import os
from googleapiclient.discovery import build

# --- AUTH ---
token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'google-token.pickle')
with open(token_path, 'rb') as f:
    creds = pickle.load(f)
docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# --- DOCUMENT CONTENT ---
# Each section: (style, text)
# Styles: TITLE, HEADING_1, HEADING_2, HEADING_3, NORMAL, NORMAL_BOLD
sections = []

def h1(text): sections.append(('HEADING_1', text))
def h2(text): sections.append(('HEADING_2', text))
def h3(text): sections.append(('HEADING_3', text))
def p(text): sections.append(('NORMAL_TEXT', text))
def title(text): sections.append(('TITLE', text))
def subtitle(text): sections.append(('SUBTITLE', text))

# ============================================================
# TITLE
# ============================================================
title("MARKET RESEARCH — Master Document")
subtitle("Zakaria's Course + Boris's Machine (ww-2) + Claude's Analysis")
p("Last updated: March 9, 2026")
p("Sources: Zakaria Airakaz Course (Videos 1-12 + Market Research 2: Videos 1-2), George's personal notes, ww-2 machine research files (archetypes.md, hotwords.md, mechanisms.md)")
p("")

# ============================================================
# TABLE OF CONTENTS
# ============================================================
h1("TABLE OF CONTENTS")
p("""1. THE BIG PICTURE — Core philosophy
2. PHASE 1: Avatar Discovery — Finding sub-avatars on Reddit
3. PHASE 2: Avatar Qualification — Is this avatar worth pursuing?
4. PHASE 3: Amazon Review Mining — AI-assisted avatar discovery
5. PHASE 4: Avatar Deep Dive — The research document
6. PHASE 5: The Output — What you end up with
7. PHASE 6: YouTube Research — Emotional gold from comments
8. PHASE 7: TikTok Research — Hooks, trends, avatar language
9. PHASE 8: Amazon Deep Dive — Product-aware objections + competitor research
10. PHASE 9: AI-Accelerated Research — Speed up extraction with prompts
11. PHASE 10: Document Cleaning & Merging — One master research file
12. PHASE 11: Root Cause Research — WHY the problem exists
13. PHASE 12: Solution Mechanism — The THEORY of how to fix it
14. ZAKARIA vs. GEORGE — Full comparison (updated)
15. WHAT YOU STILL NEED TO LEARN
16. 10 KEY RULES""")
p("")

# ============================================================
# GEORGE'S RAW NOTES (from Doc 2)
# ============================================================
h1("GEORGE'S RAW NOTES (from the course)")
p("""(These are George's own words from his first pass through the course. Kept as-is.)

- Basically don't copy from the other people without knowing wtf you are doing
- When I am finding a product I should look for a big avatar with a lot of archetypes with big desire and big problems — if not, keep looking
- People buy things for the fix of their problems. People don't buy the product but the outcome that the product provides
- So first comes the magnitude of desire
- If I have a product that is for hair loss, which people would suffer the most from it? Woman. What woman? And then when we kinda figure this out we need to find a winning archetype and then test a lot of angles for this archetype. When done, find new archetypes and make iterations on existing winning ones. That's the game. More fires, more fuel on each fire.
- The problems I have to think about: mental pain and physical pain. How big is that pain? And then what is the outcome — how big is the desire?
- Archetype is the question: for what does the person want the solution for? 1, 2, 3, everything, or just give me the dopamine?
- The big thing in this course is that I will know how to make advertorials (NOTE: this is from a later section of the course, not market research)
- How to find untapped products — this I need a clarification from Boris (NOTE: still pending)""")
p("")

# ============================================================
# 1. THE BIG PICTURE
# ============================================================
h1("1. THE BIG PICTURE")
p("From your own notes + the course:")
p("")
h3("The Core Truth")
p("People do not buy products. They buy the OUTCOME the product provides.\nYour job: find WHO has the biggest pain > understand them deeply > talk to them in their own words.")
p("")
h3("The Game")
p("""1. Find a winning archetype
2. Test a lot of angles for that archetype
3. When done > find new archetypes
4. Make iterations on existing winning archetypes
5. More fires, more fuel on each fire""")
p("")
h3("Two Types of Pain")
p("""- Mental pain (embarrassment, depression, insecurity, relationship impact)
- Physical pain (the actual condition/symptoms)
- Mental pain sells HARDER than physical pain""")
p("")
h3("Awareness Stages")
p("""- Problem UNAWARE — does not know they have the problem yet
- Problem AWARE — knows the problem, does not know solutions exist (easiest to sell to)
- Solution AWARE — knows solutions exist, comparing options
- Product AWARE — knows your specific product, needs final push
- Most AWARE — already bought from you or knows you well

Start with problem-aware and solution-aware. They have built-in desire for the fix.""")
p("")

# ============================================================
# 2. PHASE 1: Avatar Discovery
# ============================================================
h1("2. PHASE 1: AVATAR DISCOVERY")
p("Videos 1-2: What is an avatar + how to find sub-avatars on Reddit")
p("")
h2("What Zakaria Does")
p("""1. Starts with the broad problem (e.g. "hair loss")
2. Goes to Reddit > searches the problem
3. Looks at sidebar for related subreddits > each one = potential sub-avatar
4. Speed-reads 50+ posts > clicks user profiles > checks age, gender, what other subs they are in
5. Groups people into categories (sub-avatars):
   - By age (20s, 30s, 50+)
   - By gender (male, female)
   - By cause (PCOS, menopause, postpartum, stress, steroids)
   - By severity (thinning, bald spots, full bald)
   - By life stage (single, married, dating, new mom)
6. Writes down each emerging sub-avatar as a category""")
p("")
h2("Why He Does It")
p("""- Broad audience = red ocean (everyone fights for "people with hair loss")
- Specific avatar = blue ocean (nobody talks to "PCOS women with hair loss")
- If you do not have a SUPERIOR PRODUCT, you MUST have SUPERIOR UNDERSTANDING of a specific avatar
- The brand that understands the customer best makes the most money
- You cannot touch deep desires when selling to everyone — only surface stuff like "get your hair back"
- The beard brand example: they did not sell to "all men wanting beards" — they sold to single guys who want beards to attract women. THAT is the deep desire.""")
p("")
h2("How You Do It (with the machine)")
p("""- Machine does this: research.py generates 40 Reddit search queries and scrapes automatically
- You still need: to pick the broad problem and know what sub-avatars to look for
- Your edge: you can run research.py for multiple sub-avatars in parallel
- What you add: your copywriting instinct — the machine finds data, you spot the EMOTIONAL weight""")
p("")

# ============================================================
# 3. PHASE 2: Avatar Qualification
# ============================================================
h1("3. PHASE 2: AVATAR QUALIFICATION")
p("Videos 2-3: Checking if the avatar is worth pursuing")
p("")
h2("What Zakaria Does")
p("""1. For each sub-avatar, checks Facebook Ad Library (facebook.com/ads/library)
2. Searches for ads targeting that specific avatar
3. Looks for three winning scenarios:
   - NOBODY targets this avatar yet (goldmine)
   - Competitors are doing a BAD job (you can beat them)
   - You have a slightly better product for this specific avatar
4. Fills out a qualification spreadsheet per avatar:
   - Desire magnitude: How much emotional pain? (more pain = more willing to buy)
   - Competition level: High / Medium / Low (from FB Ad Library)
   - Can they pay? Teenagers = no. Working adults = yes.
   - Can you ship to them? Geographic logistics
   - Decision: Yes / No""")
p("")
h2("Why He Does It")
p("""- Not every avatar is worth pursuing
- A niche with 200 people cannot make you money
- A niche where 50 brands run 100 creatives/day will crush you at the start
- You want: BIG desire + LOW competition + CAN afford it
- Do not go TOO niche (need millions of people) or TOO broad (red ocean)""")
p("")
h2("How You Do It (with the machine)")
p("""- You can scrape FB Ad Library with scripts to count competitors faster
- Your judgment call: the machine cannot tell you if an avatar has enough emotional depth
- Speed: Zakaria spends 30+ min per avatar. You can check multiple in parallel
- Use the Google Sheets Research Template you already created to track this""")
p("")

# ============================================================
# 4. PHASE 3: Amazon Review Mining
# ============================================================
h1("4. PHASE 3: AMAZON REVIEW MINING (AI-ASSISTED)")
p("Video 3: Using ChatGPT + bulk Amazon reviews to discover hidden avatars")
p("")
h2("What Zakaria Does")
p("""1. Searches Amazon for products with 5K-55K reviews
2. Downloads all reviews using a bulk downloader tool (~$19 Chrome extension)
3. Feeds reviews into ChatGPT with a specific prompt:
   - "Extract sentences related to the core problem"
   - "Find specific avatars — NOT generic (reject 'stressed professional')"
   - "For each avatar: desire, awareness level, how it affects life, objections"
   - "Go deeper than surface-level categories"
4. ChatGPT returns avatars he never thought of (e.g. PCOS women)
5. Verifies each one on Reddit + FB Ad Library""")
p("")
h2("Why He Does It")
p("""- Reddit shows how avatars TALK
- Amazon reviews show which avatars BUY (they spent money)
- AI can process 100K reviews and spot patterns a human would miss
- This is where he discovered PCOS — a huge avatar nobody was targeting""")
p("")
h2("How You Do It (with the machine)")
p("""- Skip the paid download tools. Quick 5-min Amazon scroll to confirm people spend money = enough
- Machine's NotebookLM prompt already does avatar extraction but better
- Your use for Amazon: confirmation that people PAY in this niche (lots of reviews = lots of buyers)
- See price ranges people are willing to pay
- The real value was the PROMPT concept — the machine already has this built in""")
p("")

# ============================================================
# 5. PHASE 4: Avatar Deep Dive
# ============================================================
h1("5. PHASE 4: AVATAR DEEP DIVE (The Research Document)")
p("Videos 4-5: Going DEEP into one chosen avatar")
p("")
h2("What Zakaria Does")
p("""1. Googles the condition (if medical) to understand basics
2. Goes to the specific subreddit for this avatar
3. Also goes to RELATED subreddits (e.g. r/femalehairloss for a PCOS avatar)
   Why: a PCOS woman shares the SAME emotional pain as any woman with hair loss
   The general sub has MORE emotional posts, the condition sub has MORE solution talk
4. Fills out the Avatar Deep Dive Document as he reads""")
p("")
h2("The Deep Dive Document — Every Field Explained")
p("Each field = a different element you use in your ads. Here is what each one is, and WHY you need it:")
p("")
p("""AGE / GENDER
What: Who exactly are these people
Why for ads: Targeting + tone of voice
Example: Females, mostly 30+""")
p("")
p("""PAIN POINTS
What: What hurts emotionally
Why for ads: Becomes HOOKS — the first thing they see in your ad
Example: "I can see my scalp", "I feel so embarrassed"
In the machine: Goes into hotwords.md under A1 (physical) and B2 (identity)""")
p("")
p("""DAY-TO-DAY STRUGGLES
What: Real daily moments of pain
Why for ads: Becomes UGC SCRIPTS and visual ad concepts
Example: Crying at the hair salon, clumps of hair in the shower, avoiding going out
NOTE: These catch attention MORE than generic headlines. "I cried at the salon" > "Do you suffer from hair loss?"
In the machine: Goes into archetypes.md under "Core Pattern > World shrinkage" and hotwords.md""")
p("")
p("""VICTORIES
What: What has worked for them
Why for ads: Becomes SOCIAL PROOF angles — shows what kind of results they want to see
Example: Keto diet helped, collagen peptides, Minoxidil worked""")
p("")
p("""FAILURES
What: What they tried that did not work
Why for ads: Becomes OBJECTION HANDLING — "I tried everything and nothing worked" is THE biggest objection. You need to know what "everything" means to THEM so you can explain why those things failed.
Example: Various pills with side effects, treatments that were too expensive
In the machine: Goes into archetypes.md under "Failed Solutions" table""")
p("")
p("""GOALS / DESIRES
What: What they want to achieve
Why for ads: Becomes the PROMISE of your ad — the outcome you're selling
Example: Get hair back, feel confident, look good for partner
In the machine: Goes into hotwords.md under B1-B3""")
p("")
p("""HOPES
What: Desperate wishes (desire + willingness to act)
Why for ads: Becomes EMOTIONAL CTA — the final push to buy
Example: "I am hoping things improve", considering a wig as last resort""")
p("")
p("""BELIEFS
What: What they already trust
Why for ads: Becomes AUTHORITY ANGLES — if they trust dermatologists, use a dermatologist in the ad. If they believe diet matters, mention diet.
Example: They trust dermatologists, believe diet matters, trust DHT blockers
In the machine: Goes into mechanisms.md — the mechanism must align with what they already believe""")
p("")
p("""OBJECTIONS
What: Why they think they CANNOT fix it
Why for ads: Becomes OBJECTION CRUSHERS — you address these BEFORE they think them. This is why you search for objections: if you know the objection exists, you can kill it in the ad before it stops them from buying.
Example: "There is no cure for PCOS", "Minoxidil has side effects", "Have to use it for life"
In the machine: Goes into archetypes.md under "Failed Solutions" and mechanisms.md under "Why Old Solutions Failed" """)
p("")
p("""LEVEL OF AWARENESS
What: Where they are in the buying journey
Why for ads: Determines HOW you open the ad. Problem-aware = lead with pain. Solution-aware = lead with "why other solutions failed". Product-aware = lead with proof/results.
Example: Most are problem-aware AND solution-aware (know about DHT blockers, Minoxidil, keto)
In the machine: Goes into archetypes.md under "Awareness Points" (A1-A3, B1-B3)""")
p("")
p("""COMMUNITY LANGUAGE
What: Their specific words and slang
Why for ads: Using THEIR words makes them feel understood — you are one of them, not a marketer talking AT them. This is the difference between "hair thinning" (marketer) and "I can see my scalp through my hair" (real person).
Example: They say "T" and "AGA" (types of hair loss), "DHT blockers", "ferritin levels"
NOTE: Women use "girly language" — emotional, supportive ("amazing", "so happy for you", "this is your sign")
In the machine: This IS hotwords.md — exact phrases organized by awareness category""")
p("")
p("""RELATIONSHIP IMPACT
What: How the problem affects dating/marriage
Why for ads: This is a whole separate AD ANGLE — some of the most emotional hooks come from relationships
Example: "I am 31, single for years because of my hair", "A guy told me I was balding"
In the machine: Goes into archetypes.md — some archetypes are DEFINED by relationship impact (ARC3: The Defeated Accepter gave up on dating)""")
p("")
p("""BACKGROUND STORIES
What: Full journey posts (diagnosis > treatments > failure > hope)
Why for ads: Becomes AD SCRIPTS and HERO STORIES — the full arc of a UGC creator's story
Example: Woman goes from diagnosis > trying 6 products > crying every day > finding something that works""")
p("")
h2("Why He Does All This")
p("""- "Understand your ideal customers better than they understand themselves"
- Input = Output: quality of research = quality of ads
- Each field in this document = a different angle or hook for ads
- This IS the leverage in a competitive market
- Research is NOT a one-time thing. Every day you find new angles.""")
p("")
h2("How You Do It (with the machine)")
p("""- Machine does 70%: research.py scrapes Reddit > NotebookLM extracts archetypes, emotional patterns, verbatim quotes, failed solutions, awareness mapping
- You do the remaining 30%: read NotebookLM output > decide what becomes an archetype (ARC1, ARC2...) > write archetypes.md, hotwords.md, mechanisms.md
- Your edge over Zakaria: he does this manually for 1 avatar over hours. You run the machine for 5 avatars in parallel.
- What the machine CANNOT do: feel which quotes have the most emotional punch. When you read "I cried at the hair salon" — you KNOW that is a hook. The machine might rank it the same as "I noticed hair thinning" but you know the first one is 10x stronger.""")
p("")

# ============================================================
# 6. PHASE 5: The Output
# ============================================================
h1("6. PHASE 5: THE OUTPUT")
p("What you end up with after all the research")
p("")
h2("Zakaria's Output")
p("""- A filled-out research document per avatar
- Ad concepts in his head
- Ready to create ads manually""")
p("")
h2("Your Output (via the machine)")
p("""- products/PRODUCT/research/archetypes.md
  Contains: ARC1, ARC2, ARC3... each with awareness points (A1-B3), core pattern, deep wound components, language patterns, failed solutions, direct quotes

- products/PRODUCT/research/hotwords.md
  Contains: Exact customer phrases organized by A1 (physical), A2 (timing), A3 (social), B1 (mechanism), B2 (identity), B3 (system)

- products/PRODUCT/research/mechanisms.md
  Contains: M1, M2... each with the mechanism explanation, "aha" statement, why old solutions failed, solution connection to ingredients

- products/PRODUCT/config.json
  Contains: demographics, price, ingredients, forbidden phrases

Then the machine generates 1000+ ads/day from these files.""")
p("")

# ============================================================
# 7. PHASE 6: YouTube Research
# ============================================================
h1("7. PHASE 6: YOUTUBE RESEARCH")
p("Video 8: Finding emotional insights from YouTube comments")
p("")
h2("What Zakaria Does")
p("""1. Searches YouTube for the avatar's problem (e.g. "PCOS hair loss")
2. Filters by view count (most views first) — viral videos = proven emotional resonance
3. Reads the comments under those videos
4. Looks for the same things as Reddit: pain points, day-to-day struggles, emotional language, what they tried, what they want
5. Copies the best raw quotes into his research document""")
p("")
h2("Why He Does It")
p("""- YouTube comments are different from Reddit. Reddit = long forum posts where people explain in detail. YouTube = short emotional reactions to content they just watched.
- YouTube shows you what CONTENT resonates — if a video about "PCOS hair loss journey" has 500K views, that ANGLE works
- The comments reveal: what hooks made them click, what they relate to, what questions they still have
- YouTube comments often have more RAW emotion: "omg this is literally me", "I'm crying watching this"
- These become hooks and UGC scripts — the emotional reactions ARE the ad concepts""")
p("")
h2("How You Do It")
p("""- The machine (research.py) focuses on Reddit, not YouTube
- For YouTube: you can use YouTube comment scraper tools to extract all comments from viral videos, then feed them to the AI prompt from Phase 9
- Or do a quick manual scan: search your problem on YouTube, sort by views, read top 20-30 comments on the top 5 videos, copy the emotional gold
- What to search for specifically:
  1. Emotional reactions ("I felt this in my soul", "this made me cry")
  2. Day-to-day struggles mentioned in comments
  3. Questions they ask ("but does X actually work?") — these = objections
  4. Solutions they mention trying
  5. The EXACT language they use""")
p("")

# ============================================================
# 8. PHASE 7: TikTok Research
# ============================================================
h1("8. PHASE 7: TIKTOK RESEARCH")
p("Video 9: Understanding your avatar through TikTok content and comments")
p("")
h2("What Zakaria Does")
p("""1. Searches TikTok for the avatar's problem
2. Looks at what content goes VIRAL — which hooks get the most views
3. Reads comments to understand:
   - What the avatar engages with
   - How they talk (shorter, more emotional than Reddit)
   - What content makes them stop scrolling
4. Notes which HOOKS work best — the first 3 seconds that grab attention
5. Copies emotional comments into his research document""")
p("")
h2("Why He Does It")
p("""- TikTok = where your avatars LIVE (especially females 20-30)
- TikTok shows you WHAT HOOKS WORK — you can literally see which first-3-seconds got millions of views
- The comments are pure emotion: "omg same", "I needed this", "why is no one talking about this"
- TikTok content style = how your UGC ads should FEEL (authentic, casual, emotional)
- If a TikTok creator talking about PCOS hair loss gets 2M views, that ANGLE + HOOK is proven""")
p("")
h2("How You Do It")
p("""- The machine doesn't scrape TikTok
- This is manual research: search your problem on TikTok, watch the top videos, read comments
- What to extract:
  1. HOOKS that work (the first thing they say that gets views)
  2. Emotional comments (raw language for hotwords.md)
  3. Content ANGLES that perform (story-based? education? before/after? rant?)
  4. Creator STYLE that resonates (calm? angry? crying? friend-talking-to-friend?)
- You can copy comments in bulk and feed to the AI prompt from Phase 9
- The hooks you find here can directly inspire hook-types in the machine's components/hook-types.md""")
p("")

# ============================================================
# 9. PHASE 8: Amazon Deep Dive
# ============================================================
h1("9. PHASE 8: AMAZON DEEP DIVE — Avatar + Product/Competitor Research")
p("Video 10: Two types of Amazon research — avatar psychology + product-aware insights")
p("")
h2("TYPE 1: Avatar Research Through Amazon")
p("")
h3("What Zakaria Does")
p("""1. Searches Amazon for products related to the avatar's problem
2. Reads reviews looking for the EMOTIONAL side — not product features
3. Looks for: pain points, day-to-day struggles, turning points, what made them finally buy
4. These are people who SPENT MONEY — their words carry more weight than Reddit browsers""")
p("")
h3("Why He Does It")
p("""- Reddit = people who TALK about their problems
- Amazon = people who PAID to fix their problems
- Amazon reviewers reveal: what was the last straw that made them buy, what they expected vs what they got, how desperate they were
- This is confirmation that the avatar SPENDS money (critical for qualification)""")
p("")
h2("TYPE 2: Product/Competitor Research Through Amazon")
p("")
h3("What Zakaria Does")
p("""1. Finds products SIMILAR to what he'll sell (competitor supplements, competitor solutions)
2. Reads reviews specifically for PRODUCT-AWARE insights:
   - What features they love ("it doesn't smell bad", "easy to take")
   - What features they hate ("too many pills", "tastes horrible", "takes too long")
   - What objections they had BEFORE buying ("I was worried it wasn't FDA approved")
   - Price sensitivity ("expensive but worth it" vs "too expensive for what it is")
   - Ingredient awareness ("I specifically wanted one with biotin and saw-palmetto")
3. Documents competitor product names, prices, positioning""")
p("")
h3("Why He Does It")
p("""- Product-aware audience has DIFFERENT objections than problem-aware audience
- Problem-aware: "will anything work for me?"
- Product-aware: "is THIS product safe? FDA approved? worth the price? better than Brand X?"
- If you know these objections exist, you CRUSH them in the ad before they stop the sale
- Competitor research also shows you: gaps in the market (nobody does X), winning features to highlight, price points that work
- This feeds directly into the product development phase later""")
p("")
h2("How You Do It")
p("""- The machine doesn't do Amazon research automatically
- But the concept is simple: go to Amazon, find 3-5 products with lots of reviews in your niche, read 50-100 reviews
- What to extract for your files:
  For hotwords.md: exact phrases about pain, struggles, hopes (same categories)
  For archetypes.md: product-aware objections go into "Failed Solutions" tables
  For mechanisms.md: what they believe about HOW things work/don't work
- You can also bulk-extract reviews with tools and feed to AI (see Phase 9)""")
p("")

# ============================================================
# 10. PHASE 9: AI-Accelerated Research
# ============================================================
h1("10. PHASE 9: AI-ACCELERATED RESEARCH")
p("Video 11: Using AI to speed up data extraction from any source")
p("")
h2("The Concept")
p("""Instead of reading 1,000 reviews/comments manually, you:
1. EXTRACT all the raw data into one document (copy-paste, scraper tool, comment downloader)
2. FEED it to AI with a specific prompt
3. AI categorizes everything: pain points, struggles, goals, beliefs, objections, etc.
4. You CLEAN the output (AI makes mistakes — it adds insights that aren't in the data, miscategorizes things)

This works for ANY source: Amazon reviews, YouTube comments, TikTok comments, Reddit threads, Facebook groups, forum posts.""")
p("")
h2("Why He Does It")
p("""- Manual research = hours of reading to find 20 good quotes
- AI-accelerated = minutes to process the same data
- The RAW QUOTES are what matter, not the AI's insights — the insights are just a starting point
- You STILL need to verify everything yourself — AI sometimes makes up connections that aren't there""")
p("")
h2("The AI Prompt (Zakaria's)")
p("""Hi, I want you to act as a world-class creative strategist for a $100M/year brand in the niche [NICHE].

Your mission: conduct a deep emotions and insight-driving analysis of our ideal customer [AVATAR] to uncover the real thoughts, feelings, and struggles that drive their behavior.

You will be working from a raw data source — a document of [SOURCE TYPE: Amazon reviews / YouTube comments / Reddit threads / etc.]. These are unfiltered expressions straight from the voice of the customer.

Your task: mine this document for gold. Copy their raw language and categorize each quote into the relevant sections inside a new document titled "Avatar Deep Dive Research for [AVATAR]."

Each entry should be structured like this:
- Category: [Day-to-Day Struggles / Pain Points / Goals / Beliefs / Objections / etc.]
- Raw Quote: "[exact customer words]"
- Insight: [what this quote reveals strategically]

Rules:
- ONLY use direct quotes from the document
- Do NOT generate or paraphrase any quotes on your own
- If you do not find any raw quote that fits a specific category, SKIP IT
- No outside insights — literally only what's in the document""")
p("")
h2("How You Do It")
p("""- Your machine ALREADY does this better: research.py + NotebookLM extracts and categorizes automatically
- But this prompt is useful for sources the machine doesn't cover (Amazon, YouTube, TikTok, Facebook groups)
- Process: extract raw data > feed to Claude/ChatGPT with the prompt above > clean the output > merge into your research files
- Use o3 or o1 (reasoning models) for best results with large documents""")
p("")

# ============================================================
# 11. PHASE 10: Document Cleaning & Merging
# ============================================================
h1("11. PHASE 10: DOCUMENT CLEANING & MERGING")
p("Video 12: Combining all research into one organized master document")
p("")
h2("The Concept")
p("""After doing research from multiple sources (Reddit, Amazon, YouTube, TikTok, etc.), you have scattered documents. You need ONE master document with everything organized.

Three steps:
1. CLEAN each document manually — format each entry as: raw quote + insight tag, put in right categories, remove duplicates
2. MERGE all documents with AI — upload all cleaned docs + merge prompt
3. GROUP into emotional clusters — instead of 100 individual quotes, group them under 5-10 shared emotional themes per category""")
p("")
h2("Why He Does It")
p("""- Scattered research = wasted research. If you can't find it, you can't use it.
- One organized document = your source of truth for ALL ad copy, hooks, landing pages, offers
- Grouping by emotional theme shows you the STRONGEST angles (if 15 quotes say the same thing = that angle hits HARD)
- Clean document = faster ad creation later""")
p("")
h2("The Merge Prompt (Zakaria's)")
p("""Hi, I want you to act as a world-class creative strategist for a $100M/year brand in the niche [NICHE].

You will work with [X] filled documents that contain all raw quotes from our ideal customers [AVATAR]. These quotes are categorized and partially analyzed. Your mission:

Merge the documents into a single comprehensive document titled "Avatar Deep Dive Research."

Non-negotiables:
- Include EVERY single raw quote. Do not simplify or select. Do not omit any quote no matter how repetitive, long, or minor.
- All quotes must be preserved in their original language inside quotation marks.
- Use the full structure of the template to organize: Pain Points, Day-to-Day Struggles, Goals, Beliefs, Objections, Victories, Failures, etc.
- Insights must accompany every quote. If a quote has no insight, write one.
- If a quote is misplaced, move it to a more fitting category. Leave a small note explaining why.
- If a quote is relevant to more than one category, duplicate it across those categories with a unique insight each time.
- Never generate or paraphrase quotes. Only use quotes from the provided documents.
- No duplicates unless meaningful. If a quote appears in both documents word-for-word, keep one.

Use o3 or o1 (reasoning models) for this — you want the AI to THINK, not just be fast.""")
p("")
h2("The Grouping Prompt (Phase 2)")
p("""Now that we fully merged every raw quote, reformat the document into grouped core insights (not one-by-one breakdowns).

For each category, format like this:
- Category: Day-to-Day Struggles
  - Insight 1: "Washing their hair triggers anxiety and hopelessness"
    Raw quotes: [all grouped quotes that express this]
  - Insight 2: "Avoiding mirrors and photos"
    Raw quotes: [all grouped quotes]

Rules:
- Each category should contain 5-10 key insights
- Each insight must be supported by grouped raw quotes (verbatim)
- No raw quote should be left out
- If a quote supports multiple insights, include it in multiple places
- Keep insights emotionally rich and specific — not generic like "they feel bad" """)
p("")
h2("How You Do It")
p("""- Your machine output is ALREADY organized — archetypes.md has the archetypes with quotes, hotwords.md has the language, mechanisms.md has the mechanisms
- But if you do MANUAL research on top of machine research (YouTube, TikTok, Amazon, Facebook groups), this process is how you merge that extra data into your existing files
- The merge prompt is useful: it forces the AI to keep EVERY quote and organize properly
- End result: one document you can scan in 5 minutes and pull hooks, scripts, objection crushers from""")
p("")

# ============================================================
# 12. PHASE 11: Root Cause Research
# ============================================================
h1("12. PHASE 11: ROOT CAUSE RESEARCH")
p("Market Research 2, Video 1: Researching WHY the problem exists at a deep level")
p("")
h2("What Is Root Cause Research?")
p("""Root cause = the REAL reason the avatar has the problem. Not the symptom they see, but what's actually happening underneath.

Example:
- Symptom: "My hair is falling out"
- Surface cause: "Hormonal imbalance"
- Root cause: "PCOS causes excess androgens (DHT) + insulin resistance produces MORE DHT + chronic inflammation damages follicles — three forces attacking hair from the inside"

You go DEEPER than what the customer knows. You become the expert.""")
p("")
h2("Why He Does It (4 Strategic Reasons)")
p("""1. REMOVES OBJECTIONS — Your avatar tried 10 products and nothing worked. If you explain WHY nothing worked (those products only treated symptoms, not the root cause), they believe YOUR product is different.

2. BUILDS TRUST — You're not just saying "buy this." You're showing you understand their problem deeper than anyone — deeper than their doctor, deeper than the last 5 brands they tried.

3. CREATES THE "YES YES YES" SEQUENCE — When you explain something they already believe (like "PCOS is hormonal"), then go deeper into HOW it works, they keep nodding. By the time you introduce the product, they're already convinced.

4. GIVES YOU LEVERAGE — You can show HOW your product is different from everything else. Not "our shampoo is better" but "our product actually targets the ROOT CAUSE that no shampoo can reach." """)
p("")
h2("Where Root Cause Fits In Your Ads")
p("""- ADVERTORIALS: After hook + background story, BEFORE introducing the solution. You explain what's REALLY causing their problem, why other solutions failed, then lead into your solution mechanism.
- UGC ADS: The creator talks about her experience, mentions she tried everything, then explains she discovered the real reason nothing worked (the root cause), THEN introduces the product.
- VSLs: The education section where you build credibility by showing deep understanding.
- It works for EVERY format — the root cause section bridges "I have this problem" to "this product can fix it." """)
p("")
h2("How To Do Root Cause Research")
p("")
h3("Manual Method")
p("""Google the condition, read medical articles, WebMD, forums. Copy key findings. This works but is slow. Good for building your OWN understanding first.""")
p("")
h3("AI Method (faster)")
p("""Prompt for ChatGPT Deep Research (use o3 or o1):

"Hi, I want you to act as a world-class direct response copywriter for a $100M/year brand in the niche [NICHE]. Your job is to research and explain the root cause of a specific problem experienced by our ideal customers [AVATAR].

This is not surface level. I want you to uncover what's really happening underneath.

Your task — Deep Research: Research the root cause of the following problem: [PROBLEM]. Find what is actually causing this issue. Ensure explanation is backed by logical, factual, research-based information.

Summarize and include all important details. Write in a way that's clear — not medical/scientific jargon." """)
p("")
h3("After You Find The Root Cause")
p("""1. Write it in PLAIN ENGLISH — explain like you're talking to a friend. 4th grade reading level.
2. Create ANALOGIES — "Your scalp is like a garden. DHT is weed killer being poured on it every day."
3. Write UGC TALKING POINTS — key points a content creator can naturally explain on camera (not a script, just bullet points she can riff on)""")
p("")
h2("How You Do It (with the machine)")
p("""- The machine's mechanisms.md ALREADY contains root cause information
- Example from NOOR mechanisms.md:
  M1 (Adrenal Silica Theft): "Your adrenal glands are EXHAUSTED. They're STEALING silica from your hair and sending it to your organs just to keep you alive. Your hair is the last priority."
  M2 (GLP-1 Silica Starvation): "The drug suppresses your appetite. Your body TRIAGES every mineral. Silica — the one that holds hair in your scalp — gets redirected to organs."
- To create NEW mechanisms for new products, you DO need to do this root cause research
- The root cause research feeds directly into mechanisms.md — you can't write the mechanism without understanding what's broken""")
p("")

# ============================================================
# 13. PHASE 12: Solution Mechanism
# ============================================================
h1("13. PHASE 12: SOLUTION MECHANISM RESEARCH")
p("Market Research 2, Video 2: Developing the THEORY of how to fix the root cause")
p("")
h2("What Is A Solution Mechanism?")
p("""The solution mechanism = the THEORY of how you can fix the root cause. Not the product. Not the ingredients. Just the logical approach.

Think of it like this:
- Root cause = "A knife is stuck in this spot — that's what's causing pain"
- Solution mechanism = "We need to remove the knife from that spot"
- Product = The actual tool that removes the knife

The mechanism is the BRIDGE between "here's what's broken" and "here's the product that fixes it."

In Boris's machine, this is EXACTLY what mechanisms.md contains:
- The Mechanism (the theory, explained verbatim)
- The "Aha" Statement (the one-liner that makes the customer go "oh, THAT'S why")
- Why Old Solutions Failed (tied to the mechanism)
- The Solution Connection (how ingredients deliver the mechanism)""")
p("")
h2("Why You Need It")
p("""Social proof alone is not enough. Some customers will buy just because they see testimonials. But a big chunk of your audience — the skeptical ones — need to understand HOW it works logically before they'll trust it.

The solution mechanism creates the "aha moment" — the point where the customer goes: "This actually makes sense. This is different from everything I tried."

Without a mechanism, your ad is: "Buy this, it works, here's proof."
With a mechanism, your ad is: "Here's WHY nothing worked before, here's EXACTLY what needs to happen to fix it, and here's the product that does exactly that."

The second one converts harder because it MAKES SENSE to the customer. They don't need to take your word for it — the logic itself convinces them.""")
p("")
h2("The 'Yes Yes Yes' Sequence (Full Picture)")
p("""This is the core strategy that ties ALL the research together:

1. HOOK — Grab attention with their pain point / day-to-day struggle (from avatar research)
2. BODY — Keep them watching with emotional relatability (from archetypes + hotwords)
3. ROOT CAUSE — Explain what's REALLY causing the problem (from root cause research)
   Customer thinks: "Yes, that makes sense — hormonal imbalance IS what's causing this"
4. SOLUTION MECHANISM — Explain the theory of how to fix it (from mechanism research)
   Customer thinks: "Yes, if we stop the DHT and fix the insulin, that WOULD fix it"
5. PRODUCT / INGREDIENTS — Show how this product's ingredients deliver the mechanism
   Customer thinks: "Yes, these ingredients DO target exactly what the mechanism says"
6. SOCIAL PROOF — Testimonials, before/after, authority figures
   Customer thinks: "Yes, it actually works for real people"
7. CTA — By now most objections are handled. Only thing left = price, safety, trust.

Each "yes" builds on the previous one. Skip a step and the chain breaks.""")
p("")
h2("How To Research Solution Mechanisms")
p("""AI Prompt:

"Hi, I want you to act as a world-class product strategist for a $100M/year brand in [NICHE]. You are provided with a document filled with research-based, science-backed insight explaining the root cause behind a specific problem experienced by [AVATAR].

Your task: develop a unique solution mechanism — a clear, logical theory of action that explains how the problem can be fixed at the root level. This is NOT about the product itself. Focus on the mechanism that makes transformation possible.

If the root cause has multiple contributing factors, break them down clearly. Provide a specific theory or approach for fixing each one. Show how the mechanism addresses all the problems.

The mechanism should be:
- Unique — something the prospect hasn't heard before
- Logical — backed by science, not fluffy
- Directly tied to the root cause
- Something that makes them say 'this is different from everything I tried'

Input: [Upload your root cause research document]" """)
p("")
h3("After You Get The Mechanism")
p("""1. PLAIN ENGLISH VERSION — explain the mechanism simply: "It stops the weed killer, calms the inflammation, and rebalances your hormones so your hair can grow naturally again"
2. METAPHOR/ANALOGY — one clear visual: "Pulling weeds before planting new seeds. You wouldn't try to grow flowers in toxic soil."
3. COPY VERSION — short, punchy, emotional sentences for the "how it works" section of an advertorial or VSL
4. UGC TALKING POINTS — key points for a content creator to explain naturally on camera""")
p("")
h2("How You Do It (with the machine)")
p("""This IS what the machine does. Look at mechanisms.md for NOOR:

M1: Adrenal Silica Theft (WINNING)
- Root cause: Post-menopausal adrenal exhaustion steals silica from hair
- Mechanism: Replace depleted silica + support adrenals
- "Aha" Statement: "Silica is what literally holds your hair in your scalp. Your exhausted adrenal glands are stealing it. No blood test checks for this."
- Why old solutions failed: Biotin doesn't address silica. Collagen can't form without silica. Iron/ferritin irrelevant if silica depleted.
- Solution connection: Horsetail Extract = bioavailable silica. Pantothenic Acid = adrenal support.

M2: GLP-1 Silica Starvation
- Root cause: GLP-1 appetite suppression triggers mineral triage
- Mechanism: Flood the system with silica + reduce metabolic stress
- "Aha" Statement: "Your GLP-1 cuts your appetite, so your body triages every mineral. Silica gets redirected to organs. Your hair gets nothing."
- Solution connection: Same ingredients, different angle for different archetype (GLP-1 users)

To create new mechanisms for new products:
1. Do root cause research (Phase 11)
2. Run the mechanism prompt above
3. Write it into mechanisms.md format
4. The machine then uses it to generate 1000+ ads""")
p("")

# ============================================================
# 14. ZAKARIA vs GEORGE
# ============================================================
h1("14. ZAKARIA vs. GEORGE — Full Comparison (Updated)")
p("")
p("""STEP 1: Pick broad problem
Zakaria: Brain + intuition
George: Same — YOUR call

STEP 2: Find sub-avatars on Reddit
Zakaria: Hours of manual browsing
George: research.py scrapes automatically

STEP 3: Check competition (FB Ad Library)
Zakaria: Manual search
George: Manual (can automate later)

STEP 4: Qualify avatars
Zakaria: Spreadsheet + gut feel
George: Same + Google Sheets template

STEP 5: Amazon review mining
Zakaria: Paid tool ($19) + ChatGPT
George: Quick manual check or AI prompt

STEP 6: Deep dive research (Reddit, forums)
Zakaria: Hours of manual reading per avatar
George: research.py + NotebookLM in parallel

STEP 7: YouTube + TikTok research
Zakaria: Manual browsing + copying comments
George: Manual (same — machine doesn't cover these yet). Can speed up with comment scrapers + AI prompt from Phase 9.

STEP 8: Amazon deep dive (product/competitor)
Zakaria: Manual reading of reviews
George: Manual (same — machine doesn't cover Amazon). Can speed up with AI prompt.

STEP 9: Fill research document
Zakaria: Manual typing into Google Doc
George: Synthesize NotebookLM output into 3 markdown files (archetypes.md, hotwords.md, mechanisms.md)

STEP 10: AI-accelerated extraction
Zakaria: ChatGPT prompt on raw data
George: Machine already does this for Reddit. For other sources (YouTube, TikTok, Amazon, Facebook) — use AI prompt.

STEP 11: Clean & merge research
Zakaria: Manual cleaning + ChatGPT merge prompt
George: Machine output is already organized. Merge prompt useful for adding manual research on top.

STEP 12: Root cause research
Zakaria: Google + ChatGPT Deep Research
George: Same — this is the THINKING work. Can't skip it. Feeds into mechanisms.md.

STEP 13: Solution mechanism
Zakaria: ChatGPT prompt on root cause doc
George: Same — then writes mechanism into mechanisms.md. Machine generates ads from it.

STEP 14: Create ads
Zakaria: Manual copywriting
George: Machine generates 1000+/day from the research files

STEP 15: Test and iterate
Zakaria: Manual
George: Batch system + validation + quality gates""")
p("")
h2("The Bottom Line")
p("""Zakaria does everything MANUALLY and it takes him weeks per product.
You do the same research but the machine AUTOMATES the repetitive parts.

The parts you CANNOT automate (your judgment, your instinct, your understanding):
- Picking which avatars to pursue
- Feeling which quotes have emotional punch
- Deciding what becomes an archetype vs noise
- Root cause research (you need to understand the science yourself)
- Solution mechanism creation (this is the creative/strategic thinking)

The machine handles the VOLUME. You handle the QUALITY.""")
p("")

# ============================================================
# 15. WHAT YOU STILL NEED TO LEARN
# ============================================================
h1("15. WHAT YOU STILL NEED TO LEARN")
p("""- Advertorials — "the big thing in this course" (coming in later sections of Zakaria's course). How to write the full article-style ads that convert.
- How to find untapped products — "need clarification from Boris" (still pending)
- Awareness stages in practice — you know the theory, need practice applying it to real products
- How to create mechanisms from scratch for a new product — you've seen Boris's mechanisms.md, now you need to do it yourself
- How to develop products from the mechanism — the next section of Zakaria's course covers finding/creating products that deliver the mechanism
- Concept development — how to turn all this research into specific ad concepts (angles, hooks, formats)
- Videos 1-7 of Market Research — transcripts missing, need to transcribe on Colab""")
p("")

# ============================================================
# 16. 10 KEY RULES
# ============================================================
h1("16. TEN KEY RULES")
p("From both the course + your own experience:")
p("")
p("""1. Do not copy without understanding WHY
(Your note #1 from the course)

2. People buy outcomes, not products
The serum does not matter. The hair coming back matters.

3. Magnitude of desire = how much pain x how big the desired outcome
More pain + bigger dream = more willing to pay

4. Mental pain sells harder than physical pain
"I feel embarrassed" > "my hair is thin"

5. Start with problem-aware audiences
They already have built-in desire for the fix. Easiest to sell to.

6. Research is ongoing — not a one-time thing
Every day = new angles, new hooks, new emotional triggers

7. Action > preparation
Do not spend months researching. Get enough, then START.

8. Start with low-competition avatar, make money, THEN expand
Do not fight brands doing 100 creatives/day when you are doing 10.

9. The boring research IS the work
It is not the ad creation that wins. It is knowing what to say.

10. Do not over-complicate it
Find the pain. Speak to it. Sell the outcome.""")
p("")

# ============================================================
# NOW CREATE THE GOOGLE DOC
# ============================================================
print("Building document content...")

# Create the document
doc = docs_service.documents().create(body={'title': 'MARKET RESEARCH — Master Document'}).execute()
doc_id = doc['documentId']
print(f"Created doc: {doc_id}")

# Build full text and track positions for formatting
full_text = ""
format_ranges = []  # (start, end, style)

for style, text in sections:
    start = len(full_text) + 1  # +1 for 1-indexed (docs API)
    full_text += text + "\n"
    end = len(full_text) + 1
    format_ranges.append((start, end - 1, style))  # -1 to not include the newline in formatting

# Insert all text at once
requests = [
    {
        'insertText': {
            'location': {'index': 1},
            'text': full_text
        }
    }
]

# Apply paragraph styles
for start, end, style in format_ranges:
    if style in ('TITLE', 'SUBTITLE', 'HEADING_1', 'HEADING_2', 'HEADING_3', 'NORMAL_TEXT'):
        requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': start, 'endIndex': end},
                'paragraphStyle': {'namedStyleType': style},
                'fields': 'namedStyleType'
            }
        })

print(f"Applying {len(requests)} formatting requests...")

# Batch update in chunks (API limit)
chunk_size = 50
for i in range(0, len(requests), chunk_size):
    chunk = requests[i:i+chunk_size]
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': chunk}
    ).execute()
    print(f"  Applied batch {i//chunk_size + 1}/{(len(requests)-1)//chunk_size + 1}")

# Move to George's project folder (or root)
print(f"\nDone! Google Doc created:")
print(f"https://docs.google.com/document/d/{doc_id}/edit")

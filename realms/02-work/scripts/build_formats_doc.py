# -*- coding: utf-8 -*-
"""Build a Google Doc: Advertorial vs Landing Page vs Product Page (for George).
Uploads an HTML body to Google Drive, converted to a native Google Doc (keeps
headings, tables, and clickable links)."""
import sys, io, os
if sys.stdout is not None:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / 'scripts'))
from google_helper import get_drive
from googleapiclient.http import MediaInMemoryUpload

HTML = r"""
<h1>The 3 Formats: Advertorial vs Landing Page vs Product Page (PDP)</h1>
<p><i>A beginner's map for George. Built Jun 14, 2026. Same machine, three different rooms &mdash; each does ONE job and hands the warmed-up visitor to the next.</i></p>

<h2>0. The one-sentence difference (read this first)</h2>
<ul>
<li><b>Advertorial</b> = a story that makes you <b>curious</b>. Looks like an article, not an ad. Soft, educational. It <i>earns</i> the decision slowly.</li>
<li><b>Landing Page (LP)</b> = a focused page that makes you <b>want it</b>. Opens with the offer, asks for the decision more directly.</li>
<li><b>Product Page (PDP)</b> = the <b>buy page</b> that takes your money. Price, photos, reviews, Add to Cart. You're already sold; it just closes.</li>
</ul>
<p><b>Important overlap to kill confusion:</b> "Landing Page" is the umbrella word for <i>any</i> page you land on from an ad. An <b>advertorial is a soft, editorial-style landing page</b>. A <b>sales page / VSL page is a harder landing page</b>. So advertorial and LP aren't rivals &mdash; the advertorial is one <i>flavour</i> of landing page.</p>

<h2>1. The funnel &mdash; how they connect (the BRIDGES)</h2>
<p>A bridge is just a <b>button</b>. Each page ends with a button that carries you to the next room. Here is a REAL live funnel I walked end-to-end (Lulutox detox tea &mdash; a normal dropship operator, not a mega-brand):</p>
<ol>
<li>Facebook/native ad interrupts a scroller &nbsp;&rarr;&nbsp; <b>click the ad</b></li>
<li><b>ADVERTORIAL</b> (lifed.com "15 Beauty Products...") &nbsp;&rarr;&nbsp; button: <i>"Learn More About Lulutox &raquo;"</i></li>
<li><b>PRODUCT ADVERTORIAL</b> (lulutox "5 Reasons Why...") &nbsp;&rarr;&nbsp; button: <i>"Check Availability / Get 70% OFF"</i></li>
<li><b>PRODUCT PAGE / PDP</b> (lulutox product-1) &nbsp;&rarr;&nbsp; button: <i>"ORDER NOW!"</i></li>
<li><b>CHECKOUT</b> (cart.lulutox.com) &nbsp;&rarr;&nbsp; pay &rarr; PDF/product delivered + upsell</li>
</ol>
<p>The soft button words ("Learn More", "Check Availability") are deliberate &mdash; they make clicking feel safe. That's the craft.</p>

<h2>2. ADVERTORIAL &mdash; deep</h2>
<p><b>What it is:</b> the word = ADVERTising + eDITORIAL. A landing page disguised as an organic news story / blog post. Unlike a normal sales page that opens with an offer and asks for a decision immediately, the advertorial <b>earns the decision gradually</b> &mdash; the reader feels <i>informed</i>, not <i>sold to</i>. That psychology is why advertorials beat hard-sell pages on COLD traffic.</p>
<p><b>Its job:</b> warm up a cold/problem-aware stranger and sell the CLICK to the next page (rarely a hard buy button up top).</p>
<p><b>Structure (from your own LFS format, ww-2 / lfs-operator):</b> Shock Hook &rarr; Personal Pain Setup &rarr; Graphic Symptom Breakdown &rarr; Failed Solutions (each dismantled one by one) &rarr; Rock-Bottom Moment &rarr; Discovery + Mechanism &rarr; Timeline of Recovery &rarr; Victory State &rarr; Product CTA &rarr; P.S. close. (~1400&ndash;1700 words.)</p>
<p><b>Best for:</b> Meta cold traffic and Google problem-aware searchers.</p>

<h2>3. LANDING PAGE (LP) / SALES PAGE &mdash; deep</h2>
<p><b>What it is:</b> a single, focused page built for ONE action. It opens closer to the offer and makes the ask more directly than an advertorial. A VSL page (video sales letter) is an LP with a video doing the selling.</p>
<p><b>Its job:</b> make a warmed-up reader WANT the product &mdash; full persuasion: big promise, the mechanism (why it works), proof/testimonials, offer, guarantee, CTA.</p>
<p><b>Rule of thumb (from lfs-prompt-engine):</b> 70% motivation, 30% education. "Describe what the product DOES, not what it IS. If the reader could replicate the solution without buying, you wrote too much education."</p>
<p><b>Best for:</b> the middle of the funnel &mdash; after the advertorial, before checkout. (On simple funnels the advertorial and LP can be the same page.)</p>

<h2>4. PRODUCT PAGE (PDP) &mdash; deep</h2>
<p><b>What it is:</b> PDP = Product Detail Page = the buy page. Price, photos, reviews, variant picker, guarantee, Add to Cart / Order Now. Minimal story &mdash; the visitor is already convinced.</p>
<p><b>Its job:</b> CLOSE the sale and take payment. Reduce friction; stack trust (review counts, guarantee, financing).</p>
<p><b>Structure (high-ticket pattern, lfs-operator high-ticket-lander-research):</b> promo bar &rarr; hero &rarr; comparison matrix &rarr; benefits grid &rarr; social proof &rarr; trust block &rarr; financing &rarr; warranty &rarr; price/specs + CTA. Phone number visible for high-ticket (some buyers close by voice). Stacked discounts = "save anchoring".</p>
<p><b>Best for:</b> the bottom of the funnel &mdash; product-aware / most-aware buyers ready to pay.</p>

<h2>5. Side-by-side comparison</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th></th><th>Advertorial</th><th>Landing Page / Sales Page</th><th>Product Page (PDP)</th></tr>
<tr><td><b>Stage</b></td><td>First hello</td><td>The pitch</td><td>The cash register</td></tr>
<tr><td><b>Looks like</b></td><td>A news article / story</td><td>A long persuasion page (often a VSL)</td><td>Photos, price, reviews, cart</td></tr>
<tr><td><b>Its job</b></td><td>Make curious, sell the click</td><td>Make them want it</td><td>Take the money</td></tr>
<tr><td><b>Buy button?</b></td><td>Usually no &mdash; a link forward</td><td>At the end</td><td>Yes &mdash; that's the point</td></tr>
<tr><td><b>Feeling</b></td><td>"Huh, tell me more..."</td><td>"Okay, I need this"</td><td>"Take my money"</td></tr>
<tr><td><b>Traffic</b></td><td>Coldest (Meta) / problem-aware (Google)</td><td>Warmed up</td><td>Convinced</td></tr>
</table>

<h2>6. WHY each fits a different person &mdash; the 5 Stages of Awareness</h2>
<p>Every customer sits on a rung of this ladder (Eugene Schwartz). The format you use depends on the rung:</p>
<ol>
<li><b>Unaware</b> &mdash; doesn't know they have a problem &nbsp;&rarr;&nbsp; Meta cold &rarr; advertorial</li>
<li><b>Problem-aware</b> &mdash; feels the pain, no fix &nbsp;&rarr;&nbsp; Google "knee pain" &rarr; advertorial</li>
<li><b>Solution-aware</b> &mdash; knows fixes exist, comparing &nbsp;&rarr;&nbsp; LP / sales page</li>
<li><b>Product-aware</b> &mdash; knows YOUR product &nbsp;&rarr;&nbsp; PDP</li>
<li><b>Most-aware</b> &mdash; ready, just needs the deal &nbsp;&rarr;&nbsp; PDP / checkout offer</li>
</ol>

<h2>7. LIVE LINKS</h2>
<h3>A) Whole funnels (walk these start &rarr; finish)</h3>
<ul>
<li><b>Lulutox funnel (the one I traced):</b><br>
1. Advertorial: <a href="https://www.lifed.com/advertorial/15-beauty-products-that-will-dominate-in-2026and-3-to-avoid">lifed.com advertorial</a><br>
2. Product advertorial: <a href="https://www.lulutox-official.com/articles/t-5reasonswhy-aa21/">lulutox "5 Reasons Why"</a><br>
3. Product page: <a href="https://lulutox-official.com/products/product-1/">lulutox product-1</a><br>
4. Checkout: the "ORDER NOW" button on #3 &rarr; cart.lulutox.com</li>
</ul>
<h3>B) Just the pages (not whole funnels)</h3>
<ul>
<li><b>Advertorial page:</b> <a href="https://www.lifed.com/advertorial/15-beauty-products-that-will-dominate-in-2026and-3-to-avoid">lifed.com</a> &nbsp;|&nbsp; <a href="https://www.lulutox-official.com/articles/t-5reasonswhy-aa21/">lulutox article</a></li>
<li><b>Landing / sales page:</b> <a href="https://drinkag1.com/dailyhealthdrink">AG1 (drinkag1.com) &mdash; long DR sales page for a supplement</a></li>
<li><b>Product page (PDP):</b> <a href="https://ridge.com">The Ridge Wallet (ridge.com)</a> &nbsp;|&nbsp; <a href="https://lulutox-official.com/products/product-1/">lulutox PDP</a></li>
</ul>
<h3>C) Swipe libraries (proven winners to study)</h3>
<ul>
<li><a href="https://swiped.co">swiped.co</a> &mdash; classic sales letters / VSLs / TSLs</li>
<li><a href="https://swipepages.com/landing-page-inspiration/page-type/advertorial/">Swipe Pages &mdash; advertorial collection</a></li>
<li><a href="https://www.goodadvertorials.com/">Good Advertorials</a> &mdash; real presell pages that beat their controls</li>
</ul>

<h2>8. From YOUR OWN machines (connect this to your tools)</h2>
<p>You don't have to learn this from strangers &mdash; your projects already define it:</p>
<p><b>ww-2:</b></p>
<ul>
<li><code>docs\andromeda-format-matrix.md</code> &mdash; the master 25&times;18 format matrix + how each format meets a different emotional state</li>
<li><code>components\dr-system.md</code> &mdash; the DR engine: Single Mechanism, Pain&rarr;Agitation&rarr;Discovery&rarr;Proof&rarr;Transformation&rarr;Action (60% pain)</li>
<li><code>components\primary-copy-system.md</code> &amp; <code>static-ad-system.md</code> &mdash; the META ad's job: "sell the CLICK to the advertorial"</li>
<li><code>formats\lfs\constants.json</code> &mdash; the 11-section advertorial (LFS) structure; <code>components\hook-types.md</code> &mdash; the 6 hooks (RAGE/THIRD/DESP/DISMISS/CONFESS/MISDIAG)</li>
</ul>
<p><b>lfs-operator:</b></p>
<ul>
<li><code>products\SOLIS-Crepey\research\high-ticket-lander-research.md</code> &mdash; explicit PDP vs advertorial vs landing-page breakdown ("buying-guide-as-advertorial")</li>
<li><code>components\lfs-prompt-engine.md</code> &mdash; the 7 principles (Hook=Dual-Lock, Failed Solutions dismantled, Mechanism=Discovery Arc, CTA=Story Close, 70/30 motivation/education)</li>
<li><code>components\frameworks\opening-structures.md</code> &amp; <code>close-architecture.md</code> &mdash; how to open by audience state, how to close as an identity decision</li>
</ul>
"""

drive = get_drive()
media = MediaInMemoryUpload(HTML.encode("utf-8"), mimetype="text/html", resumable=False)
meta = {"name": "Formats Map - Advertorial vs Landing Page vs Product Page",
        "mimeType": "application/vnd.google-apps.document"}
f = drive.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
print("DOC CREATED")
print(f["webViewLink"])

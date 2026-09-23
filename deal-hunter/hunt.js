#!/usr/bin/env node
/*
 * Deal Hunter v1: low-request personal-shopping discovery and verification.
 * Uses Node's built-in fetch only. No API keys and no LLM calls.
 */
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFile } = require("child_process");

const ROOT = __dirname;
const OUTPUT = path.join(ROOT, "output");
const CACHE = path.join(OUTPUT, "cache");
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36";

function usage(exitCode = 0) {
  console.log(`\nDeal Hunter — personal purchase discovery, with no API or AI-token cost.\n\nUsage:\n  node deal-hunter/hunt.js "external SSD 1TB" --budget-bgn 200 --verify 8\n  node deal-hunter/hunt.js "USB-C SSD enclosure" --sources emag,amazon_de,aliexpress\n  node deal-hunter/hunt.js --url "https://example.com/product"\n\nOptions:\n  --budget-bgn N       Maximum delivered item price in BGN (ranking only; shipping may be unknown)\n  --verify N           Fetch and inspect only the top N discovered product pages (default: 8)\n  --max-links N        Search results kept before verification (default: 24)\n  --sources a,b        Source IDs from config/sources.json (default: all)\n  --url URL            Verify one known product link without searching\n  --fresh              Ignore the local 24-hour page cache\n  --help               Show this help\n`);
  process.exit(exitCode);
}

function args(argv) {
  const out = { verify: 8, maxLinks: 24, fresh: false, includeOlx: false, includeBrowser: false, dryRun: false };
  const positionals = [];
  for (let i = 0; i < argv.length; i++) {
    const part = argv[i];
    if (part === "--help" || part === "-h") usage();
    if (part === "--fresh") { out.fresh = true; continue; }
    if (part === "--dry-run") { out.dryRun = true; continue; }
    if (part === "--include-olx") { out.includeOlx = true; continue; }
    if (part === "--include-browser") { out.includeBrowser = true; continue; }
    if (["--budget-bgn", "--verify", "--max-links", "--sources", "--url"].includes(part)) {
      if (!argv[i + 1]) throw new Error(`Missing value for ${part}`);
      out[part.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = argv[++i];
    } else if (part.startsWith("--")) throw new Error(`Unknown option: ${part}`);
    else positionals.push(part);
  }
  out.query = positionals.join(" ");
  out.verify = Number(out.verify);
  out.maxLinks = Number(out.maxLinks);
  out.budgetBgn = out.budgetBgn === undefined ? null : Number(out.budgetBgn);
  if (!out.url && !out.query) throw new Error("Provide a product search, e.g. \"external SSD 1TB\".");
  return out;
}

function mkdir(p) { fs.mkdirSync(p, { recursive: true }); }
function clean(text = "") { return decodeHtml(text.replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim(); }
function decodeHtml(s) { return s.replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&amp;/g, "&").replace(/&nbsp;/g, " ").replace(/&lt;/g, "<").replace(/&gt;/g, ">"); }
function escapeMd(s = "") { return s.replace(/[|\r\n]/g, " ").trim(); }
function hash(s) { return crypto.createHash("sha256").update(s).digest("hex").slice(0, 20); }
function canonical(url) { try { const u = new URL(url); u.hash = ""; ["utm_source", "utm_medium", "utm_campaign", "aff", "tag"].forEach(k => u.searchParams.delete(k)); return u.toString(); } catch { return url; } }
function domainFor(url) { try { return new URL(url).hostname.replace(/^www\./, "").toLowerCase(); } catch { return ""; } }
function sourceFor(url, sources) { const host = domainFor(url); return sources.find(s => host === s.domain || host.endsWith(`.${s.domain}`)); }
function displayAvailability(source) { return source?.availability || "Online availability not yet confirmed."; }

async function fetchText(url, timeoutMs = 18000) {
  // Node's fetch cannot reach some sites from this Windows setup, while the
  // installed curl client can. curl is local, needs no key, and is given a
  // strict timeout; it is not used for concurrency or bulk crawling.
  return new Promise((resolve, reject) => {
    execFile("curl.exe", ["-L", "-sS", "--max-time", String(Math.ceil(timeoutMs / 1000)), "-A", UA,
      "-H", "Accept-Language: en-US,en;q=0.8,bg;q=0.7", url], { maxBuffer: 8 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) return reject(new Error((stderr || error.message).trim()));
      resolve({ status: 200, url, text: stdout });
    });
  });
}

// Bing is used only as an index: one request per source, at a deliberately low volume.
function parseBing(html) {
  const items = [];
  for (const block of html.match(/<li class="b_algo"[\s\S]*?<\/li>/g) || []) {
    const anchor = block.match(/<h2[^>]*>\s*<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/i);
    if (!anchor) continue;
    let resultUrl = decodeHtml(anchor[1]);
    // Bing's HTML returns a tracking URL. Its `u=a1...` parameter is the
    // base64-encoded destination; decode it locally so domain filtering works.
    try {
      const wrapped = new URL(resultUrl);
      const encoded = wrapped.searchParams.get("u");
      if (encoded && encoded.startsWith("a1")) {
        const base64 = encoded.slice(2).replace(/-/g, "+").replace(/_/g, "/");
        resultUrl = Buffer.from(base64, "base64").toString("utf8");
      }
    } catch { /* keep the original URL if Bing changes its wrapper */ }
    if (!/^https?:/i.test(resultUrl)) continue;
    const snippet = block.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
    items.push({ url: resultUrl, title: clean(anchor[2]), snippet: clean(snippet ? snippet[1] : "") });
  }
  return items;
}

function absoluteUrl(href, base) {
  try { return new URL(decodeHtml(href), base).toString(); } catch { return ""; }
}
function priceFromText(text) {
  const m = clean(text).match(/(?:Цена\s*:?\s*)?([0-9]{1,5}(?:[.,][0-9]{1,2})?)\s*(?:лв\.?|BGN|€|EUR)/i);
  if (!m) return null;
  const currency = /€|EUR/i.test(m[0]) ? "EUR" : "BGN";
  return { amount: number(m[1]), currency };
}
// These two parsers are based on the response shapes already proven in this
// workspace's earlier product-search experiment. They avoid search engines.
function parseStoreResults(html, source) {
  const results = [];
  if (source.parser === "emag") {
    for (const m of html.matchAll(/aria-label="([^"]{15,900})"([\s\S]{0,5000}?product-new-price[\s\S]{0,800})/g)) {
      const href = m[2].match(/href="([^"?#]*\/(?:pd|product)\/[^"?#]+)"/i);
      const compactPrice = m[2].match(/product-new-price[^>]*>\s*([0-9]+)<sup><small[^>]*>,<\/small>\s*([0-9]+)<\/sup>/i);
      const price = priceFromText(m[2]) || (compactPrice ? { amount: Number(`${compactPrice[1]}.${compactPrice[2]}`), currency: "BGN" } : null);
      if (href && price) results.push({ title: clean(m[1]), url: absoluteUrl(href[1], "https://www.emag.bg"), price });
    }
  } else if (source.parser === "technopolis") {
    const blocks = html.split(/<te-product-box\b/i).slice(1);
    for (const block of blocks) {
      const title = block.match(/title="([^"]{12,300})"/i);
      const href = block.match(/href="([^"]+)"/i);
      const price = priceFromText(block.slice(0, 6000));
      if (title && href && price) results.push({ title: clean(title[1]), url: absoluteUrl(href[1], "https://www.technopolis.bg"), price });
    }
  } else if (source.parser === "ardes") {
    const tiles = html.split(/<div class="product" data-sku/i).slice(1);
    for (const tile of tiles) {
      const title = tile.match(/title="\s*([^"<>]{12,300})"/i);
      const href = tile.match(/href="(\/product\/[^"?#]+)"/i);
      const price = tile.match(/class="price-num">\s*([\d.,]+)\s*<span>\s*(€|лв)/i);
      if (title && href && price) results.push({ title: clean(title[1]), url: absoluteUrl(href[1], "https://ardes.bg"), price: { amount: number(price[1]), currency: /€/.test(price[2]) ? "EUR" : "BGN" } });
    }
  } else if (source.parser === "office1") {
    for (const tile of html.match(/<[^>]+(?:product|item)[^>]*>[\s\S]{0,7000}?<\/[^>]+>/gi) || []) {
      const href = tile.match(/href="([^"?#]*(?:product|products)[^"?#]*)"/i);
      const title = tile.match(/(?:title|aria-label)="([^"<>]{12,300})"/i);
      const price = priceFromText(tile);
      if (href && title && price) results.push({ title: clean(title[1]), url: absoluteUrl(href[1], "https://office1.bg"), price });
    }
  } else if (source.parser === "aliexpress") {
    for (const tile of html.match(/<a class="us--container[^>]*>[\s\S]{0,9000}?<\/a>/gi) || []) {
      const href = tile.match(/href="([^"]*\/item\/[^"?#]+\.html[^"]*)"/i);
      const title = tile.match(/<div title="([^"]{5,600})" class="us--title/i);
      const priced = tile.match(/aria-label="(BGN|EUR|USD)\s*([0-9]+(?:\.[0-9]{1,2})?)"/i);
      if (href && title && priced) results.push({ title: clean(title[1]), url: absoluteUrl(href[1], "https://www.aliexpress.com"), price: { amount: number(priced[2]), currency: priced[1].toUpperCase() } });
    }
  }
  const seen = new Set();
  return results.filter(x => x.url && !seen.has(x.url) && seen.add(x.url));
}

async function discover(query, sources, maxLinks) {
  const collected = [];
  for (const source of sources) {
    if (source.searchUrl) {
      const directUrl = source.searchUrl.replace("{q}", encodeURIComponent(query));
      try {
        const page = await fetchText(directUrl);
        const found = page.status === 200 ? parseStoreResults(page.text, source) : [];
        console.log(`  ${source.label}: ${found.length} direct-search links`);
        found.forEach(x => collected.push({ ...x, source: source.id, discoveredBy: "store search", discoveredPrice: x.price }));
        if (found.length) continue;
      } catch (err) { console.warn(`  Direct search failed for ${source.label}: ${err.message}`); }
    }
    const search = `${query} site:${source.domain}`;
    const url = `https://www.bing.com/search?q=${encodeURIComponent(search)}&count=8&setlang=en`;
    try {
      const page = await fetchText(url);
      if (page.status !== 200) { console.warn(`  Search unavailable for ${source.label}: HTTP ${page.status}`); continue; }
      const found = parseBing(page.text).filter(x => sourceFor(x.url, [source]));
      console.log(`  ${source.label}: ${found.length} indexed links`);
      found.forEach(x => collected.push({ ...x, source: source.id, discoveredBy: "Bing site search" }));
    } catch (err) { console.warn(`  Search failed for ${source.label}: ${err.message}`); }
  }
  const seen = new Set();
  const unique = collected.filter(x => { x.url = canonical(x.url); if (seen.has(x.url)) return false; seen.add(x.url); return true; });
  // Do not let a large retailer monopolise the report simply because it
  // returned more tiles. Round-robin keeps every working source visible.
  const groups = new Map(sources.map(s => [s.id, []]));
  unique.forEach(x => (groups.get(x.source) || groups.set(x.source, []).get(x.source)).push(x));
  const ordered = [];
  for (let i = 0; ordered.length < maxLinks; i++) {
    let added = false;
    for (const source of sources) {
      const next = groups.get(source.id)?.[i];
      if (next && ordered.length < maxLinks) { ordered.push(next); added = true; }
    }
    if (!added) break;
  }
  return ordered;
}

function valueAfter(obj, keys) {
  if (!obj || typeof obj !== "object") return null;
  for (const [k, v] of Object.entries(obj)) {
    if (keys.includes(k.toLowerCase()) && (typeof v === "string" || typeof v === "number")) return String(v);
    if (v && typeof v === "object") { const found = valueAfter(v, keys); if (found) return found; }
  }
  return null;
}
function jsonLd(html) {
  const objects = [];
  for (const m of html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try { objects.push(JSON.parse(m[1].trim())); } catch { /* malformed vendor JSON-LD is common */ }
  }
  return objects;
}
function meta(html, name) {
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const patterns = [new RegExp(`<meta[^>]+(?:property|name)=["']${escaped}["'][^>]+content=["']([^"']+)["']`, "i"), new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${escaped}["']`, "i")];
  for (const p of patterns) { const m = html.match(p); if (m) return decodeHtml(m[1]); }
  return null;
}
function number(v) { if (v === null || v === undefined) return null; const s = String(v).replace(/[^0-9,.]/g, ""); if (!s) return null; const normal = s.includes(",") && s.includes(".") ? s.replace(/\./g, "").replace(",", ".") : s.replace(",", "."); const n = Number(normal); return Number.isFinite(n) ? n : null; }
function currencyToBgn(amount, currency) { if (!amount) return null; const c = (currency || "").toUpperCase(); if (c === "BGN" || c === "ЛВ") return amount; if (c === "EUR" || c === "€") return amount * 1.95583; if (c === "USD" || c === "$") return amount * 1.78; return null; }
function findPrice(html, data) {
  const amount = valueAfter(data, ["price", "lowprice"] ) || meta(html, "product:price:amount") || meta(html, "og:price:amount");
  const currency = valueAfter(data, ["pricecurrency", "currency"]) || meta(html, "product:price:currency") || meta(html, "og:price:currency");
  return { amount: number(amount), currency: currency ? currency.toUpperCase() : null };
}
function productSignals(text) {
  const t = text.toLowerCase();
  return {
    warranty: /warranty|гаранц|guarantee/.test(t),
    returnPolicy: /return.{0,20}(day|days)|връщан/.test(t),
    official: /official store|official seller|sold by amazon|authorized reseller/.test(t),
    storageRisk: /ssd|solid state|storage|nvme|flash drive|memory card/.test(t) && /[0-9]+\s*(tb|gb)/.test(t)
  };
}
function storageRiskFlags(item, source) {
  const text = `${item.title || ""} ${item.snippet || ""}`.toLowerCase();
  const flags = [];
  const capacity = text.match(/\b(1|2|4|8|16)\s*tb\b/i);
  const priceBgn = currencyToBgn(item.price?.amount, item.price?.currency);
  if (item.suspiciousStorage) flags.unshift("Browser collector detected an implausible storage claim");
  if (source?.kind === "private") flags.push("Private seller: inspect before payment");
  if (source?.trust < 60) flags.push("Lower-trust marketplace/seller lane");
  if (/ssd|solid state|hard.?disk|storage|external drive|външен.{0,20}(?:диск|памет)/i.test(text) && capacity && priceBgn !== null) {
    const tb = Number(capacity[1]);
    const floor = tb === 1 ? 65 : tb === 2 ? 100 : tb === 4 ? 180 : 260;
    if (priceBgn < floor) flags.unshift(`Claimed ${tb}TB storage is implausibly cheap (~${priceBgn.toFixed(2)} BGN)`);
  }
  if (/feeng|generic|no name|extreme pro portable|16tb|high speed portable/i.test(text)) flags.unshift("Brand/model wording needs independent verification");
  return flags;
}
function riskFor(item, source) {
  const flags = storageRiskFlags(item, source);
  let risk = "low";
  if (flags.some(x => /implausib|Brand\/model/.test(x))) risk = "high";
  else if (flags.length || source?.kind === "private" || source?.trust < 65) risk = "medium";
  return { risk, riskFlags: flags };
}
async function inspect(candidate, fresh) {
  mkdir(CACHE);
  const cacheFile = path.join(CACHE, `${hash(candidate.url)}.json`);
  if (!fresh && fs.existsSync(cacheFile)) {
    const cached = JSON.parse(fs.readFileSync(cacheFile, "utf8"));
    if (Date.now() - cached.fetchedAt < 24 * 60 * 60 * 1000) return { ...candidate, ...cached, cached: true };
  }
  try {
    const page = await fetchText(candidate.url);
    const data = jsonLd(page.text);
    const title = meta(page.text, "og:title") || valueAfter(data, ["name"]) || candidate.title;
    const extractedPrice = findPrice(page.text, data);
    const price = extractedPrice.amount ? extractedPrice : (candidate.discoveredPrice || extractedPrice);
    const record = { fetchedAt: Date.now(), finalUrl: page.url, httpStatus: page.status, title: clean(title), price, signals: productSignals(clean(page.text).slice(0, 100000)), cached: false };
    fs.writeFileSync(cacheFile, JSON.stringify(record, null, 2));
    return { ...candidate, ...record };
  } catch (err) { return { ...candidate, error: err.message, httpStatus: 0, signals: {} }; }
}

function score(item, source, budgetBgn) {
  let points = source ? source.trust : 30;
  const notes = source ? [source.notes] : ["Unknown source: check seller identity, payment protection, and return policy."];
  if (item.httpStatus === 200) points += 4;
  if (item.signals?.warranty) points += 5;
  if (item.signals?.returnPolicy) points += 4;
  if (item.signals?.official) points += 5;
  const priceBgn = currencyToBgn(item.price?.amount, item.price?.currency);
  if (budgetBgn && priceBgn !== null) {
    if (priceBgn <= budgetBgn) points += 10;
    else { points -= 18; notes.unshift(`Over the stated item budget: ~${priceBgn.toFixed(2)} BGN before any delivery charge.`); }
  }
  const riskInfo = riskFor(item, source);
  if (riskInfo.risk === "high") { points -= 32; notes.unshift(`HIGH RISK (still shown): ${riskInfo.riskFlags.join("; ")}.`); }
  else if (riskInfo.risk === "medium") { points -= 12; notes.unshift(`Risk to check: ${riskInfo.riskFlags.join("; ") || "seller and item details need verification"}.`); }
  if (item.signals?.storageRisk && source && source.trust < 65) notes.unshift("Storage warning: do not trust claimed capacity alone. Prefer Samsung, Crucial, Kingston, SanDisk, WD, or a retailer/official store with clear returns.");
  if (source?.kind === "private") notes.unshift("Private-listing rule: inspect before payment; treat condition, battery/health, accessories, and model number as unverified until checked.");
  if (source?.id === "alibaba") notes.unshift("Alibaba is usually wholesale: reject listings with MOQ, unclear shipping, or no Trade Assurance.");
  return { score: Math.max(0, Math.min(100, points)), priceBgn, notes, ...riskInfo };
}
function updateOfferHistory(items) {
  const historyFile = path.join(OUTPUT, "offer-history.json");
  let history = { version: 1, offers: {} };
  try { history = JSON.parse(fs.readFileSync(historyFile, "utf8")); } catch { /* first run */ }
  const now = new Date().toISOString();
  for (const item of items) {
    const id = `${item.source}:${hash(canonical(item.finalUrl || item.url))}`;
    const existing = history.offers[id];
    const sample = { at: now, amount: item.price?.amount ?? null, currency: item.price?.currency ?? null, priceBgn: item.priceBgn ?? null };
    const priceHistory = [...(existing?.priceHistory || [])];
    if (!priceHistory.length || JSON.stringify(priceHistory.at(-1)) !== JSON.stringify(sample)) priceHistory.push(sample);
    history.offers[id] = {
      id, source: item.source, url: item.finalUrl || item.url, title: item.title,
      firstSeen: existing?.firstSeen || now, lastSeen: now, seenCount: (existing?.seenCount || 0) + 1,
      priceHistory: priceHistory.slice(-20)
    };
    item.history = { firstSeen: history.offers[id].firstSeen, seenCount: history.offers[id].seenCount, previousPriceBgn: priceHistory.length > 1 ? priceHistory.at(-2).priceBgn : null };
  }
  fs.writeFileSync(historyFile, JSON.stringify(history, null, 2));
}
function report(items, query, budgetBgn, fileBase) {
  const now = new Date().toISOString();
  const lines = ["# Deal Hunter results", "", `Generated: ${now}`, `Search: ${query || "Direct URL verification"}`, budgetBgn ? `Budget: ${budgetBgn.toFixed(2)} BGN (delivery/VAT still require final checkout verification)` : "Budget: not set", "", "All offers are shown, including high-risk ones. Risk is a warning for you to decide on, never a hidden filter.", "", "## Shortlist", "", "| Score | Risk | Source | Product | Listed price | Availability | Link |", "|---:|---|---|---|---:|---|---|"];
  for (const item of items) {
    const listed = item.price?.amount ? `${item.price.amount} ${item.price.currency || ""}`.trim() : "Not extracted";
    lines.push(`| ${item.score} | ${String(item.risk || "unknown").toUpperCase()} | ${escapeMd(item.sourceLabel)} | ${escapeMd(item.title || "Untitled result").slice(0, 110)} | ${listed} | ${escapeMd(item.availability)} | [Open](${item.finalUrl || item.url}) |`);
  }
  lines.push("", "## Before buying", "", "- Open the final product page and use its checkout total for Bulgaria; search snippets and listed price are not final delivered cost.", "- For SSDs/storage: verify exact model, capacity, official seller/retailer, warranty, and return policy. Never buy suspiciously cheap ‘2TB’ storage from an unknown seller.", "- Marketplace reliability score is a starting filter, not a guarantee. Read current seller reviews and use platform buyer protection.", "", "## Per-item flags", "");
  for (const item of items) lines.push(`- **${escapeMd(item.title || item.url)}** — ${item.notes.join(" ")} Seen ${item.history?.seenCount || 1} time(s) since ${(item.history?.firstSeen || now).slice(0, 10)}.${item.error ? ` Fetch failed: ${item.error}.` : ""}`);
  const md = path.join(OUTPUT, `${fileBase}.md`);
  const json = path.join(OUTPUT, `${fileBase}.json`);
  fs.writeFileSync(md, lines.join("\n"));
  fs.writeFileSync(json, JSON.stringify({ generatedAt: now, query, budgetBgn, items }, null, 2));
  return { md, json };
}

function loadBrowserImport(source, query) {
  const file = path.join(OUTPUT, `${source.id}-latest.json`);
  try {
    const data = JSON.parse(fs.readFileSync(file, "utf8"));
    const age = Date.now() - Date.parse(data.collectedAt || 0);
    if (!Array.isArray(data.listings) || !Number.isFinite(age) || age > 24 * 60 * 60 * 1000) return [];
    const terms = String(query || "").toLowerCase().split(/\s+/).filter(x => x.length >= 3);
    const collectedTerms = String(data.query || "").toLowerCase().split(/\s+/).filter(x => x.length >= 3);
    const listings = data.listings || data.items;
    if (!Array.isArray(listings)) return [];
    if (terms.length && terms.every(term => collectedTerms.includes(term))) return listings;
    return listings.filter(item => !terms.length || terms.some(term => `${item.title} ${item.notes?.join(" ")}`.toLowerCase().includes(term)));
  } catch { return []; }
}

async function main() {
  const opt = args(process.argv.slice(2));
  mkdir(OUTPUT);
  const config = JSON.parse(fs.readFileSync(path.join(ROOT, "config", "sources.json"), "utf8"));
  const requested = opt.sources ? new Set(String(opt.sources).split(",").map(s => s.trim())) : null;
  const sources = config.sources.filter(s => !s.browserOnly && (!requested || requested.has(s.id)));
  const browserSources = config.sources.filter(s => s.browserOnly && ((opt.includeBrowser && (!requested || requested.has(s.id))) || opt.includeOlx && s.id === "olx" || requested?.has(s.id)));
  if (!sources.length && !opt.url && !browserSources.length) throw new Error("No configured sources selected. Check --sources against config/sources.json.");
  if (opt.dryRun) {
    console.log("Deal Hunter dry run — no websites opened and no report written.");
    console.log(`Direct sources: ${sources.map(s => s.id).join(", ") || "none"}`);
    console.log(`Browser sources: ${browserSources.map(s => s.id).join(", ") || "none"}`);
    console.log(`Limits: ${opt.maxLinks} discovered links, ${opt.verify} page checks.`);
    return;
  }
  console.log(`Deal Hunter: ${opt.url ? "verifying one direct link" : `discovering \"${opt.query}\" across ${sources.length} sources`}`);
  let candidates = opt.url ? [{ url: canonical(opt.url), title: "Direct URL", snippet: "", discoveredBy: "direct URL" }] : await discover(opt.query, sources, opt.maxLinks);
  const browserListings = opt.url ? [] : browserSources.flatMap(source => {
    const listings = loadBrowserImport(source, opt.query).map(item => ({ ...item, source: source.id }));
    console.log(`  ${source.label} browser import: ${listings.length} recent matching listings`);
    return listings;
  });
  if (!candidates.length && !browserListings.length) throw new Error("No indexed product links found. Try fewer words, a brand/model, import recent browser cards, or --url with a product page you found manually.");
  console.log(`\nFound ${candidates.length} unique links. Verifying at most ${opt.verify} pages...`);
  const inspected = [];
  for (const listing of browserListings) {
    const source = config.sources.find(s => s.id === listing.source);
    const ranking = score({ ...listing, httpStatus: 200, signals: {}, snippet: listing.notes?.join(" ") }, source, opt.budgetBgn);
    inspected.push({ ...listing, finalUrl: listing.url, httpStatus: 200, sourceLabel: source.label, availability: displayAvailability(source), ...ranking });
  }
  for (const candidate of candidates.slice(0, opt.verify)) {
    const source = sourceFor(candidate.url, sources) || sourceFor(candidate.url, config.sources);
    console.log(`  Checking ${source?.label || domainFor(candidate.url)}...`);
    const item = await inspect(candidate, opt.fresh);
    const ranking = score(item, source, opt.budgetBgn);
    inspected.push({ ...item, source: source?.id || candidate.source || "unknown", sourceLabel: source?.label || domainFor(item.finalUrl || item.url), availability: displayAvailability(source), ...ranking });
  }
  inspected.sort((a, b) => b.score - a.score || ((a.priceBgn ?? Infinity) - (b.priceBgn ?? Infinity)));
  updateOfferHistory(inspected);
  const slug = (opt.query || "direct-link").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "").slice(0, 50) || "results";
  const stamp = new Date().toISOString().slice(0, 10);
  const files = report(inspected, opt.query, opt.budgetBgn, `${stamp}-${slug}`);
  console.log(`\nDone. Markdown report: ${files.md}`);
  console.log(`Raw reusable data: ${files.json}`);
}

main().catch(err => { console.error(`\nDeal Hunter error: ${err.message}`); process.exitCode = 1; });

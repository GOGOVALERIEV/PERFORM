#!/usr/bin/env node
/*
 * Imports cards already read from an OLX browser session. OLX intentionally
 * blocks raw HTTP collectors, so browser reading and local ranking are kept
 * separate. Input is an array of { title, url, text } objects.
 */
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const OUT = path.join(ROOT, "output");
const NEARBY = ["благоевград", "джерман", "симитли", "разлог", "банско", "сандански", "петрич", "дупница"];
const RISK_WORDS = ["feeng", "extreme pro portable", "no name", "generic"];

function usage() {
  console.log("Usage: node deal-hunter/olx-import.js <browser-cards.json> [--query \"external SSD\"]");
  process.exit(1);
}
function parseCard(card, query) {
  const text = String(card.text || "").replace(/\r/g, "");
  const title = String(card.title || text.split("\n")[0] || "").trim();
  const priceMatch = text.match(/(?:^|\n)\s*([0-9]+(?:[.,][0-9]+)?)\s*(€|лв\.?|BGN)/im);
  const price = priceMatch ? Number(priceMatch[1].replace(",", ".")) : null;
  const currency = priceMatch ? (priceMatch[2].toUpperCase().startsWith("ЛВ") ? "BGN" : priceMatch[2].toUpperCase()) : null;
  const lower = `${title}\n${text}`.toLowerCase();
  const location = (text.match(/(?:гр\.|с\.)\s*[^\n-]+/i) || [""])[0].trim();
  const nearby = NEARBY.some(place => lower.includes(place));
  const queryTerms = String(query || "").toLowerCase().split(/\s+/).filter(x => x.length >= 3);
  const matchedTerms = queryTerms.filter(term => lower.includes(term)).length;
  const suspiciousStorage = /(?:ssd|външен.{0,20}(?:диск|памет)|hard.?disk)/i.test(title)
    && ((/(?:2|4|8)\s*tb/i.test(title) && price !== null && price < 50) || RISK_WORDS.some(word => lower.includes(word)));
  let score = 38 + (nearby ? 18 : 0) + Math.min(10, matchedTerms * 3);
  if (/гаранц|warranty|experienced seller/i.test(lower)) score += 8;
  if (/използвано/i.test(lower)) score -= 4;
  if (suspiciousStorage) score -= 30;
  return {
    source: "olx", sourceLabel: "OLX private listing", title, url: card.url, price: { amount: price, currency },
    location, nearby, condition: /използвано/i.test(lower) ? "used" : (/ново/i.test(lower) ? "new" : "unknown"),
    suspiciousStorage, score: Math.max(0, Math.min(100, score)),
    notes: [
      nearby ? "Nearby: inspect in person before paying." : "Not nearby: use courier inspection; do not prepay.",
      suspiciousStorage ? "High risk: capacity/brand claim looks implausible for the price. Reject unless independently verified." : "Private listing: confirm exact model, condition, accessories, and serial number."
    ]
  };
}

const input = process.argv[2];
if (!input || input.startsWith("--")) usage();
const queryIndex = process.argv.indexOf("--query");
const query = queryIndex >= 0 ? process.argv[queryIndex + 1] : "";
const cards = JSON.parse(fs.readFileSync(input, "utf8"));
if (!Array.isArray(cards)) throw new Error("Input must be a JSON array of browser cards.");
fs.mkdirSync(OUT, { recursive: true });
const listings = cards.map(card => parseCard(card, query)).filter(x => x.url && x.title);
listings.sort((a, b) => Number(b.nearby) - Number(a.nearby) || b.score - a.score || ((a.price.amount ?? Infinity) - (b.price.amount ?? Infinity)));
const result = { collectedAt: new Date().toISOString(), query, source: "olx", listings };
const target = path.join(OUT, "olx-latest.json");
fs.writeFileSync(target, JSON.stringify(result, null, 2));
console.log(`Imported ${listings.length} OLX cards -> ${target}`);
console.log(`Nearby listings: ${listings.filter(x => x.nearby).length}; suspicious storage listings: ${listings.filter(x => x.suspiciousStorage).length}`);

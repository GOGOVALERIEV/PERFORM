#!/usr/bin/env node
/*
 * Imports visible product cards from a normal browser session for marketplaces
 * that show a CAPTCHA/verification page to raw HTTP. It never bypasses either.
 */
const fs = require("fs");
const path = require("path");
const source = process.argv[2];
const input = process.argv[3];
const queryIndex = process.argv.indexOf("--query");
const query = queryIndex >= 0 ? process.argv[queryIndex + 1] : "";
if (!source || !input || source.startsWith("-") || input.startsWith("-")) {
  console.log("Usage: node deal-hunter/browser-import.js <temu|alibaba> <browser-cards.json> [--query \"external SSD\"]");
  process.exit(1);
}
if (!/^[a-z0-9_-]+$/i.test(source)) throw new Error("Invalid source id.");
const cards = JSON.parse(fs.readFileSync(input, "utf8"));
if (!Array.isArray(cards)) throw new Error("Input must be a JSON array of visible {title, url, text} cards.");
function parse(card) {
  const text = String(card.text || "").replace(/\r/g, "");
  const title = String(card.title || text.split("\n")[0] || "").trim();
  const priceMatch = text.match(/(?:^|\n|\s)(?:US\s*)?(BGN|EUR|USD|€|\$|лв\.?)\s*([0-9]+(?:[.,][0-9]+)?)/i)
    || text.match(/(?:^|\n)\s*([0-9]+(?:[.,][0-9]+)?)\s*(BGN|EUR|USD|€|\$|лв\.?)/i);
  let amount = null; let currency = null;
  if (priceMatch) {
    const firstIsCurrency = /BGN|EUR|USD|€|\$|лв/i.test(priceMatch[1]);
    amount = Number(String(firstIsCurrency ? priceMatch[2] : priceMatch[1]).replace(",", "."));
    currency = String(firstIsCurrency ? priceMatch[1] : priceMatch[2]).replace("€", "EUR").replace("$", "USD").replace(/лв\.?/i, "BGN").toUpperCase();
  }
  const lower = `${title}\n${text}`.toLowerCase();
  const suspiciousStorage = /ssd|solid state|hard.?disk|storage|външен.{0,20}(?:диск|памет)/i.test(lower)
    && (/(?:4|8|16)\s*tb/i.test(lower) || /extreme pro portable|generic|no name|high speed portable/i.test(lower));
  return { source, title, url: card.url, price: { amount, currency }, suspiciousStorage,
    notes: ["Browser-read marketplace card: verify seller, shipping, final tax, and return terms.", ...(suspiciousStorage ? ["High risk: storage claim/model wording needs independent verification."] : [])] };
}
const listings = cards.map(parse).filter(item => item.title && item.url);
const out = path.join(__dirname, "output");
fs.mkdirSync(out, { recursive: true });
const target = path.join(out, `${source}-latest.json`);
fs.writeFileSync(target, JSON.stringify({ collectedAt: new Date().toISOString(), query, source, listings }, null, 2));
console.log(`Imported ${listings.length} ${source} browser cards -> ${target}`);

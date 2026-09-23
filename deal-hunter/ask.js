#!/usr/bin/env node
/* A no-model convenience wrapper for the way a person actually asks. */
const { spawnSync } = require("child_process");
const rawArgs = process.argv.slice(2);
const dryRun = rawArgs.includes("--dry-run");
const input = rawArgs.filter(arg => arg !== "--dry-run").join(" ").trim();
if (!input) {
  console.log('Usage: node deal-hunter/ask.js "find a cheap external SSD under 220 BGN"');
  process.exit(1);
}
const m = input.match(/(?:under|below|до|под)\s*(\d+(?:[.,]\d+)?)\s*(bgn|лв\.?|eur|€)?/i);
const query = input.replace(/(?:find|search|look for|cheap|reliable|best deals?|please|under|below|до|под|a|an|the)\b/gi, " ")
  .replace(/\d+(?:[.,]\d+)?\s*(?:bgn|лв\.?|eur|€)?/gi, " ").replace(/\s+/g, " ").trim();
const argv = [require("path").join(__dirname, "hunt.js"), query || input, "--include-browser"];
if (dryRun) argv.push("--dry-run");
if (m) {
  let budget = Number(m[1].replace(",", "."));
  if (/eur|€/i.test(m[2] || "")) budget *= 1.95583;
  argv.push("--budget-bgn", String(budget));
}
const result = spawnSync(process.execPath, argv, { stdio: "inherit" });
process.exit(result.status || 0);

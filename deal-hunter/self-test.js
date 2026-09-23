#!/usr/bin/env node
/* Controlled integration smoke test: no public websites are opened. */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const ROOT = __dirname;
const NODE = process.execPath;
let failed = false;
function check(condition, message) {
  console.log(`${condition ? "PASS" : "FAIL"}  ${message}`);
  if (!condition) failed = true;
}
function run(file, args = []) {
  const result = spawnSync(NODE, [path.join(ROOT, file), ...args], { cwd: ROOT, encoding: "utf8" });
  check(result.status === 0, `${file} ${args.join(" ")}`);
  return `${result.stdout || ""}\n${result.stderr || ""}`;
}

const sources = JSON.parse(fs.readFileSync(path.join(ROOT, "config", "sources.json"), "utf8")).sources;
const byId = new Map(sources.map(source => [source.id, source]));
["emag", "technopolis", "technomarket", "office1", "ardes", "ozone", "amazon_de", "aliexpress", "olx", "temu", "alibaba"].forEach(id => check(byId.has(id), `configured source: ${id}`));
["olx", "temu", "alibaba"].forEach(id => check(byId.get(id)?.browserOnly === true, `${id} is browser-only`));
["emag", "technopolis", "ardes", "aliexpress"].forEach(id => check(Boolean(byId.get(id)?.parser), `${id} has a direct-search adapter`));

["hunt.js", "ask.js", "olx-import.js", "browser-import.js"].forEach(file => {
  const result = spawnSync(NODE, ["--check", path.join(ROOT, file)], { encoding: "utf8" });
  check(result.status === 0, `syntax: ${file}`);
});

const directPlan = run("hunt.js", ["external SSD 1TB", "--sources", "emag,technopolis,ardes,aliexpress", "--dry-run"]);
check(/no websites opened/i.test(directPlan) && /emag.*technopolis.*ardes.*aliexpress/i.test(directPlan), "direct-source dry run has the intended small plan");
const chatPlan = run("ask.js", ["find a cheap reliable external SSD under 220 BGN", "--dry-run"]);
check(/no websites opened/i.test(chatPlan) && /Browser sources: olx, temu, alibaba/i.test(chatPlan), "normal-language request becomes a browser-inclusive plan");

const fixture = path.join(ROOT, "testdata", "olx-cards.json");
run("olx-import.js", [fixture, "--query", "външен SSD"]);
run("browser-import.js", ["temu", fixture, "--query", "външен SSD"]);
run("browser-import.js", ["alibaba", fixture, "--query", "външен SSD"]);
const olxRun = run("hunt.js", ["външен SSD", "--sources", "olx", "--include-browser", "--verify", "0"]);
check(/OLX private listings browser import: 2/i.test(olxRun), "OLX cards enter the combined hunter");
const temuRun = run("hunt.js", ["външен SSD", "--sources", "temu", "--include-browser", "--verify", "0"]);
check(/Temu browser import: 2/i.test(temuRun), "Temu cards enter the combined hunter");
const alibabaRun = run("hunt.js", ["външен SSD", "--sources", "alibaba", "--include-browser", "--verify", "0"]);
check(/Alibaba browser import: 2/i.test(alibabaRun), "Alibaba cards enter the combined hunter");
const report = fs.readFileSync(path.join(ROOT, "output", `${new Date().toISOString().slice(0, 10)}-ssd.json`), "utf8");
check(/"risk": "high"/i.test(report), "implausible storage is labelled HIGH risk and retained");
const skill = fs.readFileSync(path.join(ROOT, "..", ".agents", "skills", "deal-hunter", "SKILL.md"), "utf8");
check(/^---\nname: deal-hunter\n/m.test(skill) && /Never remove an offer/i.test(skill), "chat skill is discoverable and preserves all offers");

if (failed) process.exitCode = 1;
else console.log("\nAll controlled Deal Hunter checks passed. No public store page was opened.");

#!/usr/bin/env node
/* Offline check for the TEST-only fresh sentence laboratory. */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const ROOT = path.resolve(__dirname, "..");
const node = process.execPath;
let bad = false;
function check(ok, label) { console.log(`${ok ? "PASS" : "FAIL"}  ${label}`); if (!ok) bad = true; }
function run(args) { return spawnSync(node, [path.join(__dirname, "fresh_sentence_lab.js"), ...args], { cwd: ROOT, encoding: "utf8" }); }

const syntax = spawnSync(node, ["--check", path.join(__dirname, "fresh_sentence_lab.js")], { encoding: "utf8" });
check(syntax.status === 0, "lab script parses");
const goodBrief = path.join(ROOT, "state", "redteam", "TEST-fresh-sentence-smoke.json");
const output = path.join(ROOT, "state", "redteam", "TEST-fresh-sentence-selftest-output");
const good = run([goodBrief, "--mock", "--out", output]);
check(good.status === 0, "mock three-fact run succeeds without a network call");
const manifestPath = path.join(output, "manifest.json");
const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, "utf8")) : null;
check(manifest?.testOnly === true && manifest?.mode === "mock", "output is permanently labelled TEST-only");
check(manifest?.records?.length === 3 && manifest.records.every(record => record.accepted && record.attempts?.length === 1), "every base sentence passes before assembly with an auditable attempt record");
const forbidden = run([path.join(ROOT, "state", "redteam", "not-a-test-brief.json"), "--mock"]);
check(forbidden.status !== 0 && /must start with TEST-/i.test(`${forbidden.stdout}\n${forbidden.stderr}`), "non-TEST brief is refused before generation");
const escaped = run([goodBrief, "--mock", "--out", path.join(ROOT, "outside-redteam")]);
check(escaped.status !== 0 && /output must stay under state\/redteam/i.test(`${escaped.stdout}\n${escaped.stderr}`), "output cannot escape the TEST red-team folder");
if (bad) process.exitCode = 1;
else console.log("\nAll fresh-sentence lab checks passed. No model, detector, or university system was contacted.");

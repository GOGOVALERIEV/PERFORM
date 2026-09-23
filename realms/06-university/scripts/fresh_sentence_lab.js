#!/usr/bin/env node
/*
 * TEST-ONLY red-team text laboratory.
 * It creates labelled experimental documents from a closed-book fact brief.
 * It does not submit, upload, log in, solve CAPTCHAs, or touch Blackboard.
 */
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const REDTEAM_ROOT = path.join(ROOT, "state", "redteam");
const JUDGE_MODEL = "openai/gpt-4.1-mini";
const CONSTRUCTIONS = [
  "Start with the date or period from the fact.",
  "Start with the named person, organization, or event from the fact.",
  "Put the date after the main subject instead of at the beginning.",
  "Use the fact's two clauses in reverse order only if that preserves its meaning exactly.",
  "Use a short opening phrase followed by the fact; do not add evaluation or explanation.",
  "Use a compact declarative construction with only the information in the fact."
];
function fail(message) { throw new Error(message); }
function usage() {
  console.log("Usage: node fresh_sentence_lab.js <TEST-brief.json> [--mock] [--live] [--out folder]");
  process.exit(1);
}
function parse(argv) {
  const out = { mock: false, live: false, out: null, limit: null, skipJudge: false, attempts: 1 };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--mock") out.mock = true;
    else if (argv[i] === "--live") out.live = true;
    else if (argv[i] === "--out") out.out = argv[++i] || fail("Missing --out folder.");
    else if (argv[i] === "--limit") out.limit = Number(argv[++i]) || fail("--limit must be a positive number.");
    else if (argv[i] === "--skip-judge") out.skipJudge = true;
    else if (argv[i] === "--attempts") out.attempts = Number(argv[++i]) || fail("--attempts must be a positive number.");
    else rest.push(argv[i]);
  }
  if (rest.length !== 1 || out.mock === out.live) usage();
  return { brief: rest[0], ...out };
}
function words(text) { return (text.match(/[0-9A-Za-z\u0400-\u04FF]+/g) || []).length; }
function clean(text) { return String(text || "").replace(/\s+/g, " ").replace(/^[-–—•\s]+/, "").trim(); }
function anchors(fact) {
  const nums = fact.match(/\b\d{1,4}(?:[.,]\d+)?\b/g) || [];
  const names = fact.match(/\b[А-ЯA-Z][а-яa-z-]{2,}\b/g) || [];
  return [...new Set([...nums, ...names])].slice(0, 4);
}
function mechanicalGate(sentence, fact) {
  if (!/[.!?]$/.test(sentence)) return [false, "missing final punctuation"];
  if (words(sentence) < 6 || words(sentence) > 42) return [false, "sentence length outside 6–42 words"];
  if (/\b[а-я]{22,}\b/i.test(sentence)) return [false, "possible fused word"];
  const lower = sentence.toLowerCase();
  for (const anchor of anchors(fact)) if (!lower.includes(anchor.toLowerCase())) return [false, `lost fact anchor: ${anchor}`];
  return [true, "ok"];
}
function mockSentence(fact, index) {
  let normalized = fact.replace(/^\s*(\d{4})\s*:\s*/, "През $1 г. ").replace(/[.]+$/, "");
  const starters = ["", "", "Тук се вижда нещо конкретно: ", ""];
  return `${starters[index % starters.length]}${normalized}.`;
}
function requestOpenRouter(model, messages, maxTokens = 96) {
  const authFile = path.join(process.env.USERPROFILE || "", ".pi", "agent", "auth.json");
  const key = JSON.parse(fs.readFileSync(authFile, "utf8")).openrouter?.key;
  if (!key) fail("OpenRouter key missing from the local auth file.");
  const body = JSON.stringify({ model, temperature: 0.8, max_tokens: maxTokens, reasoning: { enabled: false }, messages });
  return new Promise((resolve, reject) => {
    // Node HTTPS is unreliable on this Windows installation. curl receives
    // the JSON on stdin, so the prompt never becomes a shell command.
    const child = spawn("curl.exe", ["-sS", "--max-time", "120", "-X", "POST",
      "https://openrouter.ai/api/v1/chat/completions", "-H", `Authorization: Bearer ${key}`,
      "-H", "Content-Type: application/json", "--data-binary", "@-"], { stdio: ["pipe", "pipe", "pipe"] });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8"); child.stderr.setEncoding("utf8");
    child.stdout.on("data", chunk => stdout += chunk); child.stderr.on("data", chunk => stderr += chunk);
    child.on("error", error => reject(error));
    child.on("close", code => {
      if (code !== 0) return reject(new Error(`OpenRouter transport failed: ${stderr.slice(0, 160) || code}`));
      try { resolve(clean(JSON.parse(stdout).choices?.[0]?.message?.content)); }
      catch { reject(new Error(`OpenRouter response could not be read: ${stdout.slice(0, 160)}`)); }
    });
    child.stdin.end(body);
  });
}
async function candidateFor(fact, i, brief, live) {
  if (!live) return mockSentence(fact, i);
  const model = brief.models?.[i % brief.models.length] || "deepseek/deepseek-v4-flash-0731";
  const construction = brief.constructions?.[i % brief.constructions.length] || CONSTRUCTIONS[i % CONSTRUCTIONS.length];
  return requestOpenRouter(model, [
    { role: "system", content: "You write one grammatical Bulgarian sentence for an authorized detector-robustness experiment. Return only one sentence." },
    { role: "user", content: `Topic: ${brief.topic}\nClosed-book fact: ${fact}\nConstruction requirement: ${construction}\nWrite exactly one grammatical Bulgarian sentence from this fact. Keep all names, dates, and numbers exactly. If the fact is already a complete sentence, restate only that fact. Do not add countries, people, causes, examples, opinions, or any detail not literally written in the fact.` }
  ], 384);
}
async function judge(originalFact, sentence, live) {
  if (!live) return { pass: true, note: "mock judge: mechanical gate only" };
  const model = JUDGE_MODEL;
  const answer = await requestOpenRouter(model, [
    { role: "system", content: "You are a strict Bulgarian grammar and fact checker. Answer only PASS or FAIL." },
    { role: "user", content: `Fact: ${originalFact}\nSentence: ${sentence}\nIs the sentence grammatical and faithful to the fact?` }
  ], 256);
  return { pass: /^PASS\b/i.test(answer), note: answer ? answer.slice(0, 120) : "judge returned no explicit verdict" };
}
function assemble(sentences) {
  const groups = [];
  for (let i = 0; i < sentences.length; i += 3) groups.push(sentences.slice(i, i + 3).join(" "));
  return groups.join("\n\n") + "\n";
}
async function main() {
  const opt = parse(process.argv.slice(2));
  const brief = JSON.parse(fs.readFileSync(opt.brief, "utf8"));
  if (!String(brief.id || "").startsWith("TEST-")) fail("Safety gate: brief.id must start with TEST-.");
  if (!brief.topic || !Array.isArray(brief.facts) || brief.facts.length < 3) fail("Brief needs a topic and at least three closed-book facts.");
  const selectedFacts = opt.limit ? brief.facts.slice(0, opt.limit) : brief.facts;
  if (selectedFacts.length > 12) fail("Safety gate: controlled TEST runs are limited to 12 facts.");
  const out = path.resolve(opt.out || path.join(REDTEAM_ROOT, brief.id));
  const allowedRoot = `${path.resolve(REDTEAM_ROOT)}${path.sep}`;
  if (!`${out}${path.sep}`.startsWith(allowedRoot)) fail("Safety gate: output must stay under state/redteam.");
  fs.mkdirSync(out, { recursive: true });
  const records = [];
  console.log(`LAB: ${selectedFacts.length} fact(s), ${opt.live ? "live" : "mock"} mode, up to ${opt.attempts} attempt(s) each.`);
  for (let i = 0; i < selectedFacts.length; i++) {
    const fact = clean(selectedFacts[i]);
    const trials = [];
    let accepted = null;
    for (let attempt = 0; attempt < opt.attempts; attempt++) {
      let sentence = clean(await candidateFor(fact, i + attempt, brief, opt.live));
      if (sentence && !/[.!?]$/.test(sentence)) sentence += ".";
      const [ok, reason] = sentence ? mechanicalGate(sentence, fact) : [false, "empty model response"];
      const verdict = ok ? (opt.skipJudge ? { pass: true, note: "explicit smoke-test mode: mechanical gate only" } : await judge(fact, sentence, opt.live)) : { pass: false, note: reason };
      const trial = { candidate: sentence || null, accepted: ok && verdict.pass, gate: ok ? verdict.note : reason };
      trials.push(trial);
      if (trial.accepted) { accepted = trial; break; }
    }
    const last = trials.at(-1);
    records.push({ fact, candidate: last.candidate, sentence: accepted?.candidate || null, accepted: Boolean(accepted), gate: accepted?.gate || last.gate, attempts: trials });
  }
  const rejected = records.filter(x => !x.accepted);
  const manifest = { testOnly: true, mode: opt.live ? "live" : "mock", qualityJudge: opt.skipJudge ? "skipped for one-call smoke test" : JUDGE_MODEL, createdAt: new Date().toISOString(), brief: { id: brief.id, topic: brief.topic }, records };
  fs.writeFileSync(path.join(out, "manifest.json"), JSON.stringify(manifest, null, 2));
  if (rejected.length) fail(`Quality gate rejected ${rejected.length}/${records.length} base sentences; no assembled document was created.`);
  const text = assemble(records.map(x => x.sentence));
  fs.writeFileSync(path.join(out, `${brief.id}-fresh-sentences.txt`), text, "utf8");
  console.log(`PASS: ${records.length} base sentences passed before assembly.`);
  console.log(`TEST document: ${path.join(out, `${brief.id}-fresh-sentences.txt`)}`);
}
main().catch(error => { console.error(`LAB ERROR: ${error.message}`); process.exitCode = 1; });

/**
 * TELEGRAM BRIDGE — remote control for pi
 *
 * One Telegram chat = one pi session.
 *   Plain text  -> prompt into the CURRENT session (full tools, skills, memory)
 *   /new        -> spawn a fresh session (new "chat")
 *   /main       -> jump back to the most recent session (your "main chat")
 *   /list       -> list recent sessions
 *   /switch <n> -> jump into session n
 *   /stop       -> abort the running task
 *   /status /current -> info
 *
 * The main chat auto-resumes the most recent pi session on startup,
 * so "the chat that doesn't stop" survives PC restarts.
 */

import { Bot } from "grammy";
import {
    createAgentSessionFromServices,
    createAgentSessionRuntime,
    createAgentSessionServices,
    getAgentDir,
    SessionManager,
} from "@earendil-works/pi-coding-agent";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PERFORM_DIR = path.resolve(__dirname, "..", "..");
const CONFIG_PATH = path.join(__dirname, "config.json");
const STATE_PATH = path.join(__dirname, "state.json");

function loadConfig() {
    if (!fs.existsSync(CONFIG_PATH)) {
        fs.writeFileSync(CONFIG_PATH, JSON.stringify({ token: "PASTE_YOUR_BOT_TOKEN_HERE", allowedUserId: null }, null, 2));
        console.error("No config.json found - created one. Paste your BotFather token into it and run again.");
        process.exit(1);
    }
    const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
    if (!cfg.token || cfg.token === "PASTE_YOUR_BOT_TOKEN_HERE") {
        console.error("config.json has no token. Message @BotFather on Telegram, send /newbot, paste the token into config.json.");
        process.exit(1);
    }
    return cfg;
}

function loadState() {
    try {
        return JSON.parse(fs.readFileSync(STATE_PATH, "utf8"));
    } catch {
        return { chatSessions: {} };
    }
}

const config = loadConfig();
const state = loadState();
function saveState() {
    fs.writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}

// ---------- pi session runtime ----------

const createRuntime = async ({ cwd, sessionManager, sessionStartEvent }) => {
    const services = await createAgentSessionServices({ cwd });
    return {
        ...(await createAgentSessionFromServices({ services, sessionManager, sessionStartEvent })),
        services,
        diagnostics: services.diagnostics,
    };
};

console.log("Starting pi engine (loads skills, extensions, context from PERFORM)...");
const runtime = await createAgentSessionRuntime(createRuntime, {
    cwd: PERFORM_DIR,
    agentDir: getAgentDir(),
    sessionManager: SessionManager.create(PERFORM_DIR),
});

// Live activity feed, reset on every session (re)bind
let activity = { tools: [], text: "" };
let unsubSessionEvents = undefined;

function bindSession() {
    unsubSessionEvents?.();
    const s = runtime.session;
    activity = { tools: [], text: "" };
    unsubSessionEvents = s.subscribe((event) => {
        if (event.type === "tool_execution_start") {
            activity.tools.push(event.toolName);
        } else if (event.type === "message_update" && event.assistantMessageEvent.type === "text_delta") {
            activity.text += event.assistantMessageEvent.delta;
            if (activity.text.length > 6000) activity.text = activity.text.slice(-3000);
        }
    });
    return s;
}

let session = bindSession();

async function resumeMostRecentSession() {
    const sm = SessionManager.continueRecent(PERFORM_DIR);
    const file = sm.getSessionFile();
    if (file) {
        await runtime.switchSession(file);
        session = bindSession();
        console.log("Resumed most recent session:", file);
        return true;
    }
    return false;
}

// ---------- helpers ----------

let busy = false;

function lastAssistantText() {
    const msgs = session.messages;
    for (let i = msgs.length - 1; i >= 0; i--) {
        const m = msgs[i];
        if (m.role !== "assistant") continue;
        const parts = Array.isArray(m.content) ? m.content : [];
        const text = parts.filter((p) => p.type === "text").map((p) => p.text).join("\n").trim();
        if (text) return text;
    }
    return undefined;
}

function chunkText(text, size = 3800) {
    if (text.length <= 4000) return [text];
    const chunks = [];
    let rest = text;
    while (rest.length > 0) {
        if (rest.length <= size) { chunks.push(rest); break; }
        let cut = rest.lastIndexOf("\n", size);
        if (cut < size * 0.5) cut = size;
        chunks.push(rest.slice(0, cut));
        rest = rest.slice(cut);
    }
    return chunks;
}

async function sendLong(api, chatId, text) {
    for (const part of chunkText(text)) {
        await api.sendMessage(chatId, part);
    }
}

function sessionLabel(file) {
    return file ? path.basename(file).replace(/\.jsonl$/, "") : "(fresh, not saved yet)";
}

let ctxApi = null;

// ---------- prompt runner (one at a time) ----------

async function runPrompt(chatId, text) {
    busy = true;
    activity = { tools: [], text: "" };

    let statusMsg = null;
    let lastEdit = 0;
    const statusText = () => {
        const t = activity.tools.slice(-4).join(", ") || "thinking";
        const preview = activity.text.replace(/\s+/g, " ").trim().slice(-120);
        return "working... " + t + (preview ? "\n\n💬 " + preview : "");
    };

    try {
        const sent = await ctxApi.sendMessage(chatId, "🛠 working…");
        statusMsg = sent.message_id;
        const editTimer = setInterval(async () => {
            const now = Date.now();
            if (now - lastEdit < 3500) return;
            lastEdit = now;
            try { await ctxApi.editMessageText(chatId, statusMsg, statusText()); } catch {}
        }, 1500);

        await session.prompt(text);

        clearInterval(editTimer);
        const answer = lastAssistantText() ?? "(done - no text reply)";
        try { await ctxApi.deleteMessage(chatId, statusMsg); } catch {}
        await sendLong(ctxApi, chatId, answer);
        if (session.sessionFile) {
            state.chatSessions[String(chatId)] = session.sessionFile;
            saveState();
        }
    } catch (err) {
        clearInterval(editTimer);
        try { if (statusMsg) await ctxApi.deleteMessage(chatId, statusMsg); } catch {}
        await sendLong(ctxApi, chatId, "⚠️ Error: " + (err?.message ?? String(err)));
    } finally {
        busy = false;
    }
}

// ---------- PRICE — quick expense logger (fast path, no pi needed) ----------

const PRICE_DIR = path.join(PERFORM_DIR, "price");
const PRICE_LEDGER = path.join(PRICE_DIR, "purchases.json");

function readPurchases() {
    try { return JSON.parse(fs.readFileSync(PRICE_LEDGER, "utf8")); } catch { return []; }
}
function writePurchases(list) {
    fs.mkdirSync(PRICE_DIR, { recursive: true });
    fs.writeFileSync(PRICE_LEDGER, JSON.stringify(list, null, 2));
}
function monthTotal(list) {
    const m = new Date().toISOString().slice(0, 7); // "2026-09"
    return list.filter((p) => p.date.startsWith(m));
}
async function handleBuy(text) {
    const m = text.replace(/^\/?\s*(buy|bought)\s+/i, "");
    const num = m.match(/\d+(?:[.,]\d+)?/);
    if (!num) return null; // no number -> not a log, let pi handle it
    const amount = parseFloat(num[0].replace(",", "."));
    const what = m.replace(num[0], "").trim() || "unnamed";
    const list = readPurchases();
    list.push({ date: new Date().toISOString(), amount, what });
    writePurchases(list);
    const month = monthTotal(list);
    const sum = month.reduce((s, p) => s + p.amount, 0);
    return `✅ Logged: ${amount.toFixed(2)} BGN — ${what}\n🗓 This month: ${sum.toFixed(2)} BGN across ${month.length} buys`;
}

// ---------- telegram bot ----------

const bot = new Bot(config.token);
ctxApi = bot.api;

let recentList = [];

function checkOwner(ctx) {
    const id = ctx.from?.id;
    if (config.allowedUserId == null) {
        // First person to touch the bot becomes its owner - then it is locked forever.
        config.allowedUserId = id;
        fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
        console.log("Owner locked to Telegram user " + id);
        return true;
    }
    if (id !== config.allowedUserId) {
        console.log("Rejected message from stranger " + id);
        return false;
    }
    return true;
}

bot.command("start", async (ctx) => {
    if (!checkOwner(ctx)) return ctx.reply("🔒 This bot is private.");
    await ctx.reply(
        "🤖 Bridge online. You are talking to pi on your PC.\n\n" +
        "Just type - it goes into the current session.\n\n" +
        "/new - spawn a fresh session\n" +
        "/main - jump back to your main chat\n" +
        "/list - list sessions\n" +
        "/switch <n> - switch to session n\n" +
        "/stop - abort the current task\n" +
        "/status - engine status\n" +
        "/current - current session file"
    );
});

bot.command("new", async (ctx) => {
    if (!checkOwner(ctx)) return;
    if (busy) return ctx.reply("⏳ I'm still working - /stop first if you want to abandon it.");
    await runtime.newSession();
    session = bindSession();
    delete state.chatSessions[String(ctx.chat.id)];
    saveState();
    await ctx.reply("✨ Fresh session spawned.\n/main jumps back to your main chat anytime.");
});

bot.command("main", async (ctx) => {
    if (!checkOwner(ctx)) return;
    if (busy) return ctx.reply("⏳ I'm still working - /stop first.");
    if (await resumeMostRecentSession()) {
        state.chatSessions[String(ctx.chat.id)] = session.sessionFile;
        saveState();
        await ctx.reply("🏠 Back in your main chat: " + sessionLabel(session.sessionFile));
    } else {
        await ctx.reply("No previous session found - staying in the current one.");
    }
});

bot.command("list", async (ctx) => {
    if (!checkOwner(ctx)) return;
    const want = parseInt(ctx.message?.text?.split(/\s+/)[1] ?? "", 10) || 10;
    const infos = await SessionManager.list(PERFORM_DIR);
    const current = session.sessionFile;
    const take = Math.min(Math.max(want, 1), 50);
    recentList = infos.slice(0, take).map((i) => i.path);
    const lines = recentList.map((p, i) => (i + 1) + ". " + sessionLabel(p) + (p === current ? " <-" : ""));
    await ctx.reply("📚 Recent sessions (from PERFORM):\n\n" + lines.join("\n") + "\n\n/switch <n> to jump. /list 30 for more.");
});
bot.command("switch", async (ctx) => {
    if (!checkOwner(ctx)) return;
    if (busy) return ctx.reply("⏳ I'm still working - /stop first.");
    const n = parseInt(ctx.message?.text?.split(/\s+/)[1] ?? "", 10);
    if (!n || !recentList[n - 1]) return ctx.reply("Send /list first, then /switch <number>.");
    await runtime.switchSession(recentList[n - 1]);
    session = bindSession();
    state.chatSessions[String(ctx.chat.id)] = session.sessionFile;
    saveState();
    await ctx.reply("🔀 Switched to: " + sessionLabel(session.sessionFile));
});

bot.command("stop", async (ctx) => {
    if (!checkOwner(ctx)) return;
    if (!busy) return ctx.reply("Nothing is running.");
    await session.abort();
    await ctx.reply("🛑 Aborted.");
});

bot.command("status", async (ctx) => {
    if (!checkOwner(ctx)) return;
    await ctx.reply(
        "🧠 model: " + (session.model?.label ?? session.model?.id ?? "?") + "\n" +
        "📊 messages in context: " + session.messages.length + "\n" +
        (busy ? "🛠 busy right now" : "💤 idle") + "\n" +
        "📁 session: " + sessionLabel(session.sessionFile)
    );
});

bot.command("current", async (ctx) => {
    if (!checkOwner(ctx)) return;
    await ctx.reply("📁 " + (session.sessionFile ?? "(not saved yet)"));
});

bot.command("price", async (ctx) => {
    if (!checkOwner(ctx)) return;
    const list = readPurchases();
    const month = monthTotal(list);
    if (month.length === 0) return ctx.reply("No buys logged this month yet.");
    const sum = month.reduce((s, p) => s + p.amount, 0);
    const lines = month.map((p) => `${p.date.slice(0, 10)}  ${p.amount.toFixed(2)}  ${p.what}`);
    await ctx.reply(`🗓 This month: ${sum.toFixed(2)} BGN (${month.length} buys)\n\n${lines.join("\n")}`);
});

bot.on("message:text", async (ctx) => {
    if (!checkOwner(ctx)) return;
    const text = ctx.message.text;
    if (text.startsWith("/")) return; // unknown command - ignore

    // PRICE fast path: "buy 25 food" / "bought 12.50 kebab" -> instant log, no pi
    if (/^\/?\s*(buy|bought)\b/i.test(text)) {
        const reply = await handleBuy(text);
        if (reply) return ctx.reply(reply);
        // no number in it -> fall through to pi (e.g. "buying a new laptop soon")
    }
    if (busy) {
        if (session.isStreaming) {
            await session.steer(text);
            return ctx.reply("↩️ Steered into the running task.");
        }
        return ctx.reply("⏳ Still working. Wait, or /stop.");
    }
    await runPrompt(ctx.chat.id, text);
});

bot.catch((err) => {
    console.error("Bot error:", err.error ?? err);
});

// ---------- go ----------

console.log("PERFORM dir: " + PERFORM_DIR);
console.log("Engine ready. Connecting to Telegram (long polling)...");
bot.start({
    onStart: (me) => {
        console.log("✅ Bridge live as @" + me.username + ".");
        console.log("Open Telegram, message the bot once - the first account to do so becomes its owner.");
    },
}).catch((err) => {
    console.error("Telegram connection failed:", err?.message ?? err);
    console.error("Most likely the token in config.json is wrong or expired.");
    console.error("Get a fresh one from @BotFather (/token command) and paste it in, then rerun.");
    process.exit(1);
});

process.on("SIGINT", () => {
    console.log("Shutting down bridge...");
    bot.stop();
    process.exit(0);
});

# Telegram Bridge — Remote Control for pi

Talk to pi from your phone via Telegram. Runs on the PC, long polling (no ports open).

## First-Time Setup (one time only)
1. Telegram: message **@BotFather** -> send `/newbot` -> pick a name -> copy the token.
2. Paste the token into `config.json` (replace PASTE_YOUR_BOT_TOKEN_HERE).
3. Double-click `start-telegram.bat` (or run `node bot.mjs` in this folder).
4. Message the bot once from your Telegram account. **The first account to message it
   becomes the owner — nobody else can ever use it.** (Locked in config.json.)

## Daily Use
- Start `start-telegram.bat`. Leave the console open.
- Phone -> bot chat -> type normally. Same brain as the TUI (PERFORM cwd, all skills).

## Commands
- plain text: prompt into current session (steered into running task if I'm busy)
- `/new` — spawn a fresh session (new chat)
- `/main` — jump back to most recent session (the chat that never stops)
- `/list` — show recent sessions
- `/switch <n>` — jump into session n (after /list)
- `/stop` — abort the running task
- `/status` — model, context size, busy/idle
- `/current` — current session file

## Notes
- Main chat survives PC restarts: on startup it resumes the most recent session.
- "working…" status message shows live tool names + text preview.
- config.json holds the bot token + owner ID (gitignored — never commit).
- state.json remembers chat->session mapping.
- One task at a time. While busy: new texts steer the running task.

## Troubleshooting
- 401 Unauthorized: token wrong/expired -> @BotFather /token -> re-paste.
- No reply: check console window is still open, PC awake.
- Wrong session: /main to go back to main chat.

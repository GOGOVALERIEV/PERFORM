# NOTEBOOKLM AUTO-DRIVE MAP (2026-10-01) — 90% mapped, proven feasible

## What works (proven via CDP drive on George's Google session)
1. CDP attach: Brave with --remote-debugging-port=9222 -> notebooklm.google.com — NO login wall
   (Google session carried; George has existing notebooks)
2. Create new notebook: click "нов бележник" -> /notebook/{id}?addSource=true
3. Add source panel: "Добавяне на източници" -> chooser (Качване/Уебсайтове/Книги/Диск/Копиран текст)
4. "Копиран текст" -> textarea[formcontrolname=copiedText] -> fill works
5. "Вмъкване" -> source processed, summary generated, "1 източник" confirmed
6. Studio -> Презентация card -> customize dialog opens (Формат/Език/Дължина/Източници/Стил)

## The blockers (exactly where automation got stuck)
1. PROMO POPUPS: "Предоставяме ви повече гъвкавост..." dialog + "Ново: interactive reports"
   card + promo overlays intercept pointer events. Close buttons: mat-icon 'close'
   ('Затваряне'/'Затваряне на диалоговия прозорец') — must close via THE DIALOG'S OWN
   close btn, not remove-overlays (removing kills the form too).
2. ANGULAR FORM CONTROLS: mat-select (language) + style textarea are reactive forms.
   Native-setter + input-event filled the textarea, but the select needs
   Playwright select_option or real mousedown+click. JS clicks don't register.
   -> "Генериране сега" clicks didn't start generation (form state stayed invalid?)
3. Deck generation status: no deck card appeared in Studio after clicks. AI usage bar
   advanced (quota consumed). Either generations failed (invalid form) or deck card
   renders only after full server-side completion + page refresh.

## Next session checklist (finish in ~1 focused hour)
- Close promo dialog via its own close btn (aria 'Затваряне на диалоговия прозорец')
- Language: real-click mat-select (force=True) -> real-click option 'български'
  (worked once: mat-select showed 'български')
- Style textarea: locator.fill (worked)
- Verify Генериране сега is ENABLED (check disabled attr) before clicking
- After generate: poll Studio for deck card; if card still opens customize dialog,
  try page reload — generated decks should render as cards
- Export: deck -> Сваляне (PDF, slides-as-images per video-4 knowledge)
- Then wire as Presentation Bot auto-mode: inputs = topic + specifics + optional text
  + optional images (images -> pptx path, no images -> NotebookLM path)

## Costs learned
- Each generation attempt consumes NotebookLM/Gemini quota (AI usage bar visible)
- Limits refresh every 5 hours (per their own dialog: "Лимитите се опресняват на всеки 5 часа")

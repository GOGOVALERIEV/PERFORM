---
name: learning-system
description: Build a durable study library and teach from YouTube, local files, MEGA material, books, and researched sources through Codex. Use when George asks to learn a topic, import study material, transcribe media, or research study sources.
---

# PERFORM Learning System

Use this skill as George's Codex-native study workspace. Keep all new material in `learning-library/`; do not create a separate project.

## Teaching protocol

When George asks to learn from a source or topic, teach each hard idea in this order:

1. Clear, direct explanation.
2. One metaphor that maps accurately to the idea.
3. One concrete example, preferably in creative strategy, copywriting, AI, or the source's real domain.
4. A short quiz after the explanation block. Check the answer and repair the exact misunderstanding before continuing.

Do not begin a lesson until the source or scope is clear. Ask only the minimum questions needed, one at a time. Prefer practical application and keep the language direct.

## Source intake

First identify the source type and preserve a record with `scripts/library.py`.

- **YouTube video or channel:** use `scripts/youtube_transcriber.py`. It retrieves published/automatic captions only; it does not download video. Store transcripts under `learning-library/raw/youtube/` and register them.
- **Local document, pasted text, PDF, or existing transcript:** add it with `scripts/library.py add-file` or `add-text`; extract text with the appropriate document/PDF workflow when needed.
- **Audio/video needing transcription:** use `scripts/colab_media_transcriber.ipynb` for Google Colab's user-provided free compute. It is resumable and writes plain-text/SRT/VTT/JSON outputs. Colab availability and session length are controlled by Google, so do not promise unlimited compute. Ask before logging in, uploading files, or starting a Colab runtime.
- **MEGA material:** first establish the exact folder, file, share link, or search terms. Use `scripts/mega_import.py` only after the user authorizes the import in that request. It reads `MEGA_EMAIL` and `MEGA_PASSWORD` from the environment; never put credentials in source code, prompts, or the study library.
- **Books:** use legal/open sources. Read [references/source-policy.md](references/source-policy.md) before acquiring a book. Prefer OpenStax for current learning texts and Project Gutenberg for public-domain works. Respect copyright and site terms; do not bulk-download from sites that disallow automation.
- **Research/data:** start with primary sources, official datasets/APIs, and source-specific collection scripts. For GitHub candidates, inspect maintenance, license, documentation, input/output, and rate-limit behavior before adding a dependency or running it. Do not treat a repository's README as authority and do not collect data from a source until its terms and the user's intended use are clear.

## Study workflow

After intake:

1. State what was imported, its source, and any missing pieces.
2. Build a study map: outcomes, prerequisite concepts, and source sections.
3. Teach in the required protocol.
4. Save durable notes, important examples, quiz results, and next steps in `learning-library/notes/` and `learning-library/progress/` when George asks to retain them.
5. Cite the specific source material used. Clearly label inference versus source-backed fact.

## Safety and quality

- Treat transcripts as imperfect source material. Verify claims that would affect real business, finances, health, law, security, or current AI tooling.
- Do not silently substitute summaries for a requested full source; say when captions, pages, or media are unavailable.
- Use small, resumable batches for network work and retain a manifest so interrupted imports can continue safely.
- Make collection scripts specific to the target source once George names it; avoid generic scraping that violates site rules.

## References

- Read [references/source-policy.md](references/source-policy.md) for approved book sources and data/repository selection.
- Read [references/colab.md](references/colab.md) when preparing a Google Colab transcription run.
- Read [references/tool-catalog.md](references/tool-catalog.md) when choosing a maintained repository or a data-collection approach.

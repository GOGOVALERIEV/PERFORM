# Tool catalog

These are candidates, not automatic dependencies. Inspect their current license, release notes, and source terms before use.

| Need | Candidate | Use it for |
|---|---|---|
| YouTube captions and metadata | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Caption-first YouTube intake. Keep it updated and collect only the material requested. |
| Audio/video transcription | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Fast Whisper transcription in Google Colab or locally. The Colab notebook in this skill uses it. |
| MEGA automation | [MEGAcmd](https://github.com/meganz/MEGAcmd) | Official command-line fallback when the lightweight Python client cannot handle a requested MEGA operation. |
| Extracting the main text from permitted web pages | [Trafilatura](https://github.com/adbar/trafilatura) | Article extraction after confirming the target site's terms and the user's purpose. It is not a license to crawl a website. |

For a new data source, choose an official API or published dataset first. If none exists, create a narrowly scoped collector in `scripts/` with:

- exact target and permitted request rate;
- provenance fields (`source_url`, accessed timestamp, query/filters);
- deduplication and resumable output;
- no embedded credentials and no broad crawl by default.

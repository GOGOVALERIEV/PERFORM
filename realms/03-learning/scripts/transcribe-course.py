"""
Course Transcriber + Note Maker
===============================
Transcribes all videos in a folder using Whisper (local, free),
then generates notes using Gemini API (free).

Usage:
    python scripts/transcribe-course.py

Output:
    D:/course/transcripts/  — full text of every video
    D:/course/notes/        — key points and summaries
"""

import os
import sys
import json
import time
import pathlib
import subprocess
import requests

# Add ffmpeg to PATH so Whisper can find it
os.environ["PATH"] = r"C:\Users\User\ffmpeg" + os.pathsep + os.environ.get("PATH", "")

# === SETTINGS ===
COURSE_DIR = pathlib.Path("D:/course")
TRANSCRIPTS_DIR = COURSE_DIR / "transcripts"
NOTES_DIR = COURSE_DIR / "notes"
FFMPEG_PATH = r"C:\Users\User\ffmpeg\ffmpeg.exe"
FFPROBE_PATH = r"C:\Users\User\ffmpeg\ffprobe.exe"

# Gemini API — read key from config/.env
def _get_gemini_key():
    env_path = r"C:\Users\User\Desktop\PERFORM\config\.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    raise ValueError("GEMINI_API_KEY not found in PERFORM/config/.env")

GEMINI_API_KEY = _get_gemini_key()
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"

# Whisper model — "base" is a good balance of speed vs accuracy
# Options: tiny (fastest, least accurate), base, small, medium, large (slowest, most accurate)
WHISPER_MODEL = "medium"


def get_video_files(course_dir):
    """Find all mp4 files and sort them by folder structure."""
    videos = sorted(course_dir.rglob("*.mp4"))
    # Filter out any junk files
    videos = [v for v in videos if v.stat().st_size > 1_000_000]  # skip files under 1MB
    return videos


def make_safe_name(video_path, course_dir):
    """Turn a video path into a safe filename for the transcript."""
    rel = video_path.relative_to(course_dir)
    # Get the important parts of the path (section + video name)
    parts = rel.parts
    # Skip the top-level course folder name if it exists
    if len(parts) > 1:
        # Find the section parts (e.g., "1. Ecom masterclass/3Market Research/2.mp4")
        clean_parts = []
        for p in parts:
            # Remove special characters that cause file path issues
            clean = p.replace("–", "-").replace("—", "-")
            clean = "".join(c for c in clean if c.isalnum() or c in " -_.")
            clean = clean.strip()
            if clean:
                clean_parts.append(clean)
        return "_".join(clean_parts).replace(".mp4", "")
    return video_path.stem


def extract_audio(video_path, audio_path):
    """Extract audio from video as WAV file for Whisper."""
    print(f"    Extracting audio...")
    try:
        subprocess.run(
            [FFMPEG_PATH, "-i", str(video_path), "-ar", "16000", "-ac", "1",
             "-f", "wav", "-y", str(audio_path)],
            capture_output=True, timeout=300
        )
        return audio_path.exists()
    except Exception as e:
        print(f"    ERROR extracting audio: {e}")
        return False


def transcribe_audio(audio_path):
    """Transcribe audio using Whisper."""
    print(f"    Transcribing with Whisper ({WHISPER_MODEL} model)...")
    try:
        import whisper
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(str(audio_path), language="en", fp16=False)
        return result["text"]
    except Exception as e:
        print(f"    ERROR transcribing: {e}")
        return None


def generate_notes(transcript_text, video_name):
    """Use Gemini to generate notes from a transcript."""
    print(f"    Generating notes with Gemini...")

    # Trim transcript if it's too long for Gemini (keep under 30k chars)
    if len(transcript_text) > 30000:
        transcript_text = transcript_text[:30000] + "\n\n[TRANSCRIPT TRIMMED — original was longer]"

    prompt = f"""You are a note-taking assistant. Read this video transcript and create clear, actionable study notes.

VIDEO: {video_name}

TRANSCRIPT:
{transcript_text}

Create notes with this structure:
## {video_name}

### Key Points
- Bullet points of the most important ideas (5-15 points)

### Action Items
- Specific things to do or apply (if any)

### Important Quotes or Phrases
- Any memorable lines or phrases worth remembering

### Summary
- 2-3 sentence summary of the entire video

Write in plain English. Be specific — no vague fluff. If the video teaches a process, list the steps."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048,
        }
    }

    # Retry up to 5 times if rate limited
    for attempt in range(5):
        try:
            resp = requests.post(GEMINI_URL, json=payload, timeout=120)
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)  # 30s, 60s, 90s, 120s, 150s
                print(f"    Rate limited — waiting {wait}s (attempt {attempt + 1}/5)")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.HTTPError as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                print(f"    Rate limited — waiting {wait}s (attempt {attempt + 1}/5)")
                time.sleep(wait)
                continue
            print(f"    ERROR generating notes: {e}")
            return None
        except Exception as e:
            print(f"    ERROR generating notes: {e}")
            return None
    print(f"    FAILED after 5 retries — skipping notes (transcript still saved)")
    return None


def main():
    print("=" * 60)
    print("  COURSE TRANSCRIBER + NOTE MAKER")
    print("=" * 60)

    # Create output folders
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    # Find all videos
    videos = get_video_files(COURSE_DIR)
    print(f"\nFound {len(videos)} videos to process.\n")

    if not videos:
        print("ERROR: No video files found in", COURSE_DIR)
        return

    # Track progress
    total = len(videos)
    completed = 0
    failed = 0
    skipped = 0

    # Load Whisper model once (saves time)
    print("Loading Whisper model (first time downloads ~140MB)...")
    import whisper
    model = whisper.load_model(WHISPER_MODEL)
    print("Model loaded.\n")

    for i, video in enumerate(videos):
        safe_name = make_safe_name(video, COURSE_DIR)
        transcript_file = TRANSCRIPTS_DIR / f"{safe_name}.txt"
        notes_file = NOTES_DIR / f"{safe_name}.md"

        print(f"[{i+1}/{total}] {safe_name}")

        # Skip if already done
        if transcript_file.exists() and notes_file.exists():
            print(f"    Already done — skipping")
            skipped += 1
            continue

        # Step 1: Extract audio
        audio_path = TRANSCRIPTS_DIR / f"_temp_audio.wav"
        if not extract_audio(video, audio_path):
            print(f"    FAILED — could not extract audio")
            failed += 1
            continue

        # Step 2: Transcribe
        if transcript_file.exists():
            print(f"    Transcript exists — loading...")
            transcript = transcript_file.read_text(encoding="utf-8")
        else:
            try:
                print(f"    Transcribing with Whisper...")
                result = model.transcribe(str(audio_path), language="en", fp16=False)
                transcript = result["text"]
                transcript_file.write_text(transcript, encoding="utf-8")
                print(f"    Transcript saved ({len(transcript)} chars)")
            except Exception as e:
                print(f"    FAILED transcription: {e}")
                failed += 1
                # Clean up temp audio
                if audio_path.exists():
                    audio_path.unlink()
                continue

        # Clean up temp audio
        if audio_path.exists():
            audio_path.unlink()

        # Step 3: Generate notes with Gemini
        if not notes_file.exists():
            notes = generate_notes(transcript, safe_name)
            if notes:
                notes_file.write_text(notes, encoding="utf-8")
                print(f"    Notes saved")
            else:
                print(f"    WARNING — notes generation failed (transcript still saved)")
                # Wait a bit in case of rate limit
                time.sleep(10)

        completed += 1
        print(f"    DONE ({completed}/{total - skipped})\n")

        # Small delay between Gemini calls to avoid rate limits
        time.sleep(3)

    # Final report
    print("\n" + "=" * 60)
    print("  FINISHED")
    print("=" * 60)
    print(f"  Total videos:  {total}")
    print(f"  Completed:     {completed}")
    print(f"  Skipped:       {skipped}")
    print(f"  Failed:        {failed}")
    print(f"\n  Transcripts:   {TRANSCRIPTS_DIR}")
    print(f"  Notes:         {NOTES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

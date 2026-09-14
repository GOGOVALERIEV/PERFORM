"""
youtube_transcript_io.py -- Get YouTube transcripts via youtube-transcript.io

HOW IT WORKS:
  1. Creates an anonymous Firebase auth token (their site uses Firebase Auth)
  2. Calls their /api/transcripts/v2 endpoint with the token
  3. Returns transcript with timestamps, title, author, etc.

WHY THIS EXISTS:
  - youtube-transcript-api (Python pip package) gets blocked by YouTube
  - This routes through youtube-transcript.io's servers (their IPs, not yours)
  - No YouTube Data API key needed. No quota limits.
  - Free. No account needed.

RATE LIMITS:
  - Cloudflare protects the site. Don't call it 100x in a row.
  - If you get 429 errors, wait a minute and try again.
  - Each call creates a new anonymous Firebase user (cheap for them, but be nice).

USAGE:
  from youtube_transcript_io import get_transcript

  result = get_transcript("dQw4w9WgXcQ")
  print(result["title"])       # "Rick Astley - Never Gonna Give You Up ..."
  print(result["text"])        # Full transcript as plain text
  print(result["tracks"])      # List of tracks with timestamped segments

  # Each track has:
  #   track["language"]              = "English (auto-generated)"
  #   track["transcript"]           = list of segments
  #   track["transcript"][0]["text"] = "we're no strangers to"
  #   track["transcript"][0]["start"]= "18.8"  (seconds)
  #   track["transcript"][0]["dur"]  = "7.239" (seconds)

DEPENDENCIES:
  pip install requests
"""

import requests
import json
import sys

# Read Firebase API key from config/.env (never hardcode in public repo)
def _get_firebase_key():
    env_path = r"C:\Users\User\Desktop\PERFORM\config\.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("FIREBASE_API_KEY="):
                    return line.split("=", 1)[1].strip()
    _key = os.environ.get("FIREBASE_API_KEY", "")
    if not _key:
        raise ValueError("FIREBASE_API_KEY not found in PERFORM/config/.env")
    return _key

_FIREBASE_API_KEY = _get_firebase_key()


def get_transcript(video_id: str) -> dict:
    """
    Fetch a YouTube transcript through youtube-transcript.io's API.

    Args:
        video_id: YouTube video ID (the part after v= in the URL)
                  Example: "dQw4w9WgXcQ" from https://www.youtube.com/watch?v=dQw4w9WgXcQ

    Returns:
        dict with keys:
            - text (str): Full transcript as plain text (no timestamps)
            - title (str): Video title
            - author (str): Channel name
            - id (str): Video ID
            - tracks (list): List of transcript tracks, each with:
                - language (str): e.g. "English (auto-generated)"
                - transcript (list): List of {text, start, dur} dicts
            - languages (list): Available languages [{label, languageCode}]
            - channelId (str): YouTube channel ID
            - keywords (list): Video keywords/tags

    Raises:
        requests.HTTPError: If any HTTP request fails
        Exception: If the video has no transcript or the ID is invalid
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) "
                      "Gecko/20100101 Firefox/139.0"
    })

    # Step 1: Get anonymous Firebase auth token
    auth_url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        f"?key={_FIREBASE_API_KEY}"
    )
    auth_resp = session.post(
        auth_url,
        json={"returnSecureToken": True},
        headers={
            "Content-Type": "application/json",
            "X-Client-Version": "Firefox/JsCore/10.14.1/FirebaseCore-web",
        },
        timeout=15,
    )
    auth_resp.raise_for_status()
    id_token = auth_resp.json()["idToken"]

    # Step 2: Fetch transcript
    resp = session.post(
        "https://www.youtube-transcript.io/api/transcripts/v2",
        json={"ids": [video_id], "source": "singleVideoUI"},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {id_token}",
            "x-request-channel": "9527-c",
        },
        timeout=30,
    )
    resp.raise_for_status()

    data = resp.json()

    if data.get("failed"):
        raise Exception(f"Failed to get transcript: {data['failed']}")

    if not data.get("success"):
        raise Exception("No transcript returned (video may not have captions)")

    return data["success"][0]


def get_transcript_text(video_id: str) -> str:
    """Convenience: get just the plain text transcript (no timestamps)."""
    return get_transcript(video_id)["text"]


def get_transcript_segments(video_id: str, language_index: int = 0) -> list:
    """
    Convenience: get timestamped segments as a list of dicts.

    Each dict has: text (str), start (float), dur (float)
    """
    result = get_transcript(video_id)
    tracks = result.get("tracks", [])
    if not tracks:
        raise Exception("No transcript tracks available")
    if language_index >= len(tracks):
        raise Exception(
            f"Language index {language_index} out of range "
            f"(only {len(tracks)} tracks available)"
        )
    segments = tracks[language_index].get("transcript", [])
    return [
        {
            "text": seg["text"],
            "start": float(seg["start"]),
            "dur": float(seg["dur"]),
        }
        for seg in segments
    ]


# --- CLI usage ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript_io.py VIDEO_ID")
        print("Example: python youtube_transcript_io.py dQw4w9WgXcQ")
        sys.exit(1)

    vid = sys.argv[1]
    # Strip full URL if given
    if "youtube.com" in vid or "youtu.be" in vid:
        if "v=" in vid:
            vid = vid.split("v=")[1].split("&")[0]
        elif "youtu.be/" in vid:
            vid = vid.split("youtu.be/")[1].split("?")[0]

    print(f"Fetching transcript for: {vid}")
    print()

    result = get_transcript(vid)

    print(f"Title:     {result['title']}")
    print(f"Author:    {result['author']}")
    print(f"Languages: {[l['label'] for l in result.get('languages', [])]}")
    print()

    tracks = result.get("tracks", [])
    if tracks:
        segments = tracks[0].get("transcript", [])
        print(f"Segments: {len(segments)}")
        print()
        for seg in segments:
            start = float(seg["start"])
            mins = int(start // 60)
            secs = start % 60
            print(f"  [{mins}:{secs:05.2f}] {seg['text']}")
    else:
        print("Plain text:")
        print(result["text"])

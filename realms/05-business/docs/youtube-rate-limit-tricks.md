# YouTube Rate Limit Bypass Tricks

Reference for future projects that need to fetch YouTube data (transcripts, subtitles, metadata) without getting IP-blocked.

## What YouTube Blocks
- **Subtitle/caption downloads** (timedtext API) get blocked after ~13 rapid requests
- **Video metadata** (innertube player API) stays accessible longer
- **Page loads** (watch pages, mobile site) almost never blocked
- Block is IP-level, lasts 1-24 hours typically

## Tricks Tried (March 2026)

### 1. ANDROID_VR Innertube Client (PATCHED - doesn't work anymore)
Made requests look like they came from a VR headset. YouTube used to give VR clients higher rate limits.
```python
import youtube_transcript_api._transcripts as _t
_t.INNERTUBE_CONTEXT = {
    'client': {
        'clientName': 'ANDROID_VR',
        'clientVersion': '1.57.29',
        'androidSdkVersion': 34,
    }
}
```
**Status**: YouTube patched this. No longer bypasses rate limits.

### 2. Browser Cookies via yt-dlp (BLOCKED by Brave encryption)
Logged-in users get higher rate limits. yt-dlp can load cookies from browsers.
```python
ydl_opts = {'cookiesfrombrowser': ('brave',)}
# or
ydl_opts = {'cookiefile': 'path/to/cookies.txt'}
```
**Status**: Brave/Chrome v127+ uses DPAPI App Bound Encryption. yt-dlp can't decrypt.
See: https://github.com/yt-dlp/yt-dlp/issues/10927
**Workaround**: Use a browser extension like "Get cookies.txt LOCALLY" to export manually.

### 3. Mobile Site + Signed URLs (WORKS for page, NOT for captions)
YouTube mobile site (m.youtube.com) loads fine even when blocked. Caption URLs are embedded in the page HTML inside `ytInitialPlayerResponse`.
```python
import requests, json, re
r = requests.get('https://m.youtube.com/watch?v=VIDEO_ID', headers={
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36'
})
match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', r.text)
player = json.loads(match.group(1))
tracks = player['captions']['playerCaptionsTracklistRenderer']['captionTracks']
base_url = 'https://www.youtube.com' + tracks[0]['baseUrl']
```
**Status**: Extracts signed caption URLs, but downloading them still hits 429 when IP-blocked.

### 4. Multiple Innertube Clients (ALL return 0 tracks when blocked)
Tried: WEB, ANDROID, IOS, MWEB, TVHTML5_SIMPLY_EMBEDDED_PLAYER
```python
payload = {
    'context': {'client': {'clientName': 'ANDROID', 'clientVersion': '19.09.37'}},
    'videoId': 'VIDEO_ID'
}
r = requests.post(f'https://www.youtube.com/youtubei/v1/player?key={api_key}', json=payload)
```
**Status**: When IP-blocked, all clients return 0 caption tracks.

### 5. Different User-Agent Headers (DOESN'T bypass block)
Tried browser UA, mobile UA, etc. Block is IP-level, not UA-level.

### 6. yt-dlp Subtitle Download (SAME block as everything else)
yt-dlp's built-in subtitle downloader hits the same timedtext endpoint.
```python
ydl_opts = {
    'skip_download': True,
    'writeautomaticsub': True,
    'writesubtitles': True,
    'subtitleslangs': ['en'],
    'subtitlesformat': 'vtt',
}
```
**Status**: Gets 429 when IP-blocked. Works fine when not blocked.

## What ACTUALLY Works

### A. Change IP (BEST fix when blocked)
- **Restart router/modem** — most ISPs assign new IP on reconnect
- **Mobile hotspot** — different IP from phone carrier
- **VPN** — routes through different IP

### B. Prevention (don't get blocked in the first place)
- **8-13 second delays** between subtitle requests (randomized)
- **Batch pauses** — 60 second break every 10 videos
- **Resume capability** — script skips already-downloaded files, so you can stop and restart
- **Date filtering** — only process recent videos, don't scan entire channels

### C. yt-dlp for Metadata (WORKS even when blocked)
Video metadata (title, date, duration, caption URLs) can be fetched even when subtitle downloads are blocked.
```python
ydl_opts = {'quiet': True, 'skip_download': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    # This works — you get title, date, duration, subtitle URLs
    # But downloading from those URLs will fail if blocked
```

### D. Cookies (if you can export them)
Export cookies manually with a browser extension, save as cookies.txt, pass to yt-dlp:
```python
ydl_opts = {'cookiefile': 'path/to/cookies.txt'}
```

## Key Lesson
YouTube rate limiting is **IP-level on the timedtext API endpoint**. No client spoofing, header changes, or signed URLs bypass it. The only real fixes are: change IP, use cookies for higher limits, or wait it out.

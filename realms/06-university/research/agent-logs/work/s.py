import sys, re, html, urllib.parse, subprocess, time

q = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
url = "https://search.brave.com/search?q=" + urllib.parse.quote(q)
out = subprocess.run(["curl", "-s", "--max-time", "30", url, "-A",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "-H", "Accept-Language: en-US,en;q=0.9"], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
# Brave results: links
links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>', out)
seen = []
for l in links:
    if any(b in l for b in ["search.brave.com", "brave.com/", "imgs.search", "favicon", "youtube.com/results"]):
        continue
    if l not in seen:
        seen.append(l)
# snippets: try to get text blocks near results
txt = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', out, flags=re.S)
txt = html.unescape(re.sub(r'<[^>]+>', ' ', txt))
txt = re.sub(r'\s+', ' ', txt)
print(f"### {q}  ({len(seen)} urls)")
for l in seen[:n]:
    print("  " + l)
    # find snippet: text after domain mention
    dom = re.sub(r'https?://(www\.)?', '', l).split('/')[0]
    idx = txt.find(dom.split('.')[0] if '.' in dom else dom)
    if idx > 0:
        print("    »" + txt[idx:idx+180].strip())

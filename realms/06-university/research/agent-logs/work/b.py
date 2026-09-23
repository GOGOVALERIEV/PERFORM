import sys, re, html, urllib.parse, subprocess

q = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
url = "https://www.bing.com/search?format=rss&count=30&q=" + urllib.parse.quote(q)
out = subprocess.run(["curl", "-s", "--max-time", "25", url, "-A",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0"],
    capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
items = re.findall(r'<item><title>(.*?)</title><link>(.*?)</link><description>(.*?)</description>', out, re.S)
print(f"### {q}  ({len(items)})")
for ti, li, de in items[:n]:
    print("T:", html.unescape(ti)[:130])
    print("L:", html.unescape(li)[:150])
    d = html.unescape(re.sub(r'<[^>]+>', '', de)).replace('\n', ' ')[:220]
    print("D:", d)
    print("-")

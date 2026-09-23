import urllib.parse
from common import get
for q in ["site:olx.bg thinkpad", "site:olx.bg dell latitude"]:
    r = get("https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&count=30", timeout=30)
    fn = "bing_" + q.split()[-1].replace(":", "") + ".html"
    open(fn, "w", encoding="utf-8").write(r.text)
    print(fn, r.status_code, len(r.text))
    print("olx links:", r.text.count("olx.bg"))
    print("ck/a wrapped:", r.text.count("bing.com/ck/a"))

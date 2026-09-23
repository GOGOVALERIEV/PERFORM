import requests, re, sys
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Accept-Language": "bg,en;q=0.8"}
def get(url, timeout=30, **kw):
    r = requests.get(url, headers=UA, timeout=timeout, **kw)
    return r
def jina(url, timeout=60):
    return get("https://r.jina.ai/" + url, timeout=timeout)
def ddg(query, timeout=30):
    r = requests.post("https://html.duckduckgo.com/html/", data={"q": query}, headers=UA, timeout=timeout)
    links = re.findall(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S)
    out = []
    for href, txt in links[:12]:
        txt = re.sub(r"<[^>]+>", "", txt).strip()
        out.append((href, txt))
    return out
def budget_bgn(eur=300):
    return eur * 1.95583

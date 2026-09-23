# dsearch.py — DDG HTML + Bing RSS search helper
import urllib.request, urllib.parse, re, sys, html as htmllib, xml.etree.ElementTree as ET

UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}

def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8','ignore')

def ddg(q, n=8):
    try:
        body = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q))
    except Exception as e:
        return [('ERR', str(e), '')]
    out = []
    # result blocks: <a rel="nofollow" class="result__a" href="...">title</a> ... class="result__snippet">...
    titles = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
    snips = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', body, re.S)
    for i, (u, t) in enumerate(titles[:n]):
        sn = htmllib.unescape(re.sub('<[^>]+>','', snips[i])) if i < len(snips) else ''
        out.append((htmllib.unescape(re.sub('<[^>]+>','', t)).strip(), htmllib.unescape(u), sn.strip()))
    if not out:
        # check for anomaly / challenge
        if 'anomaly' in body.lower() or 'challenge' in body.lower() or 'captcha' in body.lower():
            return [('BLOCKED', 'ddg challenge', '')]
    return out

def bing(q, n=8):
    try:
        body = get('https://www.bing.com/search?q=' + urllib.parse.quote(q) + '&format=rss')
    except Exception as e:
        return [('ERR', str(e), '')]
    out = []
    for m in re.finditer(r'<item>(.*?)</item>', body, re.S):
        item = m.group(1)
        t = re.search(r'<title>(.*?)</title>', item, re.S)
        l = re.search(r'<link>(.*?)</link>', item, re.S)
        d = re.search(r'<description>(.*?)</description>', item, re.S)
        out.append((htmllib.unescape(t.group(1)) if t else '', htmllib.unescape(l.group(1)) if l else '', htmllib.unescape(d.group(1)) if d else ''))
    return out[:n]

if __name__ == '__main__':
    engine, q = sys.argv[1], ' '.join(sys.argv[2:])
    res = ddg(q) if engine == 'ddg' else bing(q)
    for t, u, s in res:
        print('T:', t[:120])
        print('U:', u[:200])
        print('S:', s[:220].replace('\n',' '))
        print('---')
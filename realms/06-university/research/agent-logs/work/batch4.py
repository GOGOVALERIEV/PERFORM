import urllib.request, os, time
UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
SITES = [
 ('twaingpt','https://twaingpt.ai/'),
 ('verva','https://verva.com/ai-humanizer'),
 ('netus','https://netus.ai/writer/bypass-ai-detection'),
 ('rewriteai','https://rewriteai.com/free-ai-humanizer'),
 ('cleverhumanizer','https://cleverhumanizer.ai/'),
 ('humanifyer','https://www.humanifyer.com/'),
]
def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    r = urllib.request.urlopen(req, timeout=timeout)
    return r.status, r.url, r.read().decode('utf-8','ignore')
os.makedirs('sites', exist_ok=True)
for name, url in SITES:
    out = f'sites/{name}.html'
    try:
        s, final, body = get(url)
        open(out, 'w', encoding='utf-8').write(f'URL: {final}\nSTATUS: {s}\n\n' + body)
        print(f'OK {s:3} {name:18} {len(body):7} {final[:70]}')
    except Exception as e:
        print(f'ERR {name:18} {str(e)[:90]}')
    time.sleep(1)
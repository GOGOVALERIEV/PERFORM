# batch.py — fetch many sites sequentially, save to sites/<name>.html
import urllib.request, sys, os, time, re

UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

SITES = [
 ('undetectable','https://www.undetectable.ai/'),
 ('humbot','https://www.humbot.ai/'),
 ('phrasly','https://www.phrasly.ai/'),
 ('hix-bypass','https://hix.ai/bypass'),
 ('hix-main','https://hix.ai/'),
 ('bypassgpt','https://bypassgpt.ai/'),
 ('humanizeai','https://www.humanizeai.io/'),
 ('writehuman','https://www.writehuman.com/'),
 ('stealthgpt','https://stealthgpt.ai/'),
 ('rewritify','https://www.rewritify.ai/'),
 ('grubby','https://www.grubby.ai/'),
 ('gpthumanizer','https://gpthumanizer.io/'),
 ('upass','https://upass.ai/'),
 ('uncheckai','https://uncheck.ai/'),
 ('writehybrid','https://www.writehybrid.com/'),
 ('realtouch','https://www.realtouchai.com/'),
 ('studyagent','https://www.studyagent.ai/'),
 ('thehumanizer','https://www.thehumanizer.ai/'),
]

def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    r = urllib.request.urlopen(req, timeout=timeout)
    return r.status, r.url, r.read().decode('utf-8','ignore')

os.makedirs('sites', exist_ok=True)
for name, url in SITES:
    out = f'sites/{name}.html'
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f'SKIP {name}')
        continue
    try:
        s, final, body = get(url)
        open(out, 'w', encoding='utf-8').write(f'URL: {final}\nSTATUS: {s}\n\n' + body)
        print(f'OK {s:3} {name:14} {len(body):7} {final[:60]}')
    except Exception as e:
        print(f'ERR {name:14} {str(e)[:90]}')
    time.sleep(1)
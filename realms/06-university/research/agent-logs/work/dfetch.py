# dfetch.py — fetch a URL and save to file
import urllib.request, sys, re

UA = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    r = urllib.request.urlopen(req, timeout=timeout)
    return r.status, r.url, r.read().decode('utf-8','ignore')

if __name__ == '__main__':
    url, out = sys.argv[1], sys.argv[2]
    try:
        s, final, body = get(url)
        open(out, 'w', encoding='utf-8').write('URL: '+final+'\nSTATUS: '+str(s)+'\n\n'+body)
        print('OK', s, '->', out, len(body), 'bytes')
    except Exception as e:
        print('ERR', str(e))
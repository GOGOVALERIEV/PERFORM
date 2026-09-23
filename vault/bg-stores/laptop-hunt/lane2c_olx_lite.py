"""LANE 2c: OLX last attempt - DDG lite for listing URLs + one direct fetch test."""
import re, urllib.parse
from common import get
print("== DDG lite ==")
try:
    r = get("https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote("site:olx.bg thinkpad лаптоп"), timeout=30)
    print("ddg-lite:", r.status_code, "len", len(r.text))
    links = re.findall(r'href="([^"]+)"', r.text)
    olx = [l for l in links if "olx.bg" in l]
    for l in olx[:15]: print("  ", l[:130])
except Exception as e:
    print("ERR", e)
print("\n== direct fetch of OLX search page ==")
try:
    r = get("https://www.olx.bg/ads/q-lenovo-thinkpad/", timeout=25)
    print(r.status_code, len(r.text), r.text[:200].replace("\n", " "))
except Exception as e:
    print("ERR", str(e)[:100])

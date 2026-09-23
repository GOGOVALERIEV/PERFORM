"""Agent E — arXiv search for AI-text evasion papers with code."""
import urllib.request, urllib.parse, re, json, time

OUT = r"C:/Users/User/Desktop/PERFORM/realms/06-university/research/test-runs"

QUERIES = [
    'all:"paraphrasing evades detectors"',
    'all:"recursive paraphrasing" AND all:"AI generated text"',
    'all:"evade AI-text detection"',
    'all:"translation" AND all:"AI-generated text detection"',
    'all:"perplexity" AND all:"burstiness" AND all:detection',
    'all:"detectGPT" AND all:evasion',
    'all:"TempParaphraser"',
    'all:"attacking" AND all:"AI text detectors"',
    'all:"bypassing" AND all:"AI content detection"',
    'all:"watermark" AND all:"paraphrase" AND all:evade',
]

def arxiv(q, max_results=8):
    base = "http://export.arxiv.org/api/query?"
    params = {"search_query": q, "max_results": max_results, "sortBy": "submittedDate", "sortOrder": "descending"}
    url = base + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent-E"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode()

def parse(xml):
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    out = []
    for e in entries:
        title = re.search(r"<title>(.*?)</title>", e, re.S)
        idm = re.search(r"<id>(.*?)</id>", e, re.S)
        summ = re.search(r"<summary>(.*?)</summary>", e, re.S)
        pub = re.search(r"<published>(.*?)</published>", e, re.S)
        authors = re.findall(r"<name>(.*?)</name>", e)
        out.append({
            "title": re.sub(r"\s+", " ", title.group(1)).strip(),
            "id": idm.group(1).strip(),
            "published": pub.group(1)[:10] if pub else None,
            "authors": authors[:6],
            "summary": re.sub(r"\s+", " ", summ.group(1)).strip()[:500] if summ else "",
        })
    return out

results = {}
for q in QUERIES:
    try:
        xml = arxiv(q)
        results[q] = parse(xml)
        print(f"[OK] {q}: {len(results[q])} results")
        for r in results[q][:3]:
            print(f"      {r['published']} {r['title'][:90]}")
    except Exception as e:
        results[q] = {"error": str(e)}
        print(f"[ERR] {q}: {e}")
    time.sleep(3)

with open(OUT + "/agentE_arxiv.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("Saved.")
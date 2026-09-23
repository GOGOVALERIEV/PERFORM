"""Agent E — arXiv searches, quote-free queries."""
import urllib.request, urllib.parse, re, json, time

OUT = r"C:/Users/User/Desktop/PERFORM/realms/06-university/research/test-runs"

QUERIES = [
    "all:TempParaphraser",
    "all:paraphrasing AND all:evades AND all:detectors",
    "all:recursive AND all:paraphrasing AND all:detection",
    "all:evade AND all:AI-text AND all:detection",
    "all:translation AND all:evade AND all:detection AND all:AI",
    "all:perplexity AND all:burstiness AND all:GPTZero",
    "all:owt AND all:paraphrase AND all:detector",
    "all:detectGPT AND all:evasion",
]

def arxiv(q, n=8):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "max_results": n, "sortBy": "submittedDate", "sortOrder": "descending"})
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent-E"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode()

def parse(xml):
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        i = re.search(r"<id>(.*?)</id>", e, re.S)
        p = re.search(r"<published>(.*?)</published>", e, re.S)
        s = re.search(r"<summary>(.*?)</summary>", e, re.S)
        out.append({
            "date": p.group(1)[:10] if p else "?",
            "title": re.sub(r"\s+", " ", t.group(1)).strip(),
            "id": i.group(1).strip(),
            "abs": re.sub(r"\s+", " ", s.group(1)).strip()[:400] if s else "",
        })
    return out

results = {}
for q in QUERIES:
    try:
        results[q] = parse(arxiv(q))
        print(f"[OK] {q}: {len(results[q])}")
        for r in results[q][:5]:
            print(f"   {r['date']} {r['title'][:85]}")
    except Exception as e:
        results[q] = {"error": str(e)}
        print(f"[ERR] {q}: {e}")
    time.sleep(3)

with open(OUT + "/agentE_arxiv2.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("Saved.")
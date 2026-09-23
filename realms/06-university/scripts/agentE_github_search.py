"""Agent E — Mission 2: GitHub repo search for anti-AI-detection tools."""
import json, time, urllib.request, urllib.parse, os

OUT = r"C:/Users/User/Desktop/PERFORM/realms/06-university/research/test-runs"
os.makedirs(OUT, exist_ok=True)

QUERIES = [
    "humanizer",
    "ai-humanizer",
    "undetectable ai",
    "bypass-ai-detector",
    "anti-ai-detector",
    "paraphrase evade",
    "perplexity burstiness",
    "gptzero bypass",
    "turnitin bypass",
    "ai-text-rewriter",
    "ai text humanizer",
]

HDRS = {"Accept": "application/vnd.github+json", "User-Agent": "research-agent-E"}

def gh_search(query, per_page=10):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": query, "sort": "stars", "order": "desc", "per_page": per_page})
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

results = {}
for q in QUERIES:
    try:
        data = gh_search(q)
        items = []
        for it in data.get("items", []):
            items.append({
                "full_name": it["full_name"],
                "stars": it["stargazers_count"],
                "pushed_at": it["pushed_at"],
                "updated_at": it["updated_at"],
                "description": it.get("description"),
                "language": it.get("language"),
                "license": (it.get("license") or {}).get("spdx_id"),
                "html_url": it["html_url"],
                "topics": it.get("topics"),
                "default_branch": it.get("default_branch"),
            })
        results[q] = items
        print(f"[OK] {q!r}: {len(items)} repos, top={items[0]['full_name']} ({items[0]['stars']}*)" if items else f"[OK] {q!r}: 0")
    except Exception as e:
        results[q] = {"error": str(e)}
        print(f"[ERR] {q!r}: {e}")
    time.sleep(2)  # be gentle on rate limit

with open(os.path.join(OUT, "agentE_github_search.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nSaved ->", os.path.join(OUT, "agentE_github_search.json"))
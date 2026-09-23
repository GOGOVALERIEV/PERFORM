"""Agent E — HuggingFace model search."""
import json, time, urllib.request, urllib.parse, os

OUT = r"C:/Users/User/Desktop/PERFORM/realms/06-university/research/test-runs"
os.makedirs(OUT, exist_ok=True)

QUERIES = [
    ("paraphrase", "downloads"),
    ("text humanizer", "downloads"),
    ("humanize", "downloads"),
    ("dipper", "downloads"),
    ("ai-text-detector", "downloads"),
    ("paraphrase-multilingual", "downloads"),
    ("bulgarian", "downloads"),
    ("bgpt", "downloads"),
    ("translation bg", "downloads"),
    ("ai generated text detection", "downloads"),
]

def hf_search(query, sort, limit=20):
    url = "https://huggingface.co/api/models?" + urllib.parse.urlencode(
        {"search": query, "sort": sort, "direction": -1, "limit": limit})
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent-E"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

results = {}
for q, sort in QUERIES:
    try:
        data = hf_search(q, sort)
        items = []
        for m in data:
            items.append({
                "id": m["id"],
                "downloads": m.get("downloads"),
                "likes": m.get("likes"),
                "pipeline_tag": m.get("pipeline_tag"),
                "tags": m.get("tags", [])[:10],
                "lastModified": m.get("lastModified", "")[:10],
                "library": m.get("library_name"),
            })
        results[f"{q}|{sort}"] = items
        print(f"[OK] {q!r} ({sort}): {len(items)} models | top: {items[0]['id'] if items else '-'} dls={items[0]['downloads'] if items else '-'}")
    except Exception as e:
        results[f"{q}|{sort}"] = {"error": str(e)}
        print(f"[ERR] {q!r}: {e}")
    time.sleep(1)

# Check specific models of interest
for mid in ["kalpeshk2011/dipper-paraphraser-xxl",
            "huangjj877/TempParaphraser",
            "tuner007/pegasus_paraphrase",
            "BAAI/bge-reranker-v2-m3"]:
    try:
        url = f"https://huggingface.co/api/models/{mid}"
        req = urllib.request.Request(url, headers={"User-Agent": "research-agent-E"})
        with urllib.request.urlopen(req, timeout=30) as r:
            results[f"MODEL:{mid}"] = json.loads(r.read().decode())
        print(f"[OK] model {mid}")
    except Exception as e:
        results[f"MODEL:{mid}"] = {"error": str(e)}
        print(f"[ERR] model {mid}: {e}")
    time.sleep(1)

with open(os.path.join(OUT, "agentE_hf_models.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nSaved.")
"""Agent E — fetch top repo READMEs via raw.githubusercontent (no API quota)."""
import urllib.request, os, json

OUT = r"C:/Users/User/Desktop/PERFORM/realms/06-university/research/test-runs/readmes"
os.makedirs(OUT, exist_ok=True)

REPOS = [
    ("blader/humanizer", "main"),
    ("AIScientists-Dev/academic-humanizer", "main"),
    ("lynote-ai/humanize-text", "main"),
    ("korcarc/text-humanizer", "main"),
    ("ilyautov/humanizer-ru", "main"),
    ("Moonlit-Pages/AIGC-Detector-Rewriter-Skill", "main"),
    ("chi111i/BypassAIGC", "main"),
    ("martiansideofthemoon/ai-detection-paraphrases", "main"),
    ("MADEVAL/HumanAI", "main"),
    ("Aboudjem/humanizer-skill", "main"),
    ("Hainrixz/humanizalo", "main"),
    ("epoko77-ai/im-not-ai", "main"),
    ("Nanako0129/sepia", "main"),
    ("rudra496/StealthHumanizer", "main"),
    ("HJJWorks/TempParaphraser", "main"),
    ("LifelongLazyLearner/qu-ai-wei", "main"),
]

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "research-agent-E"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

for full, branch in REPOS:
    owner, repo = full.split("/")
    fname = full.replace("/", "__") + ".md"
    path = os.path.join(OUT, fname)
    if os.path.exists(path):
        print(f"[skip] {full} (exists)")
        continue
    for cand in ["README.md", "readme.md", "Readme.md", "README.MD", "README.markdown"]:
        url = f"https://raw.githubusercontent.com/{full}/{branch}/{cand}"
        try:
            content = get(url)
            if content and "404" not in content[:20]:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"# SOURCE: {url}\n\n")
                    f.write(content)
                print(f"[OK]   {full} via {cand} ({len(content)} chars)")
                break
        except Exception as e:
            last_err = e
    else:
        print(f"[FAIL] {full} ({last_err})")

print("\nDone.")
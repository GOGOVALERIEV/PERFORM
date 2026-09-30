"""
corpus_from_openalex.py — Stage 0b corpus builder (the Elicit engine, unleashed).

Topic goes in -> real academic papers come out (from OpenAlex: 138M+ papers,
the same corpus Elicit searches) -> bullet fact-pack + corpus .txt files.

Output (per topic):
  <outdir>/fact-pack.md      — bullet fragments (Duo-safe, no finished sentences)
                               with real authors/years/citations
  <outdir>/corpus/*.txt      — per-paper text files (title, authors, year, abstract)
  <outdir>/quotes.md         — 2-3 short REAL quotes per paper (the seesaw anchors)

Usage:
  python corpus_from_openalex.py "Cold War origins" --outdir <dir> --max-papers 8
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

OPENALEX = "https://api.openalex.org/works"
UA = {"User-Agent": "ShadowScholar-Corpus/1.0 (mailto:gogovaleriev77@gmail.com)"}


def _reconstruct_abstract(inv):
    """OpenAlex stores abstracts as inverted index — rebuild the sentence."""
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def search_papers(query, max_papers=8):
    """Search OpenAlex, return structured papers."""
    r = requests.get(OPENALEX, params={
        "search": query,
        "per-page": max_papers,
        "sort": "relevance_score:desc",
        "select": ("title,publication_year,authorships,abstract_inverted_index,"
                   "cited_by_count,open_access,doi,primary_location"),
    }, headers=UA, timeout=30)
    r.raise_for_status()
    papers = []
    for w in r.json().get("results", []):
        authors = [a["author"]["display_name"] for a in w.get("authorships", [])]
        loc = w.get("primary_location") or {}
        source = ((loc.get("source") or {}).get("display_name")) or ""
        oa = (w.get("open_access") or {})
        papers.append({
            "title": w.get("title") or "Untitled",
            "year": w.get("publication_year"),
            "authors": authors,
            "journal": source,
            "citations": w.get("cited_by_count", 0),
            "doi": w.get("doi") or "",
            "oa_url": oa.get("oa_url") or "",
            "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
        })
    return papers


def extract_quotes(abstract, max_quotes=2):
    """Pick 1-2 meaty sentences from a real abstract as quote candidates."""
    if not abstract:
        return []
    sents = re.split(r"(?<=[.!?])\s+", abstract)
    sents = [s.strip() for s in sents if 60 < len(s.strip()) < 260]
    # prefer sentences with concrete content (dates, numbers, proper nouns)
    scored = sorted(sents, key=lambda s: (
        bool(re.search(r"\d{3,4}", s)),  # has a year/number
        bool(re.search(r"\b[A-Z][a-z]+\b", s)),
    ), reverse=True)
    return scored[:max_quotes]


def build_factpack(papers, topic):
    lines = [f"# FACT-PACK — {topic}", "",
             "Bullet fragments only (Duo-safe). Each fact carries its real source.",
             ""]
    quotes = []
    for i, p in enumerate(papers, 1):
        auth = ", ".join(p["authors"][:2]) or "Unknown author"
        head = f"{auth} ({p['year']}) — “{p['title']}” [{p['journal']}, {p['citations']} citations]"
        lines.append(f"## Paper {i}: {head}")
        ab = p["abstract"]
        if ab:
            sents = re.split(r"(?<=[.!?])\s+", ab)
            for s in sents[:4]:
                if len(s.strip()) > 50:
                    lines.append(f"- {s.strip()}")
        if p["doi"]:
            lines.append(f"- DOI: {p['doi']}")
        if p["oa_url"]:
            lines.append(f"- Full text (OA): {p['oa_url']}")
        lines.append("")
        # quote candidates
        for q in extract_quotes(ab):
            quotes.append(f"„{q}“\n   — {auth} ({p['year']}), {p['title']}\n")
    return "\n".join(lines), "\n".join(quotes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--max-papers", type=int, default=8)
    args = ap.parse_args()

    out = Path(args.outdir)
    (out / "corpus").mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Searching OpenAlex: {args.topic!r}")
    papers = search_papers(args.topic, args.max_papers)
    if not papers:
        print("No papers found.")
        sys.exit(1)
    print(f"      found {len(papers)} papers")

    print("[2/3] Writing corpus files...")
    for i, p in enumerate(papers, 1):
        fn = out / "corpus" / f"paper-{i:02d}.txt"
        body = (f"TITLE: {p['title']}\n"
                f"AUTHORS: {', '.join(p['authors'])}\n"
                f"YEAR: {p['year']}\n"
                f"JOURNAL: {p['journal']}\n"
                f"CITED BY: {p['citations']}\n"
                f"DOI: {p['doi']}\n"
                f"OA URL: {p['oa_url']}\n\n"
                f"ABSTRACT:\n{p['abstract']}\n")
        fn.write_text(body, encoding="utf-8")
        print(f"      {fn.name}: {p['title'][:60]} ({p['year']})")
        time.sleep(0.2)  # polite pacing

    print("[3/3] Building fact-pack + quotes...")
    pack, quotes = build_factpack(papers, args.topic)
    (out / "fact-pack.md").write_text(pack, encoding="utf-8")
    (out / "quotes.md").write_text(
        "# REAL QUOTE ANCHORS (use 2-3 per referat — seesaw law)\n\n" + quotes,
        encoding="utf-8")
    print(f"DONE → {out}/fact-pack.md, quotes.md, corpus/ ({len(papers)} papers)")


if __name__ == "__main__":
    main()

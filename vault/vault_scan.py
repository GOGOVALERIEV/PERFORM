"""VAULT SCAN - one box, one scanner.
Usage:
  python vault_scan.py rebuild              (index everything, ~seconds)
  python vault_scan.py update               (index only new files)
  python vault_scan.py scan <word> [word2]  (search all products)
  python vault_scan.py scan <word> --history (price history for matches)
  python vault_scan.py stats                (what's in the box)
  python vault_scan.py pending              (show the buy-list)
"""
import sqlite3, json, sys, datetime, glob, os
from pathlib import Path

VAULT = Path(__file__).parent
DB = VAULT / "vault.db"
EXTRA_ROOTS = [
    Path("C:/Users/User/Desktop/project-test/output/deals"),
    Path("C:/Users/User/Desktop/PERFORM/deal-hunter/output"),
    Path("C:/Users/User/Desktop/PERFORM/laptop-hunt"),
]

def category_for(path):
    s = str(path).lower()
    for cat, kw in [("olx", "olx"), ("chinese", "chinese"), ("chinese", "temu"),
                    ("chinese", "alibaba"), ("chinese", "aliexpress"), ("local", "local"),
                    ("local", "jysk")]:
        if kw in s:
            return cat
    if "bg-stores" in s or "deals" in s or "laptop-hunt" in s:
        return "bg-stores"
    return "bg-stores"

def iter_files():
    seen = set()
    roots = [VAULT] + [r for r in EXTRA_ROOTS if r.exists()]
    for root in roots:
        for f in root.rglob("*.json"):
            s = str(f)
            if "vault.db" in s or os.sep + "cache" + os.sep in s:
                continue
            rp = f.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            yield f, category_for(f)

def walk_items(obj):
    """Recursively yield every dict that looks like a product."""
    if isinstance(obj, dict):
        name = obj.get("name") or obj.get("title") or obj.get("productName") or obj.get("subject")
        if isinstance(name, str) and 3 < len(name) < 300:
            price = obj.get("price")
            if isinstance(price, dict):
                price = price.get("current", {}).get("value") or price.get("current") or price.get("selling_price")
            if isinstance(price, (int, float, str)) and str(price).strip():
                yield {"name": name, "price": str(price), "old": obj.get("old_price") or obj.get("oldPrice") or obj.get("old") or "",
                       "url": obj.get("url") or obj.get("link") or "", "store": obj.get("store") or obj.get("source") or ""}
        for v in obj.values():
            yield from walk_items(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_items(v)

def connect():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY, date_seen TEXT, store TEXT, name TEXT,
        price TEXT, old_price TEXT, url TEXT, category TEXT, source_file TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS indexed_files(
        path TEXT PRIMARY KEY, mtime REAL, items INTEGER)""")
    return c

def rebuild_or_update(full):
    c = connect()
    done = {}
    if not full:
        for p, mtime, n in c.execute("SELECT path, mtime, items FROM indexed_files"):
            done[p] = (mtime, n)
    total = 0
    for f, cat in iter_files():
        try:
            mtime = f.stat().st_mtime
        except OSError:
            continue
        sp = str(f)
        if not full and sp in done and done[sp][0] == mtime:
            continue
        c.execute("DELETE FROM items WHERE source_file=?", (sp,))
        try:
            data = json.load(open(f, encoding="utf-8", errors="ignore"))
        except Exception:
            c.execute("INSERT OR REPLACE INTO indexed_files VALUES (?,?,0)", (sp, mtime))
            continue
        n = 0
        date_guess = ""
        base = f.stem[:10]
        if re.match(r"2026-[01][0-9]-[0-3][0-9]", base):
            date_guess = base
        if not date_guess:
            date_guess = datetime.date.fromtimestamp(mtime).isoformat()
        for it in walk_items(data):
            c.execute("INSERT INTO items(date_seen,store,name,price,old_price,url,category,source_file) VALUES (?,?,?,?,?,?,?,?)",
                      (date_guess, it["store"][:40], it["name"][:250], str(it["price"])[:30],
                       str(it["old"])[:30], str(it["url"])[:250], cat, sp))
            n += 1
        c.execute("INSERT OR REPLACE INTO indexed_files VALUES (?,?,?)", (sp, mtime, n))
        total += n
    c.commit()
    mode = "REBUILT" if full else "UPDATED"
    cnt = c.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    print(f"{mode}: +{total} items | total in vault.db: {cnt}")

def scan(words, history):
    c = connect()
    q = " AND ".join(["name LIKE ?"] * len(words))
    rows = c.execute(f"SELECT date_seen, store, name, price, old_price, url, category FROM items WHERE {q} ORDER BY CAST(REPLACE(REPLACE(price,',','.'),' EUR','') AS REAL)", tuple(f"%{w}%" for w in words)).fetchall()
    print(f"matches: {len(rows)}")
    for r in rows[:60]:
        print(f"  {r[0]} | {r[6]:9} | {str(r[1])[:10]:10} | {str(r[3])[:8]:8} | {r[2][:70]}")
        if r[5]:
            print(f"           {r[5][:100]}")
    if history and rows:
        print("\n--- PRICE HISTORY ---")
        names = {}
        for r in rows:
            names.setdefault(r[2][:50], []).append((r[0], r[3], r[1]))
        for n, hist in names.items():
            if len(hist) > 1 or len(set(h[1] for h in hist)) > 1:
                print(f"  {n[:55]}: " + " -> ".join(f"{h[1]} ({h[0]}, {h[2]})" for h in hist))

def stats():
    c = connect()
    print("=== VAULT STATS ===")
    for cat, n in c.execute("SELECT category, COUNT(*) FROM items GROUP BY category ORDER BY COUNT(*) DESC"):
        print(f"  {cat:10} {n:>6} items")
    n_files = c.execute("SELECT COUNT(*) FROM indexed_files").fetchone()[0]
    total = c.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    print(f"  files indexed: {n_files} | total items: {total}")

def pending():
    d = json.load(open(VAULT / "pending" / "pending.json", encoding="utf-8"))
    print("=== PENDING BUYS ===")
    for it in d.get("winners") or d.get("items", []):
        price = it.get("price_when_seen") or it.get("price", "")
        print(f"  [{it.get('status','?'):9}] {it['item'][:60]} | {price} | {it.get('note','')[:60]}")

import re
def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "rebuild": rebuild_or_update(True)
    elif cmd == "update": rebuild_or_update(False)
    elif cmd == "scan": scan([w for w in sys.argv[2:] if not w.startswith("--")], "--history" in sys.argv)
    elif cmd == "stats": stats()
    elif cmd == "pending": pending()
    else:
        print("unknown command"); sys.exit(1)

if __name__ == "__main__":
    main()

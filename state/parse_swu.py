import re, html, json, sys

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ir1.html"
raw = open(src, encoding="utf-8", errors="replace").read()
text = html.unescape(raw).replace("\xa0", " ")
# strip tags -> separators
text = re.sub(r"<[^>]+>", "|", text)
parts = [p.strip() for p in text.split("|")]
parts = [p for p in parts if p]
# join back with spaces for context scan
joined = " | ".join(parts)

# find schedule rows: Day ... time range ... discipline ... room ... lecturer
days = ["Понеделник", "Вторник", "Сряда", "Четвъртък", "Петък", "Събота", "Неделя"]
rows = []
i = 0
while i < len(parts):
    p = parts[i]
    if p in days:
        day = p
        # scan forward until next day keyword
        j = i + 1
        chunk = []
        while j < len(parts) and parts[j] not in days:
            chunk.append(parts[j])
            j += 1
        ct = re.sub(r"\s+", " ", " ".join(chunk))
        # find time ranges and the discipline blocks
        times = re.findall(r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})", ct)
        print(f"\n### {day}")
        seen = set()
        for st, en in times:
            k = ct.find(f"{st} - {en}")
            seg = ct[k:k+400] if k >= 0 else ""
            key = (st, en)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {st}-{en} :: {seg[:350]}")
        i = j
    else:
        i += 1

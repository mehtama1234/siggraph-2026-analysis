"""Merge rich_out/*.json (keyed by gid) into data/rich.json. Reports coverage.
Falls back to a delimiter regex when an agent emits an unescaped inner quote,
which is safe because the 5 fields always appear in fixed order (bp,wh,ap,ww,po)."""
import json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "rich_out")

BLOCK = re.compile(
    r'"(\d+)"\s*:\s*\{\s*"bp"\s*:\s*"(.*?)"\s*,\s*"wh"\s*:\s*"(.*?)"\s*,'
    r'\s*"ap"\s*:\s*"(.*?)"\s*,\s*"ww"\s*:\s*"(.*?)"\s*,\s*"po"\s*:\s*"(.*?)"\s*\}',
    re.DOTALL)

LEAK = re.compile(r'"\s*,\s*"(?:bp|wh|ap|ww|po)"\s*:\s*"')
def clean(s):
    s = s.replace('\\"', '"').replace("\\n", " ")
    s = LEAK.split(s)[0]                       # drop any leaked field-delimiter litter
    return re.sub(r"\s+", " ", s).strip().rstrip('"').strip()

def rescue(text):
    out = {}
    for m in BLOCK.finditer(text):
        gid, bp, wh, ap, ww, po = m.groups()
        out[gid] = {"bp": clean(bp), "wh": clean(wh), "ap": clean(ap), "ww": clean(ww), "po": clean(po)}
    return out

rich = {}
bad = []
for f in sorted(glob.glob(os.path.join(OUT, "b*.json"))):
    raw = open(f).read()
    try:
        d = json.load(raw and __import__("io").StringIO(raw))
    except Exception:
        d = rescue(raw)
        if not d:
            bad.append(os.path.basename(f)); continue
    for gid, v in d.items():
        if isinstance(v, dict) and v.get("bp"):
            rich[str(gid)] = {k: clean(v.get(k) or "") for k in ("bp", "wh", "ap", "ww", "po")}

json.dump(rich, open(os.path.join(HERE, "data", "rich.json"), "w"), indent=1)
A = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]
tot = len(A)
have = sum(1 for p in A if str(p["gid"]) in rich)
print(f"merged {len(rich)} rich writeups -> data/rich.json")
print(f"coverage: {have}/{tot} analyzed papers ({100*have//max(tot,1)}%)")
if bad:
    print("BAD batches:", bad)

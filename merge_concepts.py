"""Merge concept_out/<key>.json (one rich essay each) into data/concepts_rich.json."""
import json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "concept_out")

FIELD = re.compile(r'"(idea|why|dots|picture)"\s*:\s*"(.*?)"\s*(?=,\s*"(?:idea|why|dots|picture)"\s*:|\}\s*$)', re.DOTALL)
def clean(s):
    s = s.replace('\\"', '"').replace("\\n", " ")
    s = re.sub(r"\s*\(\s*papers?\s+\d+(?:\s*,\s*\d+)*\s*\)", "", s)  # drop "(paper 93)" refs
    s = re.sub(r"\s*\bpapers?\s+#?\d+\b", "", s)                      # drop bare "paper 41"
    return re.sub(r"\s+", " ", s).strip()

def rescue(text):
    out = {}
    for m in FIELD.finditer(text):
        out[m.group(1)] = clean(m.group(2))
    return out

rich, bad = {}, []
for f in sorted(glob.glob(os.path.join(OUT, "*.json"))):
    key = os.path.splitext(os.path.basename(f))[0]
    raw = open(f).read()
    try:
        d = json.load(open(f))
    except Exception:
        d = rescue(raw)
        if not d:
            bad.append(key); continue
    rich[key] = {k: clean(d.get(k) or "") for k in ("idea", "why", "dots", "picture")}

json.dump(rich, open(os.path.join(HERE, "data", "concepts_rich.json"), "w"), indent=1)
print(f"merged {len(rich)} rich concept essays -> data/concepts_rich.json")
for k, v in rich.items():
    miss = [f for f in ("idea", "why", "dots", "picture") if not v[f]]
    print(f"  {k:14} idea:{len(v['idea']):4} why:{len(v['why']):4} dots:{len(v['dots']):4} pic:{len(v['picture']):3}" + (f"  MISSING {miss}" if miss else ""))
if bad:
    print("BAD:", bad)

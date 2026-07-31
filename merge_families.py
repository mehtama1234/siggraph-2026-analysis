"""Merge generated paper-family essays into data/families_rich.json."""
import json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "family_out")
FIELDS = ("problem_shape", "naive_failure", "mathematical_principle", "why_math_matters", "paper_family", "what_changed", "limits")
FIELD = re.compile(r'"(' + "|".join(FIELDS) + r')"\s*:\s*"(.*?)"\s*(?=,\s*"(?:' + "|".join(FIELDS) + r')"\s*:|\}\s*$)', re.DOTALL)

def clean(s):
    s = str(s or "").replace('\\"', '"').replace("\\n", " ")
    s = s.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip()

def rescue(text):
    return {m.group(1): clean(m.group(2)) for m in FIELD.finditer(text)}

rich, bad = {}, []
for f in sorted(glob.glob(os.path.join(OUT, "*.json"))):
    key = os.path.splitext(os.path.basename(f))[0]
    raw = open(f).read()
    try:
        d = json.loads(raw)
    except Exception:
        d = rescue(raw)
        if not d:
            bad.append(key)
            continue
    rich[key] = {k: clean(d.get(k, "")) for k in FIELDS}

json.dump(rich, open(os.path.join(HERE, "data", "families_rich.json"), "w"), indent=1)
print(f"merged {len(rich)} family essays -> data/families_rich.json")
if bad:
    print("BAD:", bad)

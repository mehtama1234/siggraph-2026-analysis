"""Assemble all rich concept essays (in CG order) into one file the synthesis agent reads."""
import json, os
from build_math import CG, groups, HERE

C = json.load(open(os.path.join(HERE, "data", "concepts_rich.json")))
out = []
for c in CG:
    if not groups[c["key"]]:
        continue
    r = C.get(c["key"], {})
    out.append({"title": c["title"], "n_papers": len(groups[c["key"]]),
                "idea": r.get("idea", ""), "why": r.get("why", ""),
                "math": r.get("math", ""), "family": r.get("family", ""),
                "dots": r.get("dots", "")})
json.dump({"concepts": out}, open(os.path.join(HERE, "data", "synth_in.json"), "w"), indent=1)
print(f"wrote synth_in.json with {len(out)} concepts")

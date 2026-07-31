"""One input file per math concept (key, title, current intro/why, and the papers
under it with their plain 'uses' note) for the rich-concept Haiku pass."""
import json, os
from build_math import CG, groups, title_of, WHY, HERE

outdir = os.path.join(HERE, "data", "concept_in")
os.makedirs(outdir, exist_ok=True)
n = 0
for c in CG:
    ps = groups[c["key"]]
    if not ps:
        continue
    papers = [{"title": title_of.get(gid, ""), "uses": mv.get("plain", "")} for gid, mv in ps]
    rec = {"key": c["key"], "title": c["title"], "intro": c["intro"], "why": WHY.get(c["key"], ""),
           "n_total": len(papers), "papers": papers[:36]}
    json.dump(rec, open(os.path.join(outdir, c["key"] + ".json"), "w"), indent=1)
    n += 1
keys = [c["key"] for c in CG if groups[c["key"]]]
print(f"wrote {n} concept input files: {keys}")

"""Report which deep-generation jobs are still missing or legacy.

This is a resume helper for the Haiku workflows. It maps missing deep paper
records back to batch filenames and lists missing concept/family keys.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

PAPER_FIELDS = ("bp", "wh", "naive", "ap", "mech", "math", "dots", "ww", "po", "limits")
CONCEPT_FIELDS = ("idea", "why", "math", "family", "dots", "picture")
FAMILY_FIELDS = ("problem_shape", "naive_failure", "mathematical_principle", "why_math_matters", "paper_family", "what_changed", "limits")

def load(path, default):
    full = os.path.join(HERE, path)
    return json.load(open(full)) if os.path.exists(full) else default

def complete(rec, fields):
    return isinstance(rec, dict) and all(str(rec.get(f, "")).strip() for f in fields)

def batch_gid_map(dirname):
    out = {}
    full = os.path.join(HERE, dirname)
    if not os.path.isdir(full):
        return out
    for name in sorted(os.listdir(full)):
        if not name.endswith(".json"):
            continue
        try:
            data = json.load(open(os.path.join(full, name)))
        except Exception:
            continue
        if isinstance(data, list):
            for p in data:
                if "gid" in p:
                    out[str(p["gid"])] = name[:-5]
        elif isinstance(data, dict):
            for p in data.values():
                if isinstance(p, dict) and "gid" in p:
                    out[str(p["gid"])] = name[:-5]
    return out

analysis = load("data/analysis.json", {"papers": []})["papers"]
rich = load("data/rich.json", {})
concepts = load("data/concepts_rich.json", {})
families = load("data/families_rich.json", {})
manifest = load("data/family_manifest.json", {"families": []})["families"]

batches = batch_gid_map("data/batches")

missing_batches, missing_gids = set(), []
for p in analysis:
    gid = str(p["gid"])
    if complete(rich.get(gid), PAPER_FIELDS):
        continue
    missing_gids.append(gid)
    missing_batches.add(batches.get(gid, f"gid:{gid}"))

missing_concepts = [k for k, v in concepts.items() if not complete(v, CONCEPT_FIELDS)]
missing_families = [f["key"] for f in manifest if not complete(families.get(f["key"]), FAMILY_FIELDS)]

print("deep generation todo")
print(f"paper gids needing deep schema: {len(missing_gids)}")
print("rich_workflow batches:", " ".join(sorted(missing_batches)) or "none")
print("concept keys:         ", " ".join(missing_concepts) or "none")
print("family keys:          ", " ".join(missing_families) or "none")

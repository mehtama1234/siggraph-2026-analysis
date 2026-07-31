"""Print compact progress toward the deep first-principles content target."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    path = os.path.join(HERE, "data", name)
    return json.load(open(path)) if os.path.exists(path) else None

def has_fields(rec, fields):
    return isinstance(rec, dict) and all(str(rec.get(f, "")).strip() for f in fields)

def pct(n, d):
    return f"{n}/{d} ({100*n//max(d,1)}%)"

analysis = load("analysis.json") or {"papers": []}
rich = load("rich.json") or {}
concepts = load("concepts_rich.json") or {}
synth = load("synth_out.json") or {}
families = load("families_rich.json") or {}
manifest = load("family_manifest.json") or {"families": []}

paper_fields = ("bp", "wh", "naive", "ap", "mech", "math", "dots", "ww", "po", "limits")
concept_fields = ("idea", "why", "math", "family", "dots", "picture")
family_fields = ("problem_shape", "naive_failure", "mathematical_principle", "why_math_matters", "paper_family", "what_changed", "limits")
synth_fields = ("thread", "arc", "punchline")

expected_papers = [str(p["gid"]) for p in analysis["papers"]]
deep_papers = sum(1 for gid in expected_papers if has_fields(rich.get(gid), paper_fields))
deep_concepts = sum(1 for r in concepts.values() if has_fields(r, concept_fields))
deep_families = sum(1 for f in manifest["families"] if has_fields(families.get(f["key"]), family_fields))

print("deep-content status")
print("papers:   ", pct(deep_papers, len(expected_papers)))
print("concepts: ", pct(deep_concepts, len(concepts)))
print("families: ", pct(deep_families, len(manifest["families"])))
deep_synth = has_fields(synth, synth_fields) and "family" in " ".join(str(v).lower() for v in synth.values())
print("synthesis:", "deep/family-aware" if deep_synth else "legacy or incomplete")

"""Validate that generated analysis meets the deep first-principles content contract.

This is intentionally stricter than "does the page build". It checks whether the
generated JSON actually contains the deep per-paper, concept, synthesis, and
paper-family fields required by FIRST_PRINCIPLES_GOAL.md.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

RICH_FIELDS = {
    "bp": 90,
    "wh": 90,
    "naive": 60,
    "ap": 90,
    "mech": 130,
    "math": 130,
    "dots": 90,
    "ww": 100,
    "po": 55,
    "limits": 55,
}
CONCEPT_FIELDS = {
    "idea": 120,
    "why": 100,
    "math": 120,
    "family": 100,
    "dots": 120,
    "picture": 35,
}
FAMILY_FIELDS = {
    "problem_shape": 120,
    "naive_failure": 90,
    "mathematical_principle": 120,
    "why_math_matters": 120,
    "paper_family": 120,
    "what_changed": 70,
    "limits": 70,
}
SYNTH_FIELDS = {"thread": 45, "arc": 140, "punchline": 70}

BAD_MARKERS = ("**", "SOTA", "state-of-the-art", "leverage", "novel framework", "paradigm")

def load(name, required=True):
    path = os.path.join(HERE, "data", name)
    if not os.path.exists(path):
        if required:
            return None, [f"missing data/{name}"]
        return {}, []
    return json.load(open(path)), []

def words(s):
    return len(str(s or "").split())

def check_map(label, data, fields, expected_keys=None):
    problems = []
    if data is None:
        return problems
    if expected_keys is not None:
        missing_keys = sorted(set(expected_keys) - set(data))
        if missing_keys:
            problems.append(f"{label}: missing {len(missing_keys)} expected records, examples: {missing_keys[:8]}")
    for key, rec in data.items():
        if not isinstance(rec, dict):
            problems.append(f"{label}:{key}: record is not an object")
            continue
        for field, min_words in fields.items():
            text = rec.get(field, "")
            if words(text) < min_words:
                problems.append(f"{label}:{key}.{field}: {words(text)} words < {min_words}")
        joined = " ".join(str(v) for v in rec.values())
        for marker in BAD_MARKERS:
            if marker in joined:
                problems.append(f"{label}:{key}: contains banned/artifact marker {marker!r}")
    return problems

def main():
    problems = []

    analysis, errs = load("analysis.json")
    problems.extend(errs)
    rich, errs = load("rich.json")
    problems.extend(errs)
    concepts, errs = load("concepts_rich.json")
    problems.extend(errs)
    synth, errs = load("synth_out.json")
    problems.extend(errs)
    families, errs = load("families_rich.json")
    problems.extend(errs)
    manifest, errs = load("family_manifest.json")
    problems.extend(errs)

    if analysis and rich:
        expected = [str(p["gid"]) for p in analysis["papers"]]
        problems.extend(check_map("paper", rich, RICH_FIELDS, expected))
    if concepts:
        problems.extend(check_map("concept", concepts, CONCEPT_FIELDS))
    if synth:
        problems.extend(check_map("synthesis", {"synth": synth}, SYNTH_FIELDS))
    if manifest and families:
        expected = [f["key"] for f in manifest["families"]]
        problems.extend(check_map("family", families, FAMILY_FIELDS, expected))

    if problems:
        print(f"deep content validation FAILED: {len(problems)} issues")
        for p in problems[:80]:
            print(" -", p)
        if len(problems) > 80:
            print(f" ... {len(problems) - 80} more")
        return 1

    print("deep content validation passed")
    print(f"papers: {len(rich)} · concepts: {len(concepts)} · families: {len(families)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

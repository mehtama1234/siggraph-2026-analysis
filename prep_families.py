"""Prepare one input file per theme/subtheme for paper-family essays.

Each family file gives the generation pass enough evidence to explain why the
papers in that theme belong together: theme counts, examples, and representative
analyzed papers with problem/approach/contribution/methods.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "family_in")
os.makedirs(OUT, exist_ok=True)

themes = json.load(open(os.path.join(HERE, "data", "themes.json")))["themes"]
analysis = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]

STOP = {"and", "the", "with", "for", "from", "into", "use", "using", "systems", "models", "fields"}

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def terms(theme):
    words = re.findall(r"[a-z0-9]+", theme.lower())
    return [w for w in words if len(w) > 2 and w not in STOP]

def score(theme_terms, p):
    text = " ".join(str(p.get(k) or "") for k in ("title", "problem", "approach", "contribution", "primary_theme"))
    text += " " + " ".join(p.get("methods") or [])
    low = text.lower()
    return sum(1 for t in theme_terms if t in low)

written = []
for t in themes:
    theme = t["theme"]
    tt = terms(theme)
    ranked = sorted((p for p in analysis if score(tt, p)), key=lambda p: -score(tt, p))[:40]
    rec = {
        "key": slug(theme),
        "theme": theme,
        "n_papers": t["n"],
        "pct": t.get("pct"),
        "theme_examples": t.get("examples", []),
        "representative_papers": [
            {
                "title": p.get("title"),
                "problem": p.get("problem"),
                "approach": p.get("approach"),
                "contribution": p.get("contribution"),
                "primary_theme": p.get("primary_theme"),
                "methods": p.get("methods") or [],
            }
            for p in ranked
        ],
    }
    path = os.path.join(OUT, rec["key"] + ".json")
    json.dump(rec, open(path, "w"), indent=1)
    written.append(rec["key"])

json.dump({"families": [{"theme": t["theme"], "key": slug(t["theme"])} for t in themes]},
          open(os.path.join(HERE, "data", "family_manifest.json"), "w"), indent=1)
print(f"wrote {len(written)} family input files")

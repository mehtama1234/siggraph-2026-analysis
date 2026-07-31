# SIGGRAPH 2026 — computer graphics conference analysis

A first-principles analysis of the **153 technical papers** of SIGGRAPH 2026
(published as ACM Transactions on Graphics).

**Live:** https://mehtama1234.github.io/siggraph-2026-analysis/

- **index.html** — the theme landscape + LLM-tagged technique bars
- **explorer.html** — searchable explorer of all 153 papers (problem/approach/contribution)
- **deep.html** — a first-principles "deep read": the field as the life of a virtual object
  (describe → behave → look → capture → invent → present), with every stage, sub-theme, and
  paper explained in plain, no-jargon language.

Data: Semantic Scholar (ACM TOG 2026, 100% abstracts). Per-paper analysis + plain-language
rewrites by an LLM (Haiku).

Deep-analysis standard: [FIRST_PRINCIPLES_GOAL.md](FIRST_PRINCIPLES_GOAL.md). The current pipeline has
separate generation passes for per-paper deep essays, recurring mathematical concepts, whole-field
synthesis, and theme/subtheme paper-family essays.

Pipeline: `ingest.py → mine_themes.py → prep_families.py → (Haiku workflows: rich_workflow.js,
concepts_workflow.js, family_workflow.js, synth_workflow.js) → merge_*.py → build_*.py →
validate_deep_content.py`.

`validate_deep_content.py` is the quality gate for the deep pass. It fails if any paper, concept,
synthesis, or family essay is still missing the required first-principles fields or is too short.
Use `deep_status.py` during generation to see compact progress across papers, concepts, families,
and synthesis. Use `deep_todo.py` to list the exact paper batches, concept keys, and family keys
that still need the deep schema.

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
rewrites by an LLM (Haiku). Pipeline: `ingest.py → mine_themes.py → (Haiku workflow) →
merge_*.py → build_*.py`.

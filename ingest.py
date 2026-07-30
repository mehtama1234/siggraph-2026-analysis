"""Ingest SIGGRAPH 2026 technical papers (published as ACM Transactions on Graphics
vol 45 / 2026). S2 has 100% abstracts + 97% open PDFs for these."""
import json, os, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
FIELDS = "title,abstract,externalIds,openAccessPdf,url"
def fetch(token=None):
    params = {"venue": "ACM Transactions on Graphics", "year": "2026", "fields": FIELDS}
    if token: params["token"] = token
    url = BASE + "?" + urllib.parse.urlencode(params)
    for a in range(7):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.loads(r.read())
        except Exception as e:
            print(f"  retry {a+1} ({str(e)[:40]})", flush=True); time.sleep(5*(a+1))
    raise RuntimeError("failed")
papers, token = [], None
while True:
    d = fetch(token)
    for p in (d.get("data") or []):
        ext = p.get("externalIds") or {}
        t = (p.get("title") or "").strip()
        if t.lower().startswith("erratum") or t.lower().startswith("correction"): continue
        papers.append({"paperId": p.get("paperId"), "title": t, "abstract": p.get("abstract"),
                       "doi": ext.get("DOI"), "arxiv": ext.get("ArXiv"),
                       "pdf": (p.get("openAccessPdf") or {}).get("url") or None, "url": p.get("url")})
    print(f"total {len(papers)} / {d.get('total')}", flush=True)
    token = d.get("token")
    if not token or not d.get("data"): break
    time.sleep(3)
seen, uniq = set(), []
for p in papers:
    k = p["title"].lower()
    if k and k not in seen: seen.add(k); uniq.append(p)
wa = sum(1 for p in uniq if p["abstract"])
json.dump({"venue": "SIGGRAPH 2026 (ACM TOG vol 45)", "n_papers": len(uniq), "with_abstract": wa, "papers": uniq},
          open(os.path.join(HERE,"data","papers.json"),"w"), indent=1)
print(f"-> {len(uniq)} papers, {wa} abstracts ({wa*100//max(len(uniq),1)}%)")

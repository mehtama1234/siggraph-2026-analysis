import json, os, glob
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
d=json.load(open(os.path.join(HERE,"data","papers.json")))
papers=[{"title":p["title"],"doi":p.get("doi"),"url":p.get("url"),"pdf":p.get("pdf"),"arxiv":p.get("arxiv")}
        for p in d["papers"] if p.get("abstract")]
for i,p in enumerate(papers): p["gid"]=i
by=dict((p["gid"],p) for p in papers)
an={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and g in by:
                an[g]={k:a.get(k) for k in ("problem","approach","contribution","primary_theme","methods")}
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
merged=[{**by[g], **an[g]} for g in sorted(an)]
json.dump({"n_papers":len(papers),"n_analyzed":len(merged),"bad_batches":bad,"papers":merged},
          open(os.path.join(HERE,"data","analysis.json"),"w"),indent=1)
print(f"analyzed {len(merged)}/{len(papers)}; bad {bad}")
# normalize method tags
CANON={r"gaussian splat|3dgs":"gaussian splatting", r"diffusion":"diffusion", r"nerf|radiance field|neural render":"neural rendering",
 r"implicit|sdf|signed distance":"implicit surfaces", r"mesh":"mesh", r"point cloud":"point clouds",
 r"finite element|fem|mpm|material point":"physics FEM/MPM", r"monte carlo|path tracing|ray trac":"monte carlo rendering",
 r"neural network|mlp|deep":"neural nets", r"transformer|attention":"transformers", r"gan|generative adversarial":"GAN",
 r"optimization":"optimization", r"differentiable":"differentiable", r"brdf|svbrdf|material":"materials/BRDF",
 r"skinning|rigging|skeletal":"rigging/skinning", r"cloth|yarn|fiber":"cloth/fiber sim", r"fluid|sph|lbm":"fluid sim",
 r"parameteriz|uv":"UV/parameterization", r"reinforcement":"reinforcement learning", r"text[- ]to":"text-to-3D",
 r"real[- ]?time|gpu":"real-time/GPU", r"physics|simulation|dynamics":"physical simulation"}
import re
mc=Counter()
for p in merged:
    seen=set()
    for t in (p.get("methods") or []):
        tl=str(t).lower().strip(); lab=None
        for pat,name in CANON.items():
            if re.search(pat,tl): lab=name; break
        lab=lab or None
        if lab and lab not in seen: mc[lab]+=1; seen.add(lab)
json.dump({"n_analyzed":len(merged),"methods":[{"tag":k,"n":v} for k,v in mc.most_common(24)]},
          open(os.path.join(HERE,"data","summary.json"),"w"),indent=1)
print("top methods:", ", ".join(f"{k}({v})" for k,v in mc.most_common(12)))

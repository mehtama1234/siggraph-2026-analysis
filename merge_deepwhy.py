import json, os, glob, re
HERE=os.path.dirname(os.path.abspath(__file__))
dw={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out6","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("deep_why"): dw[str(g)]=a["deep_why"]
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
subs=[(r'\bneural networks?\b','systems that learn from examples'),(r'\bmeshes\b','3D models'),(r'\bmesh\b','3D model'),
 (r'\bgradients?\b','the downhill direction'),(r'\bvariance\b','spread of error'),(r'\bconvex\b','bowl-shaped'),(r'\beigen\w*\b','natural-mode'),
 (r'\bdiffusion\b','image-generating'),(r'\bstochastic\b','random'),(r'\bmatrix\b','grid of numbers'),(r'\btensors?\b','number grids'),
 (r'\btokens?\b','pieces'),(r'\bsolvers?\b','methods'),(r'\bvertices\b','corner points'),(r'\bvertex\b','corner point'),
 (r'\bmanifolds?\b','surface'),(r'\bkernels?\b','local rule'),(r'\bimplicit\b','rule-based'),(r'\blatent\b','hidden'),(r'\bdifferentiable\b','smoothly adjustable')]
n=0
for k in dw:
    for pat,rep in subs:
        t=re.sub(pat,rep,dw[k],flags=re.I)
        if t!=dw[k]: n+=1; dw[k]=t
json.dump(dw, open(os.path.join(HERE,"data","deepwhy.json"),"w"), indent=1)
al=' '.join(dw.values())
banned=['mesh','vertex','tensor','gradient','matrix','neural network','diffusion','eigen','manifold','convex','latent','solver','kernel','token','differentiable']
resid={b:len(re.findall(r'\b'+b+r'\b',al,re.I)) for b in banned if re.search(r'\b'+b+r'\b',al,re.I)}
wc=sum(len(v.split()) for v in dw.values())//max(len(dw),1)
print(f"siggraph deepwhy {len(dw)}, cleaned {n}, avg {wc} words, bad {bad}, residual {resid or 'CLEAN'}")

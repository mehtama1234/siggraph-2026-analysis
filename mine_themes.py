"""Theme-mine SIGGRAPH 2026 over title+abstract with a computer-graphics taxonomy."""
import json, os, re
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE,"data","papers.json"))); ps = d["papers"]
THEMES = {
 "Neural Rendering & Radiance Fields": [r"neural render", r"radiance field", r"\bnerf\b", r"gaussian splat", r"\b3dgs\b", r"novel view", r"view synthesis", r"differentiable render"],
 "Generative 3D & Diffusion": [r"diffusion", r"generative", r"text[- ]to[- ]3d", r"\bgan\b", r"score[- ]based", r"flow matching", r"latent.*3d", r"asset generation", r"3d generation"],
 "Geometry Processing & Meshes": [r"\bmesh\b", r"geometry process", r"remesh", r"parameteriz", r"\buv\b", r"surface reconstruct", r"point cloud", r"implicit surface", r"\bsdf\b", r"subdivision", r"quad"],
 "Physical Simulation": [r"simulation", r"physics", r"finite element", r"\bfem\b", r"\bmpm\b", r"\bpbd\b", r"collision", r"contact", r"elastic", r"deformabl", r"rigid body"],
 "Fluids, Smoke & Granular": [r"fluid", r"smoke", r"\bsph\b", r"lattice boltzmann", r"\blbm\b", r"granular", r"sand", r"liquid", r"free surface", r"navier"],
 "Cloth, Hair & Fibers": [r"\bcloth\b", r"\byarn\b", r"\bhair\b", r"fiber", r"knit", r"woven", r"garment", r"textile"],
 "Character Animation & Motion": [r"animation", r"\bmotion\b", r"character", r"skinning", r"rigging", r"skeletal", r"locomotion", r"physics[- ]based character", r"motion capture", r"retarget"],
 "Appearance, Materials & BRDF": [r"\bbrdf\b", r"material", r"appearance", r"reflectance", r"\bbssrdf\b", r"svbrdf", r"texture synthesis", r"shading model", r"subsurface"],
 "Rendering & Light Transport": [r"path tracing", r"light transport", r"monte carlo", r"ray tracing", r"global illumination", r"importance sampl", r"denois", r"real[- ]?time render", r"rasteriz", r"radiosity"],
 "Computational Photography & Imaging": [r"computational photograph", r"\bhdr\b", r"deblur", r"image[- ]based", r"tone mapping", r"camera", r"relighting", r"super[- ]?resolution", r"denoising.*image"],
 "Fabrication & 3D Printing": [r"fabricat", r"3d print", r"additive manufactur", r"computational design.*fabric", r"cnc", r"knitting machine", r"self[- ]?assembl"],
 "VR/AR & Displays": [r"\bvr\b", r"\bar\b", r"virtual reality", r"augmented reality", r"holograph", r"display", r"head[- ]?mounted", r"stereo", r"light field display", r"perception"],
 "Faces & Avatars": [r"\bface\b", r"avatar", r"facial", r"head avatar", r"portrait", r"expression", r"talking head", r"relightable avatar"],
 "Sketching & Vector / 2D": [r"sketch", r"vector graphic", r"\bsvg\b", r"line drawing", r"illustration", r"stroke", r"2d animation", r"stylization"],
 "Sound & Multisensory": [r"\bsound\b", r"audio", r"acoustic", r"haptic", r"multisensory"],
 "Neural Fields & Representations": [r"neural field", r"implicit neural", r"\bmlp\b representation", r"coordinate network", r"positional encoding", r"neural representation"],
}
C = {t:[re.compile(p,re.I) for p in ps_] for t,ps_ in THEMES.items()}
for p in ps:
    text=(p["title"]+" "+(p["abstract"] or "")).lower()
    p["themes"]=[t for t,pat in C.items() if any(x.search(text) for x in pat)]
N=len(ps); tc=Counter(); ex={t:[] for t in THEMES}
for p in ps:
    for t in p["themes"]:
        tc[t]+=1
        if len(ex[t])<6: ex[t].append(p["title"])
uncat=sum(1 for p in ps if not p["themes"])
OUT={"venue":d["venue"],"n_papers":N,"with_abstract":d["with_abstract"],"n_uncategorized":uncat,
     "themes":[{"theme":t,"n":n,"pct":round(n*100/N,1),"examples":ex[t]} for t,n in tc.most_common()]}
json.dump(OUT,open(os.path.join(HERE,"data","themes.json"),"w"),indent=1)
print(f"{N} papers, {uncat} uncategorized")
for t,n in tc.most_common(): print(f"  {n:>3}  {t}")

import json, os, glob
from collections import Counter
HERE=os.path.dirname(os.path.abspath(__file__))
math={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out3","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("math_plain"):
                math[str(g)]={"tags":a.get("math_tags") or [], "plain":a["math_plain"]}
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
json.dump(math, open(os.path.join(HERE,"data","math.json"),"w"), indent=1)
tc=Counter()
for v in math.values():
    for t in v["tags"]: tc[t]+=1
print(f"math: {len(math)} papers, bad {bad}")
print("=== math-idea frequency across papers ===")
for t,n in tc.most_common(): print(f"  {n:>3}  {t}")

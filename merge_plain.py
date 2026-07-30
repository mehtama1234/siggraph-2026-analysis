import json, os, glob
HERE=os.path.dirname(os.path.abspath(__file__))
plain={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out2","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("plain_problem"):
                plain[str(g)]={"p":a["plain_problem"],"a":a.get("plain_approach","")}
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
json.dump(plain, open(os.path.join(HERE,"data","plain.json"),"w"), indent=1)
print(f"plain: {len(plain)} papers, bad {bad}")

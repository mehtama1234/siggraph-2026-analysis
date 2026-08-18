#!/usr/bin/env python3
"""Build the two missing signature synthesis pages for SIGGRAPH 2026, matching
the CVPR site's connective tissue: hub.html ("the one machine of computer
graphics" — the 16 mined themes arranged as the pipeline that makes a virtual
world) and idea-graph.html (themes wired by shared papers). Links into the
existing rich pages (deep/explorer/math). Run: python3 build_hub_graph.py"""
import html, itertools, collections, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s), quote=False)

TH = json.load(open(ROOT/"data/themes.json"))["themes"]
CNT = {t["theme"]: t["n"] for t in TH}
EX = {t["theme"]: set(t.get("examples", [])) for t in TH}

# the graphics "one machine": 8 stages that turn an idea into a believable world
STAGES = [
 ("Represent","give the world a shape a computer can hold",
   ["Geometry Processing & Meshes","Neural Fields & Representations"]),
 ("Simulate","let physics move it — bend, break, splash, flow",
   ["Physical Simulation","Fluids, Smoke & Granular","Cloth, Hair & Fibers"]),
 ("Animate","give characters motion and life",
   ["Character Animation & Motion","Faces & Avatars"]),
 ("Dress","describe how every surface reflects and scatters light",
   ["Appearance, Materials & BRDF"]),
 ("Light","transport light through the scene to make an image",
   ["Rendering & Light Transport","Neural Rendering & Radiance Fields"]),
 ("Generate","conjure new shapes, textures, and scenes from a prompt or a sketch",
   ["Generative 3D & Diffusion","Sketching & Vector / 2D"]),
 ("Capture","pull the real world back in through a camera or sensor",
   ["Computational Photography & Imaging"]),
 ("Show & make","push it out to a headset, a display, or a 3D printer",
   ["VR/AR & Displays","Fabrication & 3D Printing","Sound & Multisensory"]),
]
STAGE_OF = {th:i for i,(_,_,ths) in enumerate(STAGES) for th in ths}
COLORS = ["#4FA8B8","#6C8CE0","#8B7BE0","#C77DBB","#D98A5B","#5BB98A","#C9A94F","#8493A8"]

# one plain framing line per theme (first-principles, plain language)
FRAME = {
 "Geometry Processing & Meshes":"The biggest slice of the field: how to store, clean, cut, and reshape the triangle meshes that everything else is built on.",
 "Physical Simulation":"Make a computer obey Newton — so cloth drapes, jelly wobbles, and structures bend the way real matter does.",
 "Character Animation & Motion":"Turn a rigid 3D model into something that walks, gestures, and moves like a living thing.",
 "Appearance, Materials & BRDF":"Pin down exactly how each surface sends light back to the eye — the difference between plastic, skin, velvet, and gold.",
 "Generative 3D & Diffusion":"Ask for a shape or a scene and have a model dream it up, the 3D cousin of image generators.",
 "Rendering & Light Transport":"Follow light as it bounces through a scene and add it all up into a photograph that never existed.",
 "Faces & Avatars":"Capture and rebuild a human face and body faithfully enough to stand in for the real person.",
 "Computational Photography & Imaging":"Squeeze a better picture out of imperfect cameras by computing what the sensor alone could not capture.",
 "Fluids, Smoke & Granular":"The hardest simulation of all — water, smoke, and sand, where billions of particles move as one.",
 "VR/AR & Displays":"Get a convincing image all the way to the eye through headsets, holograms, and new kinds of screens.",
 "Cloth, Hair & Fibers":"Handle the fiddliest matter in graphics — thousands of interacting strands and threads.",
 "Sketching & Vector / 2D":"Meet the artist where they draw: strokes, curves, and flat 2D art, made smart.",
 "Neural Rendering & Radiance Fields":"Skip the mesh entirely — learn the scene as a field of color and density you can fly a camera through.",
 "Fabrication & 3D Printing":"Close the loop from pixels to atoms: design something on screen so it can actually be manufactured.",
 "Neural Fields & Representations":"Store a shape not as points but as a little neural network you can query anywhere, at any resolution.",
 "Sound & Multisensory":"Reach past the eyes — sound, touch, and haptics that make a virtual world felt as well as seen.",
}

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} · SIGGRAPH 2026</title>
<style>
:root{{--bg:#0E1420;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--accent:#4FA8B8;--line:rgba(150,170,205,.14);--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,system-ui,Segoe UI,Roboto,sans-serif}}
a{{color:var(--accent)}}
.top{{border-bottom:1px solid var(--line);padding:12px 22px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-family:var(--mono);font-size:13px}}
.top .brand{{font-weight:700;color:var(--ink);text-decoration:none;margin-right:8px}}
.top a{{text-decoration:none;color:var(--soft)}}.top a.on{{color:var(--accent)}}
main{{max-width:1080px;margin:0 auto;padding:28px 22px 80px}}
.kick{{font-family:var(--mono);font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.08em}}
h1{{font-size:30px;margin:6px 0 10px}}.lead{{font-size:18px;color:var(--soft);max-width:820px;line-height:1.6}}
.stage{{border:1px solid var(--line);border-radius:12px;padding:15px 18px;margin:14px 0;background:rgba(255,255,255,.015)}}
.stage h3{{margin:0 0 3px;font-size:17px}}.stage .sub{{color:var(--dim);font-size:14px;margin:0 0 11px}}
.snum{{font-family:var(--mono);font-size:12px;color:#0E1420;padding:2px 9px;border-radius:20px;margin-right:9px;font-weight:700}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.chip{{display:block;text-decoration:none;border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:rgba(255,255,255,.02);min-width:180px}}
.chip:hover{{border-color:var(--accent)}}
.chip .nm{{color:var(--ink);font-size:14px;font-weight:600}}
.chip .fr{{color:var(--dim);font-size:12.5px;margin-top:3px;line-height:1.4}}
.chip .n{{float:right;font-family:var(--mono);font-size:11px;color:var(--accent)}}
.thesis{{border-top:1px solid var(--line);margin-top:26px;padding-top:18px;color:var(--soft);max-width:80ch}}
.legend{{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0;font-size:13px;color:var(--soft)}}
.legend span{{display:inline-flex;align-items:center;gap:6px}}.dot{{width:11px;height:11px;border-radius:50%}}
canvas{{width:100%;height:640px;border:1px solid var(--line);border-radius:12px;display:block;background:#0b1018}}
</style></head><body>
<div class="top"><a class="brand" href="index.html">SIGGRAPH 2026</a>
<a href="course.html">Course</a><a href="deep.html">Deep read</a><a href="explorer.html">Explorer</a>
<a href="math.html">Mathematics</a><a class="{h}" href="hub.html">The Machine</a><a class="{g}" href="idea-graph.html">Idea Graph</a></div>
<main>
"""
FOOT = "</main></body></html>\n"

def chip(th):
    n = CNT.get(th, "")
    return (f'<a class="chip" href="deep.html"><span class="n">{n}</span>'
            f'<div class="nm">{esc(th)}</div><div class="fr">{esc(FRAME.get(th,""))}</div></a>')

def build_hub():
    o = [HEAD.format(title="The Machine", h="on", g="")]
    o.append('<div class="kick">the one machine of computer graphics</div>')
    o.append('<h1>All 16 themes are one pipeline</h1>')
    o.append('<p class="lead">The 153 SIGGRAPH 2026 papers scatter across sixteen themes, but read top to bottom they are one machine: the pipeline that turns an idea into a believable virtual world — represent it, simulate it, animate it, dress it in materials, light it, generate more of it, capture the real world into it, and finally show or fabricate it. Each tile carries its share of the papers and opens the deep read.</p>')
    for i,(name,sub,ths) in enumerate(STAGES):
        c = COLORS[i]
        o.append(f'<div class="stage"><h3><span class="snum" style="background:{c}">{i+1:02d}</span>{esc(name)}</h3>'
                 f'<p class="sub">{esc(sub)}</p><div class="chips">'
                 + "".join(chip(t) for t in ths) + '</div></div>')
    o.append('<p class="thesis"><strong>The through-line:</strong> graphics is the science of faking reality convincingly and cheaply. Every theme is one place where a brute-force physical truth (every light ray, every fiber, every atom of water) is too expensive, so the field replaces it with a structure a computer can afford — a mesh, a material model, a learned field, a few importance-sampled rays — while guarding the one property that would betray the fake if it were lost. Learn where each theme sits in this pipeline and the conference stops being a list and becomes a map.</p>')
    o.append(FOOT)
    (ROOT/"hub.html").write_text("\n".join(o))

def build_graph():
    names = [t["theme"] for t in TH]
    pairs = collections.Counter()
    for a,b in itertools.combinations(names,2):
        s = len(EX[a] & EX[b])
        if s: pairs[(a,b)] = s
    nodes = [{"id":t,"n":CNT[t],"stage":STAGE_OF.get(t,7),"fr":FRAME.get(t,"")} for t in names]
    edges = [{"s":a,"t":b,"w":w} for (a,b),w in pairs.items()]
    o = [HEAD.format(title="Idea Graph", h="", g="on")]
    o.append('<div class="kick">the idea graph</div>')
    o.append('<h1>The 16 themes, wired by shared papers</h1>')
    o.append('<p class="lead">Every theme is a dot, sized by how many papers it holds and colored by where it sits in the <a href="hub.html">pipeline</a>. A line joins two themes when the same paper lives in both — the field\'s real bridges, where materials meet simulation or generation meets photography. Drag a dot; click it to jump to the deep read.</p>')
    o.append('<div class="legend">' + "".join(
        f'<span><i class="dot" style="background:{COLORS[i]}"></i>{esc(STAGES[i][0])}</span>' for i in range(len(STAGES))) + '</div>')
    o.append('<canvas id="g"></canvas>')
    o.append(f'<script>const NODES={json.dumps(nodes)};const EDGES={json.dumps(edges)};const COLORS={json.dumps(COLORS)};</script>')
    o.append(GRAPH_JS)
    o.append(FOOT)
    (ROOT/"idea-graph.html").write_text("\n".join(o))

GRAPH_JS = r"""<script>
const cv=document.getElementById('g'),ctx=cv.getContext('2d');let W,H;
function size(){const r=cv.getBoundingClientRect();W=cv.width=r.width*devicePixelRatio;H=cv.height=r.height*devicePixelRatio;ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);}
size();addEventListener('resize',size);const w=()=>cv.getBoundingClientRect().width,h=()=>cv.getBoundingClientRect().height;
NODES.forEach((n,i)=>{n.x=w()/2+Math.cos(i)*200+Math.random()*30;n.y=h()/2+Math.sin(i*1.6)*180+Math.random()*30;n.vx=0;n.vy=0;n.r=6+Math.sqrt(n.n)*1.7;});
const id2i={};NODES.forEach((n,i)=>id2i[n.id]=i);
const E=EDGES.map(e=>({s:id2i[e.s],t:id2i[e.t],w:e.w}));let drag=null,hover=null;
function tick(){for(let i=0;i<NODES.length;i++){const a=NODES[i];for(let j=i+1;j<NODES.length;j++){const b=NODES[j];let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;const rep=2600/(d*d);a.vx-=dx/d*rep;a.vy-=dy/d*rep;b.vx+=dx/d*rep;b.vy+=dy/d*rep;}}
for(const e of E){const a=NODES[e.s],b=NODES[e.t];let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;const f=(d-120)*0.01*e.w;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
const cx=w()/2,cy=h()/2;for(const n of NODES){n.vx+=(cx-n.x)*0.003;n.vy+=(cy-n.y)*0.003;n.vx*=0.86;n.vy*=0.86;if(n!==drag){n.x+=n.vx;n.y+=n.vy;}n.x=Math.max(50,Math.min(w()-50,n.x));n.y=Math.max(30,Math.min(h()-30,n.y));}}
function draw(){ctx.clearRect(0,0,w(),h());for(const e of E){const a=NODES[e.s],b=NODES[e.t];ctx.strokeStyle='rgba(79,168,184,'+(0.10+0.16*e.w)+')';ctx.lineWidth=e.w;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
for(const n of NODES){ctx.beginPath();ctx.arc(n.x,n.y,n===hover?n.r+2:n.r,0,7);ctx.fillStyle=COLORS[n.stage];ctx.fill();ctx.strokeStyle='#0b1018';ctx.lineWidth=2;ctx.stroke();
ctx.fillStyle=n===hover?'#EAEEF4':'#B4BFD0';ctx.font=(n===hover?'700 ':'')+'12px system-ui';ctx.fillText(n.id,n.x+n.r+4,n.y+4);}}
function loop(){tick();draw();requestAnimationFrame(loop);}loop();
function at(x,y){for(const n of NODES){if(Math.hypot(n.x-x,n.y-y)<n.r+4)return n;}return null;}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;if(drag){drag.x=x;drag.y=y;}else{hover=at(x,y);cv.style.cursor=hover?'pointer':'default';}});
cv.addEventListener('mousedown',e=>{const r=cv.getBoundingClientRect();drag=at(e.clientX-r.left,e.clientY-r.top);});
addEventListener('mouseup',()=>drag=null);
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const n=at(e.clientX-r.left,e.clientY-r.top);if(n)location.href='deep.html';});
</script>"""

def wire_index():
    p = ROOT/"index.html"; t = p.read_text()
    if 'hub.html' in t: return
    anchor = '<a href="math.html"'
    btn = ('<a href="hub.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">&rarr; the one machine</a>'
           '<a href="idea-graph.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">&rarr; the idea graph</a>')
    i = t.find(anchor)
    if i != -1:
        # insert the two buttons right before the math.html button
        t = t[:i] + btn + t[i:]
        p.write_text(t); print("wired hub+idea-graph buttons into index.html")

def main():
    build_hub(); build_graph(); wire_index()
    print("built hub.html + idea-graph.html")

if __name__ == "__main__":
    main()

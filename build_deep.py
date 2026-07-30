# -*- coding: utf-8 -*-
"""
Build the first-principles "deep read" of SIGGRAPH 2026: the whole conference as
the life of a virtual object — describe → behave → look → capture → invent →
present. Plain-language framing (written here), every paper placed under its stage
with its one-line contribution (from the LLM analysis). No jargon in the framing.
"""
import json, os, re, html
from subtheme_framing import FRAMING
HERE = os.path.dirname(os.path.abspath(__file__))
papers_raw = json.load(open(os.path.join(HERE, "data", "papers.json")))["papers"]
analysis = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]
PLAIN = json.load(open(os.path.join(HERE, "data", "plain.json"))) if os.path.exists(os.path.join(HERE, "data", "plain.json")) else {}
def esc(s): return html.escape(str(s or ""))

# join analysis (problem/approach/contribution) with abstract by title
abst = {p["title"].lower(): (p.get("abstract") or "") for p in papers_raw}
for a in analysis:
    a["abstract"] = abst.get(a["title"].lower(), "")

# theme taxonomy (same as mine_themes) — assign each paper its themes
THEMES = {
 "Neural Rendering & Radiance Fields": [r"neural render", r"radiance field", r"\bnerf\b", r"gaussian splat", r"\b3dgs\b", r"novel view", r"view synthesis", r"differentiable render"],
 "Generative 3D & Diffusion": [r"diffusion", r"generative", r"text[- ]to[- ]3d", r"\bgan\b", r"score[- ]based", r"flow matching", r"latent.*3d", r"asset generation", r"3d generation"],
 "Geometry Processing & Meshes": [r"\bmesh\b", r"geometry process", r"remesh", r"parameteriz", r"\buv\b", r"surface reconstruct", r"point cloud", r"implicit surface", r"\bsdf\b", r"subdivision", r"quad"],
 "Physical Simulation": [r"simulation", r"physics", r"finite element", r"\bfem\b", r"\bmpm\b", r"\bpbd\b", r"collision", r"contact", r"elastic", r"deformabl", r"rigid body"],
 "Fluids, Smoke & Granular": [r"fluid", r"smoke", r"\bsph\b", r"lattice boltzmann", r"\blbm\b", r"granular", r"sand", r"liquid", r"free surface", r"navier"],
 "Cloth, Hair & Fibers": [r"\bcloth\b", r"\byarn\b", r"\bhair\b", r"fiber", r"knit", r"woven", r"garment", r"textile"],
 "Character Animation & Motion": [r"animation", r"\bmotion\b", r"character", r"skinning", r"rigging", r"skeletal", r"locomotion", r"motion capture", r"retarget"],
 "Appearance, Materials & BRDF": [r"\bbrdf\b", r"material", r"appearance", r"reflectance", r"\bbssrdf\b", r"svbrdf", r"texture synthesis", r"shading model", r"subsurface"],
 "Rendering & Light Transport": [r"path tracing", r"light transport", r"monte carlo", r"ray tracing", r"global illumination", r"importance sampl", r"denois", r"real[- ]?time render", r"rasteriz", r"radiosity"],
 "Computational Photography & Imaging": [r"computational photograph", r"\bhdr\b", r"deblur", r"image[- ]based", r"tone mapping", r"camera", r"relighting", r"super[- ]?resolution", r"denoising.*image"],
 "Fabrication & 3D Printing": [r"fabricat", r"3d print", r"additive manufactur", r"cnc", r"knitting machine", r"self[- ]?assembl"],
 "VR/AR & Displays": [r"\bvr\b", r"\bar\b", r"virtual reality", r"augmented reality", r"holograph", r"display", r"head[- ]?mounted", r"stereo", r"light field display", r"perception"],
 "Faces & Avatars": [r"\bface\b", r"avatar", r"facial", r"head avatar", r"portrait", r"expression", r"talking head"],
 "Sketching & Vector / 2D": [r"sketch", r"vector graphic", r"\bsvg\b", r"line drawing", r"illustration", r"stroke", r"2d animation", r"stylization"],
 "Sound & Multisensory": [r"\bsound\b", r"audio", r"acoustic", r"haptic", r"multisensory"],
 "Neural Fields & Representations": [r"neural field", r"implicit neural", r"coordinate network", r"positional encoding", r"neural representation"],
}
C = {t: [re.compile(p, re.I) for p in pats] for t, pats in THEMES.items()}
# match specific / appearance themes before broad grabbers (geometry, simulation,
# generative) so a "material" or "rendering" paper isn't stolen by a mesh keyword.
PRIORITY = [
 "Fabrication & 3D Printing", "VR/AR & Displays", "Sound & Multisensory", "Sketching & Vector / 2D",
 "Faces & Avatars", "Cloth, Hair & Fibers", "Fluids, Smoke & Granular", "Computational Photography & Imaging",
 "Appearance, Materials & BRDF", "Rendering & Light Transport", "Character Animation & Motion",
 "Neural Rendering & Radiance Fields", "Generative 3D & Diffusion",
 "Physical Simulation", "Geometry Processing & Meshes", "Neural Fields & Representations",
]
def theme_of(a):
    text = (a["title"] + " " + a["abstract"]).lower()
    for t in PRIORITY:
        if any(x.search(text) for x in C[t]):
            return t
    return "Other"

for a in analysis:
    a["theme"] = theme_of(a)

# ---- the six acts of the lifecycle, with plain-language framing --------------
ACTS = [
 {"n": "I", "title": "Describing a shape",
  "themes": ["Geometry Processing & Meshes", "Neural Fields & Representations"],
  "problem": "Before a computer can do anything with an object, it needs a way to hold its shape — and there is no obvious one. The real world is smooth and endlessly detailed; a computer has only numbers and finite memory. So the very first question of graphics is quietly hard: how do you store a shape faithfully, and then clean it, measure it, simplify it or edit it without the whole thing falling apart?",
  "approach": "The workhorse answer is to cover a surface in a fine shell of tiny flat triangles — a mesh — fine enough to look smooth. A newer answer describes a shape not as a pile of triangles but as a rule a computer can evaluate anywhere (\"is this point inside or outside, and how far to the surface?\"). This year's work is mostly about doing all of this faster, cleaner, and more automatically — better triangles, quicker measurements, shapes that repair and simplify themselves."},
 {"n": "II", "title": "Making it behave",
  "themes": ["Physical Simulation", "Fluids, Smoke & Granular", "Cloth, Hair & Fibers", "Character Animation & Motion"],
  "problem": "A static shape is dead. To feel real, it has to move the way matter actually moves — cloth folds and creases, water splashes and settles, sand piles and slides, a character walks and catches its balance. That behavior is governed by the physics of the real world, which we can write down as equations but which are punishingly expensive to compute step after step, and which tend to blow up into nonsense if you cut the wrong corner.",
  "approach": "Two broad strategies. One is to simulate the physics directly, using numerical tricks that take the biggest time-steps they can get away with while staying stable, and that handle the hard moments — things touching, colliding, tangling — without exploding. The other is to learn motion from examples, especially for characters, so a body can move naturally and react on its own. This year leans on coupling different materials together (water with sand, cloth with bodies), going faster, and staying stable under stress."},
 {"n": "III", "title": "Making it look right",
  "themes": ["Appearance, Materials & BRDF", "Rendering & Light Transport"],
  "problem": "You only see an object because light bounces off it into your eye. So to turn a shape into a picture, the computer has to act out that journey of light — how each surface answers light differently (matte paper, polished metal, human skin all behave unlike each other) and how light ricochets around a scene, bouncing off one thing to softly illuminate another. Done the obvious way this is astronomically expensive, because light goes everywhere and most of it never reaches the camera.",
  "approach": "Split the problem in two. First, compact models of how a given surface reflects light, so you can capture the look of a material without tracking every microscopic detail. Second, trace only the light paths that matter — follow rays from the eye, spend effort where it changes the image most, and let a cleanup step remove the leftover speckle. The 2026 work pushes all of this toward being both more accurate and fast enough to happen while you watch."},
 {"n": "IV", "title": "Getting reality in",
  "themes": ["Computational Photography & Imaging", "Faces & Avatars"],
  "problem": "Often you do not want to build a world by hand — you want to capture the real one. But a camera is a narrow, lossy window: it sees a limited range of brightness, from one viewpoint, frozen in a blur if anything moved, under whatever light happened to be there. Reality is far richer than any single photo. The problem is to recover the fuller truth — a scene's real range of light, a person's face and how it would look under new lighting — from imperfect, incomplete pictures.",
  "approach": "Combine many limited shots into one richer whole, and lean on what we already know about how the world and human faces are built to fill the gaps sensibly rather than inventing them. This year that shows up as squeezing a wider range of light out of ordinary cameras, relighting captured scenes and people, and turning photos or video of a person into a controllable stand-in you can pose and light freely."},
 {"n": "V", "title": "Letting the machine invent it",
  "themes": ["Generative 3D & Diffusion", "Neural Rendering & Radiance Fields"],
  "problem": "Building 3D content by hand is slow and needs rare expertise — every shape, texture, and scene is painstaking craft. The newer ambition is to have the computer create it: hand it a description or a few images and get back a usable shape, a material, a whole scene. And once a scene has been captured, to be able to re-photograph it from any new angle, as if you had really been standing there.",
  "approach": "The same wave of generative models that learned to conjure images — by starting from noise and steadily refining it toward something plausible — is now turning out shapes, textures, and scenes. Alongside it, a way of storing a captured scene not as fixed geometry but as something a computer can render afresh from any viewpoint. This is the fastest-rising corner of graphics, and the one most visibly reshaped by machine learning."},
 {"n": "VI", "title": "Getting it back out",
  "themes": ["VR/AR & Displays", "Fabrication & 3D Printing", "Sketching & Vector / 2D", "Sound & Multisensory"],
  "problem": "A virtual world is useless trapped inside the computer. It has to reach a human — through a screen, a headset, sound, or touch — or cross over into a real physical object that can be built. Each of those channels has stubborn physical limits: a display can only show so much, a printer or knitting machine can only make certain shapes, an artist's pen expects to behave like a pen. The problem is to present the virtual thing convincingly, or manufacture it faithfully, within what the hardware and the human senses actually allow.",
  "approach": "Design the output around its real constraints: displays tuned to how human eyes and perception actually work, fabrication that plans backward from what a machine can physically produce, and drawing and 2D tools that meet artists in the way they already work. Here the virtual finally becomes something a person can see, wear, hear, hold, or build."},
]

def paper_row(a):
    pl = PLAIN.get(str(a.get("gid")))
    if pl:
        body = (f"<div class='ppa'><span class='pk'>problem</span> {esc(pl['p'])}</div>"
                f"<div class='ppa'><span class='pk ap'>approach</span> {esc(pl['a'])}</div>")
    else:
        body = f"<div class='pc'>{esc(a.get('contribution') or a.get('problem') or '')}</div>"
    return f"<div class='pr'><div class='pt'>{esc(a['title'])}</div>{body}</div>"

placed = set()
def act_papers(themes):
    rows = []
    for t in themes:
        group = [a for a in analysis if a["theme"] == t and a["title"] not in placed]
        if not group: continue
        for a in group: placed.add(a["title"])
        rows.append((t, group))
    return rows

def act_html(act):
    groups = act_papers(act["themes"])
    ncount = sum(len(g) for _, g in groups)
    inner = ""
    for t, group in groups:
        inner += f"<div class='sub'>{esc(t)} <span class='sn'>{len(group)}</span></div>"
        fr = FRAMING.get(t)
        if fr:
            inner += f"<p class='subframe'><b>Problem.</b> {fr[0]} <b>Approach.</b> {fr[1]}</p>"
        inner += "".join(paper_row(a) for a in group)
    return f"""<section id="act{act['n']}">
  <div class="anum">Stage {act['n']} · {ncount} papers</div>
  <h2>{esc(act['title'])}</h2>
  <p class="prob"><b>The problem.</b> {act['problem']}</p>
  <p class="appr"><b>The approach.</b> {act['approach']}</p>
  <div class="papers">{inner}</div>
</section>"""

acts_rendered = "".join(act_html(a) for a in ACTS)
# any leftover (Other / themes not in an act)
leftover = [a for a in analysis if a["title"] not in placed]
if leftover:
    rows = "".join(paper_row(a) for a in leftover)
    acts_rendered += f"""<section><div class="anum">Also · {len(leftover)} papers</div>
    <h2>Everything else</h2><p class="prob">Papers that sit across or between the stages above — the field's long tail.</p>
    <div class="papers">{rows}</div></section>"""

toc = "".join(f"<a href='#act{a['n']}'><b>{a['n']}.</b> {esc(a['title'])}</a>" for a in ACTS)

P = f"""<meta charset="utf-8">
<title>SIGGRAPH 2026 · the deep read</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}.mono{{font-family:var(--mono)}}a{{color:var(--accent)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:12px 0 0;color:#fff;letter-spacing:-.02em}}
.dek{{font-size:20px;color:var(--soft);margin-top:18px;max-width:64ch;font-family:var(--serif);line-height:1.5}}
.lead{{font-family:var(--serif);font-size:21px;line-height:1.5;color:#fff;margin:18px 0}}
section{{padding:44px 0;border-top:1px solid var(--line)}}
.anum{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}
h2{{font-family:var(--serif);font-size:30px;margin:0 0 14px;color:#fff}}
.prob,.appr{{font-size:16.5px}}
.toc{{font-family:var(--mono);font-size:13px;color:var(--dim);margin:22px 0 0;line-height:2}}.toc a{{color:var(--soft);text-decoration:none;display:block}}.toc a:hover{{color:var(--accent)}}.toc b{{color:var(--accent);font-weight:400}}
.papers{{margin-top:20px}}
.sub{{font-family:var(--mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--amber);margin:22px 0 8px;border-bottom:1px solid var(--line);padding-bottom:5px}}.sub .sn{{color:var(--faint);margin-left:4px}}
.subframe{{font-size:14.5px;color:var(--soft);margin:0 0 12px;padding:10px 14px;background:var(--bg2);border:1px solid var(--line);border-left:2px solid var(--amber);border-radius:9px}}.subframe b{{color:var(--amber);font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase}}
.pr{{padding:9px 0;border-bottom:1px solid rgba(150,170,205,.07)}}
.pt{{font-family:var(--serif);font-size:16.5px;color:#fff;line-height:1.3}}
.pc{{font-size:14px;color:var(--soft);margin-top:2px}}
.ppa{{font-size:13.5px;color:var(--soft);margin-top:3px;padding-left:70px;text-indent:-70px;line-height:1.5}}
.pk{{display:inline-block;width:62px;font-family:var(--mono);font-size:9.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--rose);text-align:right;margin-right:8px}}.pk.ap{{color:var(--accent)}}
.pm{{font-family:var(--mono);font-size:11px;color:var(--faint);margin-top:3px}}
.aha{{font-family:var(--serif);font-size:23px;line-height:1.45;color:#fff;border-left:3px solid var(--accent);padding-left:20px;margin:14px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}
</style>
<div class="wrap">
<header style="padding:0 0 8px">
  <div class="kick">SIGGRAPH 2026 · the deep read · first principles</div>
  <h1>The life of a virtual object.</h1>
  <p class="dek">All {len(analysis)} technical papers of SIGGRAPH 2026, arranged not as a list of topics but as one story — the journey every made-up thing takes inside a computer, from a bare shape to something you can see, wear, or build. Read straight through, the whole field turns out to be answering a single question in six stages.</p>
  <p class="lead">How do you teach a computer to make and move a believable world — one that looks and behaves like reality, but that a person can create and control?</p>
  <p>That's the whole of computer graphics on one line. Everything below is a piece of the answer. A virtual object has to be <em>described</em> as a shape, made to <em>behave</em> like real matter, <em>lit</em> so a camera can see it; often it's <em>captured</em> from the real world, increasingly <em>invented</em> by the machine itself, and finally <em>delivered</em> back to a human or a workshop. Six stages, one lifecycle — and this year, a single new thread (machine learning, and especially the kind that generates) running through every one of them.</p>
  <div class="toc">{toc}</div>
</header>
{acts_rendered}
<section>
  <div class="anum">Connecting the dots</div>
  <h2>One lifecycle, one shift</h2>
  <p>Lay the six stages end to end and the whole conference is a single pipeline: a thing is <b>described</b>, made to <b>behave</b>, <b>lit</b> to be seen, <b>captured</b> from reality, <b>invented</b> by the machine, and <b>delivered</b> to the world. Each stage exists because the one before it left something undone — a shape is nothing until it moves, motion is invisible until it's lit, and lighting a hand-built world is pointless if you could have captured or generated one instead.</p>
  <p>And one change cuts across all six. The old craft of graphics was built from physics and geometry — equations for light, meshes for shape, simulations for motion. This year, a learned layer sits on top of every stage: the machine now helps describe shapes, predict motion, clean up lighting, fill in captured reality, and — most of all — invent new content outright. The single most-used tool across these {len(analysis)} papers is the generative kind of model that a few years ago only made pictures.</p>
  <p class="aha">Computer graphics has always been the craft of making a believable world by hand, one physical rule at a time. Its 2026 turn is the same craft learning to generate itself — geometry and physics still at the core, but a machine that increasingly describes, captures, and invents the world for us.</p>
  <p class="src">All {len(analysis)} SIGGRAPH 2026 technical papers (ACM Transactions on Graphics), each read for its contribution by a language model; stages and framing written from first principles. Browse/search them in the <a href="explorer.html">explorer</a> · overview in the <a href="index.html">landscape</a>.</p>
</section>
</div>
"""
open(os.path.join(HERE, "site", "deep.html"), "w", encoding="utf-8").write(P)
placed_n = len(placed) + len(leftover)
print("wrote site/deep.html ·", len(P)//1024, "KB · papers placed:", placed_n, "· FFFD:", P.count("�"))

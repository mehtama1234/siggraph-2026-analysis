# -*- coding: utf-8 -*-
"""The mathematics of computer graphics, from first principles: the small set of
mathematical ideas that recur across SIGGRAPH 2026, each explained plainly, with
every paper placed under the idea it leans on and its own plain-language math note."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
MATH = json.load(open(os.path.join(HERE, "data", "math.json")))
_wm = os.path.join(HERE, "data", "whymath.json")
WHYMATH = json.load(open(_wm)) if os.path.exists(_wm) else {}
_dw = os.path.join(HERE, "data", "deepwhy.json")
DEEPWHY = json.load(open(_dw)) if os.path.exists(_dw) else {}
_rc = os.path.join(HERE, "data", "rich.json")
RICH = json.load(open(_rc)) if os.path.exists(_rc) else {}
_cr = os.path.join(HERE, "data", "concepts_rich.json")
CONCEPTS = json.load(open(_cr)) if os.path.exists(_cr) else {}
_sy = os.path.join(HERE, "data", "synth_out.json")
SYNTH = json.load(open(_sy)) if os.path.exists(_sy) else {}
analysis = json.load(open(os.path.join(HERE, "data", "analysis.json")))["papers"]
def esc(s): return html.escape(str(s or ""))

def story_html(gid):
    r = RICH.get(str(gid))
    if not r: return ""
    parts = [("bp","the big picture"),("wh","why it's hard"),("ap","what they do"),
             ("ww","why it works"),("po","the payoff")]
    secs = "".join(f"<div class='sec {k}'><span class='lbl'>{lbl}</span><p>{esc(r.get(k))}</p></div>"
                   for k,lbl in parts if r.get(k))
    return f"<details class='story'><summary>the full first-principles story</summary>{secs}</details>"

# concept-level "why it works" — the underlying mathematical principle, first-principles.
WHY = {
 "modes": "It works because real shapes and images are not random static — they pour almost all of their content into a few smooth, large-scale patterns and leave only a little in the fine, jagged ones. So keeping the handful of dominant patterns and dropping the rest changes almost nothing you would ever notice. The deeper truth: the world is mostly smooth, and smoothness means the information lives in the coarse patterns.",
 "curve": "It works because how a surface curves is an intrinsic fact about it — it does not depend on where you place it, how you rotate it, or how finely you chop it into pieces. That makes curvature a true, stable property you can measure and then preserve. Deform a shape while keeping its curvature story intact and it still reads as the same material; smooth by evening out curvature and you remove bumps without inventing new features.",
 "integrate": "It works because although the total is a sum over infinitely many contributions, they are not equally important — most of the light, most of the mass, is concentrated. And a continuous total can always be trapped between an under-estimate and an over-estimate that both tighten as you chop it into finer pieces. So a finite sum of small pieces is guaranteed to close in on the true infinite total: you never reach infinity, you just get as close as you like.",
 "random": "It works because of one quiet guarantee: the average of many independent random samples equals, on average, exactly the true total you are chasing — the randomness cancels itself out. And the leftover error shrinks in a predictable way as you add samples, so a noisy guess sharpens into a reliable one just by taking more. Aim the samples where the answer varies most and that error shrinks faster still.",
 "time": "It works because over a short enough moment almost anything changes nearly in a straight line — its rate of change right now is a good guide to where it will be an instant later. So one tiny step forward using the current rate is accurate, and repeating it traces the true motion. Keep the steps small and the small errors stay small instead of piling up into nonsense — which is the entire discipline of simulation.",
 "optimize": "It works because the slope of how-wrong always points the way that makes things worse, so stepping the opposite way can only improve — and you halt exactly where no small change helps, a resting point. When the how-wrong score is shaped like a single bowl, that resting point is the one best answer; even when it is bumpier you reliably fall into a good one. Physics leans on the same truth: real things settle into their lowest-energy state.",
 "solve": "It works because a genuine physical balance — a hanging cloth, a shape at rest — has exactly one state where every little force cancels against its neighbours at the same time. Writing that forces-cancel-here condition at every point gives a web of equations whose single joint solution IS that balanced state. There is no guessing involved: the equations pin down the one arrangement that satisfies everyone at once, and solving them finds it exactly.",
 "connect": "It works because smooth things do not jump: between two nearby known values the truth stays close to their blend, so filling the gaps with a gentle blend is rarely far off. And the relationships that matter — who is nearest, how things connect, how one shape maps onto another — survive the honest coordinate changes graphics uses, so you can carry a problem into a convenient frame, solve it there, and carry the answer back unharmed.",
 "learn": "It works because of a bargain between simplicity and coverage: when the real rule is far simpler than the mountain of data, and the examples you show cover the territory well, any rule forced to match all those examples has almost no room left to be wrong on the new ones — it is squeezed toward the true rule. It fails in exactly the opposite case: when the rule is as tangled as the data, or the examples leave whole regions unseen.",
}

# concept groups (my plain-language first-principles narrative), priority order:
# specific/foundational first, generic "learning from examples" last.
CG = [
 {"key":"modes","title":"Finding a thing's natural patterns",
  "tags":["finding a shape's natural modes of vibration","frequencies and levels of detail"],
  "intro":"Every shape and every image is secretly built from a set of natural patterns — the basic ways a bell likes to ring, the coarse-to-fine layers of detail in a picture. Uncover those few underlying patterns and you can smooth, shrink, or animate a thing by working with its handful of important modes instead of all its raw data. The big-picture problem: raw data is bulky and noisy; its natural patterns are few and clean."},
 {"key":"curve","title":"Measuring the shape of a shape",
  "tags":["measuring how a surface curves"],
  "intro":"Before you can smooth, bend, or decorate a surface, you have to measure its local geometry — how sharply it curves here, how it stretches there, which way it faces. This is the mathematics of curvature: treating a surface not as a bag of points but as something with real, measurable geometric properties at every spot. Almost everything you'd do to a shape begins by measuring how it curves."},
 {"key":"integrate","title":"Adding up an infinity of tiny contributions",
  "tags":["adding up infinitely many tiny contributions"],
  "intro":"The color of a single pixel is really the total of all the light arriving there from every direction — a continuous infinity of contributions. The mass of a blob, the total force on a surface: the same shape of problem, a sum over something continuous. You can never add up infinitely many things exactly, so the whole game is approximating these totals accurately and cheaply — the quiet math behind turning light into a picture."},
 {"key":"random","title":"Smart randomness",
  "tags":["smart random sampling","probability and likelihood"],
  "intro":"When there are far too many possibilities to check them all — every path a ray of light might take, every plausible arrangement — you sample a well-chosen few at random and average the results, trusting the average to land near the true answer. The art is aiming your limited samples where they matter most, so the estimate sharpens quickly instead of staying speckled with noise. It's how graphics tames problems that are, strictly, infinite."},
 {"key":"time","title":"Stepping the world forward in time",
  "tags":["evolving a system step by step over time"],
  "intro":"To animate matter you rarely have a formula for where everything ends up. What you have is the rule for how things change from one instant to the next — this push, this flow, this collision. So you march forward in tiny time-steps, applying the rule again and again, and watch the motion emerge. The whole craft of simulation is taking the largest steps you can without the march spiralling into nonsense."},
 {"key":"optimize","title":"Finding the least-bad arrangement",
  "tags":["finding the arrangement with least energy","following the slope downhill to improve","constraints that must all hold at once"],
  "intro":"A remarkable share of graphics reduces to one move: invent a single number that measures how wrong a configuration is — how stretched the cloth, how far a shape sits from its target, how ugly a layout — then search for the arrangement that makes that number as small as possible, often while certain conditions must stay exactly satisfied. The usual way to search is to feel which small change lowers the number and keep stepping downhill until you can't do better. Score it, then minimise: this runs quietly under fitting, shaping, and much of learning."},
 {"key":"solve","title":"Making everything balance at once",
  "tags":["solving a big system of equations"],
  "intro":"Graphics is full of situations where thousands of little pieces each pull on their neighbours — every point of a cloth, every corner of a shape, every cell of a fluid — and you need the single overall state where all those local demands are satisfied at the same time. You can't settle one piece at a time; you have to solve them all together, as one enormous set of equations that must all hold at once. Much of the field's craft is making these giant balancing acts solvable fast enough to use."},
 {"key":"connect","title":"The connective tissue: between, across, and nearby",
  "tags":["filling in smoothly between known points","transformations and coordinate changes","distances and nearest matches","finding distances and nearest matches","networks and connections"],
  "intro":"A great deal of graphics is quieter bookkeeping between the samples you have: given values at a few points, produce a smooth field everywhere in between; carry a shape from one frame to the next; find what's nearest, or how things connect. Filling-in, coordinate changes, nearest-matches, connectivity — these are the connective tissue that ties the flashier machinery together, and they turn up in almost every paper somewhere."},
 {"key":"learn","title":"Learning the rule from examples",
  "tags":["learning a function from examples"],
  "intro":"Sometimes the rule connecting input to output is too tangled to write down — how a face should move, what a plausible texture looks like, how to fill a gap convincingly. So instead of deriving the rule, you show the computer a great many examples and let it settle on a rule that reproduces them, then trust it on new cases. This learned layer is now the single most common mathematical move in the field — but notice it usually sits on top of the older tools above, not in place of them."},
]

# assign each paper (with math data) to the first concept group its tags hit
title_of = {str(a.get("gid")): a["title"] for a in analysis}
placed = set(); groups = {c["key"]: [] for c in CG}
for gid, mv in MATH.items():
    tags = set(mv.get("tags") or [])
    for c in CG:
        if tags & set(c["tags"]):
            groups[c["key"]].append((gid, mv)); placed.add(gid); break

def concept_html(c):
    ps = groups[c["key"]]
    rows = ""
    for gid, mv in ps:
        why = WHYMATH.get(gid, "")
        rows += (f"<div class='pr'><div class='pt'>{esc(title_of.get(gid,''))}</div>"
                 f"<div class='mp'><span class='pk'>uses</span> {esc(mv['plain'])}</div>"
                 + (f"<div class='mp wy'><span class='pk wk'>why it works</span> {esc(why)}</div>" if why else "")
                 + (f"<details class='dw'><summary>the deeper reason</summary><div class='dwb'>{esc(DEEPWHY.get(gid,''))}</div></details>" if DEEPWHY.get(gid) else "")
                 + story_html(gid)
                 + "</div>")
    cr = CONCEPTS.get(c["key"])
    if cr and cr.get("idea"):
        head = (f"<p class='intro'>{esc(cr['idea'])}</p>"
                f"<div class='whybox'><div class='wt'>Why it works — the principle</div><p>{esc(cr.get('why') or WHY.get(c['key'],''))}</p></div>"
                + (f"<div class='dotsbox'><div class='wt dt'>Connecting the dots across these {len(ps)} papers</div><p>{esc(cr['dots'])}</p></div>" if cr.get('dots') else "")
                + (f"<div class='picture'><span class='pl'>picture it</span> {esc(cr['picture'])}</div>" if cr.get('picture') else ""))
    else:
        whybox = (f"<div class='whybox'><div class='wt'>Why it works — the principle</div><p>{esc(WHY[c['key']])}</p></div>"
                  if c["key"] in WHY else "")
        head = f"<p class='intro'>{c['intro']}</p>{whybox}"
    return (f"<section><div class='anum'>{len(ps)} papers</div><h2>{esc(c['title'])}</h2>"
            f"{head}<div class='papers'>{rows}</div></section>")

concepts_html = "".join(concept_html(c) for c in CG if groups[c["key"]])

def _mb(s):  # escape, then render **bold** -> <b> and *italic* -> <i>
    s = esc(s)
    parts = s.split("**")
    s = "".join(p if i % 2 == 0 else f"<b>{p}</b>" for i, p in enumerate(parts))
    parts = s.split("*")
    return "".join(p if i % 2 == 0 else f"<i>{p}</i>" for i, p in enumerate(parts))

synth_block = ""
if SYNTH.get("thread"):
    synth_block = (
        "<section class='synth'>"
        "<div class='anum'>the whole field in one page</div>"
        "<h2>A few ideas, one machine</h2>"
        f"<p class='synth-thread'>{_mb(SYNTH['thread'])}</p>"
        f"<div class='dotsbox'><div class='wt dt'>how the ideas fit together</div><p>{_mb(SYNTH['arc'])}</p></div>"
        f"<p class='aha'>{_mb(SYNTH['punchline'])}</p>"
        "</section>")
NA = len(MATH)
from collections import Counter
tc = Counter(t for v in MATH.values() for t in v["tags"])

P = f"""<meta charset="utf-8">
<title>SIGGRAPH 2026 · the mathematics of graphics</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;font-size:17px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}a{{color:var(--accent)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:12px 0 0;color:#fff;letter-spacing:-.02em}}
.dek{{font-size:20px;color:var(--soft);margin-top:18px;max-width:64ch;font-family:var(--serif);line-height:1.5}}
.lead{{font-family:var(--serif);font-size:21px;line-height:1.5;color:#fff;margin:18px 0}}
section{{padding:44px 0;border-top:1px solid var(--line)}}
.anum{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}
h2{{font-family:var(--serif);font-size:29px;margin:0 0 12px;color:#fff}}
.intro{{font-size:16.5px}}
.papers{{margin-top:16px}}
.pr{{padding:10px 0;border-bottom:1px solid rgba(150,170,205,.06)}}
.pt{{font-family:var(--serif);font-size:15.5px;color:#fff}}
.mp{{font-size:13.5px;color:var(--dim);margin-top:3px;padding-left:82px;text-indent:-82px}}
.mp.wy{{color:var(--soft)}}
.pk{{display:inline-block;width:74px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--faint);text-align:right;margin-right:8px}}.pk.wk{{color:var(--accent)}}
.dw{{margin:5px 0 0 82px}}.dw summary{{font-family:var(--mono);font-size:10.5px;color:var(--accent);cursor:pointer;list-style:none}}.dw summary::-webkit-details-marker{{display:none}}.dw summary::before{{content:'▸ ';color:var(--faint)}}.dw[open] summary::before{{content:'▾ '}}
.dwb{{font-size:13.5px;color:var(--soft);margin-top:6px;padding:10px 14px;background:rgba(79,168,184,.05);border-left:2px solid var(--line);border-radius:0 8px 8px 0;line-height:1.6}}
.story{{margin:5px 0 0 82px}}.story>summary{{font-family:var(--mono);font-size:10.5px;color:var(--accent);cursor:pointer;list-style:none}}.story>summary::-webkit-details-marker{{display:none}}.story>summary::before{{content:'▸ ';color:var(--faint)}}.story[open]>summary::before{{content:'▾ '}}
.story .sec{{margin:8px 0;padding-left:12px;border-left:1px solid var(--line)}}
.story .sec .lbl{{font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:2px}}
.story .sec.bp .lbl{{color:var(--accent)}}.story .sec.wh .lbl{{color:var(--rose)}}.story .sec.ap .lbl{{color:var(--viol)}}.story .sec.ww .lbl{{color:var(--amber)}}.story .sec.po .lbl{{color:#6FCF97}}
.story .sec p{{margin:0;color:var(--ink);font-size:13.5px;line-height:1.6}}
.whybox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.whybox .wt{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}}.whybox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.dotsbox{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--viol);border-radius:12px;padding:14px 18px;margin:6px 0 4px}}
.dotsbox .wt.dt{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--viol);margin-bottom:6px}}.dotsbox p{{margin:0;font-size:15.5px;color:var(--ink)}}
.picture{{font-size:15px;color:var(--soft);font-style:italic;margin:8px 0 4px;padding-left:14px;border-left:2px solid var(--amber)}}
.picture .pl{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);font-style:normal;margin-right:8px}}
.synth{{background:linear-gradient(180deg,rgba(79,168,184,.06),rgba(79,168,184,0));border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:8px 0 30px}}
.synth h2{{margin:2px 0 12px}}
.synth-thread{{font-size:17px;color:var(--ink);line-height:1.6}}
.bars{{margin-top:14px}}
.bar{{display:flex;align-items:center;gap:12px;margin:5px 0;font-family:var(--mono);font-size:12px}}
.bl{{width:280px;color:var(--soft);text-align:right;flex:0 0 auto}}
.bt{{flex:1;height:14px;background:rgba(150,170,205,.06);border-radius:4px;overflow:hidden}}.bf{{display:block;height:100%;background:#4FA8B8}}.bv{{width:34px;color:var(--ink)}}
@media(max-width:640px){{.bl{{width:150px;font-size:10.5px}}}}
.aha{{font-family:var(--serif);font-size:23px;line-height:1.45;color:#fff;border-left:3px solid var(--accent);padding-left:20px;margin:14px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}
</style>
<div class="wrap">
<header style="padding:0 0 8px">
  <div class="kick">SIGGRAPH 2026 · the mathematics of graphics · first principles</div>
  <h1>A small toolkit, used everywhere.</h1>
  <p class="dek">Computer graphics looks like many different crafts — cloth, light, faces, fluids, shapes. Underneath, nearly all of it runs on the same short list of mathematical ideas. This is that list — and for each one, not just <em>what</em> it is but <b>why it actually works</b>: the underlying principle that makes the trick valid. Every 2026 paper is placed under the idea it leans on, with a plain note on the math it uses and why that math is sound.</p>
  <p class="lead">How do you turn the messy, continuous, physical world into numbers a computer can balance, minimise, add up, and predict?</p>
  <p>That is what all of this math is for. A shape, a splash of water, a lit scene — each has to become a problem of a familiar mathematical shape before a computer can touch it. Read the ideas below in order and you'll see the same handful of moves recur across wildly different papers: balance everything at once, find the least-bad arrangement, step forward in time, add up an infinity of small things, sample cleverly, measure how things curve, find their natural patterns, and — increasingly — learn the rule from examples. A whole field, on one small toolkit.</p>
  <div class="bars"><div style="font-family:var(--mono);font-size:11px;color:var(--faint);margin-bottom:8px">HOW OFTEN EACH IDEA APPEARS (across {NA} papers, a paper can use several)</div>
  {''.join(f"<div class='bar'><span class='bl'>{esc(t)}</span><span class='bt'><span class='bf' style='width:{n/tc.most_common(1)[0][1]*100:.0f}%'></span></span><span class='bv'>{n}</span></div>" for t,n in tc.most_common())}</div>
</header>
{synth_block}
{concepts_html}
<section>
  <div class="anum">Connecting the dots</div>
  <h2>Different worlds, the same few moves</h2>
  <p>Line the ideas up and the surprise is how few there are. A cloth simulation and a shape-fitting method look nothing alike, yet both come down to finding the least-bad arrangement. A water splash and a stress test both march forward in time. A rendered image and a total force both add up an infinity of tiny contributions. The worlds differ; the mathematical moves repeat.</p>
  <p>And one move is spreading across all the others. Learning a rule from examples — the newest tool — is now the most common of all, but look closely and it rarely replaces the older math; it sits on top of it. A learned method still fills in between points, still measures how a surface curves, still minimises an error. The 2026 story isn't that graphics stopped being mathematical — it's that a learned layer now rides on the same small toolkit the field has always used.</p>
  <p class="aha">Every believable pixel and every convincing motion is one of a few mathematical questions in disguise: what balances, what is least, what comes next, what adds up — and, now, what can be learned. Master those few and the whole field opens up.</p>
  <p class="src">Each paper's core mathematical idea was read from its abstract by a language model and named from a fixed plain-language vocabulary; the framing of each idea is written from first principles. See the papers themselves in the <a href="deep.html">deep read</a> · the <a href="explorer.html">explorer</a> · the <a href="index.html">landscape</a>.</p>
</section>
</div>
"""
open(os.path.join(HERE, "site", "math.html"), "w", encoding="utf-8").write(P)
print("wrote site/math.html ·", len(P)//1024, "KB · placed:", len(placed), "of", NA, "· FFFD:", P.count("�"))

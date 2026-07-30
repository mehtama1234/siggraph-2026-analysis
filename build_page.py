import json, os, html
HERE=os.path.dirname(os.path.abspath(__file__))
T=json.load(open(os.path.join(HERE,"data","themes.json")))
S=json.load(open(os.path.join(HERE,"data","summary.json")))
def esc(s): return html.escape(str(s))
N=T["n_papers"]
def bars(items,key,nkey,col):
    mx=max(i[nkey] for i in items)
    return "".join(f"<div class='bar'><span class='bl'>{esc(i[key])}</span><span class='bt'><span class='bf' style='width:{i[nkey]/mx*100:.1f}%;background:{col}'></span></span><span class='bv'>{i[nkey]}</span></div>" for i in items)
def cards():
    out=""
    for t in T["themes"][:10]:
        ex="".join(f"<li>{esc(x)}</li>" for x in t["examples"][:3])
        out+=f"<div class='tcard'><div class='th'><span class='tn'>{esc(t['theme'])}</span><span class='tc'>{t['n']}</span></div><ul class='tex'>{ex}</ul></div>"
    return out
P=f"""<meta charset="utf-8">
<title>SIGGRAPH 2026 · the landscape</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;font-size:17px}}
.wrap{{max-width:900px;margin:0 auto;padding:0 24px}}
p{{color:var(--soft);margin:0 0 16px}}b{{color:var(--ink)}}em{{color:#fff;font-style:italic}}.mono{{font-family:var(--mono)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}}
h1{{font-family:var(--serif);font-size:clamp(32px,6vw,52px);line-height:1.05;margin:14px 0 0;color:#fff;letter-spacing:-.02em}}
h2{{font-family:var(--serif);font-size:27px;margin:0 0 6px;color:#fff}}
.dek{{font-size:19px;color:var(--soft);margin-top:18px;max-width:64ch}}
section{{padding:42px 0;border-top:1px solid var(--line)}}
.eye{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-bottom:12px}}
.stat{{display:flex;gap:26px;flex-wrap:wrap;margin:22px 0 6px}}.stat .sn{{font-family:var(--serif);font-size:34px;color:#fff;line-height:1}}.stat .sl{{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:6px}}
.note{{background:var(--bg2);border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:12px;padding:14px 18px;margin:18px 0}}.note .nt{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:6px}}.note p{{margin:0;font-size:14.5px;color:var(--soft)}}
.bar{{display:flex;align-items:center;gap:12px;margin:7px 0;font-family:var(--mono);font-size:12.5px}}
.bar .bl{{width:230px;color:var(--soft);text-align:right;flex:0 0 auto}}.bar .bt{{flex:1;height:18px;background:rgba(150,170,205,.06);border-radius:5px;overflow:hidden}}.bar .bf{{display:block;height:100%}}.bar .bv{{width:40px;color:var(--ink)}}
@media(max-width:640px){{.bar .bl{{width:140px;font-size:11px}}}}
.tgrid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}@media(max-width:640px){{.tgrid{{grid-template-columns:1fr}}}}
.tcard{{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}.th{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}}.tn{{font-family:var(--serif);font-size:16px;color:#fff}}.tc{{font-family:var(--mono);font-size:13px;color:var(--accent)}}.tex{{margin:0;padding-left:16px}}.tex li{{font-size:12.5px;color:var(--dim);margin:3px 0}}
.aha{{font-family:var(--serif);font-size:21px;line-height:1.4;color:#fff;border-left:3px solid var(--accent);padding-left:18px;margin:8px 0}}
.src{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}}.src a{{color:var(--accent);text-decoration:none}}
a{{color:var(--accent)}}
</style>
<div class="wrap">
<header style="padding:60px 0 8px">
  <div class="kick">SIGGRAPH 2026 · computer graphics</div>
  <h1>What computer graphics is working on in 2026.</h1>
  <p class="dek">The <b>{N} technical papers</b> of SIGGRAPH 2026 (published as ACM Transactions on Graphics), read for their topics and — by a language model — for what each one actually contributes. Uniquely clean data: <b>100% carry abstracts</b> and 97% are open-access.</p>
  <div class="stat"><div><div class="sn">{N}</div><div class="sl">technical papers</div></div><div><div class="sn">100%</div><div class="sl">with abstracts</div></div><div><div class="sn">{len(T['themes'])}</div><div class="sl">themes</div></div></div>
  <div class="note"><div class="nt">a note on scope</div><p>SIGGRAPH's technical papers publish as ACM Transactions on Graphics articles. This is the {N} available so far for 2026 (the conference is in August; the volume is still filling, so more may land). Every paper here was read individually — <a href="explorer.html">explore them</a>.</p></div>
</header>
<section>
  <div class="eye">The landscape · topics</div>
  <h2>Geometry and simulation still rule — with a generative wave rising</h2>
  <p>The classic pillars of graphics dominate: <b>geometry processing</b> and <b>physical simulation</b> lead by a wide margin, followed by animation, materials, and rendering. But the fastest-rising newcomer is unmistakable — <b>generative 3D &amp; diffusion</b> is already the fifth-largest theme:</p>
  <div style="margin-top:14px">{bars(T['themes'],'theme','n','#4FA8B8')}</div>
</section>
<section>
  <div class="eye">The techniques · read out of {S['n_analyzed']} abstracts</div>
  <h2>What they build with</h2>
  <p>The methods a language model tagged across the papers. The headline: <b>diffusion is now the single most-used technique</b> — the generative-model wave that reshaped images and video has fully arrived in graphics — sitting alongside the field's enduring tools: Monte-Carlo rendering, meshes, implicit surfaces, and FEM/MPM simulation.</p>
  <div style="margin-top:14px">{bars(S['methods'],'tag','n','#9B8CE0')}</div>
</section>
<section>
  <div class="eye">Inside the themes · real papers</div>
  <h2>What each theme contains</h2>
  <div class="tgrid">{cards()}</div>
</section>
<section>
  <div class="eye">Go deeper</div>
  <h2>Explore all {S['n_analyzed']} papers by what they contribute</h2>
  <p>Every paper read for its problem, approach and contribution. Search and filter the full set.</p>
  <p><a href="explorer.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:#0E1420;background:var(--accent);border-radius:9px;padding:10px 22px;text-decoration:none;font-weight:600">→ open the paper explorer</a>  <a href="deep.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ the deep read: the field as one story</a>  <a href="math.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ the mathematics of graphics</a></p>
</section>
<section>
  <div class="eye">The one-line read</div>
  <p class="aha">SIGGRAPH 2026 is still, at heart, about geometry and physics — meshes, materials, and simulation — but diffusion has become its most-used tool, and generative 3D is now one of its biggest topics: the classic craft of graphics, learning to generate itself.</p>
  <p class="src">Data: Semantic Scholar (ACM Transactions on Graphics 2026, 100% abstracts / 97% open PDFs) + DBLP. Themes from a deterministic keyword taxonomy over title+abstract; per-paper problem/approach/contribution/technique from a Haiku pass over all {N} abstracts. Code: <span class="mono">ingest.py · mine_themes.py · merge_analysis.py</span>.</p>
</section>
</div>
"""
open(os.path.join(HERE,"site","index.html"),"w",encoding="utf-8").write(P)
print("wrote site/index.html ·", len(P)//1024,"KB · FFFD:", P.count("�"))

import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, "data", "analysis.json")))
RP = os.path.join(HERE, "data", "rich.json")
RICH = json.load(open(RP)) if os.path.exists(RP) else {}
def esc(s): return html.escape(str(s or ""))

recs = []
for p in A["papers"]:
    r = RICH.get(str(p["gid"]))
    doi = p.get("doi")
    recs.append({
        "t": p["title"],
        "th": p.get("primary_theme") or "", "m": p.get("methods") or [],
        "pr": p.get("problem") or "", "ap": p.get("approach") or "", "co": p.get("contribution") or "",
        "u": p.get("url") or p.get("pdf") or p.get("arxiv") or (("https://doi.org/" + doi) if doi else ""),
        "rc": r or None,
    })
DATA = json.dumps(recs, ensure_ascii=False)
nrich = sum(1 for r in recs if r["rc"])

P = f"""<meta charset="utf-8">
<title>SIGGRAPH 2026 · paper explorer</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;
--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--viol:#9B8CE0;--serif:"Iowan Old Style",Palatino,Georgia,serif;
--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55;font-size:16px}}
.wrap{{max-width:920px;margin:0 auto;padding:0 20px 60px}}
a{{color:var(--accent)}}
.top{{position:sticky;top:0;background:linear-gradient(180deg,#0E1420,#0E1420f0);padding:18px 0 12px;border-bottom:1px solid var(--line);z-index:5}}
h1{{font-family:var(--serif);font-size:26px;margin:0 0 4px;color:#fff}}
.sub{{font-family:var(--mono);font-size:12px;color:var(--dim);margin-bottom:12px}}.sub a{{text-decoration:none}}
.controls{{display:flex;gap:10px;flex-wrap:wrap;align-items:center}}
#q{{flex:1;min-width:220px;background:#0C1119;border:1px solid var(--line);border-radius:9px;color:var(--ink);padding:9px 12px;font-size:14px;font-family:var(--sans)}}
#count{{font-family:var(--mono);font-size:12px;color:var(--faint);margin:12px 0 4px}}
.card{{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0}}
.ct{{font-family:var(--serif);font-size:17px;color:#fff;line-height:1.3}}
.cmeta{{font-family:var(--mono);font-size:11px;color:var(--dim);margin:5px 0 9px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.vtag{{color:#0E1420;background:var(--accent);border-radius:5px;padding:1px 6px;font-weight:600}}
.thtag{{color:var(--soft);border:1px solid var(--line);border-radius:5px;padding:1px 6px}}
.mtag{{color:var(--faint)}}
.pac{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;font-size:13.5px;margin-top:4px}}
.pac .k{{font-family:var(--mono);font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--dim);padding-top:2px}}
.pac .k.pr{{color:var(--rose)}}.pac .k.ap{{color:var(--accent)}}.pac .k.co{{color:var(--amber)}}
.pac .val{{color:var(--soft)}}
.story{{margin-top:10px;border-top:1px solid var(--line);padding-top:2px}}
.story>summary{{font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--accent);cursor:pointer;padding:7px 0;list-style:none}}
.story>summary::-webkit-details-marker{{display:none}}
.story>summary::before{{content:"▸ ";color:var(--accent)}}
.story[open]>summary::before{{content:"▾ "}}
.story[open]>summary{{color:var(--dim)}}
.sec{{margin:11px 0}}
.sec .lbl{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:3px}}
.sec.bp .lbl{{color:var(--accent)}}.sec.wh .lbl{{color:var(--rose)}}.sec.naive .lbl{{color:#D38D63}}.sec.ap .lbl{{color:var(--viol)}}
.sec.mech .lbl{{color:#7EC7D8}}.sec.math .lbl{{color:#D8BE5F}}.sec.dots .lbl{{color:#B69CF0}}
.sec.ww .lbl{{color:var(--amber)}}.sec.po .lbl{{color:#6FCF97}}.sec.limits .lbl{{color:#A7B0BF}}
.sec p{{margin:0;color:var(--ink);font-size:14px;line-height:1.62}}
.more{{text-align:center;margin:20px 0}}.more button{{font-family:var(--mono);font-size:13px;color:var(--accent);background:none;border:1px solid var(--line);border-radius:9px;padding:8px 20px;cursor:pointer}}
</style>
<div class="wrap">
<div class="top">
  <h1>SIGGRAPH 2026 · paper explorer</h1>
  <div class="sub"><a href="index.html">← the landscape</a> · {len(recs):,} ACM Transactions on Graphics papers · each with a quick read + an expandable plain-language first-principles story ({nrich} rich)</div>
  <div class="controls">
    <input id="q" placeholder="search titles, problems, methods…  (e.g. 'cloth', 'fluid', 'neural', 'texture')" autocomplete="off">
  </div>
  <div id="count"></div>
</div>
<div id="list"></div>
<div class="more"><button id="more">show more</button></div>
</div>
<script>
const DATA = {DATA};
let query = "", shown = 0, filtered = DATA, PAGE = 40;
const list = document.getElementById("list"), countEl = document.getElementById("count"), moreBtn = document.getElementById("more");
function esc(s){{return (s||"").replace(/[&<>]/g, c=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[c]));}}
function sec(cls,lbl,txt){{ return txt?`<div class="sec ${{cls}}"><span class="lbl">${{lbl}}</span><p>${{esc(txt)}}</p></div>`:""; }}
function story(rc){{
  if(!rc) return "";
  return `<details class="story"><summary>read the full first-principles story</summary>
    ${{sec("bp","the big picture",rc.bp)}}
    ${{sec("wh","why it's hard",rc.wh)}}
    ${{sec("naive","the naive solution",rc.naive)}}
    ${{sec("ap","the core idea",rc.ap)}}
    ${{sec("mech","how the mechanism runs",rc.mech)}}
    ${{sec("math","mathematical concepts",rc.math)}}
    ${{sec("dots","connecting the dots",rc.dots)}}
    ${{sec("ww","why it works",rc.ww)}}
    ${{sec("po","the payoff",rc.po)}}
    ${{sec("limits","limits and assumptions",rc.limits)}}
  </details>`;
}}
function card(r){{
  const m = (r.m||[]).slice(0,5).map(x=>esc(x)).join(" · ");
  return `<div class="card">
    <div class="ct">${{r.u?`<a href="${{r.u}}" target="_blank" style="text-decoration:none;color:#fff">${{esc(r.t)}}</a>`:esc(r.t)}}</div>
    <div class="cmeta"><span class="vtag">TOG</span>${{r.th?`<span class="thtag">${{esc(r.th)}}</span>`:""}}<span class="mtag">${{m}}</span></div>
    <div class="pac">
      <span class="k pr">problem</span><span class="val">${{esc(r.pr)}}</span>
      <span class="k ap">approach</span><span class="val">${{esc(r.ap)}}</span>
      <span class="k co">gives</span><span class="val">${{esc(r.co)}}</span>
    </div>${{story(r.rc)}}</div>`;
}}
function apply(){{
  const q = query.toLowerCase().split(/\\s+/).filter(Boolean);
  filtered = DATA.filter(r=>{{
    if(!q.length) return true;
    const rc = r.rc?Object.values(r.rc).join(" "):"";
    const hay = (r.t+" "+r.th+" "+r.pr+" "+r.ap+" "+r.co+" "+(r.m||[]).join(" ")+" "+rc).toLowerCase();
    return q.every(w=>hay.includes(w));
  }});
  shown = 0; list.innerHTML = "";
  countEl.textContent = filtered.length.toLocaleString() + " papers" + (query?` · "${{query}}"`:"");
  render();
}}
function render(){{
  const next = filtered.slice(shown, shown+PAGE);
  list.insertAdjacentHTML("beforeend", next.map(card).join(""));
  shown += next.length;
  moreBtn.style.display = shown < filtered.length ? "" : "none";
}}
document.getElementById("q").addEventListener("input", e=>{{query=e.target.value; apply();}});
moreBtn.addEventListener("click", render);
apply();
</script>
"""
for out in [os.path.join(HERE, "explorer.html"), os.path.join(HERE, "site", "explorer.html")]:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(P)
print("wrote explorer.html ·", len(P)//1024, "KB ·", len(recs), "papers ·", nrich, "rich · FFFD:", P.count("�"))

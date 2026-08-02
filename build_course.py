"""Build the plain-language course-spine essay page."""

import html
import os

from course_spine import COURSE_DEK, COURSE_SECTIONS, COURSE_TITLE

HERE = os.path.dirname(os.path.abspath(__file__))


def esc(value):
    return html.escape(str(value or ""))


def section_html(section, index):
    body = "".join(f"<p>{esc(p)}</p>" for p in section["body"])
    return (
        f"<section id='part-{index}'>"
        f"<div class='eye'>{esc(section['kicker'])}</div>"
        f"<h2>{esc(section['title'])}</h2>"
        f"{body}"
        "</section>"
    )


toc = "".join(
    f"<a href='#part-{i}'><b>{i}.</b> {esc(s['title'])}</a>"
    for i, s in enumerate(COURSE_SECTIONS, 1)
)
sections = "".join(section_html(s, i) for i, s in enumerate(COURSE_SECTIONS, 1))

P = f"""<meta charset="utf-8">
<title>SIGGRAPH 2026 · {esc(COURSE_TITLE)}</title>
<style>
:root{{--bg:#0E1420;--bg2:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--faint:#5A6577;--line:rgba(150,170,205,.14);--accent:#4FA8B8;--amber:#E3A63A;--rose:#E0748A;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.78;font-size:18px}}
.wrap{{max-width:820px;margin:0 auto;padding:0 24px 64px}}
p{{color:var(--soft);margin:0 0 17px}}b{{color:var(--ink)}}a{{color:var(--accent)}}
.kick{{font-family:var(--mono);font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-top:56px}}
h1{{font-family:var(--serif);font-size:clamp(34px,6vw,56px);line-height:1.05;margin:12px 0 0;color:#fff}}
.dek{{font-family:var(--serif);font-size:21px;line-height:1.5;color:var(--soft);margin-top:18px}}
.toc{{font-family:var(--mono);font-size:13px;margin:24px 0 4px;line-height:2}}.toc a{{display:block;color:var(--soft);text-decoration:none}}.toc a:hover{{color:var(--accent)}}.toc b{{color:var(--accent);font-weight:400}}
section{{padding:42px 0;border-top:1px solid var(--line)}}
.eye{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--amber);margin-bottom:8px}}
h2{{font-family:var(--serif);font-size:30px;line-height:1.15;margin:0 0 14px;color:#fff}}
.nav{{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:22px;padding-top:16px;border-top:1px solid var(--line)}}.nav a{{text-decoration:none}}
</style>
<div class="wrap">
<header>
  <div class="kick">SIGGRAPH 2026 · first principles · no jargon</div>
  <h1>{esc(COURSE_TITLE)}</h1>
  <p class="dek">{esc(COURSE_DEK)}</p>
  <div class="toc">{toc}</div>
</header>
{sections}
<div class="nav">Continue into the <a href="deep.html">deep read</a>, the <a href="math.html">math map</a>, the <a href="explorer.html">paper explorer</a>, or the <a href="source-code/">runnable demos</a>.</div>
</div>
"""

for rel in ("course.html", os.path.join("site", "course.html")):
    path = os.path.join(HERE, rel)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    open(path, "w", encoding="utf-8").write(P)

print("wrote course.html and site/course.html ·", len(P) // 1024, "KB · FFFD:", P.count("�"))

"""Builds submission.html (and, via headless Chrome, the PDF draft) from writeup.md and the two chart SVGs."""
import re, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
read = lambda p: open(os.path.join(HERE, p), encoding="utf-8").read()

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t

def md(src):
    out, para, lst = [], [], None
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(i)}</li>" for i in lst[1]) + f"</{lst[0]}>"); lst = None
    for line in src.splitlines():
        if line.startswith("## "): flush(); out.append(f"<h2>{inline(line[3:])}</h2>")
        elif re.match(r"^- ", line):
            if not lst or lst[0] != "ul": flush(); lst = ("ul", [])
            lst[1].append(line[2:])
        elif re.match(r"^\d+\. ", line):
            if not lst or lst[0] != "ol": flush(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\d+\. ", "", line))
        elif not line.strip(): flush()
        else:
            if lst: flush()
            para.append(line.strip())
    flush(); return "\n".join(out)

REPO = "https://github.com/jeronperey/tennis-ethical-vs-deceptive"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Do aces win matches?</title>
<style>
@page cover {{ size: 11in 8.5in; margin: 0.35in; }}
@page doc {{ size: 8.5in 11in; margin: 0.8in; }}
body {{ margin: 0; font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif; color: #1f2328; font-size: 11.5pt; line-height: 1.45; }}
.cover {{ page: cover; break-after: page; }}
.doc {{ page: doc; break-before: page; }}
.cover h1 {{ text-align: center; font-size: 30pt; margin: 4pt 0 14pt; }}
.pair {{ display: flex; gap: 20px; justify-content: center; }}
.pair figure {{ margin: 0; width: 48%; }}
.pair figcaption {{ font-size: 18pt; font-weight: 800; margin-bottom: 4pt; }}
.pair svg {{ width: 100%; height: auto; display: block; }}
h2 {{ font-size: 15pt; margin: 18pt 0 4pt; }}
h1.sec {{ font-size: 20pt; margin: 0 0 10pt; }}
p {{ margin: 0 0 8pt; }} li {{ margin-bottom: 3pt; }}
code {{ font-size: 10pt; }} .todo {{ background: #fff3b0; padding: 0 3px; }}
</style></head><body>
<section class="cover"><h1>Do aces win matches?</h1>
<div class="pair"><figure><figcaption>A</figcaption>{read("visualization_A.svg")}</figure>
<figure><figcaption>B</figcaption>{read("visualization_B.svg")}</figure></div></section>

<section class="doc"><h1 class="sec">Implementation</h1>
<p>Both visualizations are static SVG charts built with D3 (v7.9.0) from the same processed data.</p>
<ul>
<li><strong>Source code (public):</strong> <a href="{REPO}">{REPO}</a></li>
<li><code>prepare_data.py</code>: data processing (applies the exclusions and writes the win rates by ace gap).</li>
<li><code>visualizations.js</code> and <code>index.html</code>: the two D3 visualizations, labelled A and B on the page.</li>
<li><code>data/raw/</code> and <code>data/processed/</code>: the source files and the small CSVs the charts use.</li></ul></section>

<section class="doc"><h1 class="sec">Write-up</h1>{md(read("writeup.md"))}</section>

<section class="doc"><h1 class="sec">References</h1><ul>
<li>Sackmann, J. <em>Tennis Abstract: ATP match data</em>, 2015–2024 (CC BY-NC-SA 4.0). Accessed through the archive at github.com/Aneeshers/tennis-sackmann-archive, which redistributes Jeff Sackmann's data (github.com/JeffSackmann).</li>
<li>Bostock, M., Ogievetsky, V., and Heer, J. D3: Data-Driven Documents, v7.9.0. d3js.org.</li>
<li>Lan, X., and Liu, Y. "I Came Across a Junk": Understanding Design Flaws of Data Visualization from the Public's Perspective. <em>IEEE Transactions on Visualization and Computer Graphics</em>, 31(1), 393–403, 2025. doi:10.1109/TVCG.2024.3456341</li>
<li>Mahbub, R., Islam, M. S., Laskar, M. T., Rahman, M., Nayeem, M. T., and Hoque, E. The Perils of Chart Deception: How Misleading Visualizations Affect Vision-Language Models. <em>2025 IEEE Visualization and Visual Analytics (VIS)</em>, 6–10. doi:10.1109/VIS60296.2025.00006</li>
<li>DATA 3302 course notes, Fall 2026: marks and channels (Cleveland and McGill channel ranking), zero baseline and lie factor.</li>
<li>My Assignment 2 visualization ("Do Aces Win Matches?"), which this ethical chart is based on.</li></ul></section>
</body></html>"""
open(os.path.join(HERE, "submission.html"), "w", encoding="utf-8").write(page)
print("wrote submission.html")

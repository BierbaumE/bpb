"""BPB Runde 30 - Name 'BierbaumPerformanceBrothers' IM Netz-Quadrat unter BPB. Aufruf: python3 -I runde30_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde29_gen.py")).read().split("nd, nw, nc =")[0])
def with_name(R, ly=256, cap=150, mw=340, ncap=27, ny=436, stroke=5):
    FIT["quadrat"] = (300, 185, 340)
    old = FIT["quadrat"]; FIT["quadrat"] = (ly, cap, mw)
    svg = framed(R, "quadrat"); FIT["quadrat"] = old
    nd, nw, _ = text_path(mf, "BierbaumPerformanceBrothers", ncap, tracking=1.2, max_w=400)
    name = (f'<g transform="translate({(600 - nw) / 2:.1f} {ny})"><path d="{nd}" fill="{R["text"]}" stroke="{R["tile"]}" stroke-width="{stroke}" '
            f'stroke-linejoin="round" paint-order="stroke"/></g>')
    return svg.replace("</svg>", name + "</svg>")
VAR = {"a": dict(), "b": dict(ly=246, cap=140, ncap=30, ny=440)}
meta = []
for k, R in LOGOS.items():
    for v, kw in VAR.items():
        open(os.path.join(OUT, f"{k}-{v}.svg"), "w").write(with_name(R, **kw)); meta.append((k, v))
json.dump(list(LOGOS), open(os.path.join(OUT, "meta.json"), "w")); json.dump(NAMES, open(os.path.join(OUT, "names.json"), "w")); print("ok")

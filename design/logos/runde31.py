"""BPB Runde 31 - Name im Netz-Quadrat, lesbar: Name auf einer deckenden Leiste (kein Netz dahinter), groesser.
Aufruf: python3 -I runde31_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde29_gen.py")).read().split("nd, nw, nc =")[0])
def band_logo(R, mode):
    old = FIT["quadrat"]
    FIT["quadrat"] = (232, 150, 340) if mode == "a" else (232, 140, 320)
    svg = framed(R, "quadrat"); FIT["quadrat"] = old
    dpath = SHAPES["quadrat"][0]; cx, cy = SHAPES["quadrat"][1]
    ins = f'transform="translate({cx} {cy}) scale(.962) translate({-cx} {-cy})"'
    top = 392 if mode == "a" else 358
    o = [f'<clipPath id="cpn"><path d="{dpath}" {ins}/></clipPath><g clip-path="url(#cpn)">',
         f'<rect x="0" y="{top}" width="600" height="220" fill="{R["tile"]}"/><rect x="0" y="{top}" width="600" height="3" fill="{R["border"]}" opacity=".9"/>']
    if mode == "a":
        nd, nw, nc = text_path(mf, "BierbaumPerformanceBrothers", 40, tracking=1, max_w=470)
        o.append(f'<g transform="translate({(600 - nw) / 2:.1f} {top + 78 + nc / 2:.1f})"><path d="{nd}" fill="{R["text"]}"/></g>')
    else:
        d2, w2, c2 = text_path(mf, "PerformanceBrothers", 50, tracking=1, max_w=470)
        d1, w1, c1 = text_path(mf, "Bierbaum", c2, tracking=1, max_w=470)
        b1 = top + 28 + c2 + 4; b2 = b1 + c2 + 20
        o.append(f'<g transform="translate({(600 - w1) / 2:.1f} {b1:.1f})"><path d="{d1}" fill="{R["text"]}"/></g><g transform="translate({(600 - w2) / 2:.1f} {b2:.1f})"><path d="{d2}" fill="{R["text"]}"/></g>')
    o.append("</g>")
    # Rand der Form oben drueber erneut zeichnen, damit die Leiste nicht darueberragt
    o.append(f'<path d="{dpath}" fill="none" stroke="{R["border"]}" stroke-width="12" transform="translate({cx} {cy}) scale(1.0) translate({-cx} {-cy})" opacity="0"/>')
    return svg.replace("</svg>", "".join(o) + "</svg>")
for k, R in LOGOS.items():
    for m in "ab": open(os.path.join(OUT, f"{k}-{m}.svg"), "w").write(band_logo(R, m))
json.dump(list(LOGOS), open(os.path.join(OUT, "meta.json"), "w")); json.dump(NAMES, open(os.path.join(OUT, "names.json"), "w")); print("ok")

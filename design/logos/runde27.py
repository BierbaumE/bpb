"""BPB Runde 27 - Endfassung-Paket 'Digital Nacht' (Bungee, Quadrat, groeberes Netz): Haupt, Symbol, Klein, Einfarbig, Wortmarke.
Aufruf: python3 -I runde27_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde22_gen.py")).read().split("FAV = {")[0])
DIG = dict(tile="#1a1433", grid="#ff7ab0", text="#ffffff", border="#ff7ab0", accent="#ff9cc7")
CUR["f"] = loadf("bungee/Bungee-Regular.ttf", None); CUR["tr"] = 6
def simple(R, shape="quadrat"):
    dpath, (cx, cy), _ = SHAPES[shape]; ly, cap, mw = FIT[shape]
    d, w, cp, tx, base = geom(cap * 1.08, ly, mw * 1.04)
    ins = lambda s: f'transform="translate({cx} {cy}) scale({s}) translate({-cx} {-cy})"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><path d="{dpath}" fill="{R["border"]}"/>'
            f'<path d="{dpath}" fill="{R["tile"]}" {ins(.93)}/><g transform="translate({tx:.1f} {base:.1f})">'
            f'<path d="{d}" fill="{R["text"]}" stroke="{R["tile"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"/></g></svg>')
W = lambda n, s: open(os.path.join(OUT, n), "w").write(s)
main = framed(DIG, "quadrat"); W("bpb-haupt.svg", main)
W("bpb-klein.svg", simple(DIG))
W("bpb-einfarbig-weiss.svg", simple(dict(tile="#000000", border="#ffffff", text="#ffffff", grid="#fff", accent="#fff")))
W("bpb-einfarbig-schwarz.svg", simple(dict(tile="#ffffff", border="#000000", text="#000000", grid="#000", accent="#000")))
mf = loadf("manrope/Manrope[wght].ttf", {"wght": 800})
nd, nw, nc = text_path(mf, "BierbaumPerformanceBrothers", 74, tracking=2, max_w=930)
inner = main.split(">", 1)[1].rsplit("</svg>", 1)[0]
for tag, col in (("dunkel", "#ffffff"), ("hell", "#1a1433")):
    W(f"bpb-wortmarke-{tag}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 380"><svg x="10" y="10" width="360" height="360" viewBox="0 0 600 600">{inner}</svg>'
      f'<g transform="translate(420 150)"><path d="{nd}" fill="{col}"/></g>'
      f'<text x="424" y="250" font-family="sans-serif" font-weight="700" font-size="30" letter-spacing="9" fill="#ff7ab0">SOFTWARE &amp; BERATUNG</text></svg>')
print("ok")

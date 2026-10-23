"""BPB Runde 33 - Logo frei stehend, Name daneben (Bungee, gleicher Farbstil, zweizeilig). Aufruf: python3 -I runde33_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde29_gen.py")).read().split("nd, nw, nc =")[0])
def lum(h): h = h.lstrip("#"); r, g, bl = (int(h[i:i + 2], 16) for i in (0, 2, 4)); return (.3 * r + .59 * g + .11 * bl) / 255
def name_block(R, bg, x0, wmax=570, cap0=80):
    dark = bg == "dunkel"
    c1 = R["text"] if dark else R["tile"]
    acc = (R["border"] if lum(R["border"]) > .35 else R["grid"]) if dark else (R["border"] if lum(R["border"]) < .85 else R["grid"])
    c2 = acc if dark else mix(acc, "#000000", .4)
    sh = mix(c1, "#000000", .55) if dark else mix(c1, "#ffffff", .5)
    dm, wm, cap = text_path(CUR["f"], "Performance", cap0, tracking=2, max_w=wmax)
    parts = [text_path(CUR["f"], t, cap, tracking=2, max_w=wmax) for t in ("Bierbaum", "Performance", "Brothers")]
    gap = 16; H = 3 * cap + 2 * gap; y = 190 - H / 2 + cap
    out = ""
    for i, ((d, w, cp), col) in enumerate(zip(parts, (c1, c2, c1))):
        ex = "".join(f'<path d="{d}" fill="{sh}" transform="translate({j * .9:.1f} {j * 1.1:.1f})"/>' for j in range(6, 0, -1))
        g = f'<path d="{d}" fill="{col}" opacity=".5" filter="url(#gl)"/>' if (i == 1 and dark) else ""
        out += f'<g transform="translate({x0} {y + i * (cap + gap):.1f})">{g}{ex}<path d="{d}" fill="{col}"/></g>'
    return out, cap
def lockup(R, bg, side):
    main = framed(R, "quadrat"); inner = main.split(">", 1)[1].rsplit("</svg>", 1)[0]
    blk, cap = name_block(R, bg, 410 if side == "l" else 20)
    lx = 10 if side == "l" else 630
    logo = f'<svg x="{lx}" y="10" width="360" height="360" viewBox="0 0 600 600">{inner}</svg>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 380"><defs><filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter></defs>'
            f'{blk}{logo}</svg>')
for k, R in LOGOS.items():
    for bg in ("dunkel", "hell"):
        for side in "lr":
            open(os.path.join(OUT, f"{k}-{bg}-{side}.svg"), "w").write(lockup(R, bg, side))
json.dump(list(LOGOS), open(os.path.join(OUT, "meta.json"), "w")); json.dump(NAMES, open(os.path.join(OUT, "names.json"), "w")); print("ok")

"""BPB Runde 34 - Logo frei, Name daneben IN EINER ZEILE, ohne Leerzeichen (Farbwechsel markiert die Woerter).
Aufruf: python3 -I runde34_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde33_gen.py")).read().split("def lockup")[0])
FONTS2 = {"bungee": CUR["f"], "titan": loadf("titanone/TitanOne-Regular.ttf", None)}
SEG = ("Bierbaum", "Performance", "Brothers")
def one_line(R, bg, font, side, W=1080, ext=5):
    dark = bg == "dunkel"
    c1 = R["text"] if dark else R["tile"]
    acc = (R["border"] if lum(R["border"]) > .42 else R["grid"]) if dark else (R["border"] if lum(R["border"]) < .85 else R["grid"])
    c2 = acc if dark else mix(acc, "#000000", .4)
    sh = mix(c1, "#000000", .55) if dark else mix(c1, "#ffffff", .5)
    cap, tr = 60, 2
    def lay(cap):
        xs, x, parts = [], 0, []
        for t in SEG:
            d, w, cp = text_path(font, t, cap, tracking=tr)
            parts.append((d, x)); x += w + tr
        return parts, x - tr
    parts, tot = lay(cap)
    cap *= W / tot; parts, tot = lay(cap)
    x0 = 400 if side == "l" else 1500 - 400 - tot + 0
    if side == "r": x0 = 1500 - 400 - tot
    y = 190 + cap / 2
    out = ""
    for (d, x), col in zip(parts, (c1, c2, c1)):
        exs = "".join(f'<path d="{d}" fill="{sh}" transform="translate({j * .9:.1f} {j * 1.1:.1f})"/>' for j in range(ext, 0, -1))
        gl = f'<path d="{d}" fill="{col}" opacity=".5" filter="url(#gl)"/>' if (col == c2 and dark) else ""
        out += f'<g transform="translate({x0 + x:.1f} {y:.1f})">{gl}{exs}<path d="{d}" fill="{col}"/></g>'
    main = framed(R, "quadrat"); inner = main.split(">", 1)[1].rsplit("</svg>", 1)[0]
    lx = 10 if side == "l" else 1130
    logo = f'<svg x="{lx}" y="10" width="360" height="360" viewBox="0 0 600 600">{inner}</svg>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 380"><defs><filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter></defs>{out}{logo}</svg>')
for k, R in LOGOS.items():
    for fn, f in FONTS2.items():
        for bg in ("dunkel", "hell"):
            for side in "lr":
                open(os.path.join(OUT, f"{k}-{fn}-{bg}-{side}.svg"), "w").write(one_line(R, bg, f, side))
json.dump(list(LOGOS), open(os.path.join(OUT, "meta.json"), "w")); json.dump(NAMES, open(os.path.join(OUT, "names.json"), "w")); print("ok")

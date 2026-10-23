"""BPB Runde 35 - Sonnenlogo vom Anfang (BPB auf Sonne, Name darunter) neu als Vektor in fuenf Farbdarstellungen.
Aufruf: python3 -I runde35_gen.py <ofl-Ordner> <Ausgabe>   (Schriften: Archivo Black, Manrope aus gf-ofl via Argument 3)"""
import sys, os, json
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
OFL, OUT, GF = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
def text_path(font, text, cap, tracking=0.0, max_w=None):
    upm = font["head"].unitsPerEm; capu = font["OS/2"].sCapHeight
    gs, cm = font.getGlyphSet(), font.getBestCmap()
    for _ in range(2):
        s = cap / capu; x, parts = 0.0, []
        for ch in text:
            g = gs[cm[ord(ch)]]; pen = SVGPathPen(gs); g.draw(TransformPen(pen, (s, 0, 0, -s, x, 0))); parts.append(pen.getCommands()); x += g.width * s + tracking
        w = x - tracking
        if max_w and w > max_w: cap *= max_w / w; tracking *= max_w / w
        else: break
    return " ".join(parts), w, cap
def capfix(f):
    gs = f.getGlyphSet(); bp = BoundsPen(gs); gs[f.getBestCmap()[ord("H")]].draw(bp); f["OS/2"].sCapHeight = int(bp.bounds[3]); return f
AB = capfix(TTFont(os.path.join(OFL, "archivoblack/ArchivoBlack-Regular.ttf")))
MF = capfix(instancer.instantiateVariableFont(TTFont(os.path.join(GF, "manrope/Manrope[wght].ttf")), {"wght": 800}))
V = [  # Name, Hintergrund (Farben, flach wenn eine), Sonne, Schrift, Kontur, Name
 ("Sonnenuntergang (wie bisher)", ["#3f2fa8", "#9b3ac0", "#e8508f", "#ffb35c"], "#ffe27a", "#ffffff", "#2a1a55", "#1a0d3d"),
 ("Flach Violett / Gelb", ["#3f2fa8"], "#ffe27a", "#ffffff", "#1c1240", "#ffffff"),
 ("Nacht / Rosa", ["#14102b"], "#ff7ab0", "#ffffff", "#14102b", "#ffffff"),
 ("Schwarz-Weiß-Grau", ["#111111"], "#cfcfcf", "#ffffff", "#000000", "#ffffff"),
 ("Wald / Creme", ["#0b2a1c"], "#c9a227", "#f4eee2", "#0b2a1c", "#f4eee2"),
]
bd, bw, bc = text_path(AB, "BPB", 150, tracking=6, max_w=480)
nd, nw, nc = text_path(MF, "BIERBAUMPERFORMANCEBROTHERS", 26, tracking=6, max_w=560)
meta = []
for i, (n, bg, sun, tx, ol, nm) in enumerate(V, 1):
    if len(bg) > 1:
        stops = "".join(f'<stop offset="{j / (len(bg) - 1):.2f}" stop-color="{c}"/>' for j, c in enumerate(bg))
        fill = "url(#bg)"; defs = f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient>'
    else: fill = bg[0]; defs = ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 480"><defs>{defs}<clipPath id="c"><rect width="680" height="480" rx="44"/></clipPath></defs>'
           f'<g clip-path="url(#c)"><rect width="680" height="480" fill="{fill}"/><circle cx="340" cy="222" r="150" fill="{sun}"/>'
           f'<g transform="translate({(680 - bw) / 2:.1f} {222 + bc / 2 - 6:.1f})"><path d="{bd}" fill="{tx}" stroke="{ol}" stroke-width="9" stroke-linejoin="round" paint-order="stroke"/></g>'
           f'<g transform="translate({(680 - nw) / 2:.1f} 432)"><path d="{nd}" fill="{nm}"/></g></g></svg>')
    open(os.path.join(OUT, f"sonne-{i}.svg"), "w").write(svg); meta.append((i, n))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w")); print("ok")

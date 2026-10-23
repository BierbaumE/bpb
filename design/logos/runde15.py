"""BPB Runde 15 - Gravitationsnetz in voll gefuellten Formen; Grau sowie zwei-, drei-, vielfarbig.
Aufruf: python3 -I runde15_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4/10/11/13/14_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde14_gen.py")).read().split("def framed(")[0])   # SHAPES, rpath, xtra, Helfer, PAL2, pal()

PAL3 = {
 "grau":   PAL2["grau"],
 "zwei":   pal("Zweifarbig", ["#19d3ff", "#19d3ff", "#ff3cc8", "#ff3cc8"], ["#c4f3ff", "#c4f3ff", "#ffc4ec", "#ffc4ec"], "#0d1233", "#03040d", "#7a7cff", "#ffffff", "#cfd4ff", "#3b45c9", "#0a0c26", "#ffffff"),
 "drei":   pal("Dreifarbig", ["#ffc400", "#ff3c7a", "#6a4cff", "#ff3c7a"], ["#ffe98a", "#ffb0cc", "#c8b8ff", "#ffb0cc"], "#24102e", "#06030a", "#ff5a9a", "#fff6e8", "#ffc4d8", "#c42a70", "#220612", "#ffffff"),
 "viel":   pal("Vielfarbig", ["#ff4d4d", "#ffb020", "#35e08a", "#2e9bff", "#a24dff"], ["#ffb0b0", "#ffe0a0", "#a8f5cc", "#a8d4ff", "#dcb8ff"], "#15151f", "#040407", "#7ad0ff", "#ffffff", "#d6e6ff", "#4d6fd8", "#0b0d1c", "#ffffff"),
}
# Buchstaben je Form: (Mittelpunkt y, Hoehe, max. Breite) - Form wird voll ausgefuellt
FIT = {"kreis": (300, 170, 300), "quadrat": (300, 185, 340), "raute": (300, 160, 275), "dreieck": (388, 140, 250), "sechseck": (300, 180, 320), "schild": (272, 172, 300)}

def netz(P, cyc, cap, mw):
    c = (300, cyc)
    def warp(x, y):
        dx, dy = x - c[0], y - c[1]; dd = math.hypot(dx, dy) + 1e-6
        k = 1 - .88 * math.exp(-(dd / 120) ** 2) - .25 * math.exp(-(dd / 260) ** 2)
        return c[0] + dx * k, c[1] + dy * k
    def grid(stroke):
        g = ""
        for horiz in (True, False):
            for i in range(-1, 24):
                v = i * 27 + 6; seg = [warp(*((j, v) if horiz else (v, j))) for j in range(0, 601, 10)]
                g += f'<polyline points="{pts(seg)}" fill="none" stroke="{stroke}" stroke-width="{2.6 if i % 3 == 0 else 1.5}"/>'
        return g
    gm, gh = grid("url(#gm)"), grid("url(#gh)")
    return (f'<g opacity=".55">{gm}</g><g mask="url(#m)" filter="url(#gl)" opacity=".9">{gh}</g><g mask="url(#m)" opacity=".95">{gh}</g>'
            f'<circle cx="300" cy="{cyc}" r="{cap * .9:.0f}" fill="url(#well)"/>'
            f'<circle cx="300" cy="{cyc}" r="{cap * .57:.0f}" fill="none" stroke="{P["hi"][1]}" stroke-width="5" opacity=".85" filter="url(#gl)"/>'
            + letters3d(P, cap, cyc, mw, ext=15, glow=True))

def framed(P, shape):
    dpath, (cx, cy), _ = SHAPES[shape]
    ly, cap, mw = FIT[shape]
    ins = lambda s: f'transform="translate({cx} {cy}) scale({s}) translate({-cx} {-cy})"'
    # Maske fuer das Leuchten im Netz folgt dem Buchstabenmittelpunkt
    ex = xtra(P).replace('<radialGradient id="mk">', f'<radialGradient id="mk" gradientUnits="userSpaceOnUse" cx="300" cy="{ly}" r="330">')
    d = defs(P, extra=ex); o = []
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["glow"]}" stroke-width="8" opacity=".55" filter="url(#gl)"/>')
    o.append(f'<path d="{dpath}" fill="#000" opacity=".7" filter="url(#ds)" transform="translate(0 14)"/>')
    o.append(f'<path d="{dpath}" fill="url(#bz)"/>')
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["edge"]}" stroke-opacity=".8" stroke-width="1.2"/>')
    o.append(f'<path d="{dpath}" fill="#05060a" {ins(.972)}/>')
    o.append(f'<clipPath id="cp"><path d="{dpath}" {ins(.962)}/></clipPath>')
    o.append(f'<g clip-path="url(#cp)"><path d="{dpath}" fill="url(#bg)" {ins(.962)}/>{netz(P, ly, cap, mw)}</g>')
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".5" stroke-width="1" {ins(.962)}/>')
    return svgwrap(P, "".join(o), d)

for shape in SHAPES:
    for pn, P in PAL3.items():
        open(os.path.join(OUT, f"n-{shape}_{pn}.svg"), "w").write(framed(P, shape))
print("ok")

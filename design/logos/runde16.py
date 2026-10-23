"""BPB Runde 16 - Gravitationsnetz in Formen: klare Farbrollen (Flaeche, Netz, Schrift, Rand), transparenter Grund, kein schwarzes Umfeld.
Aufruf: python3 -I runde16_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4/10/11/13/14/15_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde15_gen.py")).read().split("def netz(")[0])   # SHAPES, FIT, Helfer, defs, letters3d, mix, pal

ROLES = {   # tile = Flaeche, grid = Netz, text = Schrift, border = Rand, accent = Leuchtring; optional s1/s2 = Seitenflaeche der Schrift
 "dunkel": dict(tile="#1b1e24", grid="#8e959f", text="#ffffff", border="#d9dde3", accent="#ffffff"),
 "hell":   dict(tile="#eceef1", grid="#a9afb8", text="#1b1e24", border="#1b1e24", accent="#1b1e24", s1="#6b7078", s2="#2a2d33"),
 "zwei":   dict(tile="#0c2a63", grid="#ffb400", text="#ffb400", border="#ffb400", accent="#ffb400"),
 "drei":   dict(tile="#1c1038", grid="#ff3c8e", text="#ffd23c", border="#ffd23c", accent="#ff3c8e"),
 "viel":   dict(tile="#0d1b2e", grid="#2ee6c5", text="#ffcf3d", border="#ff4d6d", accent="#8a6bff"),
}
def toP(R):
    t = R["text"]
    return dict(bg1=mix(R["tile"], "#ffffff", .06), bg2=R["tile"], f1=mix(t, "#ffffff", .28), f2=t,
                s1=R.get("s1", mix(t, "#000000", .35)), s2=R.get("s2", mix(t, "#000000", .8)), edge=mix(t, "#ffffff", .55),
                glow=R["accent"], bright=R["grid"], mid=R["grid"], deep=R["tile"], hi=[R["grid"]] * 4, cols=[R["grid"]] * 4)

def halo(R, cyc, cap, mw):
    d, w, cp, tx, base = geom(cap, cyc, mw)
    dark = "#000000" if R["tile"] < "#808080" else "#7d838c"
    st = lambda wd, col, op, f="": f'<path d="{d}" fill="{col}" stroke="{col}" stroke-width="{wd}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}" {f}/>'
    return (f'<g transform="translate({fmt(tx)} {fmt(base)})">' + st(70, dark, .55, 'filter="url(#gl2)"') + st(30, R["accent"], .42, 'filter="url(#gl)"')
            + st(15, dark, .8, 'filter="url(#sf)"') + '</g>')

def netz(P, R, cyc, cap, mw):
    c = (300, cyc)
    def warp(x, y):
        dx, dy = x - c[0], y - c[1]; dd = math.hypot(dx, dy) + 1e-6
        k = 1 - .88 * math.exp(-(dd / 120) ** 2) - .25 * math.exp(-(dd / 260) ** 2)
        return c[0] + dx * k, c[1] + dy * k
    g = ""
    for horiz in (True, False):
        for i in range(-1, 24):
            v = i * 27 + 6; seg = [warp(*((j, v) if horiz else (v, j))) for j in range(0, 601, 10)]
            g += f'<polyline points="{pts(seg)}" fill="none" stroke="{R["grid"]}" stroke-width="{2.6 if i % 3 == 0 else 1.5}"/>'
    return (f'<g opacity=".5">{g}</g><g mask="url(#m)" filter="url(#gl)" opacity=".8">{g}</g><g mask="url(#m)" opacity=".95">{g}</g>'
            + halo(R, cyc, cap, mw)
            + letters3d(P, cap, cyc, mw, ext=15, glow=True))

def framed(R, shape):
    P = toP(R); dpath, (cx, cy), _ = SHAPES[shape]; ly, cap, mw = FIT[shape]
    ins = lambda s: f'transform="translate({cx} {cy}) scale({s}) translate({-cx} {-cy})"'
    wellc = "#000" if R["tile"] < "#808080" else "#8a8f98"
    ex = (f'<radialGradient id="mk" gradientUnits="userSpaceOnUse" cx="300" cy="{ly}" r="330"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></radialGradient>'
          '<mask id="m"><rect width="600" height="600" fill="url(#mk)"/></mask>'
          f'<radialGradient id="well"><stop offset="0" stop-color="{wellc}" stop-opacity=".95"/><stop offset=".62" stop-color="{wellc}" stop-opacity=".6"/><stop offset="1" stop-color="{wellc}" stop-opacity="0"/></radialGradient>')
    d = defs(P, extra=ex); b = R["border"]; o = []
    o.append(f'<path d="{dpath}" fill="#000" opacity=".35" filter="url(#ds)" transform="translate(0 12)"/>')   # leichter Schatten, kein Umfeld
    o.append(f'<path d="{dpath}" fill="{b}"/>')
    o.append(f'<path d="{dpath}" fill="none" stroke="{mix(b, "#ffffff", .55)}" stroke-opacity=".85" stroke-width="1.2"/>')
    o.append(f'<path d="{dpath}" fill="{R["tile"]}" {ins(.972)}/>')
    o.append(f'<clipPath id="cp"><path d="{dpath}" {ins(.962)}/></clipPath>')
    o.append(f'<g clip-path="url(#cp)"><path d="{dpath}" fill="url(#bg)" {ins(.962)}/>{netz(P, R, ly, cap, mw)}</g>')
    o.append(f'<path d="{dpath}" fill="none" stroke="{mix(b, "#000000", .4)}" stroke-opacity=".7" stroke-width="1" {ins(.962)}/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">{d}{"".join(o)}</svg>'

for shape in SHAPES:
    for rn, R in ROLES.items():
        open(os.path.join(OUT, f"r-{shape}_{rn}.svg"), "w").write(framed(R, shape))
print("ok")

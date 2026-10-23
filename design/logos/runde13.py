"""BPB Runde 13 - Gravitationsnetz mit Rand/Abhebung: A Metallrahmen, B Glaslinse, C Neon-Eckrahmen, D schwebende Platte.
Aufruf: python3 -I runde13_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4/10/11_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde11_gen.py")).read().split("def gitter(P):")[0])

def extra(P):
    dark = mix(P["deep"], "#000000", .55)
    return (lg("gm", P["cols"]) + lg("gh", P["hi"]) +
            '<radialGradient id="mk"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></radialGradient>'
            '<mask id="m"><rect width="600" height="600" fill="url(#mk)"/></mask>'
            '<radialGradient id="well"><stop offset="0" stop-color="#000" stop-opacity=".95"/><stop offset=".6" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="bz" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P["hi"][0]}"/><stop offset=".22" stop-color="{P["cols"][0]}"/><stop offset=".5" stop-color="{dark}"/><stop offset=".78" stop-color="{P["cols"][2]}"/><stop offset="1" stop-color="{P["hi"][2]}"/></linearGradient>'
            '<radialGradient id="vg"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>'
            '<linearGradient id="gl2g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>')

def content(P):
    c = (300, 300)
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
            '<circle cx="300" cy="300" r="150" fill="url(#well)"/>'
            f'<circle cx="300" cy="300" r="96" fill="none" stroke="{P["hi"][1]}" stroke-width="5" opacity=".85" filter="url(#gl)"/>'
            + letters3d(P, 168, 300, 300, ext=16, glow=True))

def svgwrap(P, body, d):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">{d}<rect width="600" height="600" fill="#08090d"/>'
            f'<circle cx="300" cy="320" r="330" fill="{P["glow"]}" opacity=".12" filter="url(#gl2)"/>{body}</svg>')

def A(P):   # Metallrahmen mit Fase
    d = defs(P, extra=extra(P)); o = []
    o.append('<rect x="30" y="52" width="540" height="540" rx="92" fill="#000" opacity=".7" filter="url(#ds)"/>')
    o.append('<rect x="26" y="26" width="548" height="548" rx="90" fill="url(#bz)"/>')
    o.append(f'<rect x="27" y="27" width="546" height="546" rx="89" fill="none" stroke="{P["edge"]}" stroke-opacity=".7" stroke-width="2"/>')
    o.append('<rect x="46" y="46" width="508" height="508" rx="72" fill="#05060a"/>')
    o.append('<clipPath id="cp"><rect x="50" y="50" width="500" height="500" rx="68"/></clipPath>')
    o.append(f'<g clip-path="url(#cp)"><rect x="50" y="50" width="500" height="500" fill="url(#bg)"/>{content(P)}<rect x="50" y="50" width="500" height="500" rx="68" fill="none" stroke="#000" stroke-width="26" opacity=".7" filter="url(#ds)"/></g>')
    o.append(f'<rect x="50" y="50" width="500" height="500" rx="68" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".35" stroke-width="1.5"/>')
    return svgwrap(P, "".join(o), d)

def B(P):   # Glaslinse
    d = defs(P, extra=extra(P)); o = []
    o.append('<circle cx="300" cy="316" r="270" fill="#000" opacity=".7" filter="url(#ds)"/>')
    o.append('<circle cx="300" cy="300" r="274" fill="url(#bz)"/>')
    o.append(f'<circle cx="300" cy="300" r="274" fill="none" stroke="{P["edge"]}" stroke-opacity=".7" stroke-width="2"/>')
    o.append('<circle cx="300" cy="300" r="252" fill="#05060a"/>')
    o.append('<clipPath id="cp"><circle cx="300" cy="300" r="246"/></clipPath>')
    o.append(f'<g clip-path="url(#cp)"><rect width="600" height="600" fill="url(#bg)"/>{content(P)}<circle cx="300" cy="300" r="246" fill="url(#vg)"/>'
             '<ellipse cx="226" cy="168" rx="170" ry="74" transform="rotate(-28 226 168)" fill="url(#gl2g)"/></g>')
    o.append(f'<circle cx="300" cy="300" r="246" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".45" stroke-width="2"/>')
    return svgwrap(P, "".join(o), d)

def chamfer(x0, y0, x1, y1, c):
    return pts([(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)])

def C(P):   # Neon-Eckrahmen
    d = defs(P, extra=extra(P)); o = []
    outer, inner, tile = chamfer(26, 26, 574, 574, 58), chamfer(42, 42, 558, 558, 46), chamfer(54, 54, 546, 546, 38)
    o.append(f'<polygon points="{outer}" fill="none" stroke="url(#gh)" stroke-width="10" opacity=".8" filter="url(#gl)"/>')
    o.append(f'<polygon points="{outer}" fill="none" stroke="url(#gh)" stroke-width="4" stroke-linejoin="round"/>')
    o.append(f'<polygon points="{inner}" fill="none" stroke="url(#gm)" stroke-width="1.6" stroke-linejoin="round"/>')
    o.append(f'<clipPath id="cp"><polygon points="{tile}"/></clipPath><polygon points="{tile}" fill="#05060a"/>')
    o.append(f'<g clip-path="url(#cp)"><rect width="600" height="600" fill="url(#bg)"/>{content(P)}</g>')
    for (x, y, dx, dy) in [(300, 26, 1, 0), (300, 574, 1, 0), (26, 300, 0, 1), (574, 300, 0, 1)]:   # Mittelmarken
        o.append(f'<line x1="{x - 28 * dx}" y1="{y - 28 * dy}" x2="{x + 28 * dx}" y2="{y + 28 * dy}" stroke="{P["hi"][1]}" stroke-width="7" stroke-linecap="round"/>')
    return svgwrap(P, "".join(o), d)

def D(P):   # schwebende Platte mit Dicke und Schatten
    d = defs(P, extra=extra(P)); o = []
    o.append('<ellipse cx="300" cy="572" rx="230" ry="22" fill="#000" opacity=".75" filter="url(#ds)"/>')
    g = ['<g transform="rotate(-4 300 300) translate(0 -10)">']
    for i in range(18, 0, -1):
        g.append(f'<rect x="{50 + i * .35:.2f}" y="{50 + i * 1.0:.2f}" width="500" height="500" rx="64" fill="{mix(P["s1"], P["s2"], i / 18)}"/>')
    g.append('<rect x="50" y="50" width="500" height="500" rx="64" fill="#05060a"/><clipPath id="cp"><rect x="50" y="50" width="500" height="500" rx="64"/></clipPath>')
    g.append(f'<g clip-path="url(#cp)"><rect x="50" y="50" width="500" height="500" fill="url(#bg)"/>{content(P)}<rect x="50" y="50" width="500" height="500" fill="url(#sheen)"/></g>')
    g.append(f'<rect x="50" y="50" width="500" height="500" rx="64" fill="none" stroke="{P["edge"]}" stroke-opacity=".75" stroke-width="2"/></g>')
    return svgwrap(P, "".join(o) + "".join(g), d)

for tn, f in {"A-rahmen": A, "B-linse": B, "C-neon": C, "D-platte": D}.items():
    for pn in ("nebula", "aurora", "glut"):
        open(os.path.join(OUT, f"g-{tn}_{pn}.svg"), "w").write(f(PAL2[pn]))
print("ok")

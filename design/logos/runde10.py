"""BPB Runde 10 - Tiefe: Verlaeufe, Leuchten, Schatten, Buchstaben mit Koerper; drei Paletten (Grau, Glut, Smaragd).
Aufruf: python3 -I runde10_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py daneben fuer text_path)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde4_gen.py")).read().split("def fmt")[0])
def fmt(v): return f"{v:.1f}"
def pts(l): return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in l)
def P_(c, r, a): return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
def mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))

PAL = {
 "grau":    dict(bg1="#232730", bg2="#050608", bright="#ffffff", mid="#8d939e", deep="#2c3038", glow="#dfe6f2", f1="#ffffff", f2="#aeb4c0", s1="#7b808a", s2="#14151a", edge="#ffffff"),
 "glut":    dict(bg1="#34140a", bg2="#070201", bright="#ffd584", mid="#ff7a1f", deep="#7d1f06", glow="#ff8d2e", f1="#fff3d2", f2="#ffb04a", s1="#c8480c", s2="#260a03", edge="#fff7e0"),
 "smaragd": dict(bg1="#0a2e33", bg2="#010a0c", bright="#a6fff1", mid="#1fc9a2", deep="#0a5560", glow="#36ecc6", f1="#ecfffc", f2="#6be8d2", s1="#139b8a", s2="#021a1d", edge="#eafffb"),
}

def defs(P, face=None, extra=""):
    f1, f2 = face or (P["f1"], P["f2"])
    return (f'<defs><radialGradient id="bg" cx="50%" cy="46%" r="75%"><stop offset="0" stop-color="{P["bg1"]}"/><stop offset="1" stop-color="{P["bg2"]}"/></radialGradient>'
            f'<linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{f1}"/><stop offset="1" stop-color="{f2}"/></linearGradient>'
            '<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>'
            '<filter id="gl2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
            '<filter id="sf" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.8"/></filter>'
            '<filter id="ds" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="6"/></filter>'
            f'{extra}</defs>')

def geom(cap, cy, max_w, tr=6):
    d, w, cap = text_path(ANTON, "BPB", cap, tracking=tr, max_w=max_w)
    return d, w, cap, (600 - w) / 2, cy + cap / 2

def letters3d(P, cap, cy, max_w, ext=15, edge=True, glow=False, side=None):
    d, w, cap, tx, base = geom(cap, cy, max_w)
    s1, s2 = side or (P["s1"], P["s2"])
    o = [f'<g transform="translate({fmt(tx)} {fmt(base)})">']
    if glow: o.append(f'<path d="{d}" fill="{P["glow"]}" opacity=".55" filter="url(#gl)"/>')
    o.append(f'<path d="{d}" fill="#000" opacity=".6" filter="url(#ds)" transform="translate({ext * .9:.1f} {ext * 1.1 + 6:.1f})"/>')
    for i in range(ext, 0, -1):
        o.append(f'<path d="{d}" fill="{mix(s1, s2, i / ext)}" transform="translate({i * .85:.2f} {i * 1.0:.2f})"/>')
    o.append(f'<path d="{d}" fill="url(#face)"/>')
    o.append(f'<clipPath id="lc"><path d="{d}"/></clipPath><rect x="-10" y="{fmt(-cap)}" width="{fmt(w + 20)}" height="{fmt(cap * .55)}" fill="url(#gloss)" clip-path="url(#lc)" opacity=".7"/>')
    if edge: o.append(f'<path d="{d}" fill="none" stroke="{P["edge"]}" stroke-width="1.6" stroke-opacity=".75" stroke-linejoin="round"/>')
    o.append('</g>')
    return "".join(o)

def wrap(b, d): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">{d}<rect width="600" height="600" fill="url(#bg)"/>{b}</svg>'

# ---------------- 1 Supernova
def supernova(P):
    r = random.Random(5); c = (300, 300); o = []
    d = defs(P, face=("#585d68", "#0b0c0f"),
             extra=f'<radialGradient id="sg"><stop offset="0" stop-color="{P["glow"]}" stop-opacity=".75"/><stop offset=".55" stop-color="{P["mid"]}" stop-opacity=".22"/><stop offset="1" stop-color="{P["mid"]}" stop-opacity="0"/></radialGradient>'
                   f'<radialGradient id="core"><stop offset="0" stop-color="{P["f1"]}"/><stop offset=".55" stop-color="{P["bright"]}"/><stop offset="1" stop-color="{P["mid"]}"/></radialGradient>')
    o.append('<circle cx="300" cy="300" r="300" fill="url(#sg)"/>')
    rays = ""
    for k in range(34):
        a = k * 2 * math.pi / 34 + r.uniform(-.03, .03); L = r.choice([292, 255, 210, 292, 180]); w = .05
        rays += f'<polygon points="{pts([P_(c, 70, a - w), P_(c, L, a), P_(c, 70, a + w)])}" fill="{P["bright"] if k % 3 else P["mid"]}" fill-opacity="{.9 if k % 3 else .7}"/>'
    o.append(f'<g filter="url(#gl)" opacity=".8">{rays}</g>{rays}')
    for rad, sw, dash, col in [(150, 16, "70 20 12 34 100 16", P["bright"]), (200, 10, "40 26 120 14 22 40", P["mid"]), (250, 6, "16 30 60 24 8 50", P["bright"])]:
        tr = f'transform="rotate({r.randint(0, 90)} 300 300)"'
        o.append(f'<circle cx="300" cy="300" r="{rad}" fill="none" stroke="{col}" stroke-width="{sw * 1.8}" stroke-dasharray="{dash}" opacity=".55" filter="url(#gl)" {tr}/>'
                 f'<circle cx="300" cy="300" r="{rad}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}" {tr}/>')
    star = [P_(c, 142 if k % 2 == 0 else 108, k * math.pi / 12) for k in range(24)]
    o.append(f'<polygon points="{pts(star)}" fill="{P["glow"]}" filter="url(#gl2)" opacity=".9"/>')
    o.append(f'<polygon points="{pts(star)}" fill="url(#core)"/><polygon points="{pts(star)}" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>')
    o.append(letters3d(P, 150, 300, 250, ext=12, side=(mix(P["deep"], "#000000", .2), "#050505")))
    return wrap("".join(o), d)

# ---------------- 2 Gravitationsloch
def gitter(P):
    c = (300, 300)
    def warp(x, y):
        dx, dy = x - c[0], y - c[1]; dd = math.hypot(dx, dy) + 1e-6
        k = 1 - .88 * math.exp(-(dd / 120) ** 2) - .25 * math.exp(-(dd / 260) ** 2)
        return c[0] + dx * k, c[1] + dy * k
    g = ""
    for horiz in (True, False):
        for i in range(-1, 24):
            v = i * 27 + 6; seg = [warp(*((j, v) if horiz else (v, j))) for j in range(0, 601, 10)]
            g += f'<polyline points="{pts(seg)}" fill="none" stroke="currentColor" stroke-width="{2.6 if i % 3 == 0 else 1.5}"/>'
    d = defs(P, extra=f'<radialGradient id="mk"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></radialGradient>'
                      '<mask id="m"><rect width="600" height="600" fill="url(#mk)"/></mask>'
                      f'<radialGradient id="well"><stop offset="0" stop-color="#000" stop-opacity=".95"/><stop offset=".6" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
                      f'<g id="grid">{g}</g>')
    o = [f'<use href="#grid" color="{P["mid"]}" opacity=".5"/>',
         f'<use href="#grid" color="{P["glow"]}" mask="url(#m)" filter="url(#gl)" opacity=".9"/>',
         f'<use href="#grid" color="{P["bright"]}" mask="url(#m)" opacity=".95"/>',
         '<circle cx="300" cy="300" r="150" fill="url(#well)"/>',
         f'<circle cx="300" cy="300" r="96" fill="none" stroke="{P["glow"]}" stroke-width="5" opacity=".8" filter="url(#gl)"/>',
         letters3d(P, 168, 300, 300, ext=16, glow=True)]
    return wrap("".join(o), d)

# ---------------- 3 Schwarzes Loch (Draufsicht)
def loch(P):
    r = random.Random(17); cx, cy = 300, 318; o = []
    d = defs(P, extra=f'<radialGradient id="halo"><stop offset="0" stop-color="{P["glow"]}" stop-opacity=".0"/><stop offset=".5" stop-color="{P["glow"]}" stop-opacity=".35"/><stop offset="1" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>'
                      '<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000"/><stop offset=".8" stop-color="#030304"/><stop offset="1" stop-color="#0c0d10"/></radialGradient>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="290" fill="url(#halo)"/>')
    def band(r0, a0, span, wmax, drift, col, op):
        out, inn = [], []
        for k in range(29):
            t = k / 28; a = math.radians(a0 + span * t); wt = (math.sin(math.pi * t) ** .8) * wmax; rr = r0 + drift * t
            out.append((cx + (rr + wt / 2) * math.cos(a), cy + (rr + wt / 2) * math.sin(a))); inn.append((cx + (rr - wt / 2) * math.cos(a), cy + (rr - wt / 2) * math.sin(a)))
        return f'<polygon points="{pts(out + inn[::-1])}" fill="{col}" fill-opacity="{op}"/>'
    bands = ""
    for i in range(16):
        r0 = r.uniform(162, 262); wm = 34 - (r0 - 162) * .16 + r.uniform(-4, 4)
        bands += band(r0, r.uniform(0, 360), r.uniform(70, 210), max(8, wm), r.uniform(-26, 26), P["bright"] if i % 2 == 0 else P["mid"], fmt(r.uniform(.4, .9)))
    rim = band(150, 95, 120, 26, -6, P["bright"], 1) + band(168, 120, 70, 12, 0, P["mid"], 1)
    grp = f'transform="rotate(-8 {cx} {cy}) translate(0 {fmt(cy * .06)}) scale(1 .94)"'
    o.append(f'<g {grp} filter="url(#gl)" opacity=".8">{bands}{rim}</g><g {grp} filter="url(#sf)">{bands}</g><g {grp}>{rim}</g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="144" fill="none" stroke="{P["glow"]}" stroke-width="6" opacity=".7" filter="url(#gl)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="url(#sh)"/><circle cx="{cx}" cy="{cy}" r="139" fill="none" stroke="{P["bright"]}" stroke-opacity=".35" stroke-width="2"/>')
    o.append(letters3d(P, 124, cy, 218, ext=12, glow=True))
    return wrap("".join(o), d)

# ---------------- 4 Matrix (Aufloesung)
def matrix(P):
    r = random.Random(5); o = []
    d = defs(P)
    heads = ""
    for cx in range(40, 570, 26):
        n = r.randint(5, 14); y0 = r.uniform(0, 430)
        for k in range(n):
            y = y0 + k * 22
            if y > 590: break
            last = k == n - 1
            o.append(f'<rect x="{cx - 7}" y="{fmt(y)}" width="14" height="17" rx="2" fill="{P["bright"] if last else P["mid"]}" fill-opacity="{1 if last else fmt(0.12 + 0.55 * k / n)}"/>')
            if last: heads += f'<rect x="{cx - 7}" y="{fmt(y)}" width="14" height="17" rx="2" fill="{P["glow"]}"/>'
    o.append(f'<g filter="url(#gl)" opacity=".9">{heads}</g>')
    cap0 = 250; dd, w, cap, tx, base = geom(cap0, 285, 500, tr=8)
    r2 = random.Random(8); rects, sq = "", []; cw = 6.4; top = base - cap; x = tx - 3
    while x < tx + w + 22:
        cut = base - 34 * r2.random() ** 1.7
        rects += f'<rect x="{fmt(x)}" y="{fmt(top - 40)}" width="{cw + 1.4}" height="{fmt(cut - top + 40 + 12)}"/>'
        if r2.random() < .85:
            y = cut + 12
            for k in range(r2.randint(2, 8)):
                col = P["bright"] if k < 2 else (P["glow"] if k % 2 else P["mid"])
                sq.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cw - .6}" height="{r2.choice([6, 6, 10])}" fill="{col}" fill-opacity="{fmt(max(.2, 1 - k * .13))}"/>')
                y += 11 + k * 6
        x += cw
    o.append(f'<g filter="url(#gl)" opacity=".6">{"".join(sq)}</g>' + "".join(sq))
    o.append(f'<clipPath id="dz">{rects}</clipPath><g clip-path="url(#dz)">{letters3d(P, cap0, 285, 500, ext=14, glow=True)}</g>')
    return wrap("".join(o), d)

THEMES = {"t1-supernova": supernova, "t2-gitter": gitter, "t3-loch": loch, "t4-matrix": matrix}
for tn, f in THEMES.items():
    for pn, P in PAL.items():
        svg = f(P)
        open(os.path.join(OUT, f"{tn}_{pn}.svg"), "w").write(svg)
        app = svg.replace('viewBox="0 0 600 600" width="600" height="600">', 'viewBox="0 0 600 600" width="600" height="600"><clipPath id="ic"><rect width="600" height="600" rx="124"/></clipPath><g clip-path="url(#ic)"><g transform="translate(300 300) scale(.9) translate(-300 -300)">', 1).replace('</svg>', '</g></g></svg>')
        open(os.path.join(OUT, f"{tn}_{pn}_app.svg"), "w").write(app)
print("ok")

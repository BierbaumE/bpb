"""BPB Runde 11 - Gravitationsnetz + Schwarzes Loch in acht Farbwelten (auch mehrfarbig).
Aufruf: python3 -I runde11_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py und runde10_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde10_gen.py")).read().split("# ---------------- 1 Supernova")[0])   # Helfer: defs, geom, letters3d, wrap, mix

def pal(name, cols, hi, bg1, bg2, glow, f1, f2, s1, s2, edge):
    return dict(name=name, cols=cols, hi=hi, bg1=bg1, bg2=bg2, bright=hi[0], mid=cols[0], deep=cols[-1], glow=glow, f1=f1, f2=f2, s1=s1, s2=s2, edge=edge)
PAL2 = {
 "grau":    pal("Grau", ["#8d939e"] * 4, ["#ffffff"] * 4, "#232730", "#050608", "#dfe6f2", "#ffffff", "#aeb4c0", "#7b808a", "#14151a", "#ffffff"),
 "glut":    pal("Glut", ["#ff5a1a", "#ff7a1f", "#ff9a2e", "#ffb04a"], ["#ffd584", "#ffe6a8", "#ffc15a", "#fff0c8"], "#34140a", "#070201", "#ff8d2e", "#fff3d2", "#ffb04a", "#c8480c", "#260a03", "#fff7e0"),
 "smaragd": pal("Smaragd", ["#1fc9a2", "#22b8c9", "#1fc9a2", "#35d4b0"], ["#a6fff1", "#b8f8ff", "#a6fff1", "#d8fff8"], "#0a2e33", "#010a0c", "#36ecc6", "#ecfffc", "#6be8d2", "#139b8a", "#021a1d", "#eafffb"),
 "nebula":  pal("Nebula", ["#7a3cff", "#d23cff", "#ff3c9a", "#3c9cff"], ["#c8a8ff", "#f0a8ff", "#ffa8d0", "#a8d4ff"], "#1a0b33", "#040210", "#c04cff", "#ffffff", "#d6bcff", "#6a2fd0", "#150628", "#ffffff"),
 "sunset":  pal("Sonnenuntergang", ["#ffb000", "#ff6a2a", "#ff2e6e", "#8a3cff"], ["#ffe08a", "#ffb48a", "#ff9ab8", "#cfa8ff"], "#2a0c24", "#07020a", "#ff5a5a", "#fff4e0", "#ffb98a", "#c8326a", "#240618", "#fff4e8"),
 "aurora":  pal("Aurora", ["#3cff9a", "#26d4e0", "#3c8cff", "#a23cff"], ["#b6ffd8", "#b0f4ff", "#b0ccff", "#dcb0ff"], "#07202a", "#010609", "#3cf0c8", "#f0fffb", "#9cd8ff", "#1a7fb0", "#02121c", "#f0ffff"),
 "gold":    pal("Gold", ["#c9a24a", "#e8c872", "#b8892e", "#f1d88c"], ["#fff0b8", "#ffe08a", "#fff6d0", "#ffd870"], "#1c1608", "#050400", "#e8c060", "#fff8dc", "#e0b850", "#a67a1c", "#1c1204", "#fffaf0"),
 "eis":     pal("Eisblau", ["#4da6ff", "#7cc4ff", "#3a86ff", "#a0d8ff"], ["#d6ecff", "#ffffff", "#bfe0ff", "#e8f6ff"], "#0a1a30", "#010308", "#58b0ff", "#ffffff", "#a8d4ff", "#2a6ab8", "#04101f", "#ffffff"),
}
def lg(idn, cols):
    st = "".join(f'<stop offset="{i / (len(cols) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(cols))
    return f'<linearGradient id="{idn}" gradientUnits="userSpaceOnUse" x1="40" y1="40" x2="560" y2="560">{st}</linearGradient>'

def gitter(P):
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
    d = defs(P, extra=lg("gm", P["cols"]) + lg("gh", P["hi"]) +
             '<radialGradient id="mk"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></radialGradient>'
             '<mask id="m"><rect width="600" height="600" fill="url(#mk)"/></mask>'
             '<radialGradient id="well"><stop offset="0" stop-color="#000" stop-opacity=".95"/><stop offset=".6" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')
    gm, gh = grid("url(#gm)"), grid("url(#gh)")
    o = [f'<g opacity=".55">{gm}</g>', f'<g mask="url(#m)" filter="url(#gl)" opacity=".9">{gh}</g>', f'<g mask="url(#m)" opacity=".95">{gh}</g>',
         '<circle cx="300" cy="300" r="150" fill="url(#well)"/>',
         f'<circle cx="300" cy="300" r="96" fill="none" stroke="{P["hi"][1]}" stroke-width="5" opacity=".85" filter="url(#gl)"/>',
         letters3d(P, 168, 300, 300, ext=16, glow=True)]
    return wrap("".join(o), d)

def loch(P):
    r = random.Random(17); cx, cy = 300, 318; o = []
    d = defs(P, extra=f'<radialGradient id="halo"><stop offset="0" stop-color="{P["glow"]}" stop-opacity="0"/><stop offset=".5" stop-color="{P["glow"]}" stop-opacity=".35"/><stop offset="1" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>'
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
        bands += band(r0, r.uniform(0, 360), r.uniform(70, 210), max(8, wm), r.uniform(-26, 26), (P["hi"] if i % 2 == 0 else P["cols"])[i % 4], fmt(r.uniform(.4, .9)))
    rim = band(150, 95, 120, 26, -6, P["hi"][0], 1) + band(168, 120, 70, 12, 0, P["cols"][1], 1)
    grp = f'transform="rotate(-8 {cx} {cy}) translate(0 {fmt(cy * .06)}) scale(1 .94)"'
    o.append(f'<g {grp} filter="url(#gl)" opacity=".8">{bands}{rim}</g><g {grp} filter="url(#sf)">{bands}</g><g {grp}>{rim}</g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="144" fill="none" stroke="{P["glow"]}" stroke-width="6" opacity=".7" filter="url(#gl)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="url(#sh)"/><circle cx="{cx}" cy="{cy}" r="139" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".35" stroke-width="2"/>')
    o.append(letters3d(P, 124, cy, 218, ext=12, glow=True))
    return wrap("".join(o), d)

for tn, f in {"t2-gitter": gitter, "t3-loch": loch}.items():
    for pn, P in PAL2.items():
        svg = f(P)
        open(os.path.join(OUT, f"{tn}_{pn}.svg"), "w").write(svg)
        app = svg.replace('viewBox="0 0 600 600" width="600" height="600">', 'viewBox="0 0 600 600" width="600" height="600"><clipPath id="ic"><rect width="600" height="600" rx="124"/></clipPath><g clip-path="url(#ic)"><g transform="translate(300 300) scale(.9) translate(-300 -300)">', 1).replace('</svg>', '</g></g></svg>')
        open(os.path.join(OUT, f"{tn}_{pn}_app.svg"), "w").write(app)
print("ok")

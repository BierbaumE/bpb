"""BPB Runde 12 - Schwarzes Loch: feinere Raender (mehr, duennere Baender + Haarlinien), groesserer schwarzer Kern.
Aufruf: python3 -I runde12_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py, runde10_gen.py, runde11_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde11_gen.py")).read().split("def gitter(P):")[0])   # Helfer + Paletten PAL2

def loch(P):
    r = random.Random(23); cx, cy = 300, 316; o = []; R = 172
    d = defs(P, extra=f'<radialGradient id="halo"><stop offset="0" stop-color="{P["glow"]}" stop-opacity="0"/><stop offset=".55" stop-color="{P["glow"]}" stop-opacity=".30"/><stop offset="1" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>'
                      '<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000"/><stop offset=".85" stop-color="#020203"/><stop offset="1" stop-color="#0b0c0f"/></radialGradient>'
                      '<filter id="sf2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="0.8"/></filter>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="292" fill="url(#halo)"/>')
    def band(r0, a0, span, wmax, drift, col, op):
        out, inn = [], []
        for k in range(33):
            t = k / 32; a = math.radians(a0 + span * t); wt = (math.sin(math.pi * t) ** .9) * wmax; rr = r0 + drift * t
            out.append((cx + (rr + wt / 2) * math.cos(a), cy + (rr + wt / 2) * math.sin(a))); inn.append((cx + (rr - wt / 2) * math.cos(a), cy + (rr - wt / 2) * math.sin(a)))
        return f'<polygon points="{pts(out + inn[::-1])}" fill="{col}" fill-opacity="{op}"/>'
    bands = ""
    for i in range(32):                                                       # viele, duennere Wirbelbaender
        r0 = r.uniform(186, 274); wm = 22 - (r0 - 186) * .16 + r.uniform(-3, 3)
        bands += band(r0, r.uniform(0, 360), r.uniform(50, 190), max(5, wm), r.uniform(-18, 18), (P["hi"] if i % 3 == 0 else P["cols"])[i % 4], fmt(r.uniform(.35, .85)))
    hair = ""
    for i in range(14):                                                       # Haarlinien: feine Raender
        r0 = r.uniform(180, 282); hair += band(r0, r.uniform(0, 360), r.uniform(110, 300), r.uniform(1.8, 3.4), r.uniform(-10, 10), P["hi"][i % 4], fmt(r.uniform(.5, .95)))
    rim = band(R + 4, 95, 125, 15, -4, P["hi"][0], 1) + band(R + 17, 118, 72, 6, 0, P["cols"][1], 1) + band(R + 26, 130, 40, 3, 0, P["hi"][2], .9)
    grp = f'transform="rotate(-8 {cx} {cy}) translate(0 {fmt(cy * .06)}) scale(1 .94)"'
    o.append(f'<g {grp} filter="url(#gl)" opacity=".7">{bands}{rim}</g><g {grp} filter="url(#sf2)">{bands}</g><g {grp}>{hair}{rim}</g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 4}" fill="none" stroke="{P["glow"]}" stroke-width="5" opacity=".7" filter="url(#gl)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sh)"/><circle cx="{cx}" cy="{cy}" r="{R - 1}" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".35" stroke-width="1.6"/>')
    o.append(letters3d(P, 150, cy, 268, ext=13, glow=True))
    return wrap("".join(o), d)

for pn, P in PAL2.items():
    svg = loch(P)
    open(os.path.join(OUT, f"t3-loch2_{pn}.svg"), "w").write(svg)
    app = svg.replace('viewBox="0 0 600 600" width="600" height="600">', 'viewBox="0 0 600 600" width="600" height="600"><clipPath id="ic"><rect width="600" height="600" rx="124"/></clipPath><g clip-path="url(#ic)"><g transform="translate(300 300) scale(.9) translate(-300 -300)">', 1).replace('</svg>', '</g></g></svg>')
    open(os.path.join(OUT, f"t3-loch2_{pn}_app.svg"), "w").write(app)
print("ok")

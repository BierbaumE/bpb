"""BPB Runde 14 - Formenfamilie: feiner Rand, Logo in Kreis / Quadrat / Raute / Dreieck / Sechseck / Schild.
Aufruf: python3 -I runde14_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4/10/11/13_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde13_gen.py")).read().split("def A(P):")[0])    # extra(), content() (Netz), svgwrap(), PAL2, Helfer

def loch_content(P):
    r = random.Random(23); cx, cy = 300, 316; o = []; R = 172
    o.append(f'<circle cx="{cx}" cy="{cy}" r="292" fill="url(#halo)"/>')
    def band(r0, a0, span, wmax, drift, col, op):
        out, inn = [], []
        for k in range(33):
            t = k / 32; a = math.radians(a0 + span * t); wt = (math.sin(math.pi * t) ** .9) * wmax; rr = r0 + drift * t
            out.append((cx + (rr + wt / 2) * math.cos(a), cy + (rr + wt / 2) * math.sin(a))); inn.append((cx + (rr - wt / 2) * math.cos(a), cy + (rr - wt / 2) * math.sin(a)))
        return f'<polygon points="{pts(out + inn[::-1])}" fill="{col}" fill-opacity="{op}"/>'
    bands = ""
    for i in range(32):
        r0 = r.uniform(186, 274); wm = 22 - (r0 - 186) * .16 + r.uniform(-3, 3)
        bands += band(r0, r.uniform(0, 360), r.uniform(50, 190), max(5, wm), r.uniform(-18, 18), (P["hi"] if i % 3 == 0 else P["cols"])[i % 4], fmt(r.uniform(.35, .85)))
    hair = "".join(band(r.uniform(180, 282), r.uniform(0, 360), r.uniform(110, 300), r.uniform(1.8, 3.4), r.uniform(-10, 10), P["hi"][i % 4], fmt(r.uniform(.5, .95))) for i in range(14))
    rim = band(R + 4, 95, 125, 15, -4, P["hi"][0], 1) + band(R + 17, 118, 72, 6, 0, P["cols"][1], 1) + band(R + 26, 130, 40, 3, 0, P["hi"][2], .9)
    grp = f'transform="rotate(-8 {cx} {cy}) translate(0 {fmt(cy * .06)}) scale(1 .94)"'
    o.append(f'<g {grp} filter="url(#gl)" opacity=".7">{bands}{rim}</g><g {grp} filter="url(#sf2)">{bands}</g><g {grp}>{hair}{rim}</g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 4}" fill="none" stroke="{P["glow"]}" stroke-width="5" opacity=".7" filter="url(#gl)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sh)"/><circle cx="{cx}" cy="{cy}" r="{R - 1}" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".35" stroke-width="1.6"/>')
    o.append(letters3d(P, 150, cy, 268, ext=13, glow=True))
    return "".join(o)

def xtra(P):
    return extra(P) + (f'<radialGradient id="halo"><stop offset="0" stop-color="{P["glow"]}" stop-opacity="0"/><stop offset=".55" stop-color="{P["glow"]}" stop-opacity=".30"/><stop offset="1" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>'
                       '<radialGradient id="sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000"/><stop offset=".85" stop-color="#020203"/><stop offset="1" stop-color="#0b0c0f"/></radialGradient>'
                       '<filter id="sf2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="0.8"/></filter>')

def rpath(pt, r):
    n = len(pt); d = ""
    for i in range(n):
        p0, p1, p2 = pt[i - 1], pt[i], pt[(i + 1) % n]
        def un(a, b):
            l = math.hypot(b[0] - a[0], b[1] - a[1]); return ((b[0] - a[0]) / l, (b[1] - a[1]) / l)
        v1, v2 = un(p1, p0), un(p1, p2)
        a = (p1[0] + v1[0] * r, p1[1] + v1[1] * r); b = (p1[0] + v2[0] * r, p1[1] + v2[1] * r)
        d += f'{"M" if i == 0 else "L"} {fmt(a[0])} {fmt(a[1])} Q {fmt(p1[0])} {fmt(p1[1])} {fmt(b[0])} {fmt(b[1])} '
    return d + "Z"

hexp = [(300 + 272 * math.cos(math.radians(-90 + 60 * k)), 300 + 272 * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
SHAPES = {   # name: (Pfad, Mittelpunkt, Inhalts-Transform)
 "kreis":    ("M 38 300 a 262 262 0 1 0 524 0 a 262 262 0 1 0 -524 0 Z", (300, 300), "translate(300 300) scale(.94) translate(-300 -300)"),
 "quadrat":  (rpath([(44, 44), (556, 44), (556, 556), (44, 556)], 70), (300, 300), "translate(300 300) scale(.9) translate(-300 -300)"),
 "raute":    (rpath([(300, 26), (574, 300), (300, 574), (26, 300)], 46), (300, 300), "translate(300 300) scale(.74) translate(-300 -300)"),
 "dreieck":  (rpath([(300, 34), (568, 502), (32, 502)], 56), (300, 346), "translate(300 372) scale(.7) translate(-300 -300)"),
 "sechseck": (rpath(hexp, 44), (300, 300), "translate(300 300) scale(.88) translate(-300 -300)"),
 "schild":   ("M 66 66 Q 66 42 90 42 H 510 Q 534 42 534 66 V 290 Q 534 470 300 566 Q 66 470 66 290 Z", (300, 300), "translate(300 292) scale(.9) translate(-300 -300)"),
}

def framed(P, shape, kind):
    dpath, (cx, cy), ct = SHAPES[shape]
    ins = lambda s: f'transform="translate({cx} {cy}) scale({s}) translate({-cx} {-cy})"'
    d = defs(P, extra=xtra(P)); o = []
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["glow"]}" stroke-width="8" opacity=".55" filter="url(#gl)"/>')
    o.append(f'<path d="{dpath}" fill="#000" opacity=".7" filter="url(#ds)" transform="translate(0 14)"/>')
    o.append(f'<path d="{dpath}" fill="url(#bz)"/>')                                                          # feine Metallkante
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["edge"]}" stroke-opacity=".8" stroke-width="1.2"/>')
    o.append(f'<path d="{dpath}" fill="#05060a" {ins(.972)}/>')
    o.append(f'<clipPath id="cp"><path d="{dpath}" {ins(.962)}/></clipPath>')
    body = content(P) if kind == "netz" else loch_content(P)
    o.append(f'<g clip-path="url(#cp)"><path d="{dpath}" fill="url(#bg)" {ins(.962)}/><g transform="{ct}">{body}</g></g>')
    o.append(f'<path d="{dpath}" fill="none" stroke="{P["hi"][0]}" stroke-opacity=".5" stroke-width="1" {ins(.962)}/>')
    return svgwrap(P, "".join(o), d)

ORDER = [("kreis", "nebula"), ("quadrat", "aurora"), ("raute", "glut"), ("dreieck", "sunset"), ("sechseck", "smaragd"), ("schild", "eis")]
for kind in ("netz", "loch"):
    for shape, pn in ORDER:
        open(os.path.join(OUT, f"f-{kind}_{shape}_{pn}.svg"), "w").write(framed(PAL2[pn], shape, kind))
print("ok")

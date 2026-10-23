"""BPB Runde 6 - Raumzeit: Supernova / Gravitationsloch / Schwarzes Loch / Riss. Nur Schwarz/Weiss/Grau.
Aufruf: python3 -I runde6_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4.py im selben Ordner fuer text_path)"""
import sys, os, math, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runde4_gen.py")).read()
exec(src.split("def fmt")[0])
def fmt(v): return f"{v:.1f}"
def pts(l): return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in l)
def P(c, r, a): return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))

def letters(ink, paper, cap, cy, ow=16, rot=0, halo=False):
    d, w, cap = text_path(ANTON, "BPB", cap, tracking=6, max_w=500)
    tx = (600 - w) / 2; base = cy + cap / 2
    pre = f'<path d="{d}" fill="{paper}" stroke="{paper}" stroke-width="{ow + 14}" stroke-linejoin="round"/>' if halo else ""
    return (f'<g transform="rotate({rot} 300 {fmt(cy)}) translate({fmt(tx)} {fmt(base)})">{pre}'
            f'<path d="{d}" fill="{ink}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="miter"/><path d="{d}" fill="{paper}"/></g>')

def supernova(ink, paper, mid):
    r = random.Random(5); c = (300, 300); o = []
    for k in range(34):                                     # Strahlen
        a = k * 2 * math.pi / 34 + r.uniform(-.03, .03); L = r.choice([290, 250, 205, 290, 175]); w = .045
        o.append(f'<polygon points="{pts([P(c, 60, a - w), P(c, L, a), P(c, 60, a + w)])}" fill="{ink if k % 3 else mid}"/>')
    for rad, sw, dash, col in [(150, 16, "70 20 12 34 100 16", ink), (200, 10, "40 26 120 14 22 40", mid), (250, 6, "16 30 60 24 8 50", ink)]:
        o.append(f'<circle cx="300" cy="300" r="{rad}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}" transform="rotate({r.randint(0,90)} 300 300)"/>')
    core = [P(c, 128 if k % 2 == 0 else 100, k * math.pi / 12) for k in range(24)]
    o.append(f'<circle cx="300" cy="300" r="170" fill="{paper}"/>')
    o.append(f'<polygon points="{pts(core)}" fill="{ink}"/>')
    return "".join(o) + letters(ink, paper, 150, 300, ow=13, halo=False)

def gitter(ink, paper, mid):
    c = (300, 300); o = []
    def warp(x, y):
        dx, dy = x - c[0], y - c[1]; d = math.hypot(dx, dy) + 1e-6
        k = 1 - .88 * math.exp(-(d / 120) ** 2) - .25 * math.exp(-(d / 260) ** 2)
        return c[0] + dx * k, c[1] + dy * k
    r = random.Random(2)
    for horiz in (True, False):
        for i in range(-1, 24):
            v = i * 27 + 6; seg = []; gap = r.random() < .25
            for j in range(0, 601, 10):
                x, y = (j, v) if horiz else (v, j); seg.append(warp(x, y))
            o.append(f'<polyline points="{pts(seg)}" fill="none" stroke="{ink if i % 3 == 0 else mid}" stroke-width="{3.2 if i % 3 == 0 else 2}"/>')
    ring = "".join(f'<circle cx="300" cy="300" r="{rr}" fill="none" stroke="{ink}" stroke-width="3"/>' for rr in (74, 96))
    return "".join(o) + ring + letters(ink, paper, 168, 300, ow=14, halo=True)

def loch(ink, paper, mid):
    r = random.Random(9); c = (300, 392); o = []
    o.append(f'<ellipse cx="300" cy="400" rx="262" ry="62" fill="none" stroke="{mid}" stroke-width="26"/>')
    o.append(f'<ellipse cx="300" cy="400" rx="232" ry="46" fill="none" stroke="{ink}" stroke-width="7"/>')
    o.append(f'<circle cx="300" cy="392" r="132" fill="{ink}"/>')
    o.append(f'<path d="M 120 400 A 180 180 0 0 1 480 400" fill="none" stroke="{ink}" stroke-width="9"/>')
    o.append(f'<path d="M 36 404 A 264 264 0 0 1 564 404" fill="none" stroke="{mid}" stroke-width="5"/>')
    for k in range(18):                                   # Spaghettifizierung: Splitter in Richtung Loch
        x = r.uniform(110, 490); y = r.uniform(235, 330); a = math.atan2(392 - y, 300 - x); L = r.uniform(34, 80); w = r.uniform(3, 7)
        o.append(f'<polygon points="{pts([(x + w * math.sin(a), y - w * math.cos(a)), (x - w * math.sin(a), y + w * math.cos(a)), (x + L * math.cos(a), y + L * math.sin(a))])}" fill="{ink}"/>')
    o.append(f'<ellipse cx="300" cy="400" rx="262" ry="62" fill="none" stroke="{mid}" stroke-width="26" clip-path="url(#lf)"/>')
    clip = '<clipPath id="lf"><rect x="0" y="400" width="600" height="200"/></clipPath>'
    return clip + "".join(o) + letters(ink, paper, 170, 215, ow=14, halo=True)

def riss(ink, paper, mid):
    r = random.Random(13); o = []
    def jag(p0, p1, n, amp):
        out = []
        for i in range(n + 1):
            t = i / n; x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
            a = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); j = 0 if i in (0, n) else r.uniform(-amp, amp)
            out.append((x - j * math.sin(a), y + j * math.cos(a)))
        return out
    top = jag((-30, 345), (630, 150), 15, 20); bot = jag((-30, 480), (630, 292), 15, 20)
    o.append(f'<polygon points="{pts(top + bot[::-1])}" fill="{ink}"/>')
    o.append(f'<polyline points="{pts([(x, y - 11) for x, y in top])}" fill="none" stroke="{mid}" stroke-width="9"/>')
    o.append(f'<polyline points="{pts([(x, y + 11) for x, y in bot])}" fill="none" stroke="{mid}" stroke-width="9"/>')
    for i in range(16):                                    # Sterne im Spalt
        t = r.uniform(.05, .95); x = -30 + 660 * t; yc = 412 - 190 * t + r.uniform(-30, 30); s = r.uniform(4, 9)
        o.append(f'<rect x="{fmt(x)}" y="{fmt(yc)}" width="{fmt(s)}" height="{fmt(s)}" fill="{paper}"/>')
    for i in range(7):                                     # abgerissene Fetzen
        x = r.uniform(60, 540); y = 412 - 190 * (x / 600) + r.choice([-1, 1]) * r.uniform(95, 140); s = r.uniform(12, 26)
        o.append(f'<polygon points="{pts([(x + r.uniform(-s, s), y + r.uniform(-s, s)) for _ in range(4)])}" fill="{ink}"/>')
    return "".join(o) + letters(paper, ink, 200, 300, ow=14, rot=-12, halo=False).replace(f'fill="{paper}" stroke="{paper}"', f'fill="{paper}" stroke="{paper}"')

C = {"r6a-supernova": supernova, "r6b-gitter": gitter, "r6c-loch": loch, "r6d-riss": riss}
INK, PAPER = "#111111", "#ffffff"
def svg(b, bg=None):
    r = f'<rect width="600" height="600" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">{r}{b}</svg>'
for n, f in C.items():
    w = {f"{n}_hell.svg": svg(f(INK, PAPER, "#8c8c8c"), PAPER),
         f"{n}_dunkel.svg": svg(f(PAPER, INK, "#7a7a7a"), INK),
         f"{n}_app.svg": svg(f'<rect width="600" height="600" rx="124" fill="{INK}"/><g transform="translate(300 300) scale(.84) translate(-300 -300)">{f(PAPER, INK, "#7a7a7a")}</g>')}
    for k, v in w.items(): open(os.path.join(OUT, k), "w").write(v)
print("ok")

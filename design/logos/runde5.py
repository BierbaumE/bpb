"""BPB Runde 5 - Ausbruch: BPB sprengt sich aus Fels / Vulkan / Motorblock. Nur Schwarz/Weiss/Grau.
Aufruf: python3 -I runde5_gen.py <ofl-Ordner> <Ausgabe>"""
import sys, os, math, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runde4_gen.py")).read()
sys.argv = sys.argv[:1] + [sys.argv[1], sys.argv[2]]
exec(src.split("def fmt")[0])          # text_path, ANTON, OUT
def fmt(v): return f"{v:.1f}"
def pts(l): return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in l)
def P(c, r, a): return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))

def letters(ink, paper, cap, base, ow=16):
    d, w, cap = text_path(ANTON, "BPB", cap, tracking=6, max_w=520)
    tx = (600 - w) / 2
    return (f'<g transform="translate({fmt(tx)} {fmt(base)})"><path d="{d}" fill="{ink}" stroke="{ink}" stroke-width="{ow}" stroke-linejoin="miter"/>'
            f'<path d="{d}" fill="{paper}"/></g>')

def fels(ink, paper, mid, seed=4):
    r = random.Random(seed); c = (300, 300); n = 14; out = []
    base = r.random() * 6
    for i in range(n):
        a0 = base + i * 2 * math.pi / n + 0.035; a1 = base + (i + 1) * 2 * math.pi / n - 0.035
        am = (a0 + a1) / 2; R = r.uniform(185, 262); off = r.uniform(14, 52)
        o = (off * math.cos(am), off * math.sin(am))
        poly = [P(c, 70, a0), P(c, R * r.uniform(.82, 1), a0 + .01), P(c, R * r.uniform(.7, 1.05), am), P(c, R * r.uniform(.82, 1), a1 - .01), P(c, 70, a1)]
        poly = [(x + o[0], y + o[1]) for x, y in poly]
        out.append(f'<polygon points="{pts(poly)}" fill="{[ink, mid, ink, mid, ink][i % 5] if i % 3 else ink}"/>')
    for i in range(16):                  # Brocken
        a = r.uniform(0, 6.28); d = r.uniform(255, 295); s = r.uniform(7, 19); p = P(c, d, a)
        t = [(p[0] + r.uniform(-s, s), p[1] + r.uniform(-s, s)) for _ in range(3)]
        out.append(f'<polygon points="{pts(t)}" fill="{ink}"/>')
    star = [P(c, 168 if k % 2 == 0 else 118, k * math.pi / 11 + .2) for k in range(22)]
    out.insert(0, f'<polygon points="{pts(star)}" fill="{paper}" stroke="{ink}" stroke-width="7" stroke-linejoin="round"/>')
    return "".join(out) + letters(ink, paper, 188, 394)

def vulkan(ink, paper, mid):
    r = random.Random(7); o = []
    for k in range(9):                   # Strahlen aus dem Krater
        a = math.radians(-162 + k * 18); L = r.uniform(270, 380); w = .15
        o.append(f'<polygon points="{pts([P((300, 372), 20, a - w), P((300, 372), L, a), P((300, 372), 20, a + w)])}" fill="{mid if k % 2 else ink}"/>')
    for i in range(14):
        p = (r.uniform(70, 530), r.uniform(40, 250)); s = r.uniform(6, 15)
        o.append(f'<polygon points="{pts([(p[0] + r.uniform(-s, s), p[1] + r.uniform(-s, s)) for _ in range(3)])}" fill="{ink}"/>')
    m = [(14, 580), (96, 500), (130, 508), (190, 410), (212, 420), (228, 352), (262, 386), (300, 372), (338, 386), (372, 352), (388, 420), (410, 410), (470, 508), (504, 500), (586, 580)]
    o.append(f'<polygon points="{pts(m)}" fill="{ink}"/>')
    for x0, dx in [(262, -14), (300, 6), (338, 16)]:   # Lavarisse
        z = [(x0, 392), (x0 + dx, 440), (x0 + dx * .3, 478), (x0 + dx * 1.6, 530), (x0 + dx, 575)]
        o.append(f'<polyline points="{pts(z)}" fill="none" stroke="{paper}" stroke-width="7" stroke-linejoin="miter"/>')
    return "".join(o) + letters(ink, paper, 214, 382)

def motor(ink, paper, mid):
    r = random.Random(11); o = []
    o.append(f'<rect x="40" y="282" width="520" height="262" rx="26" fill="{ink}"/>')
    c = (300, 420); hole = [P(c, r.uniform(120, 175), k * 2 * math.pi / 13 + r.uniform(-.1, .1)) for k in range(13)]
    o.append(f'<polygon points="{pts(hole)}" fill="{mid}"/>')
    for k in range(9):                   # Risse
        a = k * 2 * math.pi / 9 + .3; p = P(c, 150, a); q = P(c, r.uniform(205, 270), a + r.uniform(-.15, .15)); m = P(c, 190, a + .1)
        o.append(f'<polyline points="{pts([p, m, q])}" fill="none" stroke="{paper}" stroke-width="6"/>')
    for k in range(7):                   # fliegende Stuecke
        a = -math.pi * (.08 + .84 * k / 6) + r.uniform(-.1, .1); p = P(c, r.uniform(210, 290), a); s = r.uniform(16, 34)
        q = [(p[0] + r.uniform(-s, s), p[1] + r.uniform(-s, s)) for _ in range(4)]
        o.append(f'<polygon points="{pts(q)}" fill="{ink if k % 2 else mid}"/>')
    return "".join(o) + letters(ink, paper, 252, 452)


def matrix(ink, paper, mid):
    r = random.Random(3); o = []
    for cx in range(40, 570, 26):                      # Code-Regen
        n = r.randint(5, 14); y0 = r.uniform(10, 430)
        for k in range(n):
            y = y0 + k * 22
            if y > 580: break
            last = k == n - 1
            o.append(f'<rect x="{cx - 7}" y="{fmt(y)}" width="14" height="17" rx="2" fill="{ink if last else mid}" fill-opacity="{1 if last else fmt(0.3 + 0.7 * k / n)}"/>')
    d, w, cap = text_path(ANTON, "BPB", 210, tracking=6, max_w=470)
    base = 405; tx = (600 - w) / 2; top = base - cap - 8; bh = (cap + 16) / 8
    dxs = [0, -16, 0, 12, 0, -10, 20, 0]
    clips, parts = "", ""
    for i, dx in enumerate(dxs):
        y = top + i * bh
        clips += f'<clipPath id="mb{i}"><rect x="0" y="{fmt(y)}" width="600" height="{fmt(bh + .5)}"/></clipPath>'
        parts += (f'<g clip-path="url(#mb{i})"><g transform="translate({fmt(tx + dx)} {fmt(base)})">'
                  f'<path d="{d}" fill="{paper}" stroke="{paper}" stroke-width="18" stroke-linejoin="round"/><path d="{d}" fill="{ink}"/></g></g>')
    for i in range(22):                                # abplatzende Pixel
        x = r.uniform(70, 530); y = r.choice([r.uniform(150, 205), r.uniform(405, 450)]); s = r.uniform(7, 15)
        o.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(s)}" height="{fmt(s)}" fill="{ink if i % 3 else paper}" stroke="{ink}" stroke-width="3"/>')
    return clips + "".join(o) + parts

C = {"r5a-fels": fels, "r5b-vulkan": vulkan, "r5c-matrix": matrix}
INK, PAPER = "#111111", "#ffffff"
def svg(b, bg=None):
    r = f'<rect width="600" height="600" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">{r}{b}</svg>'
for n, f in C.items():
    w = {f"{n}_hell.svg": svg(f(INK, PAPER, "#8c8c8c"), PAPER),
         f"{n}_dunkel.svg": svg(f(PAPER, INK, "#7a7a7a"), INK),
         f"{n}_app.svg": svg(f'<rect width="600" height="600" rx="124" fill="{INK}"/><g transform="translate(300 300) scale(.86) translate(-300 -300)">{f(PAPER, INK, "#7a7a7a")}</g>')}
    for k, v in w.items(): open(os.path.join(OUT, k), "w").write(v)
print("ok")

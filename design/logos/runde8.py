"""BPB Runde 8 - Matrix feiner (BPB zerfaellt spaet, kleine Pixel) + Schwarzes Loch mit Drehung (schraeger Gasring, Lichtbogen).
Aufruf: python3 -I runde8_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py und runde7_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde4_gen.py")).read().split("def fmt")[0])
def fmt(v): return f"{v:.1f}"
def pts(l): return " ".join(f"{fmt(x)},{fmt(y)}" for x, y in l)

def rain(head, tail, seed=3):
    r = random.Random(seed); o = []
    for cx in range(40, 570, 26):
        n = r.randint(5, 14); y0 = r.uniform(0, 430)
        for k in range(n):
            y = y0 + k * 22
            if y > 590: break
            last = k == n - 1
            o.append(f'<rect x="{cx - 7}" y="{fmt(y)}" width="14" height="17" rx="2" fill="{head if last else tail}" fill-opacity="{1 if last else fmt(0.25 + 0.6 * k / n)}"/>')
    return "".join(o)

def matrix(letter, halo, head, tail):        # BPB bleibt fast ganz, zerfaellt nur im unteren Rand in feine Pixel
    r = random.Random(8)
    d, w, cap = text_path(ANTON, "BPB", 250, tracking=8, max_w=510)
    base = 285 + cap / 2; tx = (600 - w) / 2; top = base - cap
    rects, sq, cw = "", [], 6.4
    x = tx - 3
    while x < tx + w + 3:
        cut = base - 34 * r.random() ** 1.7
        rects += f'<rect x="{fmt(x)}" y="{fmt(top - 30)}" width="{cw + 1.4}" height="{fmt(cut - top + 30)}"/>'
        if r.random() < .85:
            y = cut + 3
            for k in range(r.randint(2, 8)):
                sq.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{cw - .6}" height="{r.choice([6, 6, 10])}" fill="{letter if k < 2 else (head if k % 2 else tail)}" fill-opacity="{fmt(max(.2, 1 - k * .13))}"/>')
                y += 11 + k * 6
        x += cw
    o = rain(head, tail, 5) + "".join(sq)
    o += (f'<clipPath id="dz">{rects}</clipPath><g clip-path="url(#dz)"><g transform="translate({fmt(tx)} {fmt(base)})">'
          f'<path d="{d}" fill="{halo}" stroke="{halo}" stroke-width="34" stroke-linejoin="round"/><path d="{d}" fill="{letter}"/></g></g>')
    return o

def loch(ink, paper, mid):                   # Schatten bleibt immer dunkel; Gasring schraeg, Licht um den Schatten gebogen
    r = random.Random(4); cx, cy = 300, 372; o = []
    SH = "#111111"; bright = ink if ink != SH else mid     # ink = Strichfarbe der Variante
    line = ink; soft = mid
    # Gasring: viele duenne Ellipsen mit Bewegungsstrichen (Drehung)
    rings = [(268, 30, 6, "150 26 60 18 220 34", line), (240, 26, 11, "90 20 180 30 40 22", soft), (212, 22, 15, "230 40 90 16", line),
             (184, 18, 9, "60 14 130 24 30 12", soft), (158, 14, 6, "110 20 50 18", line)]
    def disc(clip=""):
        s = ""
        for i, (rx, ry, sw, dash, col) in enumerate(rings):
            s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}" stroke-dashoffset="{i * 37}" {clip}/>'
        return s
    spir = ""
    for k, a0 in enumerate((0.4, 2.5, 4.6)):         # Spiralarme nach innen: zeigt Drehrichtung
        pp = []
        for t in range(0, 41):
            u = t / 40; a = a0 + u * 2.4; rad = 252 - 130 * u
            pp.append((cx + rad * math.cos(a), cy + rad * 0.215 * math.sin(a)))
        spir += f'<polyline points="{pts(pp)}" fill="none" stroke="{soft}" stroke-width="4" stroke-linecap="round" stroke-dasharray="26 10"/>'
    clip = '<clipPath id="lf"><rect x="0" y="372" width="600" height="300"/></clipPath>'
    back = disc() + spir
    shadow = f'<circle cx="{cx}" cy="{cy}" r="92" fill="{SH}"/>'
    lens = (f'<path d="M {cx - 126} {cy} A 126 126 0 0 1 {cx + 126} {cy}" fill="none" stroke="{line}" stroke-width="24"/>'
            f'<path d="M {cx - 105} {cy} A 105 105 0 0 1 {cx + 105} {cy}" fill="none" stroke="{soft}" stroke-width="7"/>'
            f'<path d="M {cx - 118} {cy + 2} A 118 118 0 0 0 {cx + 118} {cy + 2}" fill="none" stroke="{soft}" stroke-width="16"/>')
    front = disc('clip-path="url(#lf)"')
    sl = ""
    for k in range(16):                              # Splitter werden Richtung Loch gezogen
        x = r.uniform(120, 480); y = r.uniform(150, 250); a = math.atan2(cy - y, cx - x); L = r.uniform(34, 86); wd = r.uniform(2.5, 6)
        sl += f'<polygon points="{pts([(x + wd * math.sin(a), y - wd * math.cos(a)), (x - wd * math.sin(a), y + wd * math.cos(a)), (x + L * math.cos(a), y + L * math.sin(a))])}" fill="{line}"/>'
    d, w, cap = text_path(ANTON, "BPB", 150, tracking=6, max_w=440)
    base = 52 + cap; tx = (600 - w) / 2
    lt = (f'<g transform="translate({fmt(tx)} {fmt(base)})"><path d="{d}" fill="{paper}" stroke="{paper}" stroke-width="30" stroke-linejoin="round"/>'
          f'<path d="{d}" fill="{line}" stroke="{line}" stroke-width="14"/><path d="{d}" fill="{paper}"/></g>')
    return clip + f'<g transform="rotate(-9 {cx} {cy})">' + back + shadow + lens + front + '</g>' + sl + lt

INK, PAPER = "#111111", "#ffffff"
COL = {"hell": (INK, PAPER, INK, "#9a9a9a", PAPER), "dunkel": (PAPER, INK, PAPER, "#555555", INK), "gruen": (PAPER, INK, "#c8ffd8", "#22c55e", INK)}
def svg(b, bg): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" fill="{bg}"/>{b}</svg>'
for n, f in {"r8a-matrix": matrix, "r8b-loch": loch}.items():
    for k, (le, ha, he, ta, bg) in COL.items():
        if n == "r8b-loch":
            body = f(he if k != "hell" else INK, ha if k == "dunkel" else PAPER, "#8c8c8c" if k == "hell" else "#9a9a9a") if False else None
        open(os.path.join(OUT, f"{n}_{k}.svg"), "w").write(svg(f(le, ha, he, ta) if n == "r8a-matrix" else f(le, ha if k != "hell" else PAPER, ta), bg if n == "r8a-matrix" or k != "x" else bg))
    le, ha, he, ta, bg = COL["dunkel"]
    body = f(le, ha, he, ta) if n == "r8a-matrix" else f(le, ha, ta)
    open(os.path.join(OUT, f"{n}_app.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" rx="124" fill="{INK}"/><g transform="translate(300 300) scale(.86) translate(-300 -300)">{body}</g></svg>')
print("ok")

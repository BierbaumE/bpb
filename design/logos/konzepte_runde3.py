"""BPB-Logo Runde 3 „neu gedacht“ (22.10.2026): sechs freie Konzepte, je Lettermark + Emblem.

Vorgaben von Eike: immer BPB zusammen (auch klein), Lettermark + Emblem, sexy/ansprechend,
frei von alten Ideen. Schriften: Google Fonts (OFL, frei auch für Logos), als Umrisse
eingebettet – die SVGs brauchen keine Schriftdateien.
Aufruf: python3 konzepte.py <ausgabeordner> <schriftordner>
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
FD = sys.argv[2] if len(sys.argv) > 2 else "fonts"
os.makedirs(OUT, exist_ok=True)
_cache = {}


def font(name):
    if name not in _cache:
        _cache[name] = TTFont(os.path.join(FD, name + ".ttf"))
    return _cache[name]


def glyph_d(fname, ch, size, x, y):
    f = font(fname)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    s = size / f["head"].unitsPerEm
    g = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
    return pen.getCommands(), f["hmtx"][g][0] * s


def ink_bounds(fname, text, size, track=0.0):
    """Tatsächliche Ausdehnung (x0, y0, x1, y1) bei Grundlinie y=0, Start x=0."""
    f = font(fname)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    s = size / f["head"].unitsPerEm
    xs, ys, cur = [], [], 0.0
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            a, b, c, d = bp.bounds
            xs += [cur + a * s, cur + c * s]
            ys += [-d * s, -b * s]
        cur += f["hmtx"][g][0] * s + (track[i] if isinstance(track, (list, tuple)) and i < len(track) else (track if not isinstance(track, (list, tuple)) else 0)) * size
    return min(xs), min(ys), max(xs), max(ys)


def word(fname, text, size, x, y, track=0.0):
    """Wort als Umriss; track = Zusatzabstand je Buchstabe (em), Zahl oder Liste."""
    ds, cur = [], x
    for i, ch in enumerate(text):
        d, adv = glyph_d(fname, ch, size, cur, y)
        ds.append(d)
        t = track[i] if isinstance(track, (list, tuple)) and i < len(track) else (0 if isinstance(track, (list, tuple)) else track)
        cur += adv + t * size
    return " ".join(ds)


def word_centered(fname, text, size, cx, cy, track=0.0, by_caps=True):
    """Wort mit Tinten-Mitte auf (cx, cy)."""
    x0, y0, x1, y1 = ink_bounds(fname, text, size, track)
    return word(fname, text, size, cx - (x0 + x1) / 2, cy - (y0 + y1) / 2, track), (x1 - x0, y1 - y0)


def word_fit(fname, text, width, cx, cy, track=0.0):
    x0, _, x1, _ = ink_bounds(fname, text, 100, track)
    size = 100 * width / (x1 - x0)
    return word_centered(fname, text, size, cx, cy, track)[0], size


def arc_text(fname, text, size, cx, cy, r, center_deg=-90, spacing=0.05, bottom=False):
    f = font(fname)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    s = size / f["head"].unitsPerEm
    adv = [hmtx[cmap[ord(c)]][0] * s + spacing * size for c in text]
    total = sum(adv) - spacing * size
    pen = SVGPathPen(gs)
    a = math.radians(center_deg) + (total / r / 2 if bottom else -total / r / 2)
    for c, w in zip(text, adv):
        g = cmap[ord(c)]
        gw = hmtx[g][0] * s
        mid = a - (gw / 2) / r if bottom else a + (gw / 2) / r
        px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
        rot = mid - math.pi / 2 if bottom else mid + math.pi / 2
        ca, sa = math.cos(rot), math.sin(rot)
        gs[g].draw(TransformPen(pen, (s * ca, s * sa, s * sa, -s * ca, px - gw / 2 * ca, py - gw / 2 * sa)))
        a = a - w / r if bottom else a + w / r
    return pen.getCommands()


def lin(gid, stops, x0, y0, x1, y1):
    n = len(stops) - 1
    st = "".join(f'<stop offset="{i / n:.3f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" y1="{y0:.0f}" '
            f'x2="{x1:.0f}" y2="{y1:.0f}">{st}</linearGradient>')


def svg(vb, body, defs=""):
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}" '
            f'width="{w / 2:.0f}" height="{h / 2:.0f}"><defs>{defs}</defs>{body}</svg>')


def rrect(x0, y0, x1, y1, r):
    return (f"M {x0 + r} {y0} H {x1 - r} A {r} {r} 0 0 1 {x1} {y0 + r} V {y1 - r} A {r} {r} 0 0 1 {x1 - r} {y1} "
            f"H {x0 + r} A {r} {r} 0 0 1 {x0} {y1 - r} V {y0 + r} A {r} {r} 0 0 1 {x0 + r} {y0} Z")


def ellipse(cx, cy, rx, ry):
    return f"M {cx - rx} {cy} A {rx} {ry} 0 1 0 {cx + rx} {cy} A {rx} {ry} 0 1 0 {cx - rx} {cy} Z"


NAME = "BierbaumPerformanceBrothers"
CAPS = NAME.upper()
C = 1000  # Mittelpunkt aller Embleme (x und y)


# ======================================================================
# A · Couture – Bodoni, eng verschränkt, Champagner-Gold auf Schwarz
# ======================================================================
A = dict(bg="#0d0c0b", light="#f4efe6", gold=["#a8823e", "#e9cf8e", "#fff1c9", "#c9a45a", "#8f6c2e"],
         ink="#16130f")
A_TRACK = [-0.115, -0.115, 0]


def a_mark(on_dark=True):
    d, (w, h) = word_centered("BodoniBlack", "BPB", 600, C, C, A_TRACK)
    fill = "url(#ag)" if on_dark else A["ink"]
    defs = lin("ag", A["gold"], C - w / 2, C - h / 2, C + w / 2, C + h / 2)
    return svg((C - w / 2 - 40, C - h / 2 - 40, w + 80, h + 80), f'<path fill="{fill}" d="{d}"/>', defs)


def a_emblem(on_dark=True):
    g = "url(#ag)" if on_dark else A["ink"]
    rx, ry = 820, 560
    d, (w, h) = word_centered("BodoniBlack", "BPB", 520, C, C - 40, A_TRACK)
    name, _ = word_fit("CinzelBlack", CAPS, 980, C, C + 300, 0.12)
    orn = (f'<path fill="{g}" d="M {C} {C - 400} L {C + 26} {C - 370} L {C} {C - 340} L {C - 26} {C - 370} Z"/>'
           f'<path fill="{g}" d="M {C - 230} {C - 368} H {C - 60} V {C - 372} H {C - 230} Z M {C + 60} {C - 368} H {C + 230} V {C - 372} H {C + 60} Z"/>')
    rule = f'<path fill="{g}" d="M {C - 420} {C + 205} H {C + 420} V {C + 211} H {C - 420} Z"/>'
    body = ((f'<path fill="{A["bg"]}" d="{ellipse(C, C, rx, ry)}"/>' if on_dark else "")
            + f'<path fill="none" stroke="{g}" stroke-width="26" d="{ellipse(C, C, rx - 13, ry - 13)}"/>'
            + f'<path fill="none" stroke="{g}" stroke-width="5" d="{ellipse(C, C, rx - 62, ry - 62)}"/>'
            + f'<path fill="{g}" d="{d}"/>' + orn + rule + f'<path fill="{g}" d="{name}"/>')
    return svg((C - rx - 30, C - ry - 30, 2 * rx + 60, 2 * ry + 60), body,
               lin("ag", A["gold"], C - rx, C - ry, C + rx, C + ry))


# ======================================================================
# B · Garage – Schreibschrift mit Schwung, Oval-Plakette (Creme, Rennrot, Marine)
# ======================================================================
B = dict(cream="#f3e6cc", red="#d62839", navy="#13213c", bg="#13213c")


def swash(x0, x1, y, thick=40):
    """Spitz zulaufender Unterstrich (Schwung) als Fläche."""
    pts_top, pts_bot = [], []
    n = 60
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        yy = y - 40 * math.sin(math.pi * t) + 10 * t
        w = thick * (math.sin(math.pi * t) ** 0.7) + 2
        pts_top.append((x, yy - w / 2))
        pts_bot.append((x, yy + w / 2))
    poly = pts_top + pts_bot[::-1]
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in poly) + " Z"


def b_word(size, cx, cy):
    d, (w, h) = word_centered("MrDafoe-Regular", "BPB", size, cx, cy, [-0.06, -0.02, 0])
    sw = swash(cx - w * 0.46, cx + w * 0.58, cy + h * 0.47, thick=size * 0.07)
    return d + " " + sw, w, h


def b_mark(on_dark=True):
    d, w, h = b_word(700, C, C)
    fill = B["cream"] if on_dark else B["red"]
    return svg((C - w / 2 - 60, C - h / 2 - 60, w * 1.1 + 120, h + 160), f'<path fill="{fill}" d="{d}"/>')


def b_emblem(on_dark=True):
    rx, ry = 860, 470
    d, w, h = b_word(640, C, C - 20)
    ring = ellipse(C, C, rx, ry)
    name, _ = word_fit("Anton-Regular", CAPS, 760, C, C + ry - 10, 0.06)
    banner_w = 900
    banner = (f"M {C - banner_w / 2} {C + ry - 90} H {C + banner_w / 2} L {C + banner_w / 2 + 70} {C + ry - 10} "
              f"L {C + banner_w / 2} {C + ry + 70} H {C - banner_w / 2} L {C - banner_w / 2 - 70} {C + ry - 10} Z")
    stars = "".join(f'<path fill="{B["red"]}" d="{star(C + dx, C - ry + 95, 26)}"/>' for dx in (-90, 0, 90))
    body = (f'<path fill="{B["navy"]}" d="{ring}"/>'
            f'<path fill="{B["cream"]}" d="{ellipse(C, C, rx - 40, ry - 40)}"/>'
            f'<path fill="none" stroke="{B["navy"]}" stroke-width="10" d="{ellipse(C, C, rx - 70, ry - 70)}"/>'
            + stars
            + f'<path fill="{B["red"]}" stroke="{B["navy"]}" stroke-width="22" stroke-linejoin="round" paint-order="stroke" d="{d}"/>'
            + f'<path fill="{B["red"]}" stroke="{B["navy"]}" stroke-width="16" stroke-linejoin="round" d="{banner}"/>'
            + f'<path fill="{B["cream"]}" d="{name}"/>')
    return svg((C - rx - 120, C - ry - 60, 2 * rx + 240, 2 * ry + 160), body)


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


# ======================================================================
# C · Groove – weiche, fette Kursive, Wellen-Stempel (70er, Terrakotta/Senf)
# ======================================================================
Cc = dict(terra="#c4492d", mustard="#f2a33a", cream="#f7ead2", brown="#3a2214")
C_TRACK = [-0.13, -0.12, 0]


def c_mark(on_dark=True):
    d, (w, h) = word_centered("FrauncesSoftBlackItalic", "BPB", 640, C, C, C_TRACK)
    # zweifarbig: Schatten versetzt
    sh, _ = word_centered("FrauncesSoftBlackItalic", "BPB", 640, C + 26, C + 26, C_TRACK)
    top = Cc["cream"] if on_dark else Cc["terra"]
    shadow = Cc["mustard"]
    return svg((C - w / 2 - 50, C - h / 2 - 50, w + 130, h + 130),
               f'<path fill="{shadow}" d="{sh}"/><path fill="{top}" d="{d}"/>')


def wavy_circle(cx, cy, r, amp, n):
    pts = []
    for i in range(721):
        a = 2 * math.pi * i / 720
        rr = r + amp * math.cos(n * a)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def c_emblem(on_dark=True):
    R = 760
    d, (w, h) = word_centered("FrauncesSoftBlackItalic", "BPB", 470, C, C + 10, C_TRACK)
    sh, _ = word_centered("FrauncesSoftBlackItalic", "BPB", 470, C + 18, C + 28, C_TRACK)
    top = arc_text("Shrikhand-Regular", CAPS, 74, C, C, R - 196, -90, 0.03)
    bot = arc_text("Shrikhand-Regular", "DREI BRÜDER", 74, C, C, R - 150, 90, 0.08, bottom=True)
    body = (f'<path fill="{Cc["terra"]}" d="{wavy_circle(C, C, R, 22, 28)}"/>'
            f'<circle cx="{C}" cy="{C}" r="{R - 70}" fill="{Cc["cream"]}"/>'
            f'<circle cx="{C}" cy="{C}" r="{R - 110}" fill="{Cc["brown"]}"/>'
            f'<circle cx="{C}" cy="{C}" r="{R - 270}" fill="none" stroke="{Cc["mustard"]}" stroke-width="12"/>'
            f'<path fill="{Cc["cream"]}" d="{top}"/><path fill="{Cc["mustard"]}" d="{bot}"/>'
            + "".join(f'<path fill="{Cc["mustard"]}" d="{star(C + (R - 180) * math.cos(math.radians(a)), C + (R - 180) * math.sin(math.radians(a)), 30)}"/>' for a in (180, 0))
            + f'<path fill="{Cc["mustard"]}" d="{sh}"/><path fill="{Cc["cream"]}" d="{d}"/>')
    return svg((C - R - 40, C - R - 40, 2 * R + 80, 2 * R + 80), body)


# ======================================================================
# D · Werkstatt – Schablonenschrift, Blechmarke mit Nieten (Oliv, Knochenweiß, Signalorange)
# ======================================================================
D = dict(olive="#34412b", bone="#ece3d1", orange="#ff5b1f", dark="#1d2418")


def d_mark(on_dark=True):
    d, (w, h) = word_centered("BigShouldersStencilBlack", "BPB", 760, C, C, 0.02)
    fill = D["bone"] if on_dark else D["olive"]
    bar = f'<path fill="{D["orange"]}" d="M {C - w / 2} {C + h / 2 + 40} H {C + w / 2} V {C + h / 2 + 90} H {C - w / 2} Z"/>'
    return svg((C - w / 2 - 40, C - h / 2 - 40, w + 80, h + 170), f'<path fill="{fill}" d="{d}"/>' + bar)


def d_emblem(on_dark=True):
    W, H, ch = 1500, 1000, 110
    x0, y0, x1, y1 = C - W / 2, C - H / 2, C + W / 2, C + H / 2
    plate = (f"M {x0 + ch} {y0} H {x1 - ch} L {x1} {y0 + ch} V {y1 - ch} L {x1 - ch} {y1} H {x0 + ch} "
             f"L {x0} {y1 - ch} V {y0 + ch} Z")
    d, (w, h) = word_centered("BigShouldersStencilBlack", "BPB", 560, C, C - 40, 0.03)
    name, _ = word_fit("BigShouldersStencilBlack", CAPS, 1180, C, C + 330, 0.04)
    rivets = "".join(f'<circle cx="{x}" cy="{y}" r="30" fill="{D["dark"]}"/><circle cx="{x}" cy="{y}" r="12" fill="{D["olive"]}"/>'
                     for x in (x0 + 110, x1 - 110) for y in (y0 + 110, y1 - 110))
    band = f'<path fill="{D["orange"]}" d="M {x0 + 40} {C + 230} H {x1 - 40} V {C + 430} H {x0 + 40} Z"/>'
    body = (f'<path fill="{D["olive"]}" d="{plate}"/>'
            f'<path fill="none" stroke="{D["bone"]}" stroke-width="10" stroke-dasharray="34 22" d="{rrect(x0 + 60, y0 + 60, x1 - 60, y1 - 60, 40)}"/>'
            + rivets + band
            + f'<path fill="{D["bone"]}" d="{d}"/><path fill="{D["dark"]}" d="{name}"/>')
    return svg((x0 - 30, y0 - 30, W + 60, H + 60), body)


# ======================================================================
# E · Breit – extrem breite Groteske, Kapsel (Schwarz, Neongelb)
# ======================================================================
E = dict(black="#0b0b0c", lime="#d8ff3d", white="#f4f4f0")


def e_mark(on_dark=True):
    d, (w, h) = word_centered("SyneExtraBold", "BPB", 520, C, C, [-0.02, -0.02, 0])
    fill = E["lime"] if on_dark else E["black"]
    return svg((C - w / 2 - 40, C - h / 2 - 40, w + 80, h + 80), f'<path fill="{fill}" d="{d}"/>')


def e_emblem(on_dark=True):
    W, H = 1720, 760
    x0, y0, x1, y1 = C - W / 2, C - H / 2, C + W / 2, C + H / 2
    d, (w, h) = word_centered("SyneExtraBold", "BPB", 360, C, C - 70, [-0.02, -0.02, 0])
    name, _ = word_fit("SyneExtraBold", NAME, 1080, C, C + 200, 0.0)
    fg = E["lime"] if on_dark else E["black"]
    bgc = E["black"] if on_dark else E["white"]
    body = (f'<path fill="{bgc}" d="{rrect(x0, y0, x1, y1, H / 2)}"/>'
            f'<path fill="none" stroke="{fg}" stroke-width="16" d="{rrect(x0 + 40, y0 + 40, x1 - 40, y1 - 40, H / 2 - 40)}"/>'
            f'<path fill="{fg}" d="{d}"/><path fill="{fg}" d="{name}"/>'
            f'<circle cx="{x0 + 190}" cy="{C}" r="22" fill="{fg}"/><circle cx="{x1 - 190}" cy="{C}" r="22" fill="{fg}"/>')
    return svg((x0 - 30, y0 - 30, W + 60, H + 60), body)


# ======================================================================
# F · Neon – Leuchtröhren-Buchstaben, Schild mit Röhre (Nacht, Pink, Cyan)
# ======================================================================
F = dict(night="#0b0716", pink="#ff3ea5", cyan="#3ee8ff", white="#fff4fb")
GLOW = ('<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="14" result="b1"/>'
        '<feGaussianBlur in="SourceGraphic" stdDeviation="40" result="b2"/>'
        '<feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def f_mark(on_dark=True):
    if on_dark:
        d, (w, h) = word_centered("Monoton-Regular", "BPB", 620, C, C, [-0.01, -0.01, 0])
        body = f'<g filter="url(#glow)"><path fill="{F["pink"]}" d="{d}"/></g><path fill="{F["white"]}" opacity=".55" d="{d}"/>'
        return svg((C - w / 2 - 90, C - h / 2 - 90, w + 180, h + 180), body, GLOW)
    d, (w, h) = word_centered("Monoton-Regular", "BPB", 620, C, C, [-0.01, -0.01, 0])
    return svg((C - w / 2 - 40, C - h / 2 - 40, w + 80, h + 80), f'<path fill="{F["night"]}" d="{d}"/>')


def f_small(on_dark=True):
    """Kleinform für unter 48 px: volle Buchstaben (Bungee), gleiche Anmutung."""
    d, (w, h) = word_centered("Bungee-Regular", "BPB", 520, C, C, [-0.02, -0.02, 0])
    fill = F["pink"] if on_dark else F["night"]
    return svg((C - w / 2 - 40, C - h / 2 - 40, w + 80, h + 80), f'<path fill="{fill}" d="{d}"/>')


def f_emblem(on_dark=True):
    W, H = 1640, 1040
    x0, y0, x1, y1 = C - W / 2, C - H / 2, C + W / 2, C + H / 2
    d, (w, h) = word_centered("Monoton-Regular", "BPB", 470, C, C - 90, [-0.01, -0.01, 0])
    nm, _ = word_fit("MrDafoe-Regular", NAME, 1080, C, C + 270, -0.01)
    tube = f'<path fill="none" stroke="{F["cyan"]}" stroke-width="18" d="{rrect(x0 + 70, y0 + 70, x1 - 70, y1 - 70, 120)}"/>'
    tube_core = f'<path fill="none" stroke="#e9fdff" stroke-width="6" d="{rrect(x0 + 70, y0 + 70, x1 - 70, y1 - 70, 120)}"/>'
    body = (f'<path fill="{F["night"]}" d="{rrect(x0, y0, x1, y1, 160)}"/>'
            f'<g filter="url(#glow)">{tube}<path fill="{F["pink"]}" d="{d}"/><path fill="{F["cyan"]}" d="{nm}"/></g>'
            + tube_core + f'<path fill="{F["white"]}" opacity=".5" d="{d}"/><path fill="#e9fdff" opacity=".6" d="{nm}"/>')
    return svg((x0 - 30, y0 - 30, W + 60, H + 60), body, GLOW)


CONCEPTS = [
    ("a", "A · Couture", a_mark, a_emblem),
    ("b", "B · Garage", b_mark, b_emblem),
    ("c", "C · Groove", c_mark, c_emblem),
    ("d", "D · Werkstatt", d_mark, d_emblem),
    ("e", "E · Breit", e_mark, e_emblem),
    ("f", "F · Neon", f_mark, f_emblem),
]

if __name__ == "__main__":
    for k, _, mk, em in CONCEPTS:
        open(os.path.join(OUT, f"{k}-mark-dunkel.svg"), "w").write(mk(True))
        open(os.path.join(OUT, f"{k}-mark-hell.svg"), "w").write(mk(False))
        open(os.path.join(OUT, f"{k}-emblem.svg"), "w").write(em(True))
    open(os.path.join(OUT, "f-klein-dunkel.svg"), "w").write(f_small(True))
    open(os.path.join(OUT, "f-klein-hell.svg"), "w").write(f_small(False))
    print("ok", len(os.listdir(OUT)))

"""BPB-Logo Runde 2 (22.10.2026): Flügel (3) + Plakette (5), beide B richtig herum,
P kleiner, keine Tempostreifen, mehrere Farbwelten.

Das Zeichen wird hier neu aus Grundformen gebaut (nicht mehr aus der Recraft-Datei):
B = Schaft + zwei Bäuche, P = Bauch + spitz zulaufender Schaft, Sonne im Bauch des P,
Flügel-Balken unter den B, kräftiges V darunter. Innenräume sind echte Löcher (Maske).
Aufruf: python3 runde2.py <ausgabeordner>
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = sys.argv[1] if len(sys.argv) > 1 else "out2"
os.makedirs(OUT, exist_ok=True)
FONT_UP = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


# ---------- Grundformen ----------
def rrect(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0):
    """Rechteck mit eigenem Radius je Ecke (Pfad)."""
    return (f"M {x0 + tl} {y0} H {x1 - tr} "
            + (f"A {tr} {tr} 0 0 1 {x1} {y0 + tr} " if tr else "")
            + f"V {y1 - br} "
            + (f"A {br} {br} 0 0 1 {x1 - br} {y1} " if br else "")
            + f"H {x0 + bl} "
            + (f"A {bl} {bl} 0 0 1 {x0} {y1 - bl} " if bl else "")
            + f"V {y0 + tl} "
            + (f"A {tl} {tl} 0 0 1 {x0 + tl} {y0} " if tl else "")
            + "Z")


def circle(cx, cy, r):
    return f"M {cx - r} {cy} A {r} {r} 0 1 0 {cx + r} {cy} A {r} {r} 0 1 0 {cx - r} {cy} Z"


def poly(*pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


class Glyphs:
    """Maße des Zeichens. Alle Werte in einem 2048er-Raster."""

    def __init__(self, p_lift=60, b_w=480, gap=50, mode="gerade"):
        self.T, self.H = 580, 620                      # Oberkante und Höhe der B
        self.base = self.T + self.H
        self.pT = self.T - p_lift                      # Oberkante P
        self.bh = 384                                  # Höhe des P-Bauchs
        self.R = self.bh / 2
        self.mode = mode                               # gerade | spitze
        self.straight = mode == "gerade"
        self.pxl = 800                                 # linke Kante P oben
        self.pxr = 1240                                # rechte Kante P-Bauch
        self.sw = 200                                  # Schaftbreite
        self.tip = (self.pxl + self.sw / 2 - 12, self.base + 112) if mode == "spitze" else None
        self.b_w, self.gap = b_w, gap

    # P ---------------------------------------------------------------
    def p_left_x(self, y):
        if self.straight:
            return self.pxl
        tx, ty = self.tip
        return self.pxl + (tx - 8 - self.pxl) * (y - self.pT) / (ty - self.pT)

    def p_right_x(self, y):
        """Rechte Kante des Schafts unterhalb des Bauchs."""
        if self.straight:
            return self.pxl + 200
        tx, ty = self.tip
        sx, sy = self.p_join()
        return sx + (tx + 8 - sx) * (y - sy) / (ty - sy)

    def p_join(self):
        return self.pxl + self.sw, self.pT + 2 * self.R

    def p_body(self):
        xl, T, R = self.pxl, self.pT, self.R
        xb = self.pxr - R
        if self.straight:
            sw = 200
            return (f"M {xl + 40} {T} H {xb} A {R} {R} 0 0 1 {xb} {T + 2 * R} H {xl + sw} "
                    f"V {self.base - 30} Q {xl + sw} {self.base} {xl + sw - 30} {self.base} "
                    f"H {xl + 30} Q {xl} {self.base} {xl} {self.base - 30} V {T + 40} Q {xl} {T} {xl + 40} {T} Z")
        jx, jy = self.p_join()
        tx, ty = self.tip
        return (f"M {xl + 40} {T} H {xb} A {R} {R} 0 0 1 {xb} {T + 2 * R} H {jx:.1f} "
                f"L {tx + 9} {ty - 14} Q {tx} {ty + 8} {tx - 9} {ty - 14} "
                f"L {xl} {T + 46} Q {xl} {T} {xl + 40} {T} Z")

    def p_counter(self):
        cx, cy = self.pxr - self.R - 6, self.pT + self.R
        return cx, cy, self.R * 0.56

    def sun(self, stripes=False):
        cx, cy, r = self.p_counter()
        yh = cy + 0.74 * r
        rs = 0.60 * r
        return f"M {cx - rs} {yh} A {rs} {rs} 0 0 1 {cx + rs} {yh} Z"

    # B ---------------------------------------------------------------
    def b_shape(self, x0):
        w, T, H, base = self.b_w, self.T, self.H, self.base
        body = [rrect(x0, T, x0 + w * 0.55, base, tl=46, bl=46),
                rrect(x0, T, x0 + w * 0.90, T + H * 0.49, tl=46, tr=H * 0.245, br=H * 0.245),
                rrect(x0, T + H * 0.43, x0 + w, base, tr=H * 0.285, br=H * 0.285, bl=46)]
        holes = [rrect(x0 + w * 0.33, T + H * 0.155, x0 + w * 0.645, T + H * 0.335,
                       *(4 * [H * 0.09])),
                 rrect(x0 + w * 0.33, T + H * 0.60, x0 + w * 0.70, T + H * 0.82,
                       *(4 * [H * 0.11]))]
        return body, holes

    def layout(self):
        """Lage der beiden B: links an der Kante des P, rechts am Bauch."""
        y_up, y_lo = self.T + self.H * 0.245, self.T + self.H * 0.715
        lx = min(self.p_left_x(y_up) - self.gap - self.b_w * 0.90,
                 self.p_left_x(y_lo) - self.gap - self.b_w)
        rx = self.pxr + self.gap
        return lx, rx

    # Flügel -----------------------------------------------------------
    def wings(self, chevron=True):
        lx, rx = self.layout()
        y0, y1, g = self.base + 40, self.base + 118, 34
        tipo = 125                                      # wie weit die Spitze außen übersteht
        left_in0 = self.p_left_x(y0) - g
        left_in1 = self.p_left_x(y1) - g
        right_in0 = self.p_right_x(y0) + g if not self.straight else self.pxl + 200 + g
        right_in1 = self.p_right_x(y1) + g if not self.straight else self.pxl + 200 + g
        if self.straight:
            left_in0 = left_in1 = self.pxl - g
        rxe = rx + self.b_w
        parts = [poly((lx - tipo, y0), (left_in0, y0), (left_in1, y1), (lx - tipo * 0.35, y1)),
                 poly((right_in0, y0), (rxe + tipo, y0), (rxe + tipo * 0.35, y1), (right_in1, y1))]
        if chevron:
            cx = self.tip[0] if self.tip else (lx + rxe) / 2
            a0, a1, depth, th = lx - tipo * 0.25, rxe + tipo * 0.25, 108, 46
            yc = y1 + 34
            parts.append(poly((a0, yc), (cx - 50, yc), (cx, yc + depth * 0.55), (cx + 50, yc),
                              (a1, yc), (a1 - 40, yc + th), (cx + 74, yc + th), (cx, yc + th + depth),
                              (cx - 74, yc + th), (a0 + 40, yc + th)))
        return parts

    def bbox(self):
        lx, rx = self.layout()
        tipo = 125
        return lx - tipo, self.pT, rx + self.b_w + tipo, self.base + 118 + 34 + 46 + 108


# ---------- Text ----------
def text_path(text, size, x, y, font=FONT_UP, spacing=0.0):
    f = TTFont(font)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    s = size / f["head"].unitsPerEm
    pen, cur = SVGPathPen(gs), 0.0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + cur, y)))
        cur += hmtx[g][0] * s + spacing * size
    return pen.getCommands(), cur - spacing * size


def text_centered(text, width, cx, y, font=FONT_UP, spacing=0.0):
    _, w0 = text_path(text, 100, 0, 0, font, spacing)
    size = 100 * width / w0
    return text_path(text, size, cx - width / 2, y, font, spacing)[0], size


# ---------- Farbwelten ----------
SCHEMES = [
    # key, Name, Plakette, Verlauf (Liste), Sonne, Schrift, Rand
    ("sonne", "Sonnenuntergang", "#1b1030", ["#7b3fe4", "#e83e8c", "#ff8a3d"], "#ffd23f", "#ffffff"),
    ("wald", "Wald (Grün)", "#0d2a1e", ["#1f8f55", "#5fbf4a", "#b5e04a"], "#ffd23f", "#f1f7ec"),
    ("ozean", "Ozean (Blau)", "#0a1830", ["#1d4ed8", "#2f8cff", "#2ee0f0"], "#ffb703", "#ffffff"),
    ("renn", "Rennrot", "#141414", ["#c1121f", "#e8461e", "#ff9f1c"], "#ffd166", "#ffffff"),
    ("wappen", "Grün-Gold (wie BPF-Wappen)", "#123528", ["#c9a04a", "#e2c06e", "#c9a04a"], "#f6e2a6", "#e2c06e"),
    ("mono", "Einfarbig", "#0b0b0c", ["#ffffff", "#ffffff"], "#ffffff", "#ffffff"),
]


def grad_def(gid, stops, x0, y0, x1, y1):
    n = len(stops) - 1
    st = "".join(f'<stop offset="{i / n:.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" '
            f'x2="{x1}" y2="{y1}">{st}</linearGradient>')


# ---------- Zusammenbau ----------
def emblem_mask(g, mid, chevron=True):
    lx, rx = g.layout()
    white, black = [g.p_body()], []
    for x in (lx, rx):
        b, h = g.b_shape(x)
        white += b
        black += h
    cx, cy, r = g.p_counter()
    black.append(circle(cx, cy, r))
    white += g.wings(chevron)
    w = "".join(f'<path d="{d}" fill="#fff"/>' for d in white)
    k = "".join(f'<path d="{d}" fill="#000"/>' for d in black)
    return (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-1000" y="-1000" width="5000" height="5000">'
            f'<rect x="-1000" y="-1000" width="5000" height="5000" fill="#000"/>{w}{k}</mask>')


def emblem(g, fill, sun_fill, mid, chevron=True):
    x0, y0, x1, y1 = g.bbox()
    return (f'<defs>{emblem_mask(g, mid, chevron)}</defs>'
            f'<rect x="{x0 - 50}" y="{y0 - 50}" width="{x1 - x0 + 100}" height="{y1 - y0 + 100}" '
            f'fill="{fill}" mask="url(#{mid})"/><path fill="{sun_fill}" d="{g.sun()}"/>')


def chamfer_plate(x0, y0, x1, y1, c):
    return poly((x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1),
                (x0 + c, y1), (x0, y1 - c), (x0, y0 + c))


def shield_plate(x0, y0, x1, y1, c, point):
    cx = (x0 + x1) / 2
    return poly((x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (cx, y1 + point), (x0, y1), (x0, y0 + c))


def build(draft, sch, transparent=True):
    key, name, plate, stops, sun, ink = sch
    g = Glyphs(mode="spitze" if draft == "spitze" else "gerade")
    x0, y0, x1, y1 = g.bbox()
    cxm = (x0 + x1) / 2
    gid, mid = f"g_{draft}_{key}", f"m_{draft}_{key}"
    gdef = grad_def(gid, stops, x0, y0, x1, y1 + 200)
    fill = f"url(#{gid})"
    word = "BierbaumPerformanceBrothers"
    pad = 120
    body, vb = "", None
    if draft in ("schild", "schraeg", "spitze"):
        ty = y1 + 230
        tp, size = text_centered(word, (x1 - x0) * 0.98, cxm, ty)
        px0, py0, px1, py1 = x0 - pad, y0 - pad, x1 + pad, ty + 120
        edge = f' stroke="{fill}" stroke-width="20"' if key != "mono" else ' stroke="#ffffff" stroke-width="20"'
        rule = f'<path fill="{fill}" d="{rrect(x0 + 40, y1 + 52, x1 - 40, y1 + 66)}"/>'
        inner = (f'<path fill="{plate}"{edge} d="{chamfer_plate(px0, py0, px1, py1, 130)}"/>'
                 + emblem(g, fill, sun, mid, chevron=True) + rule
                 + f'<path fill="{ink}" d="{tp}"/>')
        if draft == "schraeg":
            t = math.tan(math.radians(9))
            cy = (py0 + py1) / 2
            body = f'<g transform="matrix(1 0 {-t:.5f} 1 {t * cy:.2f} 0)">{inner}</g>'
            ext = t * (py1 - py0) / 2
            vb = (px0 - ext - 30, py0 - 30, px1 - px0 + 2 * ext + 60, py1 - py0 + 60)
        else:
            body = inner
            vb = (px0 - 30, py0 - 30, px1 - px0 + 60, py1 - py0 + 60)
    elif draft == "wappen":
        ty = y1 + 210
        tp, size = text_centered(word, (x1 - x0) * 0.90, cxm, ty)
        px0, py0, px1, py1 = x0 - pad, y0 - pad, x1 + pad, ty + 90
        point = 300
        edge = f' stroke="{fill}" stroke-width="20"' if key != "mono" else ' stroke="#ffffff" stroke-width="20"'
        rule = f'<path fill="{fill}" d="{rrect(x0 + 40, y1 + 46, x1 - 40, y1 + 60)}"/>'
        star_y = py1 + point * 0.42
        dot = f'<path fill="{sun}" d="M {cxm - 70} {star_y + 30} A 70 70 0 0 1 {cxm + 70} {star_y + 30} Z"/>'
        body = (f'<path fill="{plate}"{edge} stroke-linejoin="round" d="{shield_plate(px0, py0, px1, py1, 130, point)}"/>'
                + emblem(g, fill, sun, mid, chevron=True) + rule + f'<path fill="{ink}" d="{tp}"/>')
        vb = (px0 - 30, py0 - 30, px1 - px0 + 60, py1 + point - py0 + 70)
    elif draft == "frei":
        ty = y1 + 200
        word_fill = fill if key != "mono" else "#ffffff"
        tp, size = text_centered(word, (x1 - x0) * 0.98, cxm, ty)
        body = emblem(g, fill, sun, mid, chevron=True) + f'<path fill="{ink}" d="{tp}"/>'
        vb = (x0 - 60, y0 - 60, x1 - x0 + 120, ty + 80 - y0)
    elif draft == "symbol":
        # App-Symbol: nur P mit Sonne auf der Plakettenfarbe, abgerundet
        gp = Glyphs(mode="gerade")
        s = 1160
        cx, cy = 1020, 860
        tile = rrect(cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2, *(4 * [240]))
        pm = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-1000" y="-1000" width="5000" height="5000">'
              f'<rect x="-1000" y="-1000" width="5000" height="5000" fill="#000"/>'
              f'<path d="{gp.p_body()}" fill="#fff"/><path d="{circle(*gp.p_counter())}" fill="#000"/></mask>')
        sc = 1.12
        tr = f"translate({cx - sc * 1020:.1f} {cy - sc * 860:.1f}) scale({sc})"
        body = (f'<path fill="{plate}" d="{tile}"/><defs>{pm}</defs><g transform="{tr}">'
                f'<rect x="600" y="400" width="900" height="1100" fill="{fill}" mask="url(#{mid})"/>'
                f'<path fill="{sun}" d="{gp.sun()}"/></g>')
        gdef = grad_def(gid, stops, 700, 450, 1350, 1400)
        vb = (cx - s / 2, cy - s / 2, s, s)
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}" '
            f'width="{w / 2:.0f}" height="{h / 2:.0f}"><defs>{gdef}</defs>{body}</svg>')


DRAFTS = [
    ("schild", "A · Schild", "Flügel-Zeichen auf aufrechter Plakette mit abgeschrägten Ecken, Name darunter."),
    ("schraeg", "B · Schild schräg", "Wie A, die ganze Plakette 9° nach vorn gelegt (näher an Entwurf 5)."),
    ("wappen", "C · Wappen", "Plakette läuft unten spitz zu wie ein Wappen."),
    ("spitze", "D · P mit Spitze", "Wie A, der Schaft des P läuft unten spitz zu wie im Original und zeigt aufs V."),
    ("frei", "E · Frei", "Zeichen und Name ohne Plakette – für Stellen, an denen kein Schild passt."),
    ("symbol", "F · App-Symbol", "Nur das P mit Sonne, ohne Tempostreifen."),
]

if __name__ == "__main__":
    for d, _, _ in DRAFTS:
        for sch in SCHEMES:
            open(os.path.join(OUT, f"{d}-{sch[0]}.svg"), "w").write(build(d, sch))
    print("ok", len(os.listdir(OUT)))

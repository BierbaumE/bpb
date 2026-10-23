"""BPB-Logo: sportliche Abwandlungen von Eikes Recraft-Entwurf (21.10.2026).

Liest die bereinigte Vorlage (logo_check.svg), baut die Teile als Pfade mit
Löchern (fill-rule evenodd, transparente Innenräume) und schreibt je Variante
drei SVGs: farbig auf dunkel, farbig auf hell, einfarbig schwarz.
Aufruf: python3 varianten.py <vorlage.svg> <ausgabeordner>
"""
import math, os, re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

d = [m for _, m in re.findall(r'<path fill="([^"]+)" d="([^"]+)"/>', open(SRC).read())][1:]
P, P_HOLE, P_HORIZ, LB, LB_LO, LB_UP, RB, RB_LO, RB_UP, R_BAR, L_BAR, WAVE, LINE = d
P_FULL = f"{P} {P_HOLE} {P_HORIZ}"
LB_FULL = f"{LB} {LB_LO} {LB_UP}"
RB_FULL = f"{RB} {RB_LO} {RB_UP}"
SUN = ("M 937.959 818.42 C 939.255 797.626 941.48 782.398 953.882 764.87 "
       "C 974.543 735.667 1002.02 725.233 1036.75 727.469 "
       "C 1082.8 737.289 1112.08 769.176 1112.13 817.295 Z")

VIOLET, PINK, ORANGE, SUNC, NIGHT = "#7b3fe4", "#e83e8c", "#ff8a3d", "#ffd23f", "#1b1030"
FONT = "/usr/share/fonts/opentype/inter/Inter-BlackItalic.otf"
T12 = math.tan(math.radians(12))


def text_path(text, size, x, y, font=FONT, spacing=0.0):
    """Text als Umriss (ohne Kerning), Rückgabe (Pfad, Breite)."""
    f = TTFont(font)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    s = size / f["head"].unitsPerEm
    pen, cur = SVGPathPen(gs), 0.0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + cur, y)))
        cur += hmtx[g][0] * s + spacing * size
    return pen.getCommands(), cur - spacing * size


def text_width(text, size, font=FONT, spacing=0.0):
    return text_path(text, size, 0, 0, font, spacing)[1]


def skew(cy=900):
    """Kursiv 12° nach vorn, um die Höhe cy herum (bleibt mittig)."""
    return f"matrix(1 0 {-T12:.5f} 1 {T12 * cy:.3f} 0)"


def wedge(x0, x1, yc, h, tip=0.18):
    """Tempostreifen: links spitz (Höhe tip*h), rechts volle Höhe, rechts schräg."""
    s = h * 0.35
    return (f"M {x0} {yc - h * tip / 2} L {x1 + s} {yc - h / 2} L {x1 - s} {yc + h / 2} "
            f"L {x0} {yc + h * tip / 2} Z")


class Look:
    """Farbwelt einer Ausgabe."""
    def __init__(self, key, bg, fill, sun, ink, label):
        self.key, self.bg, self.fill, self.sun, self.ink, self.label = key, bg, fill, sun, ink, label


LOOKS = [
    Look("dunkel", NIGHT, "url(#grad)", SUNC, "#ffffff", "Farbig auf Nacht"),
    Look("hell", "#ffffff", "url(#grad)", "#ffc400", NIGHT, "Farbig auf Weiß"),
    Look("schwarz", "#ffffff", "#0b0b0c", None, "#0b0b0c", "Einfarbig"),
]


def defs(extra=""):
    return (f'<defs><linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="216" y1="400" '
            f'x2="1830" y2="1400"><stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" '
            f'stop-color="{PINK}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>{extra}</defs>')


def p_with_sun(look, striped=False):
    """P mit Sonne; striped = Sonne im 80er-Stil mit Querstreifen (echte Lücken)."""
    sun = f'<path fill="{look.sun}" d="{SUN}"/>' if look.sun else ""
    body = f'<path fill="{look.fill}" fill-rule="evenodd" d="{P_FULL}"/>{sun}'
    if not striped:
        return body
    return f'<g mask="url(#sunstripes)">{body}</g>'


SUN_MASK = ('<clipPath id="sunclip"><path d="' + SUN + '"/></clipPath>'
            '<mask id="sunstripes" maskUnits="userSpaceOnUse" x="-500" y="-500" width="3500" height="3500">'
            '<rect x="-500" y="-500" width="3500" height="3500" fill="#fff"/>'
            '<g clip-path="url(#sunclip)" fill="#000">'
            '<rect x="900" y="770" width="260" height="12"/>'
            '<rect x="900" y="794" width="260" height="15"/></g></mask>')


def emblem(look, trail="wave", striped=False):
    """Grundzeichen: B P B + Balken; trail: wave | line | none."""
    f = look.fill
    parts = [f'<path fill="{f}" fill-rule="evenodd" d="{LB_FULL}"/>',
             f'<path fill="{f}" fill-rule="evenodd" d="{RB_FULL}"/>',
             f'<path fill="{f}" d="{L_BAR}"/>', f'<path fill="{f}" d="{R_BAR}"/>',
             p_with_sun(look, striped)]
    if trail in ("wave", "line"):
        parts.append(f'<path fill="{f}" d="{LINE}"/>')
    if trail == "wave":
        parts.append(f'<path fill="{f}" d="{WAVE}"/>')
    return "".join(parts)


# ---------- Varianten ----------

def v_kursiv(look):
    """1 Kursiv: das Original, nur 12° nach vorn gelegt."""
    return defs(), f'<g transform="{skew()}">{emblem(look, "wave")}</g>', "60 360 1900 1340"


def v_tempo(look):
    """2 Tempo: kursiv, drei Tempostreifen links, Linie mit V, ohne Welle."""
    f = look.fill
    lines = "".join(f'<path fill="{f}" d="{wedge(x0, 185, yc, h)}"/>'
                    for x0, yc, h in ((-260, 720, 62), (-160, 900, 62), (-60, 1080, 62)))
    return defs(), f'<g transform="{skew()}">{lines}{emblem(look, "line")}</g>', "-330 360 2230 1240"


def v_fluegel(look):
    """3 Flügel: aufrecht, Balken außen spitz verlängert, kräftiges V darunter."""
    f = look.fill
    tips = (f'<path fill="{f}" d="M 300 1241 L 520 1241 L 520 1368 L 440 1368 Z"/>'
            f'<path fill="{f}" d="M 1748 1241 L 1530 1241 L 1555 1368 L 1640 1368 Z"/>')
    chevron = (f'<path fill="{f}" d="M 430 1392 L 980 1392 L 1024 1478 L 1068 1392 L 1618 1392 '
               f'L 1580 1436 L 1094 1436 L 1024 1572 L 954 1436 L 468 1436 Z"/>')
    return defs(), emblem(look, "none") + tips + chevron, "180 360 1690 1270"


def v_retro(look):
    """4 Retro-Sonne: kursiv, Sonne mit 80er-Querstreifen, Linie mit V."""
    return defs(SUN_MASK), f'<g transform="{skew()}">{emblem(look, "line", striped=True)}</g>', "60 360 1900 1240"


def v_plakette(look):
    """5 Plakette: Startnummer-Schild, schräg, mit Schriftzug."""
    plate_fill = NIGHT if look.key != "schwarz" else "#0b0b0c"
    inner = Look(look.key, plate_fill, look.fill if look.key != "schwarz" else "#ffffff",
                 look.sun if look.key != "schwarz" else None, "#fff", "")
    word = "BierbaumPerformanceBrothers"
    size = 118 * 1640 / text_width(word, 118)
    w = text_width(word, size)
    tp, _ = text_path(word, size, 1024 - w / 2, 1660)
    edge = (f' stroke="{look.fill}" stroke-width="22"' if look.key != "schwarz" else "")
    plate = (f'<path fill="{plate_fill}"{edge} d="M 140 300 L 1850 300 L 1950 400 L 1950 1660 '
             f'L 1850 1790 L 140 1790 L 40 1690 L 40 400 Z"/>')
    stripe = f'<path fill="{inner.fill}" d="M 300 1470 L 1748 1470 L 1748 1490 L 300 1490 Z"/>'
    txt = f'<path fill="#ffffff" d="{tp}"/>'
    return (defs(), f'<g transform="{skew(1045)}">{plate}{emblem(inner, "none")}{stripe}</g>'
            f'<g transform="{skew(1045)}"><g transform="matrix(1 0 {T12:.5f} 1 {-T12 * 1600:.3f} 0)">{txt}</g></g>',
            "-130 250 2300 1600")


def v_zeichen(look):
    """6 Zeichen: nur P mit Sonne + zwei Tempostreifen – für App-Symbol und Favicon."""
    f = look.fill
    lines = "".join(f'<path fill="{f}" d="{wedge(x0, x1, yc, 70)}"/>'
                    for x0, x1, yc in ((430, 700, 640), (520, 760, 830)))
    tile = (f'<rect x="345" y="328" width="1160" height="1160" rx="230" fill="{NIGHT}"/>'
            if look.key == "dunkel" else "")
    return defs(), f'{tile}<g transform="{skew(900)}">{lines}{p_with_sun(look)}</g>', "345 328 1160 1160"


def lockup(look):
    """Quer: Tempo-Zeichen + Schriftzug rechts daneben."""
    f = look.fill
    _, body, _ = v_tempo(look)
    word1, word2 = "BierbaumPerformance", "Brothers"
    size = 300
    tp1, w1 = text_path(word1, size, 2050, 960)
    tp2, w2 = text_path(word2, size, 2050 + w1, 960)
    tag, wt = text_path("DREI BRÜDER. ALLE MÖGLICHKEITEN.", 150, 2060, 1230, spacing=0.06)
    words = (f'<path fill="{look.ink}" d="{tp1}"/><path fill="{f}" d="{tp2}"/>'
             f'<path fill="{look.ink}" opacity=".75" d="{tag}"/>')
    width = 2050 + w1 + w2 + 80
    return defs(), body + words, f"-330 360 {width + 330:.0f} 1240"


VARIANTS = [
    ("1-kursiv", "Kursiv", "Dein Entwurf, nur 12° nach vorn gelegt. Kleinste Änderung, wirkt sofort schneller.", v_kursiv),
    ("2-tempo", "Tempo", "Kursiv, drei Tempostreifen links (drei Brüder), Welle weg, Linie mit V bleibt.", v_tempo),
    ("3-fluegel", "Flügel", "Aufrecht wie ein Motorsport-Emblem: Balken außen spitz verlängert, kräftiges V darunter.", v_fluegel),
    ("4-retro", "Retro-Sonne", "Kursiv, Sonne mit 80er-Querstreifen wie ein Synthwave-Sonnenuntergang.", v_retro),
    ("5-plakette", "Plakette", "Startnummer-Schild mit Zeichen, Zierstreifen und Schriftzug – für Trikot, Auto, Visitenkarte.", v_plakette),
    ("6-zeichen", "Zeichen", "Nur das P mit Sonne und zwei Tempostreifen – für App-Symbol und Favicon.", v_zeichen),
    ("7-quer", "Quer mit Schriftzug", "Tempo-Zeichen mit Schriftzug, „Brothers“ farbig, Leitsatz darunter.", lockup),
]


def write(name, look, d_, body, vb, bg=True):
    x, y, w, h = vb.split()
    if name.startswith("6-") and look.key == "dunkel":
        bg = False  # App-Symbol: abgerundete Kachel statt Fläche
    bgrect = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{look.bg}"/>' if bg else ""
    size = f'width="{float(w) / 2:.0f}" height="{float(h) / 2:.0f}"'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" {size}>{d_}{bgrect}{body}</svg>')
    open(os.path.join(OUT, f"{name}-{look.key}.svg"), "w").write(svg)
    open(os.path.join(OUT, f"{name}-{look.key}-transparent.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" {size}>{d_}{body}</svg>')


if __name__ == "__main__":
    for name, title, text, fn in VARIANTS:
        for look in LOOKS:
            d_, body, vb = fn(look)
            write(name, look, d_, body, vb)
    print("ok", len(os.listdir(OUT)), "Dateien")

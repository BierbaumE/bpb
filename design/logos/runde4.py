"""BPB Logo Runde 4 - Richtung C "Durchbruch" (Leistung: das Zeichen sprengt seinen Rahmen).
Aufruf: python3 -I runde4_gen.py <google-fonts-ofl-Ordner> <Ausgabeordner>
Text liegt als Umriss in den SVGs (OFL-Schriften: Anton, Archivo Black).
Nur Schwarz/Weiss/Grau."""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OFL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def load(p):
    return TTFont(os.path.join(OFL, p))


ANTON = load("anton/Anton-Regular.ttf")
ARCHIVO = load("archivoblack/ArchivoBlack-Regular.ttf")


def text_path(font, text, cap, tracking=0.0, max_w=None):
    """Pfad (Grundlinie y=0, links x=0). cap = Kapitaelchenhoehe in px. Liefert (d, breite, cap)."""
    upm = font["head"].unitsPerEm
    capu = font["OS/2"].sCapHeight
    gs, cm = font.getGlyphSet(), font.getBestCmap()
    for _ in range(2):
        s = cap / capu
        x, parts = 0.0, []
        for ch in text:
            g = gs[cm[ord(ch)]]
            pen = SVGPathPen(gs)
            g.draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
            parts.append(pen.getCommands())
            x += g.width * s + tracking
        w = x - tracking
        if max_w and w > max_w:
            cap *= max_w / w
            tracking *= max_w / w
        else:
            break
    return " ".join(parts), w, cap


def fmt(v):
    return f"{v:.1f}"


# ---- Variante 1: SPRUNG - Zeichen steht im Block und ragt oben heraus (Farbwechsel an der Kante)
def c1(ink, paper, mid, uid, rx=30):
    d, w, cap = text_path(ANTON, "BPB", 278, tracking=8, max_w=470)
    base = 300 - (cap + 30) / 2 + cap          # Zeichen + 30 px Rand unten mittig
    by = base - 208 * cap / 278                # 3/4 des Zeichens im Block, Rest ragt heraus
    bh = (base + 30) - by
    tx = (600 - w) / 2
    return f"""
  <clipPath id="{uid}"><rect x="30" y="{fmt(by)}" width="540" height="{fmt(bh)}" rx="{rx}"/></clipPath>
  <rect x="30" y="{fmt(by)}" width="540" height="{fmt(bh)}" rx="{rx}" fill="{mid}"/>
  <path transform="translate({fmt(tx)} {fmt(base)})" d="{d}" fill="{ink}"/>
  <g clip-path="url(#{uid})"><path transform="translate({fmt(tx)} {fmt(base)})" d="{d}" fill="{paper}"/></g>"""


# ---- Variante 2: SPRUNG KURSIV - gleiches Prinzip, scharfkantig und nach vorn geneigt, Block einfarbig
def c2(ink, paper, mid, uid):
    inner = c1(ink, paper, ink, uid, rx=10)
    return f'<g transform="translate(300 300) skewX(-9) translate(-300 -300)">{inner}</g>'


# ---- Variante 3: RAHMENBRUCH - Zeichen durchbricht die Oberkante eines Strichrahmens (Aussparung)
def c3(ink, paper, mid, uid):
    d, w, cap = text_path(ANTON, "BPB", 280, tracking=8, max_w=470)
    base = 410
    tx = (600 - w) / 2
    fy, fb = base - 220, base + 40             # Rahmen: Oberkante 60 px unter Zeichenoberkante
    return f"""
  <rect x="40" y="{fmt(fy)}" width="520" height="{fmt(fb - fy)}" rx="34" fill="none" stroke="{mid}" stroke-width="28"/>
  <g transform="translate({fmt(tx)} {fmt(base)})">
    <path d="{d}" fill="{paper}" stroke="{paper}" stroke-width="30" stroke-linejoin="round"/>
    <path d="{d}" fill="{ink}"/>
  </g>"""


CONCEPTS = {"c1-sprung": c1, "c2-kursiv": c2, "c3-rahmen": c3}
INK, PAPER, MID = "#111111", "#ffffff", "#8c8c8c"


def svg(body, size=600, bg=None, vb="0 0 600 600"):
    r = f'<rect width="600" height="600" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{size}" height="{size}">'
            f"{r}{body}</svg>")


def icon(fn, uid):
    # App-Symbol: dunkle Kachel, Zeichen invertiert und leicht verkleinert
    body = fn(PAPER, INK, "#e2e2e2", uid)
    return svg(f'<rect width="600" height="600" rx="124" fill="{INK}"/>'
               f'<g transform="translate(300 300) scale(.8) translate(-300 -300)">{body}</g>')


for name, fn in CONCEPTS.items():
    k = name.split("-")[0]
    hell = fn(INK, PAPER, MID, k + "h")
    dunkel = fn(PAPER, INK, "#e2e2e2", k + "d")
    mono = fn(INK, PAPER, INK, k + "m")
    files = {
        f"{name}_hell.svg": svg(hell, bg=PAPER),
        f"{name}_dunkel.svg": svg(dunkel, bg=INK),
        f"{name}_einfarbig.svg": svg(mono, bg=PAPER),
        f"{name}_app.svg": icon(fn, k + "a"),
    }
    for fn_, s in files.items():
        with open(os.path.join(OUT, fn_), "w") as f:
            f.write(s)
print("ok", sorted(os.listdir(OUT)))

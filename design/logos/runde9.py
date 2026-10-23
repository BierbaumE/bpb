"""BPB Runde 9 - Schwarzes Loch: Spiralarme in der Rotationsebene, laufen in den Schatten (kein Saturn-Ring).
Aufruf: python3 -I runde9_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py und runde8_gen.py daneben)"""
import sys, os, math, random
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde8_gen.py")).read().split('INK, PAPER =')[0])   # Helfer + matrix aus Runde 8

def loch(ink, paper, mid, SH="#111111"):
    # Draufsicht wie die Vorlage: schwarzer Kern, weich auslaufende Wirbelbaender, Lichtrand an einer Seite.
    r = random.Random(17); cx, cy = 300, 318; line, soft = ink, mid; o = []
    for rad, w_, op in [(268, 30, .10), (244, 34, .14), (220, 30, .18)]:                 # weicher Hof
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{soft}" stroke-width="{w_}" stroke-opacity="{op}"/>')
    def band(r0, a0, span, wmax, drift, col, op):
        out, inn = [], []
        for k in range(29):
            t = k / 28; a = math.radians(a0 + span * t); wt = (math.sin(math.pi * t) ** .8) * wmax; rr = r0 + drift * t
            out.append((cx + (rr + wt / 2) * math.cos(a), cy + (rr + wt / 2) * math.sin(a)))
            inn.append((cx + (rr - wt / 2) * math.cos(a), cy + (rr - wt / 2) * math.sin(a)))
        return f'<polygon points="{pts(out + inn[::-1])}" fill="{col}" fill-opacity="{op}"/>'
    for i in range(16):                                                                    # Wirbelbaender, nach aussen duenner und heller
        r0 = r.uniform(162, 262); wm = 34 - (r0 - 162) * .16 + r.uniform(-4, 4)
        o.append(band(r0, r.uniform(0, 360), r.uniform(70, 210), max(8, wm), r.uniform(-26, 26), line if i % 2 == 0 else soft, fmt(r.uniform(.5, .95))))
    o.append(band(150, 95, 120, 26, -6, line, 1))                                           # Lichtrand unten links
    o.append(band(168, 120, 70, 12, 0, soft, 1))
    ringed = f'<g transform="rotate(-8 {cx} {cy}) translate(0 {cy * 0.06}) scale(1 .94) translate(0 {-cy * 0.06 / 0.94 * 0})">' + "".join(o[:1]) + "".join(o[1:]) + '</g>'
    shadow = f'<circle cx="{cx}" cy="{cy}" r="140" fill="{SH}"/>'
    d, w, cap = text_path(ANTON, "BPB", 124, tracking=6, max_w=218)
    base = cy + cap / 2; tx = (600 - w) / 2
    lt = f'<g transform="translate({fmt(tx)} {fmt(base)})"><path d="{d}" fill="#ffffff" stroke="{SH}" stroke-width="10" stroke-linejoin="round"/><path d="{d}" fill="#ffffff"/></g>'
    return ringed + shadow + lt

INK, PAPER = "#111111", "#ffffff"
def svg(b, bg): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" fill="{bg}"/>{b}</svg>'
n = "r9-loch"
open(os.path.join(OUT, f"{n}_hell.svg"), "w").write(svg(loch(INK, PAPER, "#8c8c8c"), PAPER))
open(os.path.join(OUT, f"{n}_dunkel.svg"), "w").write(svg(loch(PAPER, INK, "#9a9a9a"), INK))
open(os.path.join(OUT, f"{n}_gruen.svg"), "w").write(svg(loch("#c4ffe4", "#0b1a14", "#22b673", "#050806"), "#0b1a14"))
open(os.path.join(OUT, f"{n}_app.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" rx="124" fill="{INK}"/><g transform="translate(300 300) scale(.86) translate(-300 -300)">{loch(PAPER, INK, "#9a9a9a")}</g></svg>')
print("ok")

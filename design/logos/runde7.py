"""BPB Runde 7 - Matrix, Marke zuerst: BPB bleibt voll lesbar, die Matrix passiert drumherum.
Aufruf: python3 -I runde7_gen.py <ofl-Ordner> <Ausgabe>  (braucht runde4_gen.py daneben)"""
import sys, os, random
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runde4_gen.py")).read()
exec(src.split("def fmt")[0])
def fmt(v): return f"{v:.1f}"

def rain(head, tail, seed=3):
    r = random.Random(seed); o = []
    for cx in range(40, 570, 26):
        n = r.randint(5, 14); y0 = r.uniform(0, 430)
        for k in range(n):
            y = y0 + k * 22
            if y > 590: break
            last = k == n - 1
            o.append(f'<rect x="{cx - 7}" y="{fmt(y)}" width="14" height="17" rx="2" fill="{head if last else tail}" fill-opacity="{1 if last else fmt(0.3 + 0.7 * k / n)}"/>')
    return "".join(o)

def m1(letter, halo, head, tail):          # Glitch klar: Buchstaben ganz, nur zwei duenne Verschiebungen
    d, w, cap = text_path(ANTON, "BPB", 250, tracking=8, max_w=500)
    base = 300 + cap / 2; tx = (600 - w) / 2; top = base - cap
    o = [rain(head, tail)]
    o.append(f'<g transform="translate({fmt(tx)} {fmt(base)})"><path d="{d}" fill="{halo}" stroke="{halo}" stroke-width="34" stroke-linejoin="round"/>'
             f'<path d="{d}" fill="{letter}"/></g>')
    clips = ""
    for i, (y, h, dx) in enumerate([(top + 62, 10, 14), (top + 150, 9, -12)]):
        clips += f'<clipPath id="g{i}"><rect x="0" y="{fmt(y)}" width="600" height="{h}"/></clipPath>'
        o.append(f'<g clip-path="url(#g{i})"><g transform="translate({fmt(tx + dx)} {fmt(base)})"><path d="{d}" fill="{letter}"/></g></g>')
    return clips + "".join(o)

def m2(letter, halo, head, tail):          # Aufloesung: oben scharf, unten zerfaellt BPB in fallende Pixel
    r = random.Random(8)
    d, w, cap = text_path(ANTON, "BPB", 230, tracking=8, max_w=500)
    base = 270 + cap / 2; tx = (600 - w) / 2; top = base - cap
    rects, sq = "", []
    x = tx - 4
    while x < tx + w + 4:
        cut = base - r.uniform(2, 78)
        rects += f'<rect x="{fmt(x)}" y="{fmt(top - 30)}" width="13.2" height="{fmt(cut - top + 30)}"/>'
        if r.random() < .8:
            y = cut + 6
            for k in range(r.randint(2, 7)):
                sq.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="12" height="{r.choice([12, 12, 20])}" rx="2" fill="{letter if k == 0 else (head if k % 2 else tail)}" fill-opacity="{fmt(max(.25, 1 - k * .16))}"/>')
                y += 20 + k * 9
        x += 13.2
    o = rain(head, tail, 5)
    o += "".join(sq)
    o += (f'<clipPath id="dz">{rects}</clipPath><g clip-path="url(#dz)"><g transform="translate({fmt(tx)} {fmt(base)})">'
          f'<path d="{d}" fill="{halo}" stroke="{halo}" stroke-width="34" stroke-linejoin="round"/><path d="{d}" fill="{letter}"/></g></g>')
    return o

INK, PAPER = "#111111", "#ffffff"
COL = {"hell": (INK, PAPER, INK, "#9a9a9a", PAPER), "dunkel": (PAPER, INK, PAPER, "#6a6a6a", INK), "gruen": (PAPER, INK, "#c8ffd8", "#22c55e", INK)}
def svg(b, bg):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" fill="{bg}"/>{b}</svg>'
for n, f in {"r7a-glitch": m1, "r7b-aufloesung": m2}.items():
    for k, (le, ha, he, ta, bg) in COL.items():
        open(os.path.join(OUT, f"{n}_{k}.svg"), "w").write(svg(f(le, ha, he, ta), bg))
    le, ha, he, ta, bg = COL["dunkel"]
    open(os.path.join(OUT, f"{n}_app.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600"><rect width="600" height="600" rx="124" fill="{INK}"/>'
        f'<g transform="translate(300 300) scale(.86) translate(-300 -300)">{f(le, ha, he, ta)}</g></svg>')
print("ok")

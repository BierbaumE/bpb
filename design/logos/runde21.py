"""BPB Runde 21 - Anwendungen (Handy, Webseite, Visitenkarte) + vereinfachte Klein-Version fuer Bungee, Titan One, Chango.
Aufruf: python3 -I runde21_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde17_gen.py")).read().split("meta = []")[0])
FAV = {"bungee": ("Bungee", "bungee/Bungee-Regular.ttf", 6), "titan": ("Titan One", "titanone/TitanOne-Regular.ttf", 4), "chango": ("Chango", "chango/Chango-Regular.ttf", 4)}
def simple(R, shape):
    dpath, (cx, cy), _ = SHAPES[shape]; ly, cap, mw = FIT[shape]
    d, w, cp, tx, base = geom(cap * 1.08, ly, mw * 1.04)
    ins = lambda s: f'transform="translate({cx} {cy}) scale({s}) translate({-cx} {-cy})"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><path d="{dpath}" fill="{R["border"]}"/>'
            f'<path d="{dpath}" fill="{R["tile"]}" {ins(.93)}/><g transform="translate({tx:.1f} {base:.1f})">'
            f'<path d="{d}" fill="{R["text"]}" stroke="{R["tile"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"/></g></svg>')
RS = ["dunkel", "zwei", "gruen"]
for k, (n, path, tr) in FAV.items():
    CUR["f"] = loadf(path, None); CUR["tr"] = tr
    for sh in ("kreis", "quadrat", "sechseck"):
        for r in RS:
            open(os.path.join(OUT, f"{k}-{sh}-{r}.svg"), "w").write(framed(ROLES[r], sh))
            open(os.path.join(OUT, f"{k}-{sh}-{r}-klein.svg"), "w").write(simple(ROLES[r], sh))
print("ok")

"""BPB Runde 22 - Symbol-Version mit groeberem Netz (lesbar bei 40-120 px). Aufruf wie runde21_gen.py"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, "runde21_gen.py")).read().split("RS = [")[0]
src17 = open(os.path.join(here, "runde17_gen.py")).read().split("meta = []")[0]
src16 = open(os.path.join(here, "runde16_gen.py")).read().split("for shape in SHAPES")[0]
bold = src16.replace("range(-1, 24)", "range(-1, 12)").replace("i * 27 + 6", "i * 54 + 30").replace("2.6 if i % 3 == 0 else 1.5", "9 if i % 2 == 0 else 5.5")
assert bold != src16
src17 = src17.replace('src = open(os.path.join(here, "runde16_gen.py")).read().split("for shape in SHAPES")[0]', "src = BOLD")
BOLD = bold
exec(src17)
FAV = {"bungee": ("Bungee", "bungee/Bungee-Regular.ttf", 6), "titan": ("Titan One", "titanone/TitanOne-Regular.ttf", 4), "chango": ("Chango", "chango/Chango-Regular.ttf", 4)}
for k, (n, path, tr) in FAV.items():
    CUR["f"] = loadf(path, None); CUR["tr"] = tr
    for sh in ("kreis", "quadrat", "sechseck"):
        for r in ("dunkel", "zwei", "gruen", "rot"):
            open(os.path.join(OUT, f"{k}-{sh}-{r}.svg"), "w").write(framed(ROLES[r], sh))
print("ok")

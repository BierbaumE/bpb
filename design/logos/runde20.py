"""BPB Runde 20 - Favoriten-Schriften (Russo One, Bungee, Titan One, Chango) in Formenfamilie und Farbrollen.
Aufruf: python3 -I runde20_gen.py <ofl> <Ausgabe> <gf-ofl>  (braucht runde17_gen.py)"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde17_gen.py")).read().split("meta = []")[0])
FAV = {"russo": ("Russo One", "russoone/RussoOne-Regular.ttf", 6), "bungee": ("Bungee", "bungee/Bungee-Regular.ttf", 6),
       "titan": ("Titan One", "titanone/TitanOne-Regular.ttf", 4), "chango": ("Chango", "chango/Chango-Regular.ttf", 4)}
BASE = {"russo": "drei", "bungee": "gruen", "titan": "dunkel", "chango": "dunkel"}
ROLE_SET = ["dunkel", "zwei", "rot", "gruen", "violett", "orange"]
for k, (n, path, tr) in FAV.items():
    CUR["f"] = loadf(path, None); CUR["tr"] = tr
    for sh in SHAPES:
        open(os.path.join(OUT, f"s-{k}-{sh}.svg"), "w").write(framed(ROLES[BASE[k]], sh))
    for r in ROLE_SET:
        open(os.path.join(OUT, f"c-{k}-{r}.svg"), "w").write(framed(ROLES[r], "quadrat"))
print("ok")

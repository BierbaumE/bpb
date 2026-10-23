"""BPB Runde 24 - Farbpalette fuer das Bungee-Quadrat-Logo. Aufruf: python3 -I runde24_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde22_gen.py")).read().split("FAV = {")[0])
D = ("#333333", "#000000")
PAL = [  # (Gruppe, Name, tile, grid, text, border, accent, dunkle Schrift?)
 ("Schwarz-Weiß-Grau", "Schwarz / Weiß", "#0a0a0a", "#6a6a6a", "#ffffff", "#ffffff", "#ffffff", 0),
 ("Schwarz-Weiß-Grau", "Anthrazit", "#1b1e24", "#8e959f", "#ffffff", "#d9dde3", "#ffffff", 0),
 ("Schwarz-Weiß-Grau", "Silber", "#2a2f38", "#7d8696", "#e9edf2", "#c9d0da", "#ffffff", 0),
 ("Schwarz-Weiß-Grau", "Hellgrau", "#eceef1", "#a9afb8", "#1b1e24", "#1b1e24", "#1b1e24", 1),
 ("Schwarz-Weiß-Grau", "Papier", "#f7f5ef", "#cfcac0", "#111111", "#111111", "#111111", 1),
 ("Zwei Farben", "Marine / Gold", "#0c2a63", "#ffb400", "#ffb400", "#ffb400", "#ffb400", 0),
 ("Zwei Farben", "Rennrot / Weiß", "#c8102e", "#8f0b20", "#ffffff", "#ffffff", "#ffffff", 0),
 ("Zwei Farben", "Gelb / Schwarz", "#ffd23c", "#d9a800", "#111111", "#111111", "#111111", 1),
 ("Zwei Farben", "Orange / Schwarz", "#ff7a1a", "#c85a00", "#111111", "#111111", "#111111", 1),
 ("Zwei Farben", "Wald / Gold", "#0b2a1c", "#c9a227", "#f1d27a", "#c9a227", "#f1d27a", 0),
 ("Drei Farben", "Digital (Nacht)", "#1a1433", "#ff7ab0", "#ffffff", "#ff7ab0", "#ffb35c", 0),
 ("Drei Farben", "Aubergine / Pink / Gelb", "#1c1038", "#ff3c8e", "#ffd23c", "#ffd23c", "#ff3c8e", 0),
 ("Drei Farben", "Petrol / Koralle / Sand", "#0d3b44", "#ff6f59", "#f6e8cf", "#ff6f59", "#ffb199", 0),
 ("Drei Farben", "Marine / Weiß / Rot", "#0e1f4d", "#4b63b3", "#ffffff", "#e0303c", "#e0303c", 0),
 ("Mehr Farben", "Türkis / Gelb / Pink", "#0d1b2e", "#2ee6c5", "#ffcf3d", "#ff4d6d", "#8a6bff", 0),
 ("Mehr Farben", "Grün (Matrix)", "#0b2016", "#2fbf71", "#e8ffe0", "#2fbf71", "#7dffb0", 0),
 ("Mehr Farben", "Violett / Lila", "#160d33", "#8a6bff", "#ffffff", "#8a6bff", "#b9a3ff", 0),
 ("Mehr Farben", "Rosa / Schwarz", "#ff5fa2", "#c22d74", "#111111", "#111111", "#111111", 1),
 ("Mehr Farben", "Mint / Dunkelgrün", "#bff0d8", "#7fcfae", "#0b3a2a", "#0b3a2a", "#0b3a2a", 1),
 ("Mehr Farben", "Sonnenuntergang", "#2a0f3a", "#ff8a3c", "#ffe7a8", "#ff4d6d", "#ffb35c", 0),
]
CUR["f"] = loadf("bungee/Bungee-Regular.ttf", None); CUR["tr"] = 6
meta = []
for i, (g, n, t, gr, tx, b, a, dk) in enumerate(PAL, 1):
    R = dict(tile=t, grid=gr, text=tx, border=b, accent=a)
    if dk: R["s1"], R["s2"] = D
    open(os.path.join(OUT, f"p{i:02d}.svg"), "w").write(framed(R, "quadrat"))
    meta.append((i, g, n, t, gr, tx, b, a))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"))
print("ok", len(meta))

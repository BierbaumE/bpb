"""BPB Runde 25 - bereinigte Palette: nur helle/weisse Schrift, keine Zweifarbigen, keine hellen Flaechen.
Aufruf: python3 -I runde25_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde24_gen.py")).read().split("CUR[\"f\"]")[0])
KEEP = {"Schwarz / Weiß", "Anthrazit", "Silber", "Digital (Nacht)", "Petrol / Koralle / Sand", "Marine / Weiß / Rot", "Grün (Matrix)", "Violett / Lila"}
P2 = [(("Schwarz-Weiß-Grau" if n in ("Schwarz / Weiß", "Anthrazit", "Silber") else "Bisherige Favoriten"), n, t, gr, tx, b, a, 0)
      for (g, n, t, gr, tx, b, a, dk) in PAL if n in KEEP]
NEU = [("Blau-Nacht", "#0a1230", "#4da3ff", "#ffffff", "#4da3ff", "#8ccbff"), ("Cyan-Nacht", "#061e26", "#2ee6c5", "#ffffff", "#2ee6c5", "#7dfff0"),
       ("Rot-Nacht", "#1a0b0d", "#e0303c", "#ffffff", "#e0303c", "#ff6b73"), ("Magenta-Nacht", "#1f0a24", "#e03cc8", "#ffffff", "#e03cc8", "#ff8ae8"),
       ("Indigo / Cyan", "#120f3d", "#5b6cff", "#ffffff", "#2ee6c5", "#2ee6c5"), ("Violett / Pink", "#1a0f3a", "#8a6bff", "#ffffff", "#ff7ab0", "#ff7ab0"),
       ("Blau / Pink", "#0c1a3d", "#3d7bff", "#ffffff", "#ff4d9a", "#ff4d9a"), ("Smaragd / Cyan", "#04201a", "#1fbf8f", "#ffffff", "#2ee6e6", "#7dffd9"),
       ("Stahl / Rot", "#15181e", "#7d8696", "#ffffff", "#e0303c", "#e0303c"), ("Schwarz / Pink", "#0a0a0a", "#ff7ab0", "#ffffff", "#ff7ab0", "#ff7ab0")]
P2 += [("Neu: Nacht-Welten", n, t, gr, tx, b, a, 0) for (n, t, gr, tx, b, a) in NEU]
CUR["f"] = loadf("bungee/Bungee-Regular.ttf", None); CUR["tr"] = 6
meta = []
for i, (g, n, t, gr, tx, b, a, dk) in enumerate(P2, 1):
    open(os.path.join(OUT, f"q{i:02d}.svg"), "w").write(framed(dict(tile=t, grid=gr, text=tx, border=b, accent=a), "quadrat"))
    meta.append((i, g, n, t, gr, tx, b, a))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w")); print("ok", len(meta))

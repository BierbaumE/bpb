"""BPB Runde 26 - andere Schriftfarben auf den dunklen Nacht-Flaechen. Aufruf: python3 -I runde26_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde24_gen.py")).read().split("CUR[\"f\"]")[0])
DN = ("#1a1433", "#ff7ab0", "#ff7ab0", "#ff9cc7"); BN = ("#0a1230", "#4da3ff", "#4da3ff", "#8ccbff"); CN = ("#061e26", "#2ee6c5", "#2ee6c5", "#7dfff0")
RN = ("#1a0b0d", "#e0303c", "#e0303c", "#ff6b73"); MN = ("#1f0a24", "#e03cc8", "#e03cc8", "#ff8ae8"); VI = ("#160d33", "#8a6bff", "#8a6bff", "#b9a3ff")
SM = ("#04201a", "#1fbf8f", "#2ee6e6", "#7dffd9"); SW = ("#0a0a0a", "#6a6a6a", "#ffffff", "#ffffff"); AN = ("#1b1e24", "#8e959f", "#d9dde3", "#ffffff")
LIST = [("Digital Nacht · Rosa", DN, "#ff9cc7"), ("Digital Nacht · Eisblau", DN, "#cfe8ff"), ("Digital Nacht · Lila", DN, "#c9b3ff"),
 ("Blau-Nacht · Cyan", BN, "#7df3ff"), ("Blau-Nacht · Rosa", BN, "#ff8ac0"), ("Cyan-Nacht · Mintweiß", CN, "#d6fff4"), ("Cyan-Nacht · Pink", CN, "#ff6fb5"),
 ("Rot-Nacht · Silber", RN, "#e3e6ee"), ("Rot-Nacht · Rosé", RN, "#ffb3b8"), ("Magenta-Nacht · Cyan", MN, "#8ff3ff"), ("Violett · Mint", VI, "#9cffd9"),
 ("Violett · Hellrosa", VI, "#ffb5e0"), ("Smaragd · Eisblau", SM, "#d4f6ff"), ("Schwarz · Chrom", SW, "#c9d0da"), ("Schwarz · Rot", SW, "#ff4d5a"), ("Anthrazit · Cyan", AN, "#5ff0ff")]
CUR["f"] = loadf("bungee/Bungee-Regular.ttf", None); CUR["tr"] = 6
meta = []
for i, (n, (t, gr, b, a), tx) in enumerate(LIST, 1):
    open(os.path.join(OUT, f"s{i:02d}.svg"), "w").write(framed(dict(tile=t, grid=gr, text=tx, border=b, accent=a), "quadrat")); meta.append((i, n, tx))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w")); print("ok")

"""BPB Runde 29 - Logo mit ausgeschriebenem Firmennamen darunter (gestapelt), je Farbschema, hell/dunkel.
Aufruf: python3 -I runde29_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde28_gen.py")).read().split("for k, R in LOGOS.items()")[0])
LOGOS["grau"] = dict(tile="#0a0a0a", grid="#6a6a6a", text="#ffffff", border="#ffffff", accent="#ffffff")
NAMES = {"digA": "Digital A · Violett/Pink", "digB": "Digital B · Warmgrau", "digC": "Digital Nacht", "hausA": "Haus A · Grün/Holz", "hausB": "Haus B · Teal/Gelb", "hausC": "Haus C · Grün (Matrix)", "grau": "Schwarz/Weiß"}
mf = loadf("manrope/Manrope[wght].ttf", {"wght": 800})
nd, nw, nc = text_path(mf, "BierbaumPerformanceBrothers", 46, tracking=2, max_w=640)
for k, R in LOGOS.items():
    main = framed(R, "quadrat"); inner = main.split(">", 1)[1].rsplit("</svg>", 1)[0]
    for tag, col in (("dunkel", "#ffffff"), ("hell", "#1a1433")):
        open(os.path.join(OUT, f"{k}-{tag}.svg"), "w").write(
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 500"><svg x="170" y="0" width="360" height="360" viewBox="0 0 600 600">{inner}</svg>'
          f'<g transform="translate({(700 - nw) / 2:.1f} 440)"><path d="{nd}" fill="{col}"/></g></svg>')
json.dump(list(LOGOS), open(os.path.join(OUT, "meta.json"), "w")); json.dump(NAMES, open(os.path.join(OUT, "names.json"), "w")); print("ok")

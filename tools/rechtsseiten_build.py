#!/usr/bin/env python3
"""Erzeugt die Impressum- und Datenschutz-Seiten je Marke (/bytes/impressum/ usw.) aus den Dach-Seiten
public/impressum/index.html und public/datenschutz/index.html und trägt die Links in den Fußzeilen der Markenseiten ein.
Aufruf aus der Repo-Wurzel:  python3 tools/rechtsseiten_build.py
Die Dach-Seiten bleiben die Quelle für den Text; Farben je Marke stehen in public/recht-marke.css (Klassen m-bytes, m-bauhof, m-brain, m-bolide)."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / "public"
MARKEN = {  # Pfad: (Kurzname, Wortteil, Langform, Klasse)
    "bytes": ("BPBytes", "Bytes", "BierbaumPerformanceBytes", "m-bytes"),
    "bauhof": ("BPBauhof", "Bauhof", "BierbaumPerformanceBauhof", "m-bauhof"),
    "brain": ("BPBrain", "Brain", "BierbaumPerformanceBrain", "m-brain"),
    "bolide": ("BPBolide", "Bolide", "BierbaumPerformanceBolide", "m-bolide"),
}
THEMEFARBE = {"bytes": "#0e0b1a", "bauhof": "#f7f4ea", "brain": "#0a1f28", "bolide": "#12100d"}
SEITEN = {"impressum": "Impressum", "datenschutz": "Datenschutz"}

def haupttext(name):
    html = (ROOT / name / "index.html").read_text()
    m = re.search(r"<main>(.*?)</main>", html, re.S)
    return m.group(1).strip()

TEXTE = {n: haupttext(n) for n in SEITEN}

def seite(marke, was):
    kurz, wort, lang, klasse = MARKEN[marke]
    andere = [k for k in MARKEN if k != marke]
    nav = "".join(f'<a href="/{marke}/{s}/"{" aria-current=\"page\"" if s == was else ""}>{t}</a>' for s, t in SEITEN.items())
    mehr = "".join(f'<a href="/{k}/">{MARKEN[k][0]}</a>' for k in andere)
    text = TEXTE[was].replace('<h1>', f'<p class="marke">{lang} ist eine Marke von BierbaumPerformanceBrothers.</p>\n<h1>', 1)
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SEITEN[was]} – {kurz}</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{THEMEFARBE[marke]}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/recht-marke.css">
</head>
<body class="{klasse}">
<header class="hd"><a class="brand" href="/{marke}/">BP<b>{wort}</b></a><nav>{nav}</nav></header>
<main>
{text}
</main>
<footer class="ft"><span>{lang} – eine Marke von BierbaumPerformanceBrothers</span><span><a href="/{marke}/">Zur Startseite von {kurz}</a>{mehr}<a href="/">BPB</a></span></footer>
</body>
</html>
'''

for marke in MARKEN:
    for was in SEITEN:
        d = ROOT / marke / was
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(seite(marke, was))
    # Fußzeile der Markenseite: Impressum/Datenschutz der eigenen Marke
    p = ROOT / marke / "index.html"
    h = p.read_text()
    h = h.replace('<a href="/impressum/">Impressum</a>', f'<a href="/{marke}/impressum/">Impressum</a>').replace('<a href="/datenschutz/">Datenschutz</a>', f'<a href="/{marke}/datenschutz/">Datenschutz</a>')
    p.write_text(h)
print("fertig:", ", ".join(f"/{m}/{s}/" for m in MARKEN for s in SEITEN))

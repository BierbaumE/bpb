"""BPB Runde 23 - Webdesign 'Digital C Nacht' mit dem Bungee-Gravitationsnetz-Logo in allen Formen.
Aufruf: python3 -I runde23_gen.py <ofl> <Ausgabe> <gf-ofl>  (braucht runde22_gen.py)"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
s22 = open(os.path.join(here, "runde22_gen.py")).read().split("FAV = {")[0]
exec(s22)
ROLES["digital"] = dict(tile="#1a1433", grid="#ff7ab0", text="#ffffff", border="#ff7ab0", accent="#ffb35c")
CUR["f"] = loadf("bungee/Bungee-Regular.ttf", None); CUR["tr"] = 6
for sh in SHAPES:
    open(os.path.join(OUT, f"logo-{sh}.svg"), "w").write(framed(ROLES["digital"], sh))
FONTS_CSS = "".join(f'@font-face{{font-family:"{n}";src:url("file://{GF}/{p}");font-weight:200 900}}' for n, p in
    (("Bricolage Grotesque", "bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf"), ("Manrope", "manrope/Manrope[wght].ttf")))
def page(sh, logo_src="logo-%s.svg"):
    L = logo_src % sh
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>BPB Digital – {sh}</title><style>{FONTS_CSS}
body{{margin:0;font-family:'Manrope',sans-serif;background:#0e0b1a;color:#ece8f7;line-height:1.55}}a{{color:inherit;text-decoration:none}}
.h{{font-family:'Bricolage Grotesque',sans-serif}}</style></head><body>
<header style="display:flex;gap:12px 28px;align-items:center;justify-content:space-between;padding:16px 56px;border-bottom:1px solid #261f40">
<a style="display:flex;align-items:center;gap:14px"><img src="{L}" style="width:64px;height:64px"><span class="h" style="font-weight:700;font-size:20px">BPB <span style="color:#ff7ab0">Digital</span></span></a>
<nav style="display:flex;gap:26px;font-size:15px;font-weight:500;align-items:center"><a>Leistungen</a><a>Produkte</a><a>Über uns</a><a style="background:#ff7ab0;color:#0e0b1a;font-weight:700;padding:10px 20px;border-radius:10px">Kontakt</a></nav></header>
<section style="padding:70px 56px 44px;display:flex;gap:40px;align-items:center"><div style="flex:1"><p style="margin:0 0 16px;font-size:14px;font-weight:700;letter-spacing:2px;color:#ffb35c">BIERBAUMPERFORMANCEBROTHERS · SOFTWARE &amp; BERATUNG</p>
<h1 class="h" style="margin:0;font-weight:800;font-size:72px;line-height:1;letter-spacing:-2px">Apps für Leute, die <span style="color:#ff7ab0">keine Zeit</span> für Software haben.</h1>
<p style="margin:26px 0 0;max-width:600px;font-size:20px;color:#b9b0d4">Vereine, Handwerk, kleine Firmen: Wir bauen, was im Alltag gebraucht wird.</p></div>
<img src="{L}" style="width:300px;height:300px;flex:none;filter:drop-shadow(0 0 40px #ff7ab044)"></section>
<section style="padding:24px 56px 56px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
<div style="background:#17122b;border:1px solid #2e2650;border-radius:20px;padding:30px"><p style="margin:0;font-size:13px;font-weight:700;color:#ffb35c;letter-spacing:1.5px">HANDWERK</p><h2 class="h" style="margin:6px 0 8px;font-size:36px">Craftsman</h2><p style="margin:0 0 20px;color:#b9b0d4">Zeiten, Material, Rechnungen – am Handy erfasst, im Büro abgerechnet.</p><a style="background:#ff7ab0;color:#0e0b1a;font-weight:700;padding:12px 22px;border-radius:10px;display:inline-block">Demo als Chef</a></div>
<div style="background:#17122b;border:1px solid #2e2650;border-radius:20px;padding:30px"><p style="margin:0;font-size:13px;font-weight:700;color:#ffb35c;letter-spacing:1.5px">FESTE &amp; VEREINE</p><h2 class="h" style="margin:6px 0 8px;font-size:36px">Abkassiert</h2><p style="margin:0 0 20px;color:#b9b0d4">Bestellen. Bonieren. Abkassiert. Der Bon liegt sofort in Küche oder Theke.</p><a style="background:#ff7ab0;color:#0e0b1a;font-weight:700;padding:12px 22px;border-radius:10px;display:inline-block">Demo als Inhaber</a></div></section>
<footer style="padding:22px 56px;border-top:1px solid #261f40;display:flex;align-items:center;gap:14px;font-size:14px;color:#8a80ab"><img src="{L}" style="width:32px;height:32px"><span>© BierbaumPerformanceBrothers (BPB)</span></footer></body></html>'''
for sh in SHAPES:
    open(os.path.join(OUT, f"seite-{sh}.html"), "w").write(page(sh))
print("ok")

"""BPB Runde 17 - Schriftvergleich im Gravitationsnetz-Quadrat. Aufruf: python3 -I runde17_gen.py <ofl-Ordner> <Ausgabe> <gf-ofl-Ordner>"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "runde16_gen.py")).read().split("for shape in SHAPES")[0]
exec(src)
from fontTools.varLib import instancer
from fontTools.pens.boundsPen import BoundsPen
GF = sys.argv[3]
# (Nr, Gruppe, Name, Datei, Variationsachsen, Tracking)
FONTS = [
 ("hart","Anton","anton/Anton-Regular.ttf",None,6),
 ("hart","Black Ops One","blackopsone/BlackOpsOne-Regular.ttf",None,6),
 ("hart","Bebas Neue","bebasneue/BebasNeue-Regular.ttf",None,8),
 ("hart","Russo One","russoone/RussoOne-Regular.ttf",None,6),
 ("hart","Bungee","bungee/Bungee-Regular.ttf",None,6),
 ("hart","Audiowide","audiowide/Audiowide-Regular.ttf",None,6),
 ("hart","Orbitron Black","orbitron/Orbitron[wght].ttf",{"wght":900},6),
 ("weich","Fredoka Bold","fredoka/Fredoka[wdth,wght].ttf",{"wght":700,"wdth":100},4),
 ("weich","Baloo 2 ExtraBold","baloo2/Baloo2[wght].ttf",{"wght":800},4),
 ("weich","Titan One","titanone/TitanOne-Regular.ttf",None,4),
 ("weich","Chango","chango/Chango-Regular.ttf",None,4),
 ("weich","Cherry Bomb One","cherrybombone/CherryBombOne-Regular.ttf",None,4),
 ("schnoerkel","Lobster","lobster/Lobster-Regular.ttf",None,4),
 ("schnoerkel","Pacifico","pacifico/Pacifico-Regular.ttf",None,4),
 ("schnoerkel","Shrikhand","shrikhand/Shrikhand-Regular.ttf",None,4),
 ("schnoerkel","Almendra Display","almendradisplay/AlmendraDisplay-Regular.ttf",None,6),
 ("kunst","Limelight (Art Deco)","limelight/Limelight-Regular.ttf",None,6),
 ("kunst","Abril Fatface","abrilfatface/AbrilFatface-Regular.ttf",None,6),
 ("kunst","Cinzel Decorative","cinzeldecorative/CinzelDecorative-Black.ttf",None,6),
 ("kunst","Monoton","monoton/Monoton-Regular.ttf",None,6),
 ("welt","UnifrakturCook (Deutschland)","unifrakturcook/UnifrakturCook-Bold.ttf",None,6),
 ("welt","Pirata One (Fraktur)","pirataone/PirataOne-Regular.ttf",None,6),
 ("welt","Rye (Wilder Westen)","rye/Rye-Regular.ttf",None,6),
 ("welt","Yatra One (Indien)","yatraone/YatraOne-Regular.ttf",None,6),
 ("welt","ZCOOL KuaiLe (China)","zcoolkuaile/ZCOOLKuaiLe-Regular.ttf",None,6),
 ("welt","Tajawal Black (Arabien)","tajawal/Tajawal-Black.ttf",None,6),
]
CUR = {}
def geom(cap, cy, max_w, tr=6):
    d, w, cap = text_path(CUR["f"], "BPB", cap, tracking=CUR["tr"], max_w=max_w)
    return d, w, cap, (600 - w) / 2, cy + cap / 2
def loadf(path, axes):
    p = os.path.join(OFL if path.startswith("anton") else GF, path)
    f = TTFont(p)
    if axes: f = instancer.instantiateVariableFont(f, axes)
    gs = f.getGlyphSet(); bp = BoundsPen(gs); gs[f.getBestCmap()[ord("H")]].draw(bp)
    f["OS/2"].sCapHeight = int(bp.bounds[3])
    return f
ROLES.update({
 "rot":   dict(tile="#1a0b0d", grid="#c8242f", text="#ffffff", border="#e0303c", accent="#ff4b55"),
 "gruen": dict(tile="#0b2016", grid="#2fbf71", text="#e8ffe0", border="#2fbf71", accent="#7dffb0"),
 "orange":dict(tile="#f2f2f0", grid="#ff7a1a", text="#111111", border="#ff7a1a", accent="#ff7a1a", s1="#555555", s2="#222222"),
 "violett":dict(tile="#160d33", grid="#8a6bff", text="#ffffff", border="#8a6bff", accent="#b9a3ff"),
 "silber":dict(tile="#2a2f38", grid="#7d8696", text="#e9edf2", border="#c9d0da", accent="#ffffff"),
})
ORDER = ["dunkel","zwei","rot","drei","gruen","viel","hell","violett","orange","silber"]
meta = []
for i, (grp, name, path, axes, tr) in enumerate(FONTS, 1):
    CUR["f"] = loadf(path, axes); CUR["tr"] = tr
    open(os.path.join(OUT, f"f{i:02d}.svg"), "w").write(framed(ROLES[ORDER[(i-1)%len(ORDER)]], "quadrat"))
    meta.append((i, grp, name))
import json; json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"))
print("ok", len(meta))

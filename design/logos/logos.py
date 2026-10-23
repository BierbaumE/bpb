D="#1c1240"; W="#ffffff"
def svg(body,vb="0 0 200 200"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'
def sep(body,col,w=5): return f'<g stroke="{col}" stroke-width="{w}" stroke-linejoin="round">{body}</g>'
C=[]
# 1 Aufgang
def f1(c,line): return f'<path d="M18 138a32 32 0 0 1 64 0z" fill="{c[0]}"/><path d="M118 138a32 32 0 0 1 64 0z" fill="{c[2]}"/><path d="M52 138a48 48 0 0 1 96 0z" fill="{c[1]}"/><rect x="14" y="150" width="172" height="10" rx="5" fill="{line}"/>'
C.append(("Aufgang","Drei Sonnen am Horizont, klein – groß – klein: drei Brüder, ein Aufgang. Nimmt die Sonne aus dem bisherigen Logo auf.",
 lambda: f1(["#e8508f","#ffb35c","#8d7bff"],D), lambda: f1(["#e8508f","#ffb35c","#8d7bff"],W),
 lambda: sep(f1([D,D,D],D),W,6), lambda: sep(f1([W,W,W],W),"#17122b",6), "0 0 200 200"))
# 2 Aufstieg
def f2(c): return f'<rect x="28" y="100" width="40" height="70" rx="12" fill="{c[0]}"/><rect x="80" y="64" width="40" height="106" rx="12" fill="{c[1]}"/><rect x="132" y="28" width="40" height="142" rx="12" fill="{c[2]}"/>'
P3=["#8d7bff","#e8508f","#ffb35c"]
C.append(("Aufstieg","Drei Balken, jeder höher: Leistung, Wachstum, drei Brüder. Sehr einfach, wirkt aber auch wie ein Diagramm-Symbol.",
 lambda: f2(P3), lambda: f2(P3), lambda: f2([D]*3), lambda: f2([W]*3), "0 0 200 200"))
# 3 Dreifach-B
def f3(c,stem): return f'<rect x="46" y="22" width="26" height="156" rx="4" fill="{stem}"/><path d="M72 22h20a26 26 0 0 1 0 52H72z" fill="{c[0]}"/><path d="M72 74h26a26 26 0 0 1 0 52H72z" fill="{c[1]}"/><path d="M72 126h32a26 26 0 0 1 0 52H72z" fill="{c[2]}"/>'
C.append(("Dreifach-B","Ein B mit drei Bäuchen: drei Brüder in einem Buchstaben. Funktioniert auch winzig als App-Symbol.",
 lambda: f3(P3,"#3a2a8a"), lambda: f3(P3,W), lambda: sep(f3([D]*3,D),W,4), lambda: sep(f3([W]*3,W),"#17122b",4), "0 0 200 200"))
# 4 Siegel
def f4(bg,sun,txt,ring): return (f'<circle cx="100" cy="100" r="84" fill="{bg}"/><path d="M50 106a50 50 0 0 1 100 0z" fill="{sun}"/>'
  f'<rect x="40" y="112" width="120" height="6" rx="3" fill="{sun}"/>'
  f'<text x="100" y="158" text-anchor="middle" font-family="Arial Black,Arial,Helvetica,sans-serif" font-weight="900" font-size="38" letter-spacing="3" fill="{txt}">BPB</text>'
  f'<circle cx="100" cy="100" r="92" fill="none" stroke="{ring}" stroke-width="6"/>')
C.append(("Siegel","Rundes Herstellersiegel mit aufgehender Sonne über dem Kürzel – wirkt wie ein Gütestempel auf jedem Produkt.",
 lambda: f4("#2a1a6a","#ffb35c",W,"#e8508f"), lambda: f4("#2a1a6a","#ffb35c",W,"#ffb35c"), lambda: f4(D,W,W,D), lambda: f4(W,"#17122b","#17122b",W), "0 0 200 200"))
# 5 Wortmarke
def f5(l,s):
    B=f'<g fill="none" stroke="{l}" stroke-width="20"><path d="M10 10H40a20 20 0 0 1 0 40H10M10 50H44a22 22 0 0 1 0 44H10"/><path d="M10 0V104"/></g>'
    P=f'<rect x="0" y="0" width="20" height="104" fill="{l}"/><path d="M20 0H34a34 34 0 0 1 0 68H20z" fill="{s}"/>'
    return f'<g transform="translate(4 48)">{B}</g><g transform="translate(96 48)">{P}</g><g transform="translate(178 48)">{B}</g>'
C.append(("Wortmarke","Nur das Kürzel, selbst gezeichnet: Der Bauch des P ist die Sonne. Schlicht wie ein klassischer Hersteller-Schriftzug.",
 lambda: f5("#3a2a8a","#ffb35c"), lambda: f5(W,"#ffb35c"), lambda: f5(D,D), lambda: f5(W,W), "0 28 262 148"))
# 6 Gipfel
def f6(c,sun): return (f'<circle cx="150" cy="60" r="22" fill="{sun}"/><path d="M6 170 58 90l52 80z" fill="{c[0]}"/><path d="M90 170l52-80 52 80z" fill="{c[2]}"/>'
  f'<path d="M58 170 100 36l42 134z" fill="{c[1]}"/>')
C.append(("Gipfel","Drei Spitzen, die mittlere am höchsten, Sonne dahinter: Leistung und Zusammenhalt.",
 lambda: f6(P3,"#ffd65c"), lambda: f6(P3,"#ffd65c"), lambda: sep(f6([D]*3,D),W,5), lambda: sep(f6([W]*3,W),"#17122b",5), "0 0 200 200"))

html='''<!doctype html><meta charset=utf-8><style>
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f4f1fa;color:#1c1240;padding:28px;width:1400px}
h1{margin:0 0 4px;font-size:30px}p.s{margin:0 0 22px;color:#5d5580}
.g{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.c{background:#fff;border-radius:18px;padding:22px;border:1px solid #e0daf0}
.c h2{margin:0;font-size:22px}.c h2 span{color:#e8508f}.c p{margin:4px 0 14px;color:#5d5580;font-size:14px}
.r{display:flex;gap:12px;align-items:stretch;margin-top:12px}.r:first-of-type{margin-top:0}
.b{border-radius:12px;display:flex;align-items:center;justify-content:center;flex:1;padding:14px;gap:14px}
.w{background:#fff;border:1px solid #e0daf0}.d{background:#17122b}
.big svg{width:150px;height:150px}.big.wm svg{width:240px;height:133px}
.sm svg{width:30px;height:30px}.sm.wm svg{width:54px;height:30px}.sm .t{font-size:11px;color:#8a80ab}
.lock{font-weight:700;font-size:17px;justify-content:flex-start}.lock svg{width:44px;height:44px;flex:none}.lock.wm svg{width:70px}
.foot{margin-top:12px;border-radius:12px;background:#17122b;color:#ece8f7;padding:12px 18px;display:flex;align-items:center;gap:10px;font-size:14px}
.foot svg{width:26px;height:26px}.foot.wm svg{width:46px}.foot b{font-size:15px}
</style><h1>BierbaumPerformanceBrothers – Logo-Vorschläge für die Dachmarke</h1><p class=s>Je Entwurf: groß auf hell und dunkel · klein und einfarbig (Stempel, Druck, Gravur) · mit Namen · als Herstellerzeile unter einer Marke. Farben aus dem bisherigen BPB-Logo.</p><div class=g>'''
for i,(name,desc,L,Dk,ML,MD,vb) in enumerate(C,1):
    wm=" wm" if i==5 else ""
    s=lambda f: svg(f(),vb)
    slug=name.lower().replace("-","")
    open(f"bpb-logo-{i}-{slug}.svg","w").write(s(L))
    open(f"bpb-logo-{i}-{slug}-dunkel.svg","w").write(s(Dk))
    open(f"bpb-logo-{i}-{slug}-einfarbig.svg","w").write(s(ML))
    html+=f'''<div class=c><h2><span>{i}</span> {name}</h2><p>{desc}</p>
<div class=r><div class="b w big{wm}">{s(L)}</div><div class="b d big{wm}">{s(Dk)}</div></div>
<div class=r><div class="b w sm{wm}">{s(L)}{s(ML)}<span class=t>klein · einfarbig</span></div><div class="b d sm{wm}">{s(Dk)}{s(MD)}</div></div>
<div class=r><div class="b w lock{wm}">{s(L)}<span>BierbaumPerformanceBrothers</span></div></div>
<div class="foot{wm}">{s(Dk)}<span>Craftsman · Abkassiert · Garten — <b>eine Marke von BierbaumPerformanceBrothers</b></span></div></div>'''
html+='</div>'
open("sheet.html","w").write(html)

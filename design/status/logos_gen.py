import sys, os
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
D = "#1c1240"; W = "#ffffff"

def svg(body, vb="0 0 200 200"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'

def sep(body, col, w=5):
    return f'<g stroke="{col}" stroke-width="{w}" stroke-linejoin="round">{body}</g>'

C = []
P3 = ["#8d7bff", "#e8508f", "#ffb35c"]

def f1(c, line):
    return (f'<path d="M18 138a32 32 0 0 1 64 0z" fill="{c[0]}"/><path d="M118 138a32 32 0 0 1 64 0z" fill="{c[2]}"/>'
            f'<path d="M52 138a48 48 0 0 1 96 0z" fill="{c[1]}"/><rect x="14" y="150" width="172" height="10" rx="5" fill="{line}"/>')
C.append(("Aufgang", "Drei Sonnen am Horizont: klein, groß, klein. Drei Brüder, ein Aufgang. Nimmt die Sonne aus dem bisherigen Logo auf.",
          lambda: f1(["#e8508f", "#ffb35c", "#8d7bff"], D), lambda: f1(["#e8508f", "#ffb35c", "#8d7bff"], W), "0 0 200 200"))

def f2(c):
    return (f'<rect x="28" y="100" width="40" height="70" rx="12" fill="{c[0]}"/><rect x="80" y="64" width="40" height="106" rx="12" fill="{c[1]}"/>'
            f'<rect x="132" y="28" width="40" height="142" rx="12" fill="{c[2]}"/>')
C.append(("Aufstieg", "Drei Balken, jeder höher: Leistung, Wachstum, drei Brüder. Sehr einfach, wirkt aber auch wie ein Diagramm-Symbol.",
          lambda: f2(P3), lambda: f2(P3), "0 0 200 200"))

def f3(c, stem):
    return (f'<rect x="46" y="22" width="26" height="156" rx="4" fill="{stem}"/><path d="M72 22h20a26 26 0 0 1 0 52H72z" fill="{c[0]}"/>'
            f'<path d="M72 74h26a26 26 0 0 1 0 52H72z" fill="{c[1]}"/><path d="M72 126h32a26 26 0 0 1 0 52H72z" fill="{c[2]}"/>')
C.append(("Dreifach-B", "Ein B mit drei Bäuchen: drei Brüder in einem Buchstaben. Funktioniert auch winzig als App-Symbol.",
          lambda: f3(P3, "#3a2a8a"), lambda: f3(P3, W), "0 0 200 200"))

def f4(bg, sun, txt, ring):
    return (f'<circle cx="100" cy="100" r="84" fill="{bg}"/><path d="M50 106a50 50 0 0 1 100 0z" fill="{sun}"/>'
            f'<rect x="40" y="112" width="120" height="6" rx="3" fill="{sun}"/>'
            f'<text x="100" y="158" text-anchor="middle" font-family="Arial Black,Arial,Helvetica,sans-serif" font-weight="900" font-size="38" letter-spacing="3" fill="{txt}">BPB</text>'
            f'<circle cx="100" cy="100" r="92" fill="none" stroke="{ring}" stroke-width="6"/>')
C.append(("Siegel", "Rundes Herstellersiegel mit aufgehender Sonne über dem Kürzel. Wirkt wie ein Gütestempel auf jedem Produkt.",
          lambda: f4("#2a1a6a", "#ffb35c", W, "#e8508f"), lambda: f4("#2a1a6a", "#ffb35c", W, "#ffb35c"), "0 0 200 200"))

def f5(l, s):
    B = (f'<g fill="none" stroke="{l}" stroke-width="20"><path d="M10 10H40a20 20 0 0 1 0 40H10M10 50H44a22 22 0 0 1 0 44H10"/>'
         f'<path d="M10 0V104"/></g>')
    P = f'<rect x="0" y="0" width="20" height="104" fill="{l}"/><path d="M20 0H34a34 34 0 0 1 0 68H20z" fill="{s}"/>'
    return f'<g transform="translate(4 48)">{B}</g><g transform="translate(96 48)">{P}</g><g transform="translate(178 48)">{B}</g>'
C.append(("Wortmarke", "Nur das Kürzel, selbst gezeichnet: Der Bauch des P ist die Sonne. Schlicht wie ein klassischer Hersteller-Schriftzug.",
          lambda: f5("#3a2a8a", "#ffb35c"), lambda: f5(W, "#ffb35c"), "0 28 262 148"))

def f6(c, sun):
    return (f'<circle cx="150" cy="60" r="22" fill="{sun}"/><path d="M6 170 58 90l52 80z" fill="{c[0]}"/><path d="M90 170l52-80 52 80z" fill="{c[2]}"/>'
            f'<path d="M58 170 100 36l42 134z" fill="{c[1]}"/>')
C.append(("Gipfel", "Drei Spitzen, die mittlere am höchsten, Sonne dahinter: Leistung und Zusammenhalt.",
          lambda: f6(P3, "#ffd65c"), lambda: f6(P3, "#ffd65c"), "0 0 200 200"))

import json
meta = []
for i, (name, desc, L, Dk, vb) in enumerate(C, 1):
    open(os.path.join(out, f"logo-{i}-hell.svg"), "w").write(svg(L(), vb))
    open(os.path.join(out, f"logo-{i}-dunkel.svg"), "w").write(svg(Dk(), vb))
    meta.append({"nr": i, "name": name, "desc": desc})
json.dump(meta, open(os.path.join(out, "meta.json"), "w"), ensure_ascii=False)
print("ok", len(C))

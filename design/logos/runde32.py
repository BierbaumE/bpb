"""BPB Runde 32 - atmendes Logo (SMIL, schlank): Netz atmet, BPB schwebt minimal. Nur Hauptlogo (Quadrat, ohne Namen).
Aufruf: python3 -I runde32_gen.py <ofl> <Ausgabe> <gf-ofl>"""
import sys, os, math
here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(here, "runde28_gen.py")).read().split("for k, R in LOGOS.items()")[0])
DUR = "7s"
def netz(P, R, cyc, cap, mw):          # ersetzt das statische Netz durch ein atmendes
    c = (300, cyc)
    def lines(a, b):
        def warp(x, y):
            dx, dy = x - c[0], y - c[1]; dd = math.hypot(dx, dy) + 1e-6
            k = 1 - a * math.exp(-(dd / 120) ** 2) - b * math.exp(-(dd / 260) ** 2)
            return c[0] + dx * k, c[1] + dy * k
        out = []
        for horiz in (True, False):
            for i in range(-1, 12):
                v = i * 54 + 30
                out.append(((horiz, i), " ".join(f"{x:.0f},{y:.0f}" for x, y in (warp(*((j, v) if horiz else (v, j))) for j in range(0, 601, 20)))))
        return out
    A, B = lines(.88, .25), lines(.97, .31)
    g = ""
    for ((h, i), pa), (_, pb) in zip(A, B):
        g += (f'<polyline points="{pa}" fill="none" stroke="{R["grid"]}" stroke-width="{9 if i % 2 == 0 else 5.5}"><animate attributeName="points" dur="{DUR}" repeatCount="indefinite" '
              f'values="{pa};{pb};{pa}" keyTimes="0;.5;1" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></polyline>')
    d, w, cp, tx, base = geom(cap, cyc, mw)
    dark = "#000000" if R["tile"] < "#808080" else "#7d838c"
    st = lambda wd, col, op, f="": f'<use href="#bpb" fill="{col}" stroke="{col}" stroke-width="{wd}" stroke-linejoin="round" opacity="{op}" {f}/>'
    ext = 15
    s1, s2 = mix(R["text"], "#000000", .35), mix(R["text"], "#000000", .8)
    letters = (f'<g transform="translate({tx:.1f} {base:.1f})"><defs><path id="bpb" d="{d}"/></defs>'
               + st(70, dark, .55, 'filter="url(#gl2)"') + st(30, R["accent"], .42, 'filter="url(#gl)"') + st(15, dark, .8, 'filter="url(#sf)"')
               + f'<use href="#bpb" fill="#000" opacity=".6" filter="url(#ds)" transform="translate({ext * .9:.1f} {ext * 1.1 + 6:.1f})"/>'
               + "".join(f'<use href="#bpb" fill="{mix(s1, s2, i / ext)}" transform="translate({i * .85:.2f} {i:.2f})"/>' for i in range(ext, 0, -1))
               + '<use href="#bpb" fill="url(#face)"/>'
               + f'<use href="#bpb" fill="none" stroke="{mix(R["text"], "#ffffff", .55)}" stroke-width="1.6" stroke-opacity=".75" stroke-linejoin="round"/></g>')
    mk = f'<g mask="url(#m)"><g id="net">{g}</g></g>'
    return (f'<g opacity=".5"><use href="#net"/></g>' if False else "") + mk + f'<use href="#net" filter="url(#gl)" opacity=".55" mask="url(#m)"/>' + \
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -2.5;0 0" dur="{DUR}" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>{letters}</g>'
for k in ("digA", "digC"):
    s = framed(LOGOS[k], "quadrat")
    open(os.path.join(OUT, f"atmend-{k}.svg"), "w").write(s)
print("ok")

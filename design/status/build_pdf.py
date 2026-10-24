# Projektstatus-PDF (Inhalt Stand 22.10.2026; Design seit 24.10.2026 wie die Hauptseite: Nachtschwarz, Creme, Sand). Logos aus dem Repo bpb (public/<bereich>/logo.svg, Pfad /home/claude/bpb).
# Aufruf: python3 build_pdf.py (Ausgabe BPB-Projektstatus-<Datum>.pdf im Arbeitsordner). Inhalt/Stand im Text unten anpassen.
import base64,sys
from playwright.sync_api import sync_playwright
CSS="""
@page { size: A4; margin: 14mm 0 20mm 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Inter', 'DejaVu Sans', Arial, sans-serif; color: #0b0b0f; font-size: 10pt; line-height: 1.45; margin: 0; }
a { color: #8a7448; text-decoration: none; }
.cover { background: #0b0b0f; color: #f4f1ea; padding: 29mm 16mm 12mm; margin: -14mm 0 7mm; position: relative; overflow: hidden; }
.cover .sun { position: absolute; right: -14mm; bottom: -22mm; width: 70mm; height: 70mm; border-radius: 50%; background: #cdb98f; opacity: .9; }
.cover .sun2 { position: absolute; right: 22mm; bottom: -22mm; width: 38mm; height: 38mm; border-radius: 50%; background: #cdb98f; opacity: .35; }
.cover small { letter-spacing: .14em; text-transform: uppercase; font-size: 8pt; opacity: .85; }
.cover h1 { font-size: 25pt; line-height: 1.1; margin: 3mm 0 2mm; font-weight: 800; position: relative; }
.cover p { margin: 0; font-size: 10.5pt; opacity: .95; position: relative; max-width: 128mm; }
.wrap { padding: 0 16mm; }
h2 { font-size: 14.5pt; margin: 8mm 0 2.5mm; padding-bottom: 1.5mm; border-bottom: 2.5px solid #cdb98f; break-after: avoid; }
h2 .n { color: #a8915a; margin-right: 2mm; }
h3 { font-size: 10.8pt; margin: 4.5mm 0 1.5mm; color: #5c5546; break-after: avoid; }
p { margin: 0 0 2.2mm; }
ul { margin: 0 0 2.5mm; padding-left: 5mm; }
li { margin-bottom: 1mm; }
.lead { font-size: 10.5pt; }
.box { background: #f4f1ea; border: 1px solid #e3dccb; border-left: 4px solid #a8915a; border-radius: 3mm; padding: 3.5mm 4.5mm; margin: 0 0 3mm; break-inside: avoid; }
.box.warn { border-left-color: #cdb98f; background: #f7f1e3; border-color: #e3dccb; }
.box ul { margin-bottom: 0; }
.box p:last-child { margin-bottom: 0; }
table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 3.5mm; font-size: 9.2pt; }
th { text-align: left; background: #0b0b0f; color: #fff; padding: 1.8mm 2.5mm; font-weight: 600; font-size: 8.6pt; }
td { padding: 1.8mm 2.5mm; border-bottom: 1px solid #e3dccb; vertical-align: top; }
tr { break-inside: avoid; }
tbody tr:nth-child(even) td { background: #faf8f3; }
td.k { font-weight: 700; white-space: nowrap; }
.pill { display: inline-block; font-size: 7.6pt; font-weight: 700; padding: .3mm 2mm; border-radius: 10mm; white-space: nowrap; }
.p-live { background: #d9f4e3; color: #14683a; }
.p-prev { background: #ece6d6; color: #5c5546; }
.p-plan { background: #ececf1; color: #555069; }
.p-open { background: #ffe3ec; color: #b3265a; }
.p-done { background: #d9f4e3; color: #14683a; }
.p-wait { background: #fff0d1; color: #8a5a00; }
.grp { background: #efe9da !important; font-weight: 700; color: #5c5546; font-size: 8.8pt; }
.small { font-size: 8.4pt; color: #6b6b76; }
.kpis { display: flex; gap: 3mm; margin: 0 0 3.5mm; }
.kpi { flex: 1; background: #fff; border: 1px solid #e3dccb; border-radius: 3mm; padding: 3mm; text-align: center; break-inside: avoid; }
.kpi b { display: block; font-size: 17pt; color: #a8915a; line-height: 1.1; }
.kpi span { font-size: 8pt; color: #6b6b76; }
.q { counter-reset: q; }
.q tr td:first-child { width: 8mm; font-weight: 800; color: #a8915a; }
.logos { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3.5mm; margin: 2mm 0 3mm; }
.lg { border: 1px solid #e3dccb; border-radius: 3mm; padding: 2.5mm; break-inside: avoid; }
.lg h4 { margin: 0 0 1mm; font-size: 9.6pt; } .lg h4 span { color: #a8915a; }
.lg .row { display: flex; gap: 2mm; }
.lg .a, .lg .b { flex: 1; border-radius: 2mm; display: flex; align-items: center; justify-content: center; padding: 1.5mm; height: 17mm; }
.lg .a { background: #fff; border: 1px solid #e3dccb; } .lg .b { background: #0b0b0f; }
.lg svg { max-width: 100%; max-height: 100%; width: 14mm; height: 14mm; }
.lg.wm svg { width: 30mm; }
.lg p { font-size: 7.8pt; color: #6b6b76; margin: 1.5mm 0 0; line-height: 1.35; }
.form td { height: 9mm; }
.opt { white-space: nowrap; display: inline-block; margin-right: 2mm; }
.chk { display: inline-block; width: 3.2mm; height: 3.2mm; border: 1.3px solid #0b0b0f; border-radius: .6mm; margin-right: 1.3mm; vertical-align: -.5mm; }
.line { border-bottom: 1px solid #cfc8b6; height: 7mm; margin-bottom: 1mm; }
.pb { break-before: page; }
.foot-note { font-size: 8pt; color: #6b6b76; margin-top: 3mm; }
"""+"""
.lg2{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:2mm 0 3mm}.lg2 div{border:1px solid #e3dccb;border-radius:3mm;padding:2mm;text-align:center;font-size:8pt;color:#6b6b76;break-inside:avoid}.lg2 img{width:100%;border-radius:2mm;display:block;margin-bottom:1.5mm}.lg2 b{display:block;color:#0b0b0f;font-size:9pt}
"""
def img(n):
    d=base64.b64encode(open(f"/home/claude/bpb/public/{n}/logo.svg","rb").read()).decode()
    return f"data:image/svg+xml;base64,{d}"
M=[("bytes","BPBytes","BierbaumPerformanceBytes"),("bauhof","BPBauhof","BierbaumPerformanceBauhof"),("brain","BPBrain","BierbaumPerformanceBrain"),("bolide","BPBolide","BierbaumPerformanceBolide")]
logos='<div class="lg2">'+"".join(f'<div><img src="{img(n)}"><b>{k}</b>{l}</div>' for n,k,l in M)+'</div>'
STAND="22.10.2026"
HTML=f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Projektstatus BierbaumPerformanceBrothers</title><style>{CSS}</style></head><body>
<div class="cover"><div class="sun"></div><div class="sun2"></div><small>Projektstatus · Stand {STAND}</small><h1>BierbaumPerformance&shy;Brothers</h1><p>Wo wir stehen, was zuletzt passiert ist und was als Nächstes kommt. Zur Information für die Familie.</p></div>
<div class="wrap">
<h2><span class="n">1</span>Auf einen Blick</h2>
<div class="kpis"><div class="kpi"><b>4</b><span>Apps laufen</span></div><div class="kpi"><b>4</b><span>Bereiche mit eigener Seite im Entwurf</span></div><div class="kpi"><b>0</b><span>offene Feedback-Meldungen</span></div><div class="kpi"><b>10,49 $</b><span>Kosten bisher (Domain, pro Jahr)</span></div></div>
<ul>
<li><b>Die Firma:</b> BierbaumPerformanceBrothers (Kürzel BPB), ein Familienbetrieb. Geplant als Kleinunternehmer, das Gewerbe ist noch nicht angemeldet.</li>
<li><b>Die Marken sind festgelegt:</b> BPBytes, BPBauhof, BPBrain und BPBolide (siehe Abschnitt 2).</li>
<li><b>Die Apps:</b> Craftsman (Handwerker), Abkassiert (Feste und Vereine), Zuhause (Familie) und die Markt-und-Trend-Analyse laufen. Craftsman, Abkassiert und Zuhause sind auf die eigene Adresse umgezogen.</li>
<li><b>Die Webseite:</b> Sie ist online, aber noch hinter einem Passwort. Die Startseite ist neu gestaltet (schlicht und dunkel), die vier Bereichsseiten stehen als Entwurf mit Platzhaltertexten.</li>
<li><b>Gerade offen:</b> Farbwelt und Aufbau der Bereichsseiten, echte Texte und Fotos, Impressum und Datenschutz ausfüllen, Gewerbeanmeldung.</li></ul>
<div class="box warn"><b>Wichtig zu wissen</b><ul>
<li>Noch nichts ist öffentlich beworben: Die Seiten sind für Suchmaschinen gesperrt, es gibt keine echten Kunden und keine echte Bezahlung in den Apps.</li>
<li>Vor dem ersten echten Verkauf braucht es Gewerbeanmeldung, ausgefülltes Impressum und Datenschutz, geprüfte AGB und Auftragsverarbeitung (die Entwürfe liegen vor, anwaltliche Prüfung steht aus) und die Prüfung des Namens auf Markenrechte.</li>
<li>Alle Namen außer dem Firmennamen BierbaumPerformanceBrothers sind weiter änderbar; die vier Bereichsnamen sind aber bewusst entschieden.</li></ul></div>

<h2><span class="n">2</span>Das Gesamtkonzept</h2>
<p class="lead"><b>Ein Dach, vier Bereiche.</b> Unter BierbaumPerformanceBrothers stehen verschiedene Angebote, die eigenständig auftreten können und sichtbar zusammengehören. Die Abkürzung BPB bleibt, das dritte B steht je Bereich für ein B-Wort.</p>
{logos}
<table><thead><tr><th style="width:21%">Marke</th><th style="width:26%">Langform</th><th>Was ist das</th><th style="width:18%">Stand</th></tr></thead><tbody>
<tr><td class="k">BPBytes</td><td>BierbaumPerformanceBytes</td><td>Software und Apps für Vereine, Handwerksbetriebe und kleine Firmen. Die Apps Craftsman und Abkassiert sind die Produkte, mit Demo zum Ausprobieren.</td><td><span class="pill p-prev">Entwurf online</span></td></tr>
<tr><td class="k">BPBauhof</td><td>BierbaumPerformanceBauhof</td><td>Rund ums Haus und Grundstück, regional in Ebermannstadt und etwa 20 bis 30 km Umkreis. Keine Preise oder Stundensätze auf der Seite.</td><td><span class="pill p-open">Layout offen</span></td></tr>
<tr><td class="k">BPBrain</td><td>BierbaumPerformanceBrain</td><td>Beratung für Unternehmen und persönliche Beratung.</td><td><span class="pill p-prev">Platzhalter</span></td></tr>
<tr><td class="k">BPBolide</td><td>BierbaumPerformanceBolide</td><td>Fahrzeuge vermitteln, kaufen und verkaufen.</td><td><span class="pill p-prev">Platzhalter</span></td></tr></tbody></table>
<div class="box"><b>So wird geschrieben.</b> Die Kurzform (BPBytes …) steht für alles, was man sieht: Kopfzeile, Überschrift, Menü, Logo, Visitenkarte. Die Langform (BierbaumPerformanceBytes …) steht für Offizielles: Seitentitel, Fußzeile „eine Marke von BierbaumPerformanceBrothers“, Impressum, Rechnung, Angebot. Nie mit Leerzeichen, nie ganz in Großbuchstaben. Auf der Webseite sprechen wir von „Familie“ statt von „drei Brüdern“, damit weitere Familienmitglieder dazukommen können. Der Firmenname bleibt unverändert.</div>
<div class="box"><b>Das Logo.</b> Das Sonnenlogo vom Anfang ist das Arbeitslogo: BPB als Schrift, dahinter eine Sonne in der Farbe des Bereichs. Das Dachlogo hat den Sonnenuntergang. Das frühere Netz-Logo ist zu unruhig und liegt auf dem Stapel. Das Markenrecht (Namensschutz) ist noch nicht geprüft.</div>

<h3>Die Apps</h3>
<table><thead><tr><th style="width:19%">App</th><th>Wofür</th><th style="width:16%">Stand</th></tr></thead><tbody>
<tr><td class="k">Craftsman</td><td>Handwerker-App: Projekte, Zeiten, Material, Angebote, Rechnungen als PDF, Kalender, Arbeitszeit, in der größten Stufe auch Buchhaltung und Verträge. Eine Bestellstrecke mit AGB und Kündigung ist gebaut, aber ausgeschaltet.</td><td>Version 1.26.3<br><span class="pill p-live">läuft</span></td></tr>
<tr><td class="k">Abkassiert</td><td>Gastro- und Event-App für Feste und Vereine: Bestellung am Tisch, Bon an Küche oder Theke, Kassieren, Nachbestellen, Warnung bei langer Wartezeit. Bestellstrecke gebaut, ausgeschaltet.</td><td>Version 0.11.2<br><span class="pill p-live">läuft</span></td></tr>
<tr><td class="k">Zuhause</td><td>Private Familien- und Smart-Home-App: Dashboard, Kalender, Projekte mit Zeiten, Einkaufsliste.</td><td>Version 1.52.7<br><span class="pill p-live">läuft</span></td></tr>
<tr><td class="k">Markt-und-Trend-Analyse</td><td>Internes Werkzeug für Markt- und Trendanalyse.</td><td>Version 0.7.4<br><span class="pill p-wait">Umzug folgt</span></td></tr></tbody></table>
<h3>Gemeinsame Regeln für alle Apps</h3>
<ul><li>Der Herausgeber „BierbaumPerformanceBrothers“ ist überall sichtbar und zentral gesteuert.</li><li>Mehrere Betriebe sind strikt getrennt; Rollen vergibt der Inhaber.</li><li><b>Kein E-Mail-Versand aus den Apps.</b> Rechnungen und Angebote gehen über das Teilen-Menü, Benachrichtigungen über die Glocke.</li><li>Alle Apps bleiben reine Web-Dienste (Einschätzung zum EU Cyber Resilience Act, kein Rechtsrat).</li><li>Rechtstexte sind allgemein zur Dienstleistung formuliert und nennen keine einzelnen Apps. AGB und Auftragsverarbeitung stehen nicht dauerhaft öffentlich auf der Webseite, sondern erscheinen im Bestellvorgang.</li></ul>
<h3>Adressen</h3>
<table><thead><tr><th style="width:23%">Was</th><th>Adresse</th><th style="width:15%">Stand</th></tr></thead><tbody>
<tr><td class="k">Webseite</td><td>bierbaumperformancebrothers.com (Platzhalter mit Login; Seite dahinter im Aufbau)</td><td><span class="pill p-prev">im Aufbau</span></td></tr>
<tr><td class="k">Craftsman Demo</td><td><a href="https://craftsman.bierbaumperformancebrothers.com/?demo=chef">craftsman.…/?demo=chef</a> und <a href="https://craftsman.bierbaumperformancebrothers.com/?demo=worker">?demo=worker</a></td><td><span class="pill p-live">live</span></td></tr>
<tr><td class="k">Abkassiert Demo</td><td><a href="https://abkassiert.bierbaumperformancebrothers.com/?demo=owner">abkassiert.…/?demo=owner</a> (auch waiter, kitchen, bar)</td><td><span class="pill p-live">live</span></td></tr>
<tr><td class="k">Zuhause</td><td>zuhause.bierbaumperformancebrothers.com (privat)</td><td><span class="pill p-live">live</span></td></tr></tbody></table>

<h2><span class="n">3</span>Was zuletzt passiert ist</h2>
<table><thead><tr><th style="width:15%">Datum</th><th>Was</th></tr></thead><tbody>
<tr><td class="k">22.10.</td><td><ul style="margin:0">
<li><b>Markenfamilie festgelegt:</b> BPBytes, BPBauhof, BPBrain, BPBolide mit Langformen; Verwendung Kurz-/Langform entschieden.</li>
<li><b>Webseite:</b> Sonnenlogo zurück, BPB als Text, Startseite im schlichten dunklen Stil mit Familien-Formulierung, vier Bereichsseiten als Entwurf, Impressum und Datenschutz als Entwurf (noch hinter dem Login).</li>
<li><b>Rechtliches:</b> Bestellstrecke mit AGB, Widerruf, Datenschutz, Auftragsverarbeitung und Kündigungsseite in Craftsman und Abkassiert gebaut (ausgeschaltet), Texte danach allgemein umformuliert.</li>
<li>Abkassiert: Nachbestellen und Warnung bei langer Wartezeit. Zuhause: Schriften selbst ausgeliefert.</li></ul></td></tr>
<tr><td class="k">19.–21.10.</td><td><ul style="margin:0"><li>Zuhause auf die eigene Adresse umgezogen. Craftsman: Favoriten auf dem Server, Demo-Tarife, Arbeitszeit-Regeln, Offline-Buchen. Abkassiert: Wartezeit-Anzeige, Offline-Buchen.</li><li>Alle zehn Feedback-Meldungen bearbeitet. Webseite mit Platzhalter und Login online.</li></ul></td></tr>
<tr><td class="k">16.–18.10.</td><td>Domain gekauft, Abkassiert gebaut, Craftsman mit Tarifen, Kalender und Angeboten ausgebaut, Browser-Ansicht für die Apps.</td></tr></tbody></table>

<h2><span class="n">4</span>Als Nächstes</h2>
<table class="q"><tbody>
<tr><td>1</td><td><b>Bereichsseiten fertigstellen.</b> Farbwelt und Layout je Bereich wählen (für BPBauhof gibt es drei Layoutideen), echte Texte und Fotos einsetzen.</td></tr>
<tr><td>2</td><td><b>Rechtliches vor dem Start:</b> Gewerbeanmeldung, Impressum und Datenschutz ausfüllen und öffentlich schalten, AGB anwaltlich prüfen, Namensschutz (DPMA) prüfen. Erst danach wird die Sperre für Suchmaschinen und das Passwort entfernt.</td></tr>
<tr><td>3</td><td><b>Weitere Themen:</b> Trend-Analyse umziehen, Anfrageformular auf den Seiten, digitale Visitenkarten je Marke, Geschäftskonto, Backups klären, Bibliotheken selbst ausliefern.</td></tr>
<tr><td>4</td><td><b>Craftsman und Abkassiert:</b> echte Bezahlung der Tarife und Pakete, E-Rechnung, Buchhaltung für weitere Rechtsformen, Ausbau nach echtem Einsatz.</td></tr></tbody></table>

</div></body></html>"""
open("projektstatus.html","w").write(HTML)
footer=f"""<div style="width:100%;font-family:Inter,Arial,sans-serif;font-size:7.5pt;color:#6b6b76;padding:0 16mm;display:flex;justify-content:space-between;"><span>BierbaumPerformanceBrothers · Projektstatus · Stand {STAND}</span><span>Seite <span class="pageNumber"></span> von <span class="totalPages"></span></span></div>"""
import os
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto("file://"+os.getcwd()+"/projektstatus.html")
    pg.pdf(path="BPB-Projektstatus-2026-10-22.pdf",prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template="<div></div>",footer_template=footer);b.close()

# bpb – Dach-Seite BierbaumPerformanceBrothers

Cloudflare Worker (`worker.js`) mit statischen Dateien aus `public/`. Die Seite ist noch im Aufbau und liegt hinter einem Passwort.

- Adresse: `https://bierbaumperformancebrothers.com` (und `www.`), Vorschau `https://bpb.bpbrothers.workers.dev`
- **Zugang:** `worker.js` zeigt ohne Cookie nur den Platzhalter (`public/platzhalter/`) mit Login-Knopf; öffentlich sind nur die Pfade in `OEFFENTLICH` (Login, Platzhalter-CSS, Favicon, `logo-dach.svg`, robots). Nach dem Passwort (Hash im Code, nie das Passwort) folgt die Seite im Aufbau. Alles `noindex`, bis die Seite öffentlich geht.
- Seiten: `public/index.html` (Startseite), `public/digital/` (Auftritt Digital, Entwurf C), `public/impressum/` und `public/datenschutz/` (Entwürfe, allgemein formuliert, Klammern orange; Quelle sind die Entwürfe im Projekt), `public/platzhalter/`.
- **AGB und AVV stehen bewusst nicht auf der Seite**; sie kommen erst im Bestellvorgang (Link + Checkbox).
- Keine externen Schriften, Skripte oder Tracker (kein Cookie-Banner nötig); CSP in `worker.js` und `public/_headers`.
- Deploy: Workers Builds aus diesem Repo (Branch `main`), Konfiguration in `wrangler.toml`.
- Später: Verzeichnis-Seite aus `portfolio.json`, siehe `claude/KONZEPT-BPB.md` Abschnitt 4a. Vor der Veröffentlichung: Impressum/Datenschutz füllen und in `OEFFENTLICH` aufnehmen, Login und `noindex` entfernen.
- **Marke (22.10.):** BPB steht als Text im Header, Untermarken in Akzentfarbe ohne Leerzeichen („BPB**Digital**“). Das **Sonnenlogo** (SVG, Archivo Black + Manrope) steht nur dort, wo es hingehört: `public/logo-dach.svg` (Platzhalter, Login; Sonnenuntergang), `public/digital/logo.svg` (Hero von Digital; Nacht/Rosa), `public/favicon.svg` (Sonne mit BPB). Das frühere Netz-Logo (inkl. atmender Fassung) liegt auf dem Stapel und ist hier entfernt (Git-Stand `2c233aa`). Generatoren im Projekt unter `code/bpb-logos/` (`runde35.py`), Entscheidung in `claude/LOGO-RICHTUNG.md`.

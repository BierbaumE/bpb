# bpb – Dach-Seite BierbaumPerformanceBrothers

Statische Seite als Cloudflare Worker (nur Dateien, kein Skript).

- Adresse: `https://bierbaumperformancebrothers.com` (und `www.`), Vorschau `https://bpb.bpbrothers.workers.dev`
- Dateien: `public/index.html`, `public/styles.css`, `public/favicon.svg`, `public/robots.txt`, `public/_headers`
- Stand: erste Platzhalterseite „Hier entsteht die Seite …“, bewusst `noindex` (robots.txt, Meta, Header), bis Impressum und Datenschutz stehen.
- Keine externen Schriften, Skripte oder Tracker (kein Cookie-Banner nötig); CSP in `public/_headers`.
- Deploy: Workers Builds aus diesem Repo (Branch `main`), Konfiguration in `wrangler.toml`.
- Später: Verzeichnis-Seite aus `portfolio.json`, siehe `claude/KONZEPT-BPB.md` Abschnitt 4a.
- Logo (22.10.): Arbeitslogo Quadrat/Bungee mit Gravitationsnetz als SVG: `public/logo-dach.svg` (Platzhalter, Login, Startseite; Violett/Pink), `public/digital/logo.svg` (Seite Digital; Digital Nacht), `public/favicon.svg` (flache Kleinform). Atmende Fassungen (SMIL, ca. 40 KB; Netz atmet in 7 s, BPB schwebt 2,5 px) `public/logo-dach-atmend.svg` und `public/digital/logo-atmend.svg` auf Platzhalter, Login und Digital-Hero; bei „Bewegung reduzieren“ greift per `<picture>` die ruhige Fassung. Generatoren im Projekt unter `code/bpb-logos/`, Entscheidung in `claude/LOGO-RICHTUNG.md`.

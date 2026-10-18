# bpb – Dach-Seite BierbaumPerformanceBrothers

Statische Seite als Cloudflare Worker (nur Dateien, kein Skript).

- Adresse: `https://bierbaumperformancebrothers.com` (und `www.`), Vorschau `https://bpb.bpbrothers.workers.dev`
- Dateien: `public/index.html`, `public/styles.css`, `public/favicon.svg`, `public/robots.txt`, `public/_headers`
- Stand: erste Platzhalterseite „Hier entsteht die Seite …“, bewusst `noindex` (robots.txt, Meta, Header), bis Impressum und Datenschutz stehen.
- Keine externen Schriften, Skripte oder Tracker (kein Cookie-Banner nötig); CSP in `public/_headers`.
- Deploy: Workers Builds aus diesem Repo (Branch `main`), Konfiguration in `wrangler.toml`.
- Später: Verzeichnis-Seite aus `portfolio.json`, siehe `claude/KONZEPT-BPB.md` Abschnitt 4a.

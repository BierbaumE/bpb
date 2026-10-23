# design/ – Quellen für Logo und Projektstatus (wird nicht ausgeliefert)

Am 23.10.2026 aus dem claude.ai-Projekt „App+HP Entwicklung“ (`code/bpb-logos/`, `code/bpb-status/`, `code/bpb-entwuerfe/`) hierher übernommen. Ausgeliefert wird nur `public/` (siehe `wrangler.toml`, `[assets] directory`).
Verworfene Logo-Runden (0–3, 5–9, 12), `logos_gen.py` und die sechs alten Webseiten-Entwürfe (`digital-A/B/C`, `haus-A/B/C`, noch mit den Arbeitsnamen) wurden danach gelöscht (Eike, 23.10.); sie stehen in der Git-Historie (Commit `8cf7678`).

## logos/
| Datei | Stand |
|---|---|
| `runde35.py` | **Sonnenlogo** (aktuelles Arbeitslogo): BPB auf Sonne, fünf Farbdarstellungen |
| `runde38.py` | **Sonnenlogo je Bereich** (sieben Farbdarstellungen inkl. Brain „Tiefsee“ und Bolide „Graphit“, ohne Namenszeile) – Quelle der `public/<bereich>/logo.svg` (Docstring nennt noch „Runde 35“) |
| `runde16.py`–`runde34.py` | **Netz-Logo („Gravitationsnetz“), auf dem Stapel** (Eike, 22.10.: „zu unruhig“): Farbrollen, Schriftvergleich, Bungee-Quadrat, Paletten, Namenszeilen, atmende Fassung (32) |
| `runde4.py`, `runde10.py`, `runde11.py`, `runde13.py`–`runde15.py` | Bausteine des Netz-Logos (Textumrisse, Paletten, Formen) – die späteren Runden laden sie per `exec` |
| `VERLAUF.md` | Verlauf und Eikes Vorgaben der frühen Runden (vorher `claude/LOGO-VORSCHLAEGE.md` im Projekt) |

Aufruf: Dateien als `rundeN_gen.py` nebeneinander ablegen (die Skripte laden ihre Vorgänger unter diesem Namen), dann `python3 -I rundeN_gen.py <ofl-Ordner> <Ausgabe> <gf-ofl-Ordner>`. Schriften: Google Fonts per Git-Sparse-Clone (`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts`, dann `git sparse-checkout add ofl/<name>`). Text liegt als Umriss in den SVGs. Aktuelle Richtung und Regeln: `claude/LOGO-RICHTUNG.md` im Projekt.

## status/
`build_pdf.py` erzeugt das Projektstatus-PDF für die Familie (Inhalt und Stand im Skript; liest die Bereichslogos aus `public/<bereich>/logo.svg`; Playwright/Chromium, Schrift Inter). Nur auf Eikes Wunsch neu erzeugen (Regel: `claude/PROJEKTSTATUS.md` im Projekt).

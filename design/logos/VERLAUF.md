# BPB-Logo – Vorschläge und Stand (#21, zu #16 Dachdesign)

**Stand 22.10.2026, 00:28 · offen:** Eike ist noch von keinem Vorschlag überzeugt („definitiv noch nichts dabei, was für ein finales Logo reicht“). Die Entwürfe bleiben als Vorschläge liegen.

**Alle Entwürfe ansehen:** Design-Fläche „BPB Logo – sportliche Varianten“ (Artifact, privat) mit drei Seiten: Runde 1, Runde 2 und Runde 3 – neu gedacht.
https://claude.ai/artifact/TUUdWZ6WFAKYCxmgwkCaeC

## Was Eike bisher gesagt hat (Richtschnur für den nächsten Anlauf)
- Name immer **BierbaumPerformanceBrothers**, zusammengeschrieben; Kürzel **BPB**. Alle Namen sind Arbeitstitel.
- **Immer BPB zusammen**, auch in kleinen Größen. **Kein einzelnes P** als Zeichen.
- Gewünscht: **Lettermark + Emblem** als System. Der Lettermark ist der Kern, das Emblem mit Namen kommt dazu, wo Platz ist.
- Gefällt: **organische Formen** und **Emblem-Charakter**, also Hersteller- oder Retro-Abzeichen statt Schrift. Der Stil seines Recraft-Entwurfs (Emblem mit Flügel-Wirkung) gefiel.
- Gefällt: die **Plakette mit dem Namen darunter** (Runde 1, Entwurf 5), dazu Entwurf 3 „Flügel“.
- Gefällt nicht: **Tempo- und Geschwindigkeitsstreifen**. Ein **gespiegeltes B** soll wieder richtig herum stehen. Das **P in der Mitte** war zu dominant.
- Runde 2 (geometrisch neu gebaut) war „ziemlich uncool“. Die sechs ersten Vorschläge vom 19.10. waren „gruselig“.
- Ausdrücklich: **frei denken**, nicht an alten Ideen kleben (Sonne, Verlauf usw.). Es muss „wirklich sexy, ansprechend“ sein.
- Vorbilder bisher: nur eine allgemeine Übersicht der Logo-Arten (adidas, Lamborghini, CNN, KFC, Disney, Apple, Burger King). Gewählt hat er daraus die Richtung „Lettermark + Emblem“.

## Verlauf
- **Bisheriges Logo:** die Darstellung des Betriebs in Craftsman, ein „BPB“ mit Verlauf violett → pink → orange und gelber Sonne. Der Schriftzug im Bild hat noch Leerzeichen und Großbuchstaben; eine Vektorversion fehlt.
- **19.10., Runde 0:** Eike will ein schlichtes, prägnantes **Herstellerlogo** wie Puma, Jeep oder Amazon, das unter allen Marken stehen kann.
  - Sechs eigene Entwürfe: 1 Aufgang (drei Halbsonnen), 2 Aufstieg (drei Balken), 3 Dreifach-B (B mit drei Bäuchen), 4 Siegel (Sonne + BPB im Kreis), 5 Wortmarke (BPB, Bauch des P = Sonne), 6 Gipfel (drei Spitzen + Sonne).
  - Erzeugt mit `code/bpb-logos/logos.py` (je Logo SVG hell, dunkel, einfarbig).
  - Das Verteil-PDF `BPB-Logo-und-Webauftritt-Feedback.pdf` (17 Seiten mit Fragebogen) ging im Chat an Eike. Rückmeldungen aus seinem Umfeld stehen noch aus.
  - Eike, 19.10., 12:37: „gruselig“, „taugt mir noch nicht so recht“ → neuer Anlauf als #21.
- **21.10.:** Eikes Recraft-Entwurf geprüft (Rakete/Emblem, BPB mit gespiegeltem linken B, Sonne im P, Balken, Linie mit V, Welle). Erkenntnisse:
  - Das gespiegelte B liest sich leicht als „8PB“.
  - Linie und Welle verschwinden bei 32 px.
  - **Recraft Free-Plan:** Bilder bleiben Eigentum von Recraft, keine kommerzielle Nutzung, öffentlich in der Galerie. Nutzungsrechte gibt es nur für Bilder aus einem bezahlten Tarif. In welchem Tarif der Entwurf entstand, ist noch ungeklärt.
- **Runde 1 (21.10.):** sieben sportliche Abwandlungen der Recraft-Vorlage (Kursiv, Tempo, Flügel, Retro-Sonne, Plakette, Zeichen, Quer).
  - Gefallen haben 3 und 5. Tempostreifen nicht.
- **Runde 2 (22.10.):** Kombination aus Flügel und Plakette, geometrisch neu gebaut, beide B normal, P kleiner. Fünf Formen (A Schild, B schräg, C Wappen, D P mit Spitze, E frei) plus App-Symbol, jeweils in sechs Farbwelten (Sonnenuntergang, Wald, Ozean, Rennrot, Grün-Gold wie BPF-Wappen, einfarbig). Erkenntnisse:
  - Ein mittig spitz zulaufendes P liest sich als V, das ergibt „BVB“ (Borussia Dortmund). Das gilt es zu vermeiden.
  - Ein Neubau aus geraden Grundformen verliert den Charakter.
- **Runde 3 – neu gedacht (22.10.):** sechs freie Richtungen, je Lettermark + Emblem, mit Visitenkarte, App-Symbol und Kleinform.
  - **A Couture:** Bodoni, eng verschränkt, Champagner-Gold auf Schwarz, ovale Kartusche.
  - **B Garage:** Schreibschrift (Mr Dafoe) mit Schwung, ovale Plakette in Creme, Rot und Marine, Schrift bricht aus dem Rahmen.
  - **C Groove:** weiche fette Kursive (Fraunces Soft) mit Schatten, runder Stempel mit Wellenrand, Terrakotta/Senf/Braun.
  - **D Werkstatt:** Schablonenschrift (Big Shoulders Stencil), Blechmarke mit Nieten, Oliv/Knochenweiß/Signalorange.
  - **E Breit:** extrem breite Groteske (Syne), Kapsel, Neongelb auf Schwarz.
  - **F Neon:** Leuchtröhren-BPB (Monoton) in Pink, cyanfarbenes Leuchtschild. Kleinform mit Bungee.
  - Ergebnis: „noch nicht überzeugt“, als Vorschläge abgelegt.

## Technik (zum Weitermachen)
- Generatoren im Projekt unter `code/bpb-logos/`:
  - `rakete_varianten.py` (Runde 1, braucht `vorlage-recraft.svg`)
  - `runde2.py`
  - `konzepte_runde3.py` (Runde 3)
- Jeder Generator schreibt SVG-Dateien. Text liegt als Umriss darin, Schriftdateien braucht man zum Ansehen also nicht.
- Schriften für Runde 3: Google Fonts, Lizenz OFL (frei, auch für Logos). Beschaffung:
  1. `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts`
  2. `git sparse-checkout add ofl/<name>` mit `bodonimoda`, `mrdafoe`, `fraunces`, `bigshouldersstencildisplay`, `syne`, `monoton`, `bungee`, `cinzel`, `anton`, `shrikhand`.
  3. Variable Schriften per `fontTools.varLib.instancer` auf feste Schnitte bringen: FrauncesSoftBlackItalic (wght 900, SOFT 100, WONK 1, opsz 144), BodoniBlack (wght 900, opsz 96), CinzelBlack, SyneExtraBold, BigShouldersStencilBlack.
  - npm und raw.githubusercontent sind gesperrt. Der Git-Weg über den Proxy funktioniert.
- Die SVGs selbst liegen nicht im Projekt, sondern als Assets auf der Design-Fläche (oben verlinkt).

## Offen vor einem finalen Logo
- Richtung finden, die Eike wirklich überzeugt. Vorschlag: 3–5 konkrete Logos aus seinem Alltag sammeln, die er „sexy“ findet, je mit einem Satz warum (Form, Gefühl, Farbe). Eine allgemeine Logo-Übersicht reicht dafür nicht.
- Markenrecht vor der Festlegung prüfen: DPMA-Recherche (#6, #18). Ähnlichkeit zu bekannten Marken vermeiden, zum Beispiel BVB.
- Falls die Recraft-Vorlage selbst genutzt werden soll: Tarif und Nutzungsrechte klären.
- Danach: Schriftzug zusammengeschrieben, Vektor-Endfassungen mit und ohne Hintergrund (hell, dunkel, einfarbig, Kleinform), Farbwerte, Schrift und Abstände als Design-System für Apps und Webauftritte (#16).

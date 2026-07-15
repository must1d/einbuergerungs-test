# Einbürgerungstest Bayern — Lern-App

Werbefreie Lern-App für den Einbürgerungstest (Bayern). Eine einzige Datei
`index.html`, offline nutzbar, keine Werbung, kein Konto, kein Server.

**310 amtliche Fragen** = 300 bundesweite + 10 bayerische (Stand BAMF 07.05.2025).

## Modi
- **Üben** — nach Thema, mit sofortiger Lösung
- **Prüfung simulieren** — 33 Fragen (30 Bund + 3 Bayern), bestanden ab 17 richtig
- **Karteikarten** — Frage ansehen, Antwort aufdecken
- **Fehler wiederholen** — nur falsch beantwortete Fragen (im Gerät gespeichert)

## Auf dem iPhone nutzen
Zwei Wege:

**A. Kostenlos hosten (empfohlen, „von überall")**
1. Repo auf GitHub pushen, in *Settings → Pages* die Quelle auf `main` stellen.
2. Die URL in Safari auf dem iPhone öffnen.
3. Teilen-Symbol → **Zum Home-Bildschirm** → App-Icon erscheint.

**B. Ohne Internet (AirDrop)**
`index.html` per AirDrop aufs iPhone schicken, in „Dateien" öffnen.
Läuft komplett offline (alles ist in der Datei eingebettet, inkl. Bilder).

## Neu bauen
`index.html` wird aus den Rohdaten erzeugt:
```
python3 build.py
```
`build.py` filtert die 310 Fragen, bettet die 6 Bild-Fragen als Data-URIs ein
und schreibt `index.html`.

## Albanische Übersetzung
Alle 310 Fragen sind ins Albanische übersetzt (`translations/combined.json`,
index-basiert). Sie erscheint **nur beim Nachschauen der Lösung** — bei falsch
beantworteten Fragen im Üben-/Fehler-Modus, beim Aufdecken der Karteikarte und
in der Prüfungs-Auswertung — über den Knopf „🇦🇱 Shqip". Fehlt eine Übersetzung,
bleibt es bei Deutsch.

`combined.json` ist ein Array mit 310 Einträgen `{"sq","sqa":[4]}`, ausgerichtet
auf die Reihenfolge der gefilterten Fragen (Position = Index). `build.py` prüft
die Ausrichtung und bettet die Übersetzungen ein.

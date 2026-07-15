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

## Später: albanische Übersetzung
Vorgesehen, aber noch nicht gefüllt. Pro Frage kann ein Feld `sq` ergänzt
werden; die UI kann es beim Ergebnis-Review einblenden (Fallback: Deutsch).

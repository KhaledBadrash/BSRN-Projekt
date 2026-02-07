# BSRN Projekt – Buzzword-Bingo (Werkstück A, Alternative 3)

Dieses Projekt implementiert ein **Mehrspieler-Buzzword-Bingo** mit **Multiprocessing** (Host + Spielerprozesse) und **Interprozesskommunikation (IPC)** über **benannte Pipes (FIFOs)**.  
Ein **Host-Prozess** orchestriert das Spiel, Spieler **joinen** als eigene Prozesse. Die UI ist eine **Terminal-GUI** (PyTermTK) mit klickbaren Feldern; nach jedem Klick wird der **Bingo-Status** (horizontal/vertikal/diagonal) geprüft. Spielereignisse werden als **JSON** geloggt.

> Hinweis: Die Lösung nutzt `mkfifo` und `/tmp/...` und ist daher primär für **Linux/macOS** ausgelegt.

---

## Inhalte

- Installation
- Ausführen (Host / Spieler)
- Nutzung (GUI)
- Architektur (Host/Players/IPC)
- Logs & Daten
- Troubleshooting

---

## Installation

### Voraussetzungen
- Python 3.10+ (empfohlen)
- Abhängigkeiten gemäß `requirements.txt` (falls vorhanden)
- Linux/macOS (wegen `mkfifo` und `/tmp` FIFOs)

### Setup
```bash
# Repository klonen
git clone <REPO_URL>
cd <REPO_ORDNER>

# Optional: virtuelle Umgebung
python3 -m venv .venv
source .venv/bin/activate

# Dependencies installieren (falls requirements vorhanden)
pip install -r requirements.txt

Ausführen

Das Programm wird über eine zentrale Entry-Point Datei gestartet (multi.py).

1) Host starten
python3 multi.py host --size 5 --players 2

--size: Größe des Bingo-Grids (z. B. 5x5)
--players: Anzahl erwarteter Spielerprozesse

2) Spieler beitreten lassen (in separaten Terminals)
python3 multi.py join --player-id 1
python3 multi.py join --player-id 2

Ablauf (Handshake)
1. Spieler verbinden sich über FIFOs und senden READY
2. Host wartet, bis alle Spieler bereit sind
3. Host sendet START (inkl. Spielfeld-Dimensionen)
4. Spieler starten die GUI

Nutzung (GUI)

Das Bingo-Board wird als Grid mit klickbaren Buttons angezeigt.

Klick auf ein Feld toggelt die Markierung.

Nach jedem Klick erfolgt die Bingo-Prüfung:

Zeile / Spalte / Diagonale vollständig markiert → Bingo

Bei Bingo wird ein Gewinnerdialog angezeigt bzw. das Spiel beendet (je nach Implementierung).

Architektur (technischer Überblick)
Prozesse

Host-Prozess

Initialisierung

Erzeugen/Verwalten der Named Pipes

Synchronisation (READY/START)

ggf. Auswertung und Spielende

Spieler-Prozesse

Join / Verbindungsaufbau

GUI-Loop

Senden von Aktionen/Events an den Host

IPC über Named Pipes (FIFOs)

Pipes werden unter /tmp erstellt, z. B.:

/tmp/host_to_players

/tmp/players_to_host

Lifecycle:

setup_pipes: Erstellung (mkfifo)

cleanup_pipes: Entfernen am Ende

Logs & Daten

Aktionen (z. B. Klick, Position, Buzzword, Timestamp) werden in JSON persistiert.

Das Log wird vor einem neuen Spiel i. d. R. geleert bzw. neu angelegt.

Troubleshooting
„Broken pipe“, „No such file or directory“

Host muss laufen, bevor Spieler joinen (oder Pipes müssen existieren).

Prüfe, ob die FIFOs in /tmp erzeugt wurden.

Ports/Netzwerk

Es wird kein Netzwerk benötigt; Kommunikation läuft lokal über FIFOs.

# Windows

Native FIFOs via /tmp + mkfifo sind Windows-untypisch.
Empfohlen: Ausführen in WSL oder Linux/macOS.

# Git Hygiene

Empfohlene .gitignore Einträge:
__pycache__/
*.py[cod]
.venv/
venv/
.DS_Store
Thumbs.db
*.log

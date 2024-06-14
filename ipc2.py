import os  # Importiert das os-Modul für Betriebssystemfunktionen
import datetime  # Importiert das datetime-Modul für Datums- und Zeitfunktionen
import random  # Importiert das random-Modul für Zufallsoperationen
import sys
#s

class log:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.date = self.now.strftime("%d/%m/%Y %H:%M:%S")

    def logeintrag(self, eintrag):
        self.now = datetime.datetime.now()
        self.date = self.now.strftime("%d/%m/%Y %H:%M:%S")
        with open('Protokoll', 'a') as file:
            file.write(f"{self.date} {eintrag}\n")

    def logeintragstep(self):
        self.logeintrag('Step')

    def logeintragstart(self):
        self.logeintrag('Start')


# Klasse für Interprozesskommunikation und Spiel-Logik
class BingoSpiel:
    def __init__(self, wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe):
        self.wortdatei = wortdatei  # Initialisiert den Pfad zur Wortdatei
        self.xachse = xachse  # Initialisiert die Anzahl der Felder in der Breite
        self.yachse = yachse  # Initialisiert die Anzahl der Felder in der Höhe
        self.spieler_name = spieler_name  # Initialisiert den Namen des Spielers
        self.spielbrett = []  # Initialisiert das Spielfeld als leere Liste
        self.empf_pipe = empf_pipe  # Initialisiert das Leseende/ Empfänger der Pipe
        self.sender_pipe = sender_pipe  # Initialisiert das Schreibende der Pipe
        self.logger = log()  # Initialisiert das Log

    # Lädt die Wörter aus der Datei und generiert die Bingokarte
    def lade_woerter(self):
        with open(self.wortdatei, 'r') as file:  # Öffnet die Wortdatei im Lesemodus
            woerter = [line.strip() for line in
                       file.readlines()]  # Liest alle Zeilen aus der Datei und entfernt Leerzeichen
        random.shuffle(woerter)  # Mische die Wörter zufällig
        self.spielbrett = [woerter[i:i + self.xachse] for i in
                           range(0, len(woerter), self.xachse)]  # Erstellt das Spielfeld als Liste von Listen

    # Startet das Spiel
    def starte_spiel(self):
        self.lade_woerter()  # Lädt die Wörter und generiert die Bingokarte
        self.logger.logeintrag("Start des Spiels")
        self.logger.logeintrag(f"Größe des Spielfelds: ({self.xachse}/{self.yachse})")
        print(
            f"Spieler {self.spieler_name} hat das Spiel gestartet.")  # Gibt eine Meldung aus, dass das Spiel gestartet wurde

    # Markiert ein Feld auf der Bingokarte
    def markiere_feld(self, x, y):
        if 0 <= x < self.xachse and 0 <= y < self.yachse:  # Überprüft, ob die Koordinaten innerhalb des Spielfelds liegen
            wort = self.spielbrett[y][x]  # Holt das Wort an den angegebenen Koordinaten
            self.spielbrett[y][x] = 'X'  # Markiert das Feld als 'X'
            self.logger.logeintrag(f"{wort} ({x}/{y})")
            return True  # Gibt True zurück, um anzuzeigen, dass das Feld erfolgreich markiert wurde
        return False  # Gibt False zurück, wenn die Koordinaten ungültig sind

    # Überprüft, ob ein Bingo erzielt wurde
    def ueberpruefe_bingo(self):
        # Überprüft Reihen, Spalten und Diagonalen
        for reihe in self.spielbrett:  # Iteriert über jede Reihe des Spielfelds
            if all(zelle == 'X' for zelle in reihe):  # Überprüft, ob alle Zellen in der Reihe markiert sind
                return True  # Gibt True zurück, wenn eine komplette Reihe markiert ist
        for spalte in range(self.xachse):  # Iteriert über jede Spalte des Spielfelds
            if all(self.spielbrett[reihe][spalte] == 'X' for reihe in
                   range(self.yachse)):  # Überprüft, ob alle Zellen in der Spalte markiert sind
                return True  # Gibt True zurück, wenn eine komplette Spalte markiert ist
        if all(self.spielbrett[i][i] == 'X' for i in range(self.xachse)):  # Überprüft die Hauptdiagonale
            return True  # Gibt True zurück, wenn die Hauptdiagonale markiert ist
        if all(self.spielbrett[i][self.xachse - i - 1] == 'X' for i in
               range(self.xachse)):  # Überprüft die Nebendiagonale
            return True  # Gibt True zurück, wenn die Nebendiagonale markiert ist
        return False  # Gibt False zurück, wenn kein Bingo erzielt wurde

    # Beendet das Spiel und schreibt das Ende ins Log
    def beende_spiel(self, ergebnis):
        self.logger.logeintrag(f"{ergebnis}")
        self.logger.logeintrag("Ende des Spiels")

    # Startet die Interprozesskommunikation
    def starte_ipc(self):
        with open(self.empf_pipe, 'r') as pipe:
            while True:  # Endlosschleife, um kontinuierlich Nachrichten zu lesen
                nachricht = pipe.readline().strip()  # Liest eine Nachricht von der Pipe und dekodiert sie
                if nachricht:  # Überprüft, ob eine Nachricht empfangen wurde
                    x, y = map(int, nachricht.split(','))  # Zerlegt die Nachricht in x- und y-Koordinaten
                    if self.markiere_feld(x, y):  # Markiert das Feld mit den angegebenen Koordinaten
                        if self.ueberpruefe_bingo():  # Überprüft, ob ein Bingo erzielt wurde
                            print(f"{self.spieler_name} hat Bingo!")  # Gibt eine Meldung aus, dass Bingo erzielt wurde
                            self.beende_spiel("Gewonnen")
                            break  # Bricht die Schleife ab


def fork_prozess(wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe):
    pid = os.fork()
    if pid == 0:  # Kindprozess
        spiel = BingoSpiel(wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe)
        spiel.starte_spiel()
        spiel.starte_ipc()
        sys.exit(0)  # Beendet den Kindprozess nach dem Spiel
    else:  # Elternprozess
        return pid


if __name__ == "__main__":
    # Interaktiv nach den notwendigen Parametern fragen in Ubuntu
    wortdatei = input("Pfad zur Wortdatei: (z.B. Textdatei) ")  # Fragt den Pfad zur txt.datei ab

    print("Willkommen im Buzzword-Bingospiel.")
    # Abfrage
    variable = input("Neue Runde? \n [Y/N]: ")
    if variable == "Y" or variable == "y":
        xachse = int(input("Anzahl der Felder in der Breite: "))  # Fragt die Anzahl der Felder in der Breite ab
        yachse = int(input("Anzahl der Felder in der Höhe: "))  # Fragt die Anzahl der Felder in der Höhe ab
        spieler_name = input("Name des Spielers: ")  # Fragt den Namen des Spielers ab
    elif variable == "N" or variable == "n":  # elif else if
        print("Das Spiel ist beendet")
        exit()

    # Erstelle die Named Pipes
    empf_pipe = "/tmp/empf_pipe"
    sender_pipe = "/tmp/sender_pipe"

    # Erstelle die Named Pipes, falls sie nicht existieren
    if not os.path.exists(empf_pipe):
        os.mkfifo(empf_pipe)
    if not os.path.exists(sender_pipe):
        os.mkfifo(sender_pipe)

    # Initialisiert und startet den Kindprozess für das Spiel
    fork_prozess(wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe)

    with open(sender_pipe, 'w') as pipe:
        while True:
            koords = input("Geben Sie die Koordinaten zum Markieren ein (Format: x,y): ")
            if koords.lower() == "exit":
                print("Das Spiel wird beendet.")
                break
            pipe.write(f"{koords}\n")
            pipe.flush()

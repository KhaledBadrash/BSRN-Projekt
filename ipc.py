import os  # Importiert das os-Modul für Betriebssystemfunktionen-k
import Log
import datetime  # Importiert das datetime-Modul für Datums- und Zeitfunktionen
import random  #Importiert das random-Modul für Zufallsoperationen
import datetime  # Importiert das datetime-Modul für Datums- und Zeitfunktionen (Log-Datei in ipc datei implementiert)


class log: #gut diese
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


# x y achse gleich
# Klasse für Interprozesskommunikation und Spiel-Logik
class BingoSpiel:  #k
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
    def lade_woerter(self):  #k
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
            self.logger.logeintrag({self.spieler_name})
    # Markiert ein Feld auf der Bingokarte
    def markiere_feld(self, x, y):  #TBD pipe problem sender und empfänger pipe muss noch hinzugefügt werden-k
        if 0 <= x < self.xachse and 0 <= y < self.yachse:  # Überprüft, ob die Koordinaten innerhalb des Spielfelds liegen
            wort = self.spielbrett[y][x]  # Holt das Wort an den angegebenen Koordinaten
            self.spielbrett[y][x] = 'X'  # Markiert das Feld als 'X'
            self.logger.logeintrag(f"{wort} ({x}/{y})")
            return True  # Gibt True zurück, um anzuzeigen, dass das Feld erfolgreich markiert wurde
        return False  # Gibt False zurück, wenn die Koordinaten ungültig sind

    # Überprüft, ob ein Bingo erzielt wurde
    def ueberpruefe_bingo(self): #zweidimensionales array
        return False

    def beende_spiel(self, ergebnis):
        self.logger.logeintrag(f"{ergebnis}")
        self.logger.logeintrag(f"Ende des Spiels")

    # Startet die Interprozesskommunikation
    def starte_ipc(self):  #tbd
        while True:  # Endlosschleife, um kontinuierlich Nachrichten zu lesen
            nachricht = os.read(self.empf_pipe, 1024).decode()  # Liest eine Nachricht von der Pipe und dekodiert sie
            if nachricht:  # Überprüft, ob eine Nachricht empfangen wurde
                x, y = map(int, nachricht.split(','))  # Zerlegt die Nachricht in x- und y-Koordinaten
                if self.markiere_feld(x, y):  # Markiert das Feld mit den angegebenen Koordinaten
                    if self.ueberpruefe_bingo():  # Überprüft, ob ein Bingo erzielt wurde
                        print(f"{self.spieler_name} hat Bingo!")  # Gibt eine Meldung aus, dass Bingo erzielt wurde
                        self.beende_spiel()  # Beendet das Spiel
                        break  # Bricht die Schleife ab


if __name__ == "__main__":
    import argparse  # Importiert das argparse-Modul zum Parsen von Kommandozeilenargumenten

    # Parser für Kommandozeilenargumente -------> TBD bis z.82
    parser = argparse.ArgumentParser(description="Buzzword-Bingo-Spiel")
    parser.add_argument("-pipe", type=str, required=False, help="Name der benannten Pipe")
    args = parser.parse_args()  # Parst die Kommandozeilenargumente

    # Interaktiv nach den notwendigen Parametern fragen in Ubuntu

    wortdatei = input("Pfad zur Wortdatei: (z.B.Textdatei) ")  # Fragt den Pfad zur txt.datei ab k

    print("Willkommen im Buzzword-Bingospiel.")
    #Abfrage
    variable = input("Neue Runde? \n [Y/N]: ")
    if variable == "Y" or variable == "y":
        # x und y achse TBD
        xachse = int(input("Anzahl der Felder in der Breite: "))  # Fragt die Anzahl der Felder in der Breite ab
        yachse = int(input("Anzahl der Felder in der Höhe: "))  # Fragt die Anzahl der Felder in der Höhe ab
        spieler_name = input("Name des Spielers: ")  # Fragt den Namen des Spielers ab --- PID TBD
    elif variable == "N" or variable == "n":  # elif else if
        print("Das Spiel ist beendet")

    # Erstelle die Pipe
    empf_pipe, sender_pipe = os.pipe()  # Erstellt ein anonymes Pipe-Paar für die Kommunikation #k

    # Initialisiert das Spiel und startet die IPC
    spiel = BingoSpiel(wortdatei, xachse, yachse, spieler_name, empf_pipe,
                       sender_pipe)  # Initialisiert ein neues BingoSpiel-Objekt
    spiel.starte_spiel()  # Startet das Spiel
    spiel.starte_ipc()  # Startet die Interprozesskommunikation



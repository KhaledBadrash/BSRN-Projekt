import os  # Importiert das os-Modul für Betriebssystemfunktionen-k
import Log
import datetime  # Importiert das datetime-Modul für Datums- und Zeitfunktionen
import random  #Importiert das random-Modul für Zufallsoperationen


# x y achse gleich
# Klasse für Interprozesskommunikation und Spiel-Logik
class BingoSpiel:  #k
    def __init__(self, wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe):
        self.wortdatei = wortdatei  # Initialisiert den Pfad zur Wortdatei
        self.xachse = xachse  # Initialisiert die Anzahl der Felder in der Breite
        self.yachse = yachse  # Initialisiert die Anzahl der Felder in der Höhe
        self.spieler_name = spieler_name  # Initialisiert den Namen des Spielers
        self.spielbrett = []  # Initialisiert das Spielfeld als leere Liste
        self.logdatei = f" {datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-bingo-{spieler_name}.txt"  # Erstellt den Namen der Logdatei mit Zeitstempel und Spielername
        self.empf_pipe = empf_pipe  # Initialisiert das Leseende/ Empfänger der Pipe
        self.sender_pipe = sender_pipe  # Initialisiert das Schreibende der Pipe

    # Lädt die Wörter aus der Datei und generiert die Bingokarte
    def lade_woerter(self):  #k
        with open(self.wortdatei, 'r') as file:  # Öffnet die Wortdatei im Lesemodus
            woerter = [line.strip() for line in
                       file.readlines()]  # Liest alle Zeilen aus der Datei und entfernt Leerzeichen
        random.shuffle(woerter)  # Mische die Wörter zufällig
        self.spielbrett = [woerter[i:i + self.xachse] for i in
                           range(0, len(woerter), self.xachse)]  # Erstellt das Spielfeld als Liste von Listen

    # Startet das Spiel
    def starte_spiel(self):  #m
        self.lade_woerter()  # Lädt die Wörter und generiert die Bingokarte
        with open(self.logdatei, 'a') as log:  # Öffnet die Logdatei im Anhangmodus
            log.write(f"{datetime.datetime.now()} Start des Spiels\n")  # Schreibt den Start des Spiels in die Logdatei
            log.write(
                f"{datetime.datetime.now()} Größe des Spielfelds: ({self.xachse}/{self.yachse})\n")  # Schreibt die Größe des Spielfelds in die Logdatei

        print(
            f"Spieler {self.spieler_name} hat das Spiel gestartet.")  # Gibt eine Meldung aus, dass das Spiel gestartet wurde

    # Markiert ein Feld auf der Bingokarte
    def markiere_feld(self, x, y):  #TBD pipe problem sender und empfänger pipe muss noch hinzugefügt werden-k
        if 0 <= x < self.xachse and 0 <= y < self.yachse:  # Überprüft, ob die Koordinaten innerhalb des Spielfelds liegen
            wort = self.spielbrett[y][x]  # Holt das Wort an den angegebenen Koordinaten
            self.spielbrett[y][x] = 'X'  # Markiert das Feld als 'X'
            with open(self.logdatei, 'a') as log:  # Öffnet die Logdatei im Anhangmodus
                log.write(
                    f"{datetime.datetime.now()} {wort} ({x}/{y})\n")  # Schreibt das markierte Wort und die Koordinaten in die Logdatei
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
    def beende_spiel(self):
        with open(self.logdatei, 'a') as log:  # Öffnet die Logdatei im Anhangmodus
            log.write(f"{datetime.datetime.now()} Ende des Spiels\n")  # Schreibt das Ende des Spiels in die Logdatei
        print(
            f"Spieler {self.spieler_name} hat das Spiel beendet.")  # Gibt eine Meldung aus, dass das Spiel beendet wurde






#Falls Eingabe von Hoehe und Breite nicht gleich ist

startlog = Log.log()
startlog.logeintragstart()
bspLog = Log.log()
bspLog.logeintragstep()

anz_spieler = 0
#Beginn des Spieles
print("Willkommen im Buzzword-Bingospiel.")

#Abfrage
variable = input("Neue Runde? \n [Y/N]: ")
if variable == "Y" or variable == "y":
    anz_spieler = int(input("Geben Sie die Anzahl der Spieler an:"))
    feld_gr = int(input("Geben Sie die Größe ihres Spielfeldes: \n 1 = 3X3 \n 2 = 5X5 \n 3 = 7X7"))

elif variable == "N" or variable == "n":  #elif else if
    print("Das Spiel ist beendet")

    #Beginn von der Interprosesskomunikation
processes_spieler = []
#if abfrage für geldgr 1,2,3,4 also 5 möglichkeiten
num_words = 25  #testvariable für 5x5  # Beispiel: 25 zufällige Wörter

# Pfad zur Datei und Anzahl der gewünschten Wörter
file_url = input(
    "Geben Sie den gewünschten Pfad an -wordfile: ")  #https://raw.githubusercontent.com/KhaledBadrash/BSRN-Projekt/main/Textdatei


def bingo_cards(url, anz_woerter):
    # Wörter aus der Datei lesen
    response = requests.get(url)
    words = response.text.splitlines()

    # Zufällige Wörter auswählen, ohne Duplikate
    random_words = random.sample(words, anz_woerter)
    return random_words


unique_words = bingo_cards(file_url, num_words)
print("Zufällige Wörter:", unique_words)

import Log
import requests
import random
import multiprocessing as mp

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

for _ in range(anz_spieler):
    #erstelle Karte
    #IPC pro Spieler ein Prozess
    p = mp.Process(target=bingo_cards, args=(file_url, num_words))
    p.start()
    processes_spieler.append(p)
    print("Spieler ", _ + 1, " hat das Spiel beigetreten: ", {p.pid})

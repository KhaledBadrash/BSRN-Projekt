import Log
import requests
import random
import multiprocessing as mp

#Falls Eingabe von Hoehe und Breite nicht gleich ist

startlog = Log.log()
startlog.logeintragstart()
bspLog = Log.log()
bspLog.logeintragstep()

anz_spieler = 3
feld_gr = 0
processes_spieler = []
num_words = 25  # Beispiel: 25 zufällige Wörter

# Pfad zur Datei und Anzahl der gewünschten Wörter
file_url = input("-wordfile: ")

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




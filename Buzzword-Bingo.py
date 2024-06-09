import Log
import requests
import random
import multiprocessing as mp

print('Herlich Willkommen zu Buzzword-Bingo!')
eingabeBreite = int(input('Geben Sie die Breite des Spielfeldes an -xaxis: '))
eingabeHoehe = int(input('Geben Sie die Hoehe des Spielfeldes an -yaxis:  '))

#Falls Eingabe von Hoehe und Breite nicht gleich ist
if eingabeHoehe != eingabeBreite:
    print('Beide Eingaben muessen gleich sein!')

if eingabeHoehe == eingabeBreite:
    print()

startlog = Log.log()
startlog.logeintragstart()
bspLog = Log.log()
bspLog.logeintragstep()

anz_spieler = 0
feld_gr = 0
processes_spieler = []
num_words = 25  # Beispiel: 25 zufällige Wörter

# Pfad zur Datei und Anzahl der gewünschten Wörter
file_url = 'https://raw.githubusercontent.com/KhaledBadrash/BSRN-Projekt/main/Textdatei'

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




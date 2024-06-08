import Log
import requests
import random

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


#Um Wörter zufällig zu generieren
def zufaellige_woerter(url, num_words):
    # Wörter aus der Datei lesen
    response = requests.get(url)
    words = response.text.splitlines()

# Prüfen, ob genügend Wörter in der Datei vorhanden sind
    if num_words > len(words):
        raise ValueError("Es gibt nicht genügend Wörter in der Datei.")

    # Zufällige Wörter auswählen, ohne Duplikate
    random_words = random.sample(words, num_words)
    return random_words

# Pfad zur Datei und Anzahl der gewünschten Wörter
file_url = 'https://raw.githubusercontent.com/KhaledBadrash/BSRN-Projekt/main/Textdatei'
num_words = 25  # Beispiel: 25 zufällige Wörter




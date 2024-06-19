import os
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime


def read_json_log():
    try:
        with open('log_data_host.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):  # Stelle sicher, dass die Daten eine Liste sind
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json_log(data):
    with open('log_data_host.json', 'w') as file:
        json.dump(data, file, indent=4)  # Fügt Einrückungen hinzu, um die Lesbarkeit zu verbessern



# Hilfsfunktion, um Daten in eine JSON-Datei zu loggen
def host_log_data(host_name, button_text, x_wert, y_wert, auswahl_zeitpunkt):
    # Stelle sicher, dass button_text ein String ist
    if isinstance(button_text, ttk.TTkString):
        button_text = str(button_text)
    elif not isinstance(button_text, str):
        button_text = repr(button_text)

    logs = read_json_log()
    logs.append({
        'host_name': host_name,
        'button_text': button_text,
        'x_wert': x_wert,
        'y_wert': y_wert,
        'auswahl_zeitpunkt': auswahl_zeitpunkt
    })
    write_json_log(logs)

# Neue Methode zum Loggen des Spielstarts
def log_game_start(host_name, max_spieler):
    logs = read_json_log()
    start_data = {
        'host_name': host_name,
        'Event': "Spiel gestartet",
        'max_spieler': max_spieler,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(start_data)
    write_json_log(logs)


def log_win(host_name):
    logs = read_json_log()
    win_data = {
        'host_name': host_name,
        'Event': "GEWONNEN",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(win_data)
    write_json_log(logs)

def lade_woerter(woerter_pfad, xachse, yachse):
    try:
        with open(woerter_pfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            anz_woerter = xachse * yachse
            if len(woerter) < anz_woerter:
                raise ValueError("Nicht genug Wörter in der Datei.")
            zufaellige_woerter = random.sample(woerter, anz_woerter)
            return zufaellige_woerter
    except FileNotFoundError:
        return 'Die angegebene Datei konnte nicht gefunden werden'
    except ValueError as e:
        return str(e)


def gewinner_screen(parent, personal_name):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    ttk.TTkLabel(win_root, text="Gewinner! Herzlichen Glückwunsch!", pos=(2, 2))
    win_root.raiseWidget()
    log_win(personal_name)  # Loggen des Gewinnereignisses
    win_root.show()


def main(args):
    log_game_start(args.personal_name, args.max_spieler)  # Korrigierter Funktionsaufruf
    # Überprüfung, ob die Werte für X- und Y-Achse identisch sind
    if args.xachse != args.yachse:
        print("Fehler: Die Werte für X- und Y-Achse müssen identisch sein,\num ein Spielfeld generieren zu koennen")
        return

    # Überprüfung der Existenz des Dateipfades
    if not os.path.exists(args.woerter_pfad):
        print(f"Fehler: Der angegebene Dateipfad '{args.woerter_pfad}' existiert nicht."
              f"\nversuchen Sie es mit 'woerter_datei' ")
        return

    # Überprüfung, ob ein persönlicher Name angegeben wurde
    if not args.personal_name:
        print("Fehler: Es wurde kein Host-Name angegeben.")
        return

    if not args.max_spieler:
        print("Fehler: SIe haben keine maximale Spieleranzahl angegeben.")
        return


    grid_layout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=grid_layout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    if isinstance(woerter, str):  # Fehlermeldungen behandeln
        print(woerter)
        return

    klick_counter = [0]  # Klickzähler

    klick_counter = [0]  # Klickzähler initialisieren


    def klicker(button, original_text, x, y):
        def auf_knopfdruck():
            #ein schritt zurück
            if button.text() == "X":
                logs = read_json_log()
                if logs and 'button_text' in logs[-1] and logs[-1]['x_wert'] == x and logs[-1]['y_wert'] == y:
                    button.setText(logs[-1]['button_text'])  # Setze den Text auf den letzten gespeicherten Wert
                    logs.pop()  # Entferne den letzten Eintrag
                    klick_counter[0] -= 1
                    write_json_log(logs)
            elif button.text() != 'JOKER':
                button.setText("X")
                klick_counter[0] += 1  # Erhöhe den Klickzähler
                host_log_data(args.personal_name, str(original_text), x, y,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                if klick_counter[0] == 3:  # Prüfe, ob 3 X gesetzt wurden
                    gewinner_screen(root, args.personal_name)  # Zeige Gewinnerscreen

        return auf_knopfdruck

    buttons = []
    wort_index = 0  # Index für die zufälligen Wörter
    for i in range(groesse_feld):
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="JOKER")
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button], i, j))
            else:
                text = woerter[wort_index]
                wort_index += 1
                button = ttk.TTkButton(parent=root, border=True, text=text)
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button], i, j))
            buttons.append(button)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', nargs='?', help='Wörter Pfad')
    parser.add_argument('xachse', nargs='?', help='X-Achse', type=int)
    parser.add_argument('yachse', nargs='?', help='Y-Achse', type=int)
    parser.add_argument('personal_name', nargs='?', help='Persönlicher Name')
    parser.add_argument('max_spieler', nargs='?', help='Maximale Anzahl an Spielern', type=int)

    args = parser.parse_args()
    #Ich habe nargs='?' hinzugefügt,damit die Argumente optional sind.
    #Wenn ein Argument nicht angegeben wird, wird sein Wert als None gesetzt
    #und wird in der Main dann schoener ueberprueft

    if args.newround:
        main(args)

        #python3 code.py -n woerter_datei 3 3 khaled 2


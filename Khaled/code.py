import os
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime

# Hilfsfunktion, um Daten in eine JSON-Datei zu loggen


def host_log_data(host_name,button_text, x_wert, y_wert, auswahl_zeitpunkt):
    data = {
        'host_name': host_name,
        'button_text': button_text,
        'x_wert': x_wert,
        'y_wert': y_wert,
        'auswahl_zeitpunkt': auswahl_zeitpunkt

    }

    with open('log_data_host.json', 'a') as file:  # 'a' um Daten an die Datei anzuhängen
        json.dump(data, file)
        file.write('\n')  # Neue Zeile für bessere Lesbarkeit in der Datei

# Neue Methode zum Loggen des Spielstarts
def log_game_start(host_name):
    start_data = {
        'host_name': host_name,
        'Event': "Spiel gestartet",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    with open('log_data_host.json', 'a') as file:  # 'a' um Daten an die Datei anzuhängen
        json.dump(start_data, file)
        file.write('\n')  # Neue Zeile für bessere Lesbarkeit in der Datei

def log_win(host_name):
    start_data = {
        'host_name': host_name,
        'Event': "GEWONNEN",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    with open('log_data_host.json', 'a') as file:  # 'a' um Daten an die Datei anzuhängen
        json.dump(start_data, file)
        file.write('\n')  # Neue Zeile für bessere Lesbarkeit in der Datei

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


def gewinner_screen(parent):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    ttk.TTkLabel(parent=win_root, text="Gewinner! Herzlichen Glückwunsch!", pos=(2, 2))
    win_root.raiseWidget()
    log_win(args.personal_name)


def main(args):
    log_game_start(args.personal_name)
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


    grid_layout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=grid_layout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    if isinstance(woerter, str):  # Fehlermeldungen behandeln
        print(woerter)
        return

    klick_counter = [0]  # Klickzähler

    def klicker(button, original_text, x, y):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
                klick_counter[0] += 1  # Klickzähler erhöhen

                host_log_data(args.personal_name, str(original_text), x, y,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                if klick_counter[0] == 3:
                    gewinner_screen(root)
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
    args = parser.parse_args()
    #Ich habe nargs='?' hinzugefügt,damit die Argumente optional sind.
    #Wenn ein Argument nicht angegeben wird, wird sein Wert als None gesetzt
    #und wird in der Main dann schoener ueberprueft

    if args.newround:
        main(args)

        #python3 code.py -n woerter_datei 3 3 khaled


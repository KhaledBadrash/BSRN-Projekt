import os
import random
from multiprocessing import Process, Pipe

from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime


def parse_args():
    parser = ArgumentParser(description="Starte eine neue Spielrunde oder trete einer bestehenden Runde bei")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser für das Starten einer neuen Runde als Host
    host_parser = subparsers.add_parser('host', help='Starte eine neue Runde als Host')
    host_parser.add_argument('-n', '--newround', action='store_true', help="Startet eine neue Runde")
    host_parser.add_argument('woerter_pfad', help='Pfad zur Wörterliste')
    host_parser.add_argument('xachse', type=int, help='Anzahl der Zeilen')
    host_parser.add_argument('yachse', type=int, help='Anzahl der Spalten')
    host_parser.add_argument('personal_name', help='Name des Hosts')
    host_parser.add_argument('max_spieler', type=int, help='Maximale Anzahl an Spielern')

    # Subparser für das Beitreten einer bestehenden Runde als Spieler
    player_parser = subparsers.add_parser('join', help='Tritt einer bestehenden Runde bei')
    player_parser.add_argument('personal_name', help='Dein Name')

    return parser.parse_args()


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

def clear_json_log():
    write_json_log([])  # Schreibe eine leere Liste in die JSON-Datei


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

def log_joker(host_name, button_text, x_wert, y_wert, auswahl_zeitpunkt):
    # Stelle sicher, dass button_text ein String ist
    if isinstance(button_text, ttk.TTkString):
        button_text = str(button_text)
    elif not isinstance(button_text, str):
        button_text = repr(button_text)

    logs = read_json_log()
    logs.append({
        'host_name': host_name,
        'JOKER': button_text,
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

    def pruefe_bingo(max_feld, logs):

        marked_positions = [(log.get('x_wert'), log.get('y_wert')) for log in logs
                            if log.get('button_text') == 'X' or log.get('JOKER') == 'X']

        # Überprüft horizontale Linien
        for i in range(max_feld):
            if all((i, j) in marked_positions for j in range(max_feld)):
                return True

        # Überprüft vertikale Linien
        for j in range(max_feld):
            if all((i, j) in marked_positions for i in range(max_feld)):
                return True

        # Überprüft diagonale Linien (von links oben nach rechts unten)
        if all((i, i) in marked_positions for i in range(max_feld)):
            return True

        # Überprüft diagonale Linien (von rechts oben nach links unten)
        if all((i, max_feld - 1 - i) in marked_positions for i in range(max_feld)):
            return True

        return False


    def klicker(button, original_text, x, y):
        def auf_knopfdruck():
            logs = read_json_log()
            if button.text() == "X":
                # Find the log entry corresponding to the button being reverted
                log_index = next(
                    (index for (index, d) in enumerate(logs) if d.get("x_wert") == x and d.get("y_wert") == y),
                    None)
                if log_index is not None and log_index == len(logs) - 1:
                    logs.pop(log_index)  # Remove the log entry
                    button.setText(original_text)  # Set button text to original text
                    write_json_log(logs)
            else:
                button.setText("X")
                host_log_data(args.personal_name, str(original_text), x, y,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                logs.append({
                    'host_name': args.personal_name,
                    'button_text': 'X',
                    'x_wert': x,
                    'y_wert': y,
                    'auswahl_zeitpunkt': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
                })
                write_json_log(logs)

                if pruefe_bingo(groesse_feld, logs):  # Check if Bingo condition is met
                    gewinner_screen(root, args.personal_name)

        return auf_knopfdruck

    buttons = []
    wort_index = 0  # Index für die zufälligen Wörter
    for i in range(groesse_feld):
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="X")
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button], i, j))
                log_joker(args.personal_name, "X", i, j,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))# Logge den Joker

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

def game():
    args = parse_args()
    if args.command == 'host' and args.newround:
        pid = os.fork()
        if pid == 0:
            # Kindprozess für den Host
            clear_json_log()  # Leere die JSON-Datei
            main(args)
        else:
            # Elternprozess tut nichts, der Host-Prozess läuft nun eigenständig
            print(f"Host-Prozess gestartet mit PID {pid}.")
    elif args.command == 'join':
        pid = os.fork()
        if pid == 0:
            # Kindprozess für einen beitretenden Spieler
            print(f"Spieler {args.personal_name} tritt der Runde bei.")
            # Hier kann der Code zum Beitreten des Spiels hinzugefügt werden
            os._exit(0)  # Beenden Sie den Kindprozess, wenn fertig
        else:
            # Elternprozess tut nichts, der Spieler-Prozess läuft nun eigenständig
            print(f"Spieler-Prozess gestartet mit PID {pid}.")
    else:
        print("Kein gültiges Argument zum Starten oder Beitreten einer Runde angegeben.")

if __name__ == "__main__":
    game()


        #python3 bingo.py -n woerter_datei 3 3 khaled 2
        #python3 bingo.py join SpielerName



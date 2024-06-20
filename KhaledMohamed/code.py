import os
import random
import sys
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime

# Hilfsfunktionen
def parse_host_args():
    parser = ArgumentParser(description="Starte eine neue Spielrunde als Host")
    parser.add_argument('-n', '--newround', action='store_true', help="Startet eine neue Runde")
    parser.add_argument('woerter_pfad', nargs='?', help='Pfad zur Wörterliste')
    parser.add_argument('xachse', type=int, nargs='?', help='Anzahl der Zeilen')
    parser.add_argument('yachse', type=int, nargs='?', help='Anzahl der Spalten')
    parser.add_argument('personal_name', nargs='?', help='Name des Hosts')
    parser.add_argument('max_spieler', type=int, nargs='?', help='Maximale Anzahl an Spielern')
    return parser.parse_args()

def parse_player_args():
    parser = ArgumentParser(description="Trete einer existierenden Spielrunde bei")
    parser.add_argument('-j', '--join_into_round', action='store_true', help="Tritt einer Runde bei")
    parser.add_argument('player_name', nargs='?', help='Dein Name')
    return parser.parse_args()

def check_game_status():
    try:
        with open('game_status.json', 'r') as file:
            status = json.load(file)
            return status.get('is_active', False)
    except FileNotFoundError:
        return False

def set_game_status(active):
    with open('game_status.json', 'w') as file:
        json.dump({'is_active': active}, file)

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
def read_json_log_spieler():
    try:
        with open('log_data_spieler.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):  # Stelle sicher, dass die Daten eine Liste sind
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json_log_spieler(data):
    with open('log_data_spieler.json', 'w') as file:
        json.dump(data, file, indent=4)  # Fügt Einrückungen hinzu, um die Lesbarkeit zu verbessern


def log_spieler_data(player_name, button_text, x_wert, y_wert, auswahl_zeitpunkt):
    if isinstance(button_text, ttk.TTkString):
        button_text = str(button_text)
    elif not isinstance(button_text, str):
        button_text = repr(button_text)

    logs = read_json_log_spieler()
    logs.append({
        'player_name': player_name,
        'button_text': button_text,
        'x_wert': x_wert,
        'y_wert': y_wert,
        'auswahl_zeitpunkt': auswahl_zeitpunkt
    })
    write_json_log_spieler(logs)


def clear_json_logs():
    # Leere die Host Log-Datei
    with open('log_data_host.json', 'w') as file:
        json.dump([], file, indent=4)

    # Setze den Spielstatus zurück
    with open('game_status.json', 'w') as file:
        json.dump({'is_active': False}, file)

    # Leere die Spieler Log-Datei
    with open('log_data_spieler.json', 'w') as file:
        json.dump([], file, indent=4)

def log_spieler_win(player_name):
    logs = read_json_log_spieler()
    win_data = {
        'player_name': player_name,
        'Event': "GEWONNEN",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(win_data)
    write_json_log_spieler(logs)


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

def log_joker_spieler(player_name, button_text, x_wert, y_wert, auswahl_zeitpunkt):
    # Stelle sicher, dass button_text ein String ist
    if isinstance(button_text, ttk.TTkString):
        button_text = str(button_text)
    elif not isinstance(button_text, str):
        button_text = repr(button_text)

    logs = read_json_log()
    logs.append({
        'player_name': player_name,
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


def main_player(args):
    log_game_start(args.player_name, args.max_spieler)  # Korrigierter Funktionsaufruf
    # Überprüfung, ob die Werte für X- und Y-Achse identisch sind
    if check_game_status():
        print(f"{args.player_name} tritt dem Spiel bei...")
    else:
        print("Kein aktives Spiel gefunden. Bitte warten Sie, bis ein Host ein Spiel startet.")

    if args.xachse != args.yachse:
        print("Fehler: Die Werte für X- und Y-Achse müssen identisch sein,\num ein Spielfeld generieren zu koennen")
        return

    # Überprüfung, ob ein persönlicher Name angegeben wurde
    if not args.player_name:
        print("Fehler: Es wurde kein Spielername angegeben.")
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
            logs = read_json_log_spieler()
            if button.text() == "X":
                # Find the log entry corresponding to the button being reverted
                log_index = next(
                    (index for (index, d) in enumerate(logs) if d.get("x_wert") == x and d.get("y_wert") == y),
                    None)
                if log_index is not None and log_index == len(logs) - 1:
                    logs.pop(log_index)  # Remove the log entry
                    button.setText(original_text)  # Set button text to original text
                    write_json_log_spieler(logs)
            else:
                button.setText("X")
                log_spieler_data(args.player_name, str(original_text), x, y,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                logs.append({
                    'host_name': args.player_name,
                    'button_text': 'X',
                    'x_wert': x,
                    'y_wert': y,
                    'auswahl_zeitpunkt': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
                })
                write_json_log_spieler(logs)

                if pruefe_bingo(groesse_feld, logs):  # Check if Bingo condition is met
                    gewinner_screen(root, args.player_name)

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
                log_joker_spieler(args.player_name, "X", i, j,
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


def main_host(args):
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
                          datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))  # Logge den Joker

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
    parser = ArgumentParser(description="Startet das Spiel als Host oder tritt einem bestehenden Spiel bei.")
    parser.add_argument('-n', '--newround', action='store_true', help='Startet eine neue Spielrunde als Host')
    parser.add_argument('-j', '--join', help='Tritt einer bestehenden Spielrunde bei')

    parser.add_argument('woerter_pfad', nargs='?', help='Wörter Pfad')
    parser.add_argument('xachse', nargs='?', help='X-Achse', type=int)
    parser.add_argument('yachse', nargs='?', help='Y-Achse', type=int)
    parser.add_argument('personal_name', nargs='?', help='Persönlicher Name')
    parser.add_argument('max_spieler', nargs='?', help='Maximale Anzahl an Spielern', type=int)

    args = parser.parse_args()

    if args.newround:
        clear_json_logs()
        if not all([args.woerter_pfad, args.xachse, args.yachse, args.personal_name, args.max_spieler]):
            parser.error("Alle Parameter müssen für die Initiierung eines neuen Spiels angegeben werden.")
        print("Neues Spiel wird gestartet...")
        set_game_status(True)
        main_host(args)
    elif args.join:
        if check_game_status():
            print(f"{args.join} tritt dem Spiel bei...")
            main_player(args.join)
        else:
            print("Kein aktives Spiel gefunden. Bitte warten Sie, bis ein Host ein Spiel startet.")
    else:
        print(
            "Bitte geben Sie einen gültigen Befehl ein. Benutzen Sie -n um ein Spiel zu starten oder -j um einem Spiel beizutreten.")
# python3 code.py -n woerter_datei 3 3 khaled 2
# python3 code.py -j Paul

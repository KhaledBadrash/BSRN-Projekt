import os
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime

def read_json_log(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json_log(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def clear_json_log(filename):
    write_json_log(filename, [])

def host_log_data(filename, host_name, button_text, x_wert, y_wert, auswahl_zeitpunkt):
    if isinstance(button_text, ttk.TTkString):
        button_text = str(button_text)
    elif not isinstance(button_text, str):
        button_text = repr(button_text)

    logs = read_json_log(filename)
    logs.append({
        'host_name': host_name,
        'button_text': button_text,
        'x_wert': x_wert,
        'y_wert': y_wert,
        'auswahl_zeitpunkt': auswahl_zeitpunkt
    })
    write_json_log(filename, logs)

def log_game_start(filename, host_name, max_spieler):
    logs = read_json_log(filename)
    start_data = {
        'host_name': host_name,
        'Event': "Spiel gestartet",
        'max_spieler': max_spieler,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(start_data)
    write_json_log(filename, logs)

def log_win(filename, host_name):
    logs = read_json_log(filename)
    win_data = {
        'host_name': host_name,
        'Event': "GEWONNEN",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(win_data)
    write_json_log(filename, logs)

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

def gewinner_screen(parent, personal_name, log_filename):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    ttk.TTkLabel(win_root, text="Gewinner! Herzlichen Glückwunsch!", pos=(2, 2))
    win_root.raiseWidget()
    log_win(log_filename, personal_name)
    win_root.show()

def handle_game(pipe_path, args):
    log_filename = f'{args.personal_name}_log.json'
    clear_json_log(log_filename)
    log_game_start(log_filename, args.personal_name, args.max_spieler)

    if args.xachse != args.yachse:
        print("Fehler: Die Werte für X- und Y-Achse müssen identisch sein,\num ein Spielfeld generieren zu koennen")
        return

    if not os.path.exists(args.woerter_pfad):
        print(f"Fehler: Der angegebene Dateipfad '{args.woerter_pfad}' existiert nicht.\nVersuchen Sie es mit 'woerter_datei'")
        return

    if not args.personal_name:
        print("Fehler: Es wurde kein Host-Name angegeben.")
        return

    if not args.max_spieler:
        print("Fehler: Sie haben keine maximale Spieleranzahl angegeben.")
        return

    grid_layout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=grid_layout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    if isinstance(woerter, str):
        print(woerter)
        return

    def pruefe_bingo(max_feld, logs):
        marked_positions = [(log.get('x_wert'), log.get('y_wert')) for log in logs if log.get('button_text') == 'X']
        for i in range(max_feld):
            if all((i, j) in marked_positions for j in range(max_feld)):
                return True
            if all((j, i) in marked_positions for j in range(max_feld)):
                return True

    def klicker(button, original_text, x, y):
        def auf_knopfdruck():
            logs = read_json_log(log_filename)
            if button.text() == "X":
                log_index = next(
                    (index for (index, d) in enumerate(logs) if d.get("x_wert") == x and d.get("y_wert") == y),
                    None)
                if log_index is not None and log_index == len(logs) - 1:
                    logs.pop(log_index)
                    button.setText(original_text)
                    write_json_log(log_filename, logs)
            else:
                button.setText("X")
                host_log_data(log_filename, args.personal_name, str(original_text), x, y,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                logs.append({
                    'host_name': args.personal_name,
                    'button_text': 'X',
                    'x_wert': x,
                    'y_wert': y,
                    'auswahl_zeitpunkt': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
                })
                write_json_log(log_filename, logs)
                if pruefe_bingo(groesse_feld, logs):
                    gewinner_screen(root, args.personal_name, log_filename)

        return auf_knopfdruck

    buttons = []
    wort_index = 0
    for i in range(groesse_feld):
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="X")
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button], i, j))
                host_log_data(log_filename, args.personal_name, "JOKER", i, j,
                              datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
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

def main(args):
    pipe_path = "/tmp/bingo_pipe"
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    if args.newround:
        clear_json_log('log_data_host.json')

    with open(pipe_path, 'w') as pipe:
        pipe.write(json.dumps(vars(args)))
        pipe.write('\n')

    with open(pipe_path, 'r') as pipe:
        while True:
            line = pipe.readline()
            if not line:
                break
            process_args = json.loads(line.strip())
            process_args = Namespace(**process_args)
            handle_game(pipe_path, process_args)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', nargs='?', help='Wörter Pfad')
    parser.add_argument('xachse', nargs='?', help='X-Achse', type=int)
    parser.add_argument('yachse', nargs='?', help='Y-Achse', type=int)
    parser.add_argument('personal_name', nargs='?', help='Persönlicher Name')
    parser.add_argument('max_spieler', nargs='?', help='Maximale Anzahl an Spielern', type=int)

    args = parser.parse_args()

    main(args)


        #python3 code.py -n woerter_datei 3 3 khaled 2


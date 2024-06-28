import os
import random
from argparse import ArgumentParser, Namespace
import json
from datetime import datetime
from multiprocessing import Process, Pipe
import TermTk as ttk
import time
import threading
import sys


def parse_args():
    parser = ArgumentParser(description="Starte eine neue Spielrunde oder trete einer bestehenden Runde bei")
    subparsers = parser.add_subparsers(dest='command', required=True)

    host_parser = subparsers.add_parser('host', help='Starte eine neue Runde als Host')
    host_parser.add_argument('-n', '--newround', action='store_true', help="Startet eine neue Runde")
    host_parser.add_argument('woerter_pfad', help='Pfad zur Wörterliste')
    host_parser.add_argument('xachse', type=int, help='Anzahl der Zeilen')
    host_parser.add_argument('yachse', type=int, help='Anzahl der Spalten')
    host_parser.add_argument('personal_name', help='Name des Hosts')
    host_parser.add_argument('max_spieler', type=int, help='Maximale Anzahl an Spielern')

    player_parser = subparsers.add_parser('join', help='Tritt einer bestehenden Runde bei')
    player_parser.add_argument('personal_name', help='Dein Name')

    return parser.parse_args()


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
        raise FileNotFoundError('Die angegebene Datei konnte nicht gefunden werden')
    except ValueError as e:
        raise ValueError(str(e))


def setup_pipes():
    host_to_players_path = '/tmp/host_to_players'
    players_to_host_path = '/tmp/players_to_host'

    if os.path.exists(host_to_players_path):
        os.remove(host_to_players_path)
    if os.path.exists(players_to_host_path):
        os.remove(players_to_host_path)

    os.mkfifo(host_to_players_path, mode=0o666)
    os.mkfifo(players_to_host_path, mode=0o666)


def cleanup_pipes():
    os.unlink('/tmp/host_to_players')
    os.unlink('/tmp/players_to_host')


def handle_host_connections(args, conn):
    anz_spieler = args.max_spieler
    print(f"Warte auf {anz_spieler} Spieler...")
    setup_pipes()
    with open('/tmp/host_to_players', 'w') as h2p, open('/tmp/players_to_host', 'r') as p2h:
        connected_players = 0
        while connected_players < args.max_spieler:
            line = p2h.readline().strip()
            if line == 'READY':
                connected_players += 1
                print(f"Spieler {connected_players} verbunden.")
                print(f"Warte auf {anz_spieler-1} Spieler...")
                anz_spieler = anz_spieler - 1

        print("Alle Spieler sind verbunden. Das Spiel beginnt!")
        h2p.write(f'START {args.xachse} {args.yachse}\n')
        h2p.flush()
        conn.send(True)
    cleanup_pipes()


def player_process(player_name):
    with open('/tmp/host_to_players', 'r') as h2p, open('/tmp/players_to_host', 'w') as p2h:
        print(f"Spieler {player_name} ist bereit.")
        p2h.write('READY\n')
        p2h.flush()

        start_message = h2p.readline().strip()
        if start_message.startswith('START'):
            _, xachse, yachse = start_message.split()
            xachse = int(xachse)
            yachse = int(yachse)
            print(f"Spiel beginnt für {player_name}!")
            run_game_gui(player_name, xachse, yachse)


def read_json_log():
    try:
        with open('log_data_host.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json_log(data):
    with open('log_data_host.json', 'w') as file:
        json.dump(data, file, indent=4)


def clear_json_log():
    write_json_log([])


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


def gewinner_screen(parent, personal_name):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    win_root.raiseWidget()
    log_win(personal_name)  # Loggen des Gewinnereignisses
    win_root.show()

    name_root = ttk.TTkWindow(parent=parent, title=f"{personal_name} ist der Gewinner!", border=True, pos=(35, 20), size=(30, 10))
    name_root.raiseWidget()
    name_root.show()

    # Animation: Change the title color repeatedly
    def animate_title():
        colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
                  ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
        index = 0
        while True:
            win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
            name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
            index += 1
            time.sleep(0.5)
            parent.update()

    # Start the animation in a separate thread to keep the GUI responsive
    import threading
    animation_thread = threading.Thread(target=animate_title, daemon=True)
    animation_thread.start()

game_over = False

class GameApp:

    def __init__(self, args, player_name=None):
        self.args = args
        self.player_name = player_name or args.personal_name
        self.woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
        self.root = ttk.TTk()
        self.original_texts = {}

    def run(self):
        grid_layout = ttk.TTkGridLayout(parent=self.root)
        self.root.setLayout(grid_layout)

        for i in range(self.args.xachse):
            for j in range(self.args.yachse):
                if i == self.args.xachse // 2 and j == self.args.yachse // 2:
                    button = ttk.TTkButton(parent=self.root, text='X', border=True, pos=(i, j))
                    self.original_texts[button] = button.text()
                    button.clicked.connect(lambda btn=button, x=i, y=j: self.button_click(btn, x, y))
                    grid_layout.addWidget(button, i, j)
                    self.log_joker('X', i, j, datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                else:
                    wort = self.woerter[i * self.args.yachse + j]
                    button = ttk.TTkButton(parent=self.root, text=wort, border=True, pos=(i, j))
                    self.original_texts[button] = button.text()
                    button.clicked.connect(lambda btn=button, x=i, y=j: self.button_click(btn, x, y))
                    grid_layout.addWidget(button, i, j)

        self.root.mainloop()

    def button_click(self, button, x_wert, y_wert):

        global game_over

        if game_over:
            return

        logs = read_json_log()
        if button.text() == "X":
            # Find the log entry corresponding to the button being reverted
            log_index = next(
                (index for (index, d) in enumerate(logs) if d.get("x_wert") == x_wert and d.get("y_wert") == y_wert),
                None)
            if log_index is not None and log_index == len(logs) - 1:
                logs.pop(log_index)  # Remove the log entry
                button.setText(self.original_texts[button])  # Set button text to original text
                write_json_log(logs)
        else:
            original_text = button.text()
            button.setText("X")
            auswahl_zeitpunkt = datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
            self.log_data_json(original_text, x_wert, y_wert, auswahl_zeitpunkt)
            log_data = {
                'host_name': self.player_name,
                'button_text': 'X',
                'x_wert': x_wert,
                'y_wert': y_wert,
                'auswahl_zeitpunkt': auswahl_zeitpunkt
            }
            logs.append(log_data)
            write_json_log(logs)

        # Check for bingo
        if pruefe_bingo(self.args.xachse, logs):
            game_over = True
            gewinner_screen(self.root, self.player_name)

    def log_joker(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = read_json_log()
        logs.append({
            'host_name': self.player_name,
            'JOKER': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        write_json_log(logs)

    def log_data_json(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = read_json_log()
        logs.append({
            'host_name': self.player_name,
            'button_text': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        write_json_log(logs)


def run_game_gui(player_name, xachse, yachse):
    args = Namespace(
        woerter_pfad='woerter_datei',
        xachse=xachse,
        yachse=yachse,
        personal_name=player_name,
        max_spieler=3
    )
    app = GameApp(args, player_name)
    app.run()


def main(args):
    if args.command == 'host' and args.newround:
        clear_json_log()
        log_game_start(args.personal_name, args.max_spieler)

        parent_conn, child_conn = Pipe()
        connection_process = Process(target=handle_host_connections, args=(args, child_conn))
        connection_process.start()

        if parent_conn.recv():
            app = GameApp(args)
            app.run()

        connection_process.join()
    elif args.command == 'join':
        player_process(args.personal_name)
    else:
        print("Kein gültiges Argument zum Starten oder Beitreten einer Runde angegeben.")


def game():
    args = parse_args()
    main(args)


if __name__ == "__main__":
    game()
#python3 multi.py host -n woerter_datei 5 5 HostName 3

#python3 multi.py join SpielerName1
#python3 multi.py join SpielerName2
#python3 multi.py join SpielerName3


#pstree -p | grep python3
#cd KhaledMohamed
# python3 testtt.py host -n woerter_datei 5 5 khaled 1

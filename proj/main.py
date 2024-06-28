import subprocess
import os
import sys
import random
import json
import time
from argparse import ArgumentParser, Namespace
from datetime import datetime
from multiprocessing import Process

import TermTk as ttk


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

    # Hinzufügen des run_gui Befehls
    gui_parser = subparsers.add_parser('run_gui', help='Startet die GUI')
    gui_parser.add_argument('personal_name', help='Dein Name')
    gui_parser.add_argument('xachse', type=int, help='Anzahl der Zeilen')
    gui_parser.add_argument('yachse', type=int, help='Anzahl der Spalten')

    return parser.parse_args()




def start_process(*args):
    subprocess.Popen([sys.executable] + list(args))


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


def handle_host_connections(woerter_pfad, xachse, yachse, personal_name, max_spieler):
    print(f"Host-Prozess gestartet mit PID: {os.getpid()}")
    setup_pipes()
    with open('/tmp/host_to_players', 'w') as h2p, open('/tmp/players_to_host', 'r') as p2h:
        connected_players = 0
        while connected_players < max_spieler:
            line = p2h.readline().strip()
            if line == 'READY':
                connected_players += 1
                print(f"Spieler {connected_players} verbunden.")
                print(f"Warte auf {max_spieler - connected_players} Spieler...")

        print("Alle Spieler sind verbunden. Das Spiel beginnt!")
        h2p.write(f'START {xachse} {yachse}\n')
        h2p.flush()

    cleanup_pipes()
    start_process(__file__, 'run_gui', personal_name, str(xachse), str(yachse))


def player_process(player_name):
    print(f"Spieler-Prozess gestartet mit PID: {os.getpid()}")
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
            start_process(__file__, 'run_gui', player_name, str(xachse), str(yachse))


def run_game_gui(player_name, xachse, yachse):
    print(f"GameApp-Init-Prozess gestartet mit PID: {os.getpid()}")
    args = Namespace(
        woerter_pfad='woerter_datei',
        xachse=xachse,
        yachse=yachse,
        personal_name=player_name,
        max_spieler=3
    )
    game = GameApp(args, player_name)
    game.run()


class GameApp:
    def __init__(self, args, player_name=None):
        self.args = args
        self.player_name = player_name or args.personal_name
        self.woerter = self.lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
        self.root = ttk.TTk()
        self.original_texts = {}

    def run(self):
        print(f"GameApp-Prozess gestartet mit PID: {os.getpid()}")
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

        logs = self.read_json_log()
        if button.text() == "X":
            log_index = next(
                (index for (index, d) in enumerate(logs) if d.get("x_wert") == x_wert and d.get("y_wert") == y_wert),
                None)
            if log_index is not None and log_index == len(logs) - 1:
                logs.pop(log_index)
                button.setText(self.original_texts[button])
                self.write_json_log(logs)
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
            self.write_json_log(logs)

        if self.pruefe_bingo(self.args.xachse, logs):
            game_over = True
            self.gewinner_screen(self.root, self.player_name)

    def lade_woerter(self, woerter_pfad, xachse, yachse):
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

    def log_joker(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = self.read_json_log()
        logs.append({
            'host_name': self.player_name,
            'JOKER': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        self.write_json_log(logs)

    def log_data_json(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = self.read_json_log()
        logs.append({
            'host_name': self.player_name,
            'button_text': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        self.write_json_log(logs)

    def read_json_log(self):
        try:
            with open('log_data_host.json', 'r') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    return []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_json_log(self, data):
        with open('log_data_host.json', 'w') as file:
            json.dump(data, file, indent=4)

    def pruefe_bingo(self, max_feld, logs):
        marked_positions = [(log.get('x_wert'), log.get('y_wert')) for log in logs
                            if log.get('button_text') == 'X' or log.get('JOKER') == 'X']

        for i in range(max_feld):
            if all((i, j) in marked_positions for j in range(max_feld)):
                return True

        for j in range(max_feld):
            if all((i, j) in marked_positions for i in range(max_feld)):
                return True

        if all((i, i) in marked_positions for i in range(max_feld)):
            return True

        if all((i, max_feld - 1 - i) in marked_positions for i in range(max_feld)):
            return True

        return False

    def gewinner_screen(parent, personal_name):
        win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
        win_root.raiseWidget()
        parent.log_win(personal_name)  # Loggen des Gewinnereignisses
        win_root.show()

        name_root = ttk.TTkWindow(parent=parent, title=f"{personal_name} ist der Gewinner!", border=True, pos=(35, 20),
                                  size=(30, 10))
        name_root.raiseWidget()
        name_root.show()

        # Animation: Change the title color repeatedly
        def animate_title():
            print(f"Animations-Prozess gestartet mit PID: {os.getpid()}")
            colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
                      ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN,
                      ttk.TTkColor.WHITE]
            index = 0
            while True:
                win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
                name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
                index += 1
                time.sleep(0.5)
                parent.update()

        # Start the animation in a separate process to keep the GUI responsive
        animation_process = Process(target=animate_title, daemon=True)
        animation_process.start()

    def log_win(self, personal_name):
        logs = self.read_json_log()
        win_data = {
            'host_name': personal_name,
            'Event': "GEWONNEN",
            'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
        }
        logs.append(win_data)
        self.write_json_log(logs)


game_over = False


def clear_json_log():
    with open('log_data_host.json', 'w') as file:
        json.dump([], file)


def log_game_start(host_name, max_spieler, write_json_log=None):

    start_data = {
        'host_name': host_name,
        'Event': "Spiel gestartet",
        'max_spieler': max_spieler,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }



def main(args):
    print(f"Main-Prozess gestartet mit PID: {os.getpid()}")
    if args.command == 'host' and args.newround:
        clear_json_log()
        log_game_start(args.personal_name, args.max_spieler)
        handle_host_connections(args.woerter_pfad, args.xachse, args.yachse, args.personal_name, args.max_spieler)
    elif args.command == 'join':
        player_process(args.personal_name)
    elif args.command == 'run_gui':
        run_game_gui(args.personal_name, args.xachse, args.yachse)
    else:
        print("Kein gültiges Argument zum Starten oder Beitreten einer Runde angegeben.")


def game():
    args = parse_args()
    main(args)


if __name__ == "__main__":
    game()

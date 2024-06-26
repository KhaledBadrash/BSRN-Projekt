import os
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime
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
        return 'Die angegebene Datei konnte nicht gefunden werden'
    except ValueError as e:
        return str(e)


def setup_pipes(max_players):
    os.mkfifo('/tmp/host_to_players', mode=0o666)
    os.mkfifo('/tmp/players_to_host', mode=0o666)


def cleanup_pipes():
    os.unlink('/tmp/host_to_players')
    os.unlink('/tmp/players_to_host')


def host_process(args):
    setup_pipes(args.max_spieler)
    with open('/tmp/host_to_players', 'w') as h2p, open('/tmp/players_to_host', 'r') as p2h:
        connected_players = 0
        print("Warte auf Spieler...")
        while connected_players < args.max_spieler:
            line = p2h.readline().strip()
            if line == 'READY':
                connected_players += 1
                print(f"Spieler {connected_players} verbunden.")

        print("Alle Spieler sind verbunden. Das Spiel beginnt!")
        h2p.write('START\n')
        h2p.flush()
        main(args)
    cleanup_pipes()


def player_process(player_name):
    with open('/tmp/host_to_players', 'r') as h2p, open('/tmp/players_to_host', 'w') as p2h:
        print(f"Spieler {player_name} ist bereit.")
        p2h.write('READY\n')
        p2h.flush()

        start_message = h2p.readline().strip()
        if start_message == 'START':
            print(f"Spiel beginnt für {player_name}!")
            # Hier könnte die Spiellogik des Spielers integriert werden


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


def main(args):
    log_game_start(args.personal_name, args.max_spieler)
    # GUI Setup
    root = ttk.TTk()
    grid_layout = ttk.TTkGridLayout(parent=root)
    root.setLayout(grid_layout)

    # Spielbrett einrichten
    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    buttons = []
    for i in range(args.xachse):
        for j in range(args.yachse):
            wort = woerter[i * args.xachse + j]
            button = ttk.TTkButton(text=wort, pos=(i, j))
            button.clicked.connect(lambda btn=button, x=i, y=j: button_click(btn, args.personal_name, x, y))
            grid_layout.addWidget(button, i, j)
            buttons.append(button)

    # GUI starten
    root.mainloop()


def button_click(button, host_name, x, y):
    # Logik für das Klicken der Schaltflächen
    button.setText("X")
    log_data = {
        'host_name': host_name,
        'button_text': 'X',
        'x_wert': x,
        'y_wert': y,
        'auswahl_zeitpunkt': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs = read_json_log()
    logs.append(log_data)
    write_json_log(logs)


def game():
    args = parse_args()
    if args.command == 'host' and args.newround:
        pid = os.fork()
        if pid == 0:
            clear_json_log()
            host_process(args)
        else:
            print(f"Host-Prozess gestartet mit PID {pid}.")
    elif args.command == 'join':
        pid = os.fork()
        if pid == 0:
            player_process(args.personal_name)
        else:
            print(f"Spieler-Prozess gestartet mit PID {pid}.")
    else:
        print("Kein gültiges Argument zum Starten oder Beitreten einer Runde angegeben.")


if __name__ == "__main__":
    game()

#python3 multi.py host -n woerter_datei 5 5 HostName 3

#python3 multi.py join SpielerName1
#python3 multi.py join SpielerName2
#python3 multi.py join SpielerName3


#pstree -p | grep python3
#cd KhaledMohamed
# python3 multi.py host -n woerter_datei 3 3 khaled 3

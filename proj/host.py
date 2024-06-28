import os
import json
import time
from datetime import datetime


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
    start_process('gui.py', personal_name, str(xachse), str(yachse))


def start_process(script, subprocess=None, *args):
    subprocess.Popen([sys.executable, script] + list(args))


if __name__ == "__main__":
    import sys

    woerter_pfad, xachse, yachse, personal_name, max_spieler = sys.argv[1:6]
    handle_host_connections(woerter_pfad, int(xachse), int(yachse), personal_name, int(max_spieler))

import os
import sys
import subprocess

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
            start_process('gui.py', player_name, str(xachse), str(yachse))

def start_process(script, *args):
    subprocess.Popen([sys.executable, script] + list(args))

if __name__ == "__main__":
    player_name = sys.argv[1]
    player_process(player_name)

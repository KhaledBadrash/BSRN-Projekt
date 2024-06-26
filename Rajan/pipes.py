import os
import json
from datetime import datetime

from codeR import host_log_data, log_game_start, log_win, pipe_path


def read_pipe():
    pipe_path = 'pipes.py'
    try:
        with open(pipe_path, 'r') as pipe:  # Open for reading
            data = json.load(pipe)
            return data
    except FileNotFoundError:

        os.mkfifo(pipe_path)
        return None

def write_pipe(data):
    with open(pipe_path, 'w') as pipe:
        json.dump(data, pipe)

def main():
    while True:
        data = read_pipe()
        if data:
            if data['action'] == 'log_data':
                host_log_data(data['host_name'], data['button_text'],
                              data['x_wert'], data['y_wert'], data['auswahl_zeitpunkt'])
            elif data['action'] == 'log_game_start':
                log_game_start(data['host_name'], data['max_spieler'])
            elif data['action'] == 'log_win':
                log_win(data['host_name'])
            else:
                print(f"Unerkannte Aktion: {data['action']}")
        else:
            print("Keine Daten aus der Pipe gelesen.")

if __name__ == "__main__":
    main()



 #python3 pipes.py

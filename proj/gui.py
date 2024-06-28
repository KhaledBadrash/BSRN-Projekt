import sys
import os
import TermTk as ttk
import random
from argparse import Namespace
from datetime import datetime

from rich import json


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

    def gewinner_screen(self, parent, personal_name, subprocess=None, time= None):
        win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
        win_root.raiseWidget()
        self.log_win(personal_name)
        win_root.show()

        name_root = ttk.TTkWindow(parent=parent, title=f"{personal_name} ist der Gewinner!", border=True, pos=(35, 20), size=(30, 10))
        name_root.raiseWidget()
        name_root.show()

        def animate_title():
            print(f"Animations-Prozess gestartet mit PID: {os.getpid()}")
            colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
                      ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
            index = 0
            while True:
                win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
                name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
                index += 1
                time.sleep(0.5)
                parent.update()

        animation_process = subprocess.Popen([sys.executable, '-c', """
import time
import TermTk as ttk

def animate_title(win_root, name_root, personal_name):
    print(f"Animations-Prozess gestartet mit PID: {os.getpid()}")
    colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
              ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
    index = 0
    while True:
        win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
        name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
        index += 1
        time.sleep(0.5)
        parent.update()

animate_title(win_root, name_root, personal_name)
"""], shell=True)

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

if __name__ == "__main__":
    player_name, xachse, yachse = sys.argv[1:4]
    run_game_gui(player_name, int(xachse), int(yachse))

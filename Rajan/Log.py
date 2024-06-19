import json
import logging
from datetime import datetime
import random
import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.widget import TTkWidget

# Logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_event(event):
    """Log events to a JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event
    }
    with open('log.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
    logging.info(event)

def lade_woerter(woerter_pfad, xachse, yachse):
    try:
        with open(woerter_pfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            anz_woerter = xachse * yachse
            zufaellige_woerter = random.sample(woerter, anz_woerter)
            log_event("Loaded words from file.")
            return zufaellige_woerter
    except FileNotFoundError:
        error_msg = 'Die angegebene Datei konnte nicht gefunden werden'
        log_event(error_msg)
        return error_msg

def gewinner_screen():
    root = ttk.TTk()
    ttk.TTkLabel(parent=root, text="Gewinner! Herzlichen Glückwunsch!")
    root.mainloop()
    log_event("Displayed winner screen.")

def main(args):
    grid_layout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=grid_layout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    klick_counter = [0]  # Zähler für die Klicks

    def klicker(button, original_text):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
                log_event(f"Button at position ({button.pos().x()}, {button.pos().y()}) set to original text.")
            else:
                button.setText("X")
                klick_counter[0] += 1  # Klickzähler
                log_event(f"Button at position ({button.pos().x()}, {button.pos().y()}) clicked.")
                # Überprüfen, ob der Gewinnerscreen nach 3 Klicks angezeigt werden soll
                if klick_counter[0] == 3:
                    root.quit()
                    gewinner_screen()
        return auf_knopfdruck

    buttons = []
    for i in range(groesse_feld):
        row = []
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="X")
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                log_event(f"Created central button at position ({i}, {j}).")
            else:
                text = random.choice(woerter)
                button = ttk.TTkButton(parent=root, border=True, text=text)
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button]))
                log_event(f"Created button at position ({i}, {j}) with text '{text}'.")
            row.append(button)
        buttons.append(row)

    root.update()
    root.mainloop()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', help='Wörter Pfad')
    parser.add_argument('xachse', help='X-Achse', type=int)
    parser.add_argument('yachse', help='Y-Achse', type=int)
    args = parser.parse_args()

    if args.newround:
        main(args)


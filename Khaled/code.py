import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
import json
from datetime import datetime

# Hilfsfunktion, um Daten in eine JSON-Datei zu loggen
def log_data(button_text, x_value, y_value, work_date, personal_name):
    data = {
        'button_text': button_text,
        'x_value': x_value,
        'y_value': y_value,
        'work_date': work_date,
        'personal_name': personal_name
    }
    with open('log_data_host.json', 'a') as file:  # 'a' um Daten an die Datei anzuhängen
        json.dump(data, file)
        file.write('\n')  # Neue Zeile für bessere Lesbarkeit in der Datei

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

def gewinner_screen(parent):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    ttk.TTkLabel(parent=win_root, text="Gewinner! Herzlichen Glückwunsch!", pos=(2, 2))
    win_root.raiseWidget()

def main(args):
    grid_layout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=grid_layout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    if isinstance(woerter, str):  # Fehlermeldungen behandeln
        print(woerter)
        return

    klick_counter = [0]  # Klickzähler

    def klicker(button, original_text, x, y):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
                klick_counter[0] += 1  # Klickzähler erhöhen

                log_data(str(original_text), x, y, datetime.now().strftime('%d-%m-%Y %H:%M:%S'), args.personal_name)
                if klick_counter[0] == 3:
                    gewinner_screen(root)
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
    parser = ArgumentParser()
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', help='Wörter Pfad')
    parser.add_argument('xachse', help='X-Achse', type=int)
    parser.add_argument('yachse', help='Y-Achse', type=int)
    parser.add_argument('personal_name', help='Persönlicher Name')
    args = parser.parse_args()

    if args.newround:
        main(args)

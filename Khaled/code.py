import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk


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
    if isinstance(woerter, str):  # Falls eine Fehlermeldung zurückgegeben wird
        print(woerter)
        return

    klick_counter = [0]  # Zähler für die Klicks

    def klicker(button, original_text):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
                klick_counter[0] += 1  # Klickzähler
                if klick_counter[0] == 3:
                    gewinner_screen(root)
        return auf_knopfdruck

    buttons = []
    wort_index = 0  # Index für die zufälligen Wörter
    for i in range(groesse_feld):
        row = []
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="X")
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
            else:
                text = woerter[wort_index]
                wort_index += 1
                button = ttk.TTkButton(parent=root, border=True, text=text)
                original_texts[button] = button.text()
                grid_layout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button]))
            row.append(button)
        buttons.append(row)

    root.update()
    root.mainloop()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', help='Wörter Pfad')
    parser.add_argument('xachse', help='X-Achse', type=int)
    parser.add_argument('yachse', help='Y-Achse', type=int)
    args = parser.parse_args()

    if args.newround:
        main(args)

# Ubuntu Eingabe: python3 code.py -n woerter_datei 3 3
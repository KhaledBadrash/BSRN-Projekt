import argparse
import logging
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
from TermTk import TTkColor
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.widget import TTkWidget


def lade_woerter(woerterPfad, xachse, yachse):
    try:
        with open(woerterPfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            anz_woerter = xachse * yachse
            zufaellige_woerter = random.sample(woerter, anz_woerter)
            return zufaellige_woerter
    except FileNotFoundError:
        erorfile = 'Die angegebene Datei konnte nicht gefunden werden'
        return erorfile

def gewinnerScreen():  #TBD
    root = ttk.TTk()
    ttk.TTkLabel(parent=root, text="Gewinner! Herzlichen Glückwunsch!")
    root.mainloop()


def main(args):
    gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)

    root = ttk.TTk(layout=gridLayout)
    v_box_layout = ttk.TTkVBoxLayout
#    gridLayout.addItem(v_box_layout,4,1)
#    v_box_layout.addWidget(ttk.TTkButton(border=True, text="Gewonnen"))
#    v_box_layout.addWidget(ttk.TTkButton(border=True, text="Gewonnen"))

    original_texts = {}
    groesse_feld = args.xachse and args.yachse

    woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
    klick_counter = [0]  # Zähler für die Klicks
    def klicker(button, original_text):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
                klick_counter[0] += 1 #Klickzähler
                # Überprüfen, ob der Gewinnerscreen nach 3 Klicks angezeigt werden soll
                #hier könnte man dsnn die ganzen berprüfungen mit JSON einbauen
                if klick_counter[0] == 3:
                    root.quit()
                    gewinnerScreen()

        return auf_knopfdruck

    buttons = []
    for i in range(groesse_feld):
        row = []
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="JOKER")
                original_texts[button] = button.text()
                gridLayout.addWidget(button, i, j)
            else:
                text = random.choice(woerter)
                button = ttk.TTkButton(parent=root, border=True, text=text)
                original_texts[button] = button.text()
                gridLayout.addWidget(button, i, j)
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

# Ubunto eingabe: python3 bingo.py -n woerter_datei 3 3

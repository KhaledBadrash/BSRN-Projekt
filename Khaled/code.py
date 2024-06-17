import argparse
import logging
import random
from argparse import ArgumentParser, Namespace
import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkWidgets.widget import TTkWidget


def ladeWoerter(woerterPfad, xachse, yachse):
    try:
        with open(woerterPfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            anz_woerter = xachse * yachse
            zufaellige_woerter = random.sample(woerter, anz_woerter)
            return zufaellige_woerter
    except FileNotFoundError:
        erorfile = 'Die angegebene Datei konnte nicht gefunden werden'
        return erorfile


def main(args):     #GUI enthalten--> in die Funktion damit die GUI in demselben Scope wie args sind
    gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=gridLayout)

    original_texts = {}
    groesse_feld = args.xachse and args.yachse
    print(f'Feldgr: {groesse_feld}')

    woerter = ladeWoerter(args.woerter_pfad, args.xachse, args.yachse) #ladeWoerter innerhalb von main, um die Liste
                                                                       #der Wörter basierend auf den Argumenten zu laden.

    def klicker(button, original_text):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
        return auf_knopfdruck

    for i in range(groesse_feld):
        for j in range(groesse_feld):
            if i == groesse_feld // 2 and j == groesse_feld // 2:
                button = ttk.TTkButton(parent=root, border=True, text="X")
                original_texts[button] = button.text()
                gridLayout.addWidget(button, i, j)
            else:
                text = random.choice(woerter)
                button = ttk.TTkButton(parent=root, border=True, text=text)
                original_texts[button] = button.text()
                gridLayout.addWidget(button, i, j)
                button.clicked.connect(klicker(button, original_texts[button]))

    root.mainloop()


if __name__ == "__main__":
    parser = ArgumentParser()           #__main__-Block, um sicherzustellen, dass args in den globalen Bereich gelangen.
    parser.add_argument('-n', '--newround', action='store_true')
    parser.add_argument('woerter_pfad', help='Wörter Pfad') #ohne Präfix um den Pfad direkt angeben zu können
    parser.add_argument('xachse', help='X-Achse', type=int)
    parser.add_argument('yachse', help='Y-Achse', type=int)
    args = parser.parse_args()

    if args.newround:
        main(args)

import argparse
import logging
import random
import time #für den Gscreen
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

def show_winner_screen(root, buttons, groesse_feld):
    colors = [TTkCfg.color.TTkColor.bg('#FF0000'), TTkCfg.color.TTkColor.bg('#00FF00'), TTkCfg.color.TTkColor.bg('#0000FF')]
    for _ in range(10):
        for i in range(groesse_feld):
            for j in range(groesse_feld):
                button = buttons[i][j]
                button.setStyle(colors[random.randint(0, len(colors) - 1)])
                if random.random() < 0.2:
                    button.setText("GEWONNEN")
                    button.setStyle(TTkCfg.color.TTkColor.bg('#FFFF00'))
        root.update()
        time.sleep(0.5)

def main(args):
    gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
    root = ttk.TTk(layout=gridLayout)

    original_texts = {}
    groesse_feld = args.xachse

    woerter = ladeWoerter(args.woerter_pfad, args.xachse, args.yachse)
    click_count = [0]  # Zähler für die Klicks
    def klicker(button, original_text):
        def auf_knopfdruck():
            if button.text() == "X":
                button.setText(original_text)
            else:
                button.setText("X")
                click_count[0] += 1
                # Überprüfen, ob der Gewinnerscreen nach 3 Klicks angezeigt werden soll
                if click_count[0] == 3:
                    show_winner_screen(root, buttons, groesse_feld)
        return auf_knopfdruck

    buttons = []
    for i in range(groesse_feld):
        row = []
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
            row.append(button)
        buttons.append(row)

    root.update()
    show_winner_screen(root, buttons, groesse_feld)
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

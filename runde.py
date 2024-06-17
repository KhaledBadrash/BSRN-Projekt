import random
import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget


# Function to change the text of a button at a specific position
def set_button_text(buttons, row, col, new_text):
    button = buttons[row][col]
    button.setText(new_text)


# Function to create a new window with a winning message
def create_win_window():
    win_root = ttk.TTkWindow(parent=root, title="Congratulations", border=True, pos=(5, 5), size=(30, 10))
    ttk.TTkLabel(parent=win_root, text="You won!", pos=(10, 4))
    win_root.raiseWidget()


gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
root = ttk.TTk(layout=gridLayout)

original_texts = {}  # speichert die Texte pro button
groesse_Feld = 5  # bestimmt Größe des Bingofeldes

file_path = "/mnt/c/Users/M02Mu/PycharmProjects/BSRN-Projekt/Textdatei"  # Textdatei für Bingofelder

with open(file_path, 'r') as file:
    words = file.read().splitlines()  # liest den Text zeilenweise

# Shuffle words and ensure no duplicates
random.shuffle(words)
if len(words) < (groesse_Feld * groesse_Feld - 1):
    raise ValueError("Not enough unique words in the file to fill the bingo grid.")

buttons = []
word_index = 0


def clicker(button, original_text, i, j):  # streicht den Text mit X-Symbol und setzt zurück auf wiederholten Knopfdruck
    def auf_knopfdruck():
        if button.text() == "X":
            button.setText(original_text)  # setzt den Text auf Buzzword zurück, wenn es markiert war
        else:
            button.setText("X")

        # Check if the button at the specific position (2, 5) has the text "X"
        if buttons[2][5].text() == "X":
            print("SDFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")  # Create the winning window if the text is "X"

    return auf_knopfdruck


for i in range(groesse_Feld):
    row = []
    for j in range(groesse_Feld):
        if i == groesse_Feld / 2 + 0.5 - 1 and j == groesse_Feld / 2 + 0.5 - 1:  # prüft ob Joker erstellt werden muss
            # wenn ja, setzt ihn in Mitte
            button = ttk.TTkButton(parent=root, border=True, text="X")  # erstellt Joker-Button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j)  # setzt button auf Position i und j, für Höhe u. Länge
        else:
            text = words[word_index]  # wählt eine zufällige Zeile und stellt das Wort in Zeile 42 zur Verfügung
            word_index += 1
            button = ttk.TTkButton(parent=root, border=True, text=text)  # erstellt normalen button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j)
            button.clicked.connect(
                clicker(button, original_texts[button], i, j))  # Beim Anklicken führt er erstellte Klick-Methode aus
        row.append(button)
    buttons.append(row)

root.mainloop()  # startet die App

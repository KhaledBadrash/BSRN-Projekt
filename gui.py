import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget

gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
root = ttk.TTk(layout=gridLayout)

original_texts = {}  #speichert die Texte pro button
groesse_Feld = 3


def clicker(button, original_text):  #streicht den Text mit X-Symbol und setzt zurück auf wiederholten Knopfdruck
    def auf_knopfdruck():
        if button.text() == "X":
            button.setText(original_text)
        else:
            button.setText("X")

    return auf_knopfdruck


for i in range(groesse_Feld):
    for j in range(groesse_Feld):
        if i == groesse_Feld / 2 + 0.5 - 1 and j == groesse_Feld / 2 + 0.5 - 1:  #prüft ob Joker erstellt werden muss
                                                                                 #wenn ja, setzt ihn in Mitte
            button = ttk.TTkButton(parent=root, border=True, text="X")  # erstellt Joker-Button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j) #setzt button auf Position i und j, für Höhe u. Länge
        else:
            button = ttk.TTkButton(parent=root, border=True, text="Button1") #erstellt normalen button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j)
            button.clicked.connect(clicker(button, original_texts[button])) #Beim Anklicken führt er erstellte Klick-Methode aus

# Start the main event loop
root.mainloop()

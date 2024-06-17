import random #zufalls...
import TermTk as ttk #gui as -- ist für abkürzung
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget#TBD

gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0) #um das feld anziegen zu lassen und die Formatierung
root = ttk.TTk(layout=gridLayout)   #root --> APP / 'Mainbenutzer'?                   #Column? --> Notwendig?

original_texts = {}  #speichert die Texte pro button /--TBD
groesse_Feld = 8  # bestimmt Größe des Bingofeldes  /X-Y rausgehalten --muss mit args noch ..

file_path = "/mnt/c/Users/M02Mu/PycharmProjects/BSRN-Projekt/Textdatei"  #Textdatei für Bingofelder
                                                                        #Args uebergabe
with open(file_path, 'r') as file:
    words = file.read().splitlines()  #liest den Text zeilenweise


def klicker(button, original_text):  #streicht den Text mit X-Symbol und setzt zurück auf wiederholten Knopfdruck
                                    #nur max 2 moves TBD
    def auf_knopfdruck():
        if button.text() == "X":            #Wenn text X
            button.setText(original_text)   #setzt den Text auf Buzzword zurück, wenn es markierd war
        else:
            button.setText("X")             #wenn nicht x dann settet es zu X

    return auf_knopfdruck   #returnt die Methode


for i in range(groesse_Feld):       #IF für Joker
    for j in range(groesse_Feld):
        if i == groesse_Feld / 2 + 0.5 - 1 and j == groesse_Feld / 2 + 0.5 - 1 and i != 2:  #prüft ob Joker erstellt werden muss
            #wenn ja, setzt ihn in Mitte
            button = ttk.TTkButton(parent=root, border=True, text="X")  # erstellt Joker-Button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j)  #setzt button auf Position i/X und j/Y, für Höhe u. Länge
        else:
            text = random.choice(words)  #wählt eine zufällige Zeile und stellt das Wort in Zeile 42 zur Verfügung
            button = ttk.TTkButton(parent=root, border=True, text=text)  #erstellt normalen button
            original_texts[button] = button.text()
            gridLayout.addWidget(button, i, j)
            button.clicked.connect(
                clicker(button, original_texts[button]))  #Beim Anklicken führt er erstellte Klick-Methode aus



#bingo_check = true

#while bingo_check:  #Versuch Schleife zur Bingo-Überprüfung zu erstellen. TBD
#    if button.text == "X":
#        bingo_check = False
root.mainloop()  #startet die App

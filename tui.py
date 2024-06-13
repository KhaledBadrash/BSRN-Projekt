#2. textual klasse
from textual.app import App, ComposeResult
from textual.layouts import grid
from textual.widgets import Static, Button
import argparse
import os  # Importiert das os-Modul für Betriebssystemfunktionen
import self


# noch anschauen :fork() , TUI RASTER, pipes abstimmen
# Definiert eine Klasse für TestButtons, die auf der Bingokarte angezeigt werden
class TestButton(Static):  #Konstruktor
    def __init__(self, wort, x, y, sender_pipe):
        super().__init__()  # Ruft den Konstruktor der Basisklasse auf
        self.wort = wort  # Initialisiert das Wort, das auf dem Button angezeigt wird
        self.x = x  # Initialisiert die x-Koordinate des Buttons
        self.y = y  # Initialisiert die y-Koordinate des Buttons
        self.sender_pipe = sender_pipe  # Initialisiert das Schreibende der Pipe

    # Erstellt einen Button mit dem Wort, das auf der Karte angezeigt wird
    def compose(self) -> ComposeResult:
        yield Button(self.wort,
                     id=f"btn_{self.x}_{self.y}")  # Erstellt und yieldet einen Button mit dem Wort und einer ID basierend auf den Koordinaten


    # Event-Handler, wenn ein Button gedrückt wird
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.control  # Holt das gedrückte Button-Objekt
        self.sende_nachricht_zu_pipe(self.x, self.y)  # Sendet die Koordinaten des gedrückten Buttons an die Pipe
        button.label = "X"  # Markiert das Feld als "X"
        button.disabled = True  # Deaktiviert den Button

    # Sendet die Koordinaten des gedrückten Buttons über die anonyme Pipe
    def sende_nachricht_zu_pipe(self, x, y):
        os.write(self.sender_pipe, f"{x},{y}\n".encode())  # Schreibt die Koordinaten als Nachricht in die Pipe


# Definiert die Haupt-App-Klasse für das Bingospiel
class WidgetApp(App):
    def __init__(self, spiel, sender_pipe):
        self.spiel = spiel  # Initialisiert das BingoSpiel-Objekt
        self.sender_pipe = sender_pipe  # Initialisiert das Schreibende der Pipe
        super().__init__()  # Ruft den Konstruktor der Basisklasse auf

    # Komposition der Widgets in der App
    def compose(self) -> ComposeResult:
        yield Static("Buzzword Bingo", classes="header")

        # Erstellt das Raster (Versuch mit grid)
        grid = Static(id="grid")
        for y in range(self.spiel.yachse):  # Iteriert über jede Zeile des Spielfelds
            for x in range(self.spiel.xachse):  # Iteriert über jede Spalte des Spielfelds
                wort = self.spiel.spielbrett[y][x]  # Holt das Wort an den angegebenen Koordinaten
                grid.mount(TestButton(wort, x, y, self.sender_pipe))
        yield grid

    # Setzt die Stile für die Widgets, sobald die App geladen ist
    def on_mount(self) -> None:
        # Setzt die Stile für das Haupt-Static-Widget
        self.widget.styles.background = "aquamarine"  # Setzt den Hintergrund des Widgets auf aquamarin
        self.widget.styles.color = "black"  # Setzt die Textfarbe auf schwarz
        self.widget.styles.border = ("heavy", "black")  # Setzt den Rahmenstil und die Rahmenfarbe
        self.widget.styles.width = 17  # Setzt die Breite des Widgets

        # Setzt die Stile für alle TestButton-Widgets

        for test_button in self.query(TestButton):  # Iteriert über alle TestButton-Widgets
            test_button.styles.layout = "horizontal"  # Setzt das Layout auf horizontal

        #Setzt die Stile für alle Button-Widgets
        for button in self.query(Button):  # Iteriert über alle Button-Widgets
            button.styles.border = ("solid", "blue")  # Setzt den Rahmenstil und die Rahmenfarbe
            button.styles.background = "lightgrey"  # Setzt den Hintergrund des Buttons auf hellgrau
            button.styles.color = "black"  # Setzt die Textfarbe auf schwarz


if __name__ == "__main__":
    # Parser für Kommandozeilenargumente
    parser = argparse.ArgumentParser(description="Buzzword-Bingo TUI")
    parser.add_argument("-pipe", type=str, required=False, help="Name der benannten Pipe")
    args = parser.parse_args()  # Parst die Kommandozeilenargumente

    # Importiert die BingoSpiel-Klasse aus der IPC-Datei
    from ipc import BingoSpiel

    # Interaktiv nach den notwendigen Parametern fragen
    wortdatei = input("Pfad zur Wortdatei: (z.B. Textdatei) ")  # Fragt den Pfad zur Wortdatei ab
    xachse = int(input("Anzahl der Felder in der Breite: "))  # Fragt die Anzahl der Felder in der Breite ab
    yachse = int(input("Anzahl der Felder in der Höhe: "))  # Fragt die Anzahl der Felder in der Höhe ab
    spieler_name = input("Name des Spielers: ")  # Fragt den Namen des Spielers ab

    # Erstelle die Pipe
    empf_pipe, sender_pipe = os.pipe()  # Erstellt ein anonymes Pipe-Paar für die Kommunikation

    # Initialisiert das Spiel mit den angegebenen Parametern
    spiel = BingoSpiel(wortdatei, xachse, yachse, spieler_name, empf_pipe,
                       sender_pipe)  # Initialisiert ein neues BingoSpiel-Objekt
    spiel.lade_woerter()  # Lädt die Wörter und generiert die Bingokarte

    # Startet die WidgetApp
    app = WidgetApp(spiel, sender_pipe)  # Initialisiert die WidgetApp
    app.run()  # Startet die App

#TBD
#Textual CSS -->
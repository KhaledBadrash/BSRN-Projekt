#2. textual klasse
from textual.app import App, ComposeResult
from textual.widgets import Static, Button
import argparse
import os  # Importiert das os-Modul für Betriebssystemfunktionen
import self
                # noch anschauen :fork() , TUI RASTER, pipes abstimmen
# Definiert eine Klasse für TestButtons, die auf der Bingokarte angezeigt werden
class TestButton(Static): #Konstruktor
    def __init__(self, wort, x, y, sender_pipe):
        super().__init__()  # Ruft den Konstruktor der Basisklasse auf
        self.wort = wort  # Initialisiert das Wort, das auf dem Button angezeigt wird
        self.x = x  # Initialisiert die x-Koordinate des Buttons
        self.y = y  # Initialisiert die y-Koordinate des Buttons
        self.sender_pipe = sender_pipe  # Initialisiert das Schreibende der Pipe

    # Erstellt einen Button mit dem Wort, das auf der Karte angezeigt wird
    def compose(self) -> ComposeResult:
        yield Button(self.wort, id=f"btn_{self.x}_{self.y}")  # Erstellt und yieldet einen Button mit dem Wort und einer ID basierend auf den Koordinaten

    CSS = """
        TestButton {
            layout: horizontal;
        }
        """
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
        self.widget = Static("Buzzword Bingo")  # Erstellt ein Static-Widget mit dem Titel "Buzzword Bingo"
        yield self.widget  # "Yieldet" das Static-Widget

        # Erstellt TestButtons basierend auf den Wörtern auf der Bingokarte
        for y in range(self.spiel.yachse):  # Iteriert über jede Zeile des Spielfelds
            for x in range(self.spiel.xachse):  # Iteriert über jede Spalte des Spielfelds
                wort = self.spiel.spielbrett[y][x]  # Holt das Wort an den angegebenen Koordinaten
                yield TestButton(wort, x, y, self.sender_pipe)  # Erstellt und yieldet einen TestButton

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
from textual.app import App, ComposeResult #https://textual.textualize.io/widgets/button/#__tabbed_1_1
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Static, Button
import os
import textual.css as css


# Definiert eine Klasse für TestButtons, die auf der Bingokarte angezeigt werden
class BButton(App[str]):

    def compose(self) -> ComposeResult: #TBD:   Wörter zuweisung + Layout
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")

    def on_mount(self) -> None:
        self.styles.background = "aquamarine"
        self.styles.color = "black"
        (self.styles).border = ("heavy", "black")
        self.styles.width = 18  #manueel mit
        self.bu

 def create_card(self, words):
        card = []
        used_words = set()

# Definiert die Haupt-App-Klasse für das Bingospiel
class WidgetApp(App):

    def compose(self) -> ComposeResult:
        self.widget = Static("Buzzword Bingo")
        yield self.widget
        yield BButton()
        yield Grid(id="grid")  # Yield the Grid widget first

    def on_mount(self) -> None: #design der
        self.button.styles.background = "aquamarine"
        self.button.styles.color = "black"
        self.widget.styles.border = ("heavy", "black")
        self.widget.styles.width = 1000  #manueel mit


if __name__ == "__main__":
    app = WidgetApp()
    app.run()

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Static, Button
import os
import textual.css as css


# Definiert eine Klasse für TestButtons, die auf der Bingokarte angezeigt werden
class TestButton(Static):

    def compose(self) -> ComposeResult:
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")
        yield Button("Test")

    def on_mount(self) -> None:
        self.widget.styles.background = "aquamarine"
        self.widget.styles.color = "black"
        self.widget.styles.border = ("heavy", "black")
        self.widget.styles.width = 30  #manueel mit



# Definiert die Haupt-App-Klasse für das Bingospiel
class WidgetApp(App):

    def compose(self) -> ComposeResult:
        self.widget = Static("Buzzword Bingo")
        yield self.widget
        yield TestButton()
        yield Grid(id="grid")  # Yield the Grid widget first

    def on_mount(self) -> None:
        self.widget.styles.background = "aquamarine"
        self.widget.styles.color = "black"
        self.widget.styles.border = ("heavy", "black")
        self.widget.styles.width = 1000  #manueel mit


if __name__ == "__main__":

    app = WidgetApp()
    app.run()

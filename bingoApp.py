from textual.app import App, ComposeResult
from textual.widgets import Static, Button


class TestButton(Static):
    def compose(self):
        #def for schleife für bestimmung der breite
        for i in range(0, 5):  #Feldgröße wird vom scanner aus der test klasse übernommen
            yield Button("Welcome")  #wörter aus txt doc ramdom zugewiesen ohne wiederholung


class WidgetApp(App):
    def compose(self) -> ComposeResult:
        self.widget = Static("Buzzword Bingo")
        yield self.widget
        # def for schleife für bestimmung der laenge
        for i in range(0, 5):
            yield TestButton()

    CSS = """
    TestButton {
        layout: horizontal;
    }
    """

    #Schleife while schleife für spieler
    #Felder auswählen --> Effekt
    #Stritt zurück
    def on_mount(self) -> None:
        self.widget.styles.background = "aquamarine"
        self.widget.styles.color = "black"
        self.widget.styles.border = ("heavy", "black")
        self.widget.styles.width = 17  #manueel mit


if __name__ == "__main__":
    app = WidgetApp()
    app.run()

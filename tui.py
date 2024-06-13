from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Static, Button
import os
import textual.css as css

# Definiert eine Klasse für TestButtons, die auf der Bingokarte angezeigt werden
class TestButton(Static):
    def __init__(self, wort, x, y, senderb_pipe):
        super().__init__(wort)  # Setze den Text des Buttons
        self.x = x
        self.y = y
        self.senderb_pipe = senderb_pipe
        self.wort = wort  # Definiere die Instanzvariable 'wort'

    def compose(self) -> ComposeResult:
        yield Button(self.wort, id=f"btn_{self.x}_{self.y}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button = event.control
        self.sende_nachricht_zu_pipe(self.x, self.y)
        button.label = "X"
        button.disabled = True

    def sende_nachricht_zu_pipe(self, x, y):
        with open(self.senderb_pipe, 'w') as pipe:
            pipe.write(f"{x},{y}\n")
            pipe.flush()


# Definiert die Haupt-App-Klasse für das Bingospiel
class WidgetApp(App):
    CSS = """
    * {
      font-family: Arial, sans-serif;
      font-size: 16px;
      color: #333;
    }

    .header {
      background-color: #f0f0f0;
      padding: 10px;
      text-align: center;
      font-size: 24px;
      font-weight: bold;
    }

    #grid {
      grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
      grid-template-rows: repeat(auto-fit, minmax(100px, 1fr));
      gap: 10px;
      padding: 10px;
    }

    Button {
      border: solid indianred;
      background: black;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      cursor: pointer;
    }

    Button:hover {
      background: #333;
      color: #fff;
    }

    Button:disabled {
      background: #ccc;
      color: #666;
      cursor: not-allowed;
    }
    """

    def __init__(self, spielw, senderw_pipe):
        self.spielw = spielw
        self.senderw_pipe = senderw_pipe
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("Buzzword Bingo", classes="header")
        yield Grid(id="grid")  # Yield the Grid widget first

    def on_mount(self) -> None:
        grid = self.query_one("#grid")

        for y in range(self.spielw.yachse):
            for x in range(self.spielw.xachse):
                wort = self.spielw.spielbrett[y][x]
                grid.mount(TestButton(wort, x, y, self.senderw_pipe))


if __name__ == "__main__":
    from ipc import BingoSpiel

    wortdatei = input("Pfad zur Wortdatei: (z.B. Textdatei) ")
    xachse = int(input("Anzahl der Felder in der Breite: "))
    yachse = int(input("Anzahl der Felder in der Höhe: "))
    spieler_name = input("Name des Spielers: ")

    empf_pipe = "/tmp/empf_pipe"
    sender_pipe = "/tmp/sender_pipe"

    if not os.path.exists(empf_pipe):
        os.mkfifo(empf_pipe)
    if not os.path.exists(sender_pipe):
        os.mkfifo(sender_pipe)

    spiel = BingoSpiel(wortdatei, xachse, yachse, spieler_name, empf_pipe, sender_pipe)
    spiel.lade_woerter()

    app = WidgetApp(spiel, sender_pipe)
    app.run()

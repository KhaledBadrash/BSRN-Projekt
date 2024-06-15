import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import TTkWidget

# Set the GridLayout as default in the terminal widget
gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=0)
root = ttk.TTk(layout=gridLayout)

# Dictionary to store the original text of each button
original_texts = {}
groesse_Feld = 5


# Function to create a button click handler for each button
def clicker(button, original_text):
    def auf_knopfdruck():
        # Toggle the button text between "Clicked!" and the original text
        if button.text() == "X":
            button.setText(original_text)
        else:
            button.setText("X")

    return auf_knopfdruck


# Create a grid of buttons and connect each to its own click handler
for i in range(groesse_Feld):
    for j in range(groesse_Feld):
        if i == groesse_Feld / 2 + 0.5 - 1 and j == groesse_Feld / 2 + 0.5 - 1:
            button = ttk.TTkButton(parent=root, border=True, text="X")
            original_texts[button] = button.text()  # Store the original text
            gridLayout.addWidget(button, i, j)
            button.clicked.connect(clicker(button, original_texts[button]))
        else:
            button = ttk.TTkButton(parent=root, border=True, text="Button1")
            original_texts[button] = button.text()  # Store the original text
            gridLayout.addWidget(button, i, j)
            button.clicked.connect(clicker(button, original_texts[button]))

# Start the main event loop
root.mainloop()

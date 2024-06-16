import random
from tkinter import Tk, Button, Label, messagebox, simpledialog


# Buzzwords aus der Datei einlesen
def read_buzzwords(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        buzzwords = [line.strip() for line in file.readlines()]
    return buzzwords


# Bingo Brett erstellen
def create_bingo_board(buzzwords, height, width):
    random.shuffle(buzzwords)
    board = []
    index = 0
    for i in range(height):
        row = []
        for j in range(width):
            if (height % 2 != 0 and width % 2 != 0 and i == height // 2 and j == width // 2):
                row.append('')  # Leere Mitte bei ungerader Höhe und Breite
            else:
                row.append(buzzwords[index])
                index += 1
        board.append(row)
    return board


# Tkinter GUI erstellen
def create_gui(board):
    root = Tk()
    root.title("Buzzword Bingo")

    def check_bingo():
        # Check rows
        for row in buttons:
            if all(btn['state'] == 'disabled' or btn['text'] == '' for btn in row):
                messagebox.showinfo("Bingo!", "Bingo! Du hast eine komplette Reihe!")
                return

        # Check columns
        for col in range(len(buttons[0])):
            if all(buttons[row][col]['state'] == 'disabled' or buttons[row][col]['text'] == '' for row in
                   range(len(buttons))):
                messagebox.showinfo("Bingo!", "Bingo! Du hast eine komplette Spalte!")
                return

        # Check main diagonal
        if all(buttons[i][i]['state'] == 'disabled' or buttons[i][i]['text'] == '' for i in range(len(buttons))):
            messagebox.showinfo("Bingo!", "Bingo! Du hast eine komplette Diagonale!")
            return

        # Check anti-diagonal
        if all(buttons[i][len(buttons) - 1 - i]['state'] == 'disabled' or buttons[i][len(buttons) - 1 - i]['text'] == ''
               for i in range(len(buttons))):
            messagebox.showinfo("Bingo!", "Bingo! Du hast eine komplette Diagonale!")
            return

    buttons = []
    for i, row in enumerate(board):
        button_row = []
        for j, word in enumerate(row):
            btn = Button(root, text=word, width=15, height=3)

            def toggle_state(b=btn):
                if b['state'] == 'normal':
                    b.config(state='disabled')
                else:
                    b.config(state='normal')
                check_bingo()

            btn.config(command=toggle_state)
            btn.grid(row=i, column=j)
            button_row.append(btn)
        buttons.append(button_row)

    root.mainloop()


if __name__ == "__main__":
    # Datei mit Buzzwords
    filename = 'buzzwords.txt'
    buzzwords = read_buzzwords(filename)

    # Benutzer nach der Brettgröße fragen
    root = Tk()
    root.withdraw()  # Hauptfenster verstecken, da wir nur die Eingabeaufforderungen benötigen

    height = simpledialog.askinteger("Eingabe", "Geben Sie die Höhe des Bingo-Bretts ein:")
    width = simpledialog.askinteger("Eingabe", "Geben Sie die Breite des Bingo-Bretts ein:")

    if height * width > len(buzzwords) + (1 if height % 2 != 0 and width % 2 != 0 else 0):
        messagebox.showerror("Fehler", "Nicht genügend Buzzwords für diese Brettgröße!")
        root.destroy()
    else:
        bingo_board = create_bingo_board(buzzwords, height, width)
        root.destroy()  # Eingabeaufforderungsfenster schließen
        create_gui(bingo_board)

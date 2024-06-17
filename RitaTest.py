import random
import pytermtk as tk
from pytermtk import dialog


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
            if (height == 5 and width == 5 or height == 7 and width == 7) and (i == height // 2 and j == width // 2):
                row.append('')  # Leere Mitte bei 5x5 und 7x7
            else:
                row.append(buzzwords[index])
                index += 1
        board.append(row)
    return board


# GUI erstellen
def create_gui(players, boards):
    app = tk.App()
    current_player = [0]

    def update_current_player_label():
        current_player_label.config(text=f"Aktueller Spieler: {players[current_player[0]]}")

    def check_bingo(player_index):
        board = buttons[player_index]
        # Check rows
        for row in board:
            if all(btn['state'] == 'disabled' or btn['text'] == '' for btn in row):
                tk.messagebox.showinfo("Bingo!", f"Bingo! {players[player_index]} hat eine komplette Reihe!")
                return

        # Check columns
        for col in range(len(board[0])):
            if all(board[row][col]['state'] == 'disabled' or board[row][col]['text'] == '' for row in
                   range(len(board))):
                tk.messagebox.showinfo("Bingo!", f"Bingo! {players[player_index]} hat eine komplette Spalte!")
                return

        # Check main diagonal
        if all(board[i][i]['state'] == 'disabled' or board[i][i]['text'] == '' for i in range(len(board))):
            tk.messagebox.showinfo("Bingo!", f"Bingo! {players[player_index]} hat eine komplette Diagonale!")
            return

        # Check anti-diagonal
        if all(board[i][len(board) - 1 - i]['state'] == 'disabled' or board[i][len(board) - 1 - i]['text'] == '' for i
               in range(len(board))):
            tk.messagebox.showinfo("Bingo!", f"Bingo! {players[player_index]} hat eine komplette Diagonale!")
            return

    buttons = []
    button_states = []

    for player_index, board in enumerate(boards):
        player_buttons = []
        player_states = []
        for i, row in enumerate(board):
            button_row = []
            state_row = []
            for j, word in enumerate(row):
                btn = tk.Button(text=word, width=15, height=3, state='disabled')
                state_row.append('normal')

                def toggle_state(b=btn, p_index=player_index, i=i, j=j):
                    if button_states[p_index][i][j] == 'normal':
                        b.config(state='disabled')
                        button_states[p_index][i][j] = 'disabled'
                    else:
                        b.config(state='normal')
                        button_states[p_index][i][j] = 'normal'
                    check_bingo(p_index)
                    # Nächster Spieler ist dran
                    current_player[0] = (current_player[0] + 1) % len(players)
                    update_current_player_label()
                    enable_current_player_buttons()

                btn.config(command=toggle_state)
                btn.grid(row=i + 2, column=j + player_index * (len(board[0]) + 1))
                button_row.append(btn)
            player_buttons.append(button_row)
            player_states.append(state_row)
        buttons.append(player_buttons)
        button_states.append(player_states)

    current_player_label = tk.Label(text="")
    current_player_label.grid(row=0, column=0, columnspan=len(players) * (len(boards[0][0]) + 1))
    update_current_player_label()

    def enable_current_player_buttons():
        for p_index, board in enumerate(buttons):
            for i, row in enumerate(board):
                for j, btn in enumerate(row):
                    if p_index == current_player[0]:
                        if button_states[p_index][i][j] == 'normal' and btn['text'] != '':
                            btn.config(state='normal')
                    else:
                        btn.config(state='disabled')

    enable_current_player_buttons()

    app.run()


if __name__ == "__main__":
    # Datei mit Buzzwords
    filename = 'Textdatei.txt'
    buzzwords = read_buzzwords(filename)

    # Benutzer nach der Anzahl der Spieler fragen
    num_players = dialog.ask_integer("Eingabe", "Geben Sie die Anzahl der Spieler ein:")

    # Spielernamen eingeben
    players = []
    for i in range(num_players):
        player_name = dialog.ask_string("Eingabe", f"Geben Sie den Namen des Spielers {i + 1} ein:")
        players.append(player_name)

    # Benutzer nach der Brettgröße fragen
    height = dialog.ask_integer("Eingabe", "Geben Sie die Höhe des Bingo-Bretts ein:")
    width = dialog.ask_integer("Eingabe", "Geben Sie die Breite des Bingo-Bretts ein:")

    if height * width > len(buzzwords) + (1 if height == 5 and width == 5 or height == 7 and width == 7 else 0):
        tk.messagebox.showerror("Fehler", "Nicht genügend Buzzwords für diese Brettgröße!")
    else:
        boards = [create_bingo_board(buzzwords.copy(), height, width) for _ in range(num_players)]
        create_gui(players, boards)

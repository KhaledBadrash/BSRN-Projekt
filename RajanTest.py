import os
import logging
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from datetime import datetime
import multiprocessing


def create_log_file(player_name, log_directory):
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    log_file_name = os.path.join(log_directory, f"log-{date_string}-{player_name}.txt")
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Log-Datei für {player_name} erstellt.")


def generate_grid(rows, columns, buzzwords, player_name, log_directory, word_queue, my_turn_event, other_turn_event,
                  transparent=None):
    create_log_file(player_name, log_directory)
    logging.info("Das Spiel beginnt!")

    root = tk.Tk()
    root.title(f"Buzzword Bingo - {player_name}")
    root.geometry("720x480")

    icon_path = r"C:\Users\rajan\PyCharm\png-transparent-bingo-card-free-content-one-day-s-game-text-logo.png"
    if os.path.exists(icon_path):
        img = Image.open(icon_path)
        photo = ImageTk.PhotoImage(img)
        root.iconphoto(False, photo)

    grid_frame = tk.Frame(root)
    grid_frame.pack(fill=tk.BOTH, expand=True)

    for i in range(rows):
        grid_frame.rowconfigure(i, weight=1)
    for j in range(columns):
        grid_frame.columnconfigure(j, weight=1)

    button_state = {}

    def on_button_click(button):
        if button_state.get(button, False):
            button.config(bg="SystemButtonFace", relief="raised")
            logging.info(f"Auswahl von '{button['text']}' rückgängig gemacht.")
            button_state[button] = False
        else:
            button.config(bg="green", relief="sunken")
            logging.info(f"Auswahl von '{button['text']}' gemacht.")
            button_state[button] = True

        if check_win(rows, columns):
            messagebox.showinfo("Gewonnen!", f"Herzlichen Glückwunsch, {player_name}! Du hast gewonnen!")
            logging.info(f"{player_name} hat gewonnen!")
            root.quit()

    def check_win(rows, columns):
        for row in buttons:
            if all(button_state[button] for button in row):
                return True
        for j in range(columns):
            if all(button_state[buttons[i][j]] for i in range(rows)):
                return True
        return False

    buttons = []
    for i in range(rows):
        row_buttons = []
        unique_buzzwords = random.sample(buzzwords, columns)
        for j, buzzword in enumerate(unique_buzzwords):
            button = tk.Button(grid_frame, text=buzzword, font=('Times New Roman', 14))
            button.grid(row=i, column=j, sticky="nsew")
            button.config(command=lambda b=button: on_button_click(b))
            button_state[button] = False
            row_buttons.append(button)
        buttons.append(row_buttons)

    def update_board():
        if my_turn_event.is_set():
            try:
                new_word = word_queue.get_nowait()
                logging.info(f"Neues Wort empfangen: {new_word}")
                for row in buttons:
                    for button in row:
                        if button['text'] == new_word:
                            button.invoke()
                my_turn_event.clear()
                other_turn_event.set()
            except queue.Empty:
                pass
        root.after(100, update_board)

    root.after(100, update_board)
    root.mainloop()


def read_buzzword(roundfile):
    with open(roundfile, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]


def bingo_master(word_queue, buzzwords, player1_turn_event, player2_turn_event):
    while buzzwords:
        player1_turn_event.wait()
        if not buzzwords:
            break
        word = buzzwords.pop(0)
        print(f"Master zieht das Wort: {word}")
        word_queue.put(word)
        player1_turn_event.clear()
        player2_turn_event.set()


def main():
    player_name1 = input("Willkommen zum Buzzword-Bingo \n\nBitte geben Sie den Namen des 1. Spielers ein: ")
    player_name2 = input("Bitte geben Sie den Namen des 2. Spielers ein: ")
    log_directory = input("Gib den Pfad zum Verzeichnis für die Log-Datei ein: ")
    roundfile = input("Gib den Pfad zur Textdatei ein: ")

    rows = int(input("Anzahl der Zeilen (Y-Achse): "))
    columns = int(input("Anzahl der Spalten (X-Achse): "))

    buzzwords = read_buzzword(roundfile)

    word_queue = multiprocessing.Queue()
    player1_turn_event = multiprocessing.Event()
    player2_turn_event = multiprocessing.Event()

    player1_turn_event.set()

    master_process = multiprocessing.Process(target=bingo_master, args=(
    word_queue, buzzwords.copy(), player1_turn_event, player2_turn_event))
    master_process.start()

    generate_grid(rows, columns, buzzwords.copy(), player_name1, log_directory, word_queue, player1_turn_event,
                  player2_turn_event)
    generate_grid(rows, columns, buzzwords.copy(), player_name2, log_directory, word_queue, player2_turn_event,
                  player1_turn_event)

    master_process.terminate()


if __name__ == "__main__":
    main()
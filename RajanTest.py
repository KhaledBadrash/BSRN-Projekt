import curses
import random
import time

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def create_bingo_card(words, size):
    return [random.sample(words, size) for _ in range(size)]

def display_bingo_card(stdscr, card, start_y, start_x, size):
    for i in range(size):
        for j in range(size):
            stdscr.addstr(start_y + i, start_x + j * 15, f"{card[i][j]:<14}")

def check_word_on_card(card, word):
    for row in card:
        if word in row:
            return True
    return False

def mark_word_on_card(card, word):
    for row in card:
        if word in row:
            row[row.index(word)] = "X"

def check_winner(card, size):
    if all(card[i][i] == "X" for i in range(size)) or all(card[i][size - 1 - i] == "X" for i in range(size)):
        return True
    for i in range(size):
        if all(card[i][j] == "X" for j in range(size)) or all(card[j][i] == "X" for j in range(size)):
            return True
    return False

def get_input(stdscr, prompt):
    curses.echo()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    input_str = stdscr.getstr().decode('utf-8')
    curses.noecho()
    stdscr.clear()
    return input_str

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Willkommen zum Bingo Buzzword Spiel!", curses.color_pair(1)| curses.A_BOLD)
    stdscr.addstr(1, 0, "-----------------------------------------")

    # Anzahl der Spieler abfragen
    num_players_str = get_input(stdscr, "Bitte geben Sie die Anzahl der Spieler ein: ")
    num_players = int(num_players_str)

    # Größe der Bingo-Karten abfragen
    card_size_str = get_input(stdscr, "Bitte geben Sie die Größe der Bingo-Karten (z.B. 5 für 5x5) ein: ")
    card_size = int(card_size_str)

    return num_players, card_size

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    num_players, card_size = main_menu(stdscr)

    words = read_words_from_file("Textdatei")
    player_cards = [create_bingo_card(words, card_size) for _ in range(num_players)]

    for i, card in enumerate(player_cards, start=1):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Spieler {i} Karte:")
        display_bingo_card(stdscr, card, 2, 0, card_size)
        stdscr.refresh()
        time.sleep(2)

    drawn_words = []
    while True:
        drawn_word = random.choice(words)
        if drawn_word in drawn_words:
            continue
        drawn_words.append(drawn_word)
        stdscr.clear()
        stdscr.addstr(0, 0, f"Das gezogene Wort lautet: {drawn_word}", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(2)

        for i, card in enumerate(player_cards, start=1):
            if check_word_on_card(card, drawn_word):
                mark_word_on_card(card, drawn_word)
                stdscr.clear()
                stdscr.addstr(0, 0, f"Spieler {i} hat das Wort {drawn_word} auf der Karte!", curses.color_pair(1))
                display_bingo_card(stdscr, card, 2, 0, card_size)
                stdscr.refresh()
                time.sleep(5)
                if check_winner(card, card_size):
                    stdscr.addstr(7, 0, f"Spieler {i} hat gewonnen!", curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(5)
                    return

if __name__ == "__main__":
    curses.wrapper(main)
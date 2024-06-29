import multiprocessing  #MP -> Verwaltung von Prozessen
import os               #für Betriebssystem-Interaktionen
import random
from argparse import ArgumentParser, Namespace #Verarbeitung von Kommandozeilenargumenten -> Terminal args
import json   #Verarbeitung von JSON-Daten
from datetime import datetime #Datums- und Zeitfunktionen
from multiprocessing import Process, Pipe #Prozessverwaltung und IPC
import TermTk as ttk #GUI
import time
import threading
import sys


def parse_args():
    #Funktion für die Kommandozeilenargumente
    parser = ArgumentParser(description="Starte eine neue Spielrunde oder trete einer bestehenden Runde bei")
    subparsers = parser.add_subparsers(dest='command', required=True)

    #Subparser für den Host
    host_parser = subparsers.add_parser('host', help='Starte eine neue Runde als Host')
    host_parser.add_argument('-n', '--newround', action='store_true', help="Startet eine neue Runde")
    host_parser.add_argument('woerter_pfad', help='Pfad zur Wörterliste')
    host_parser.add_argument('xachse', type=int, help='Anzahl der Zeilen')
    host_parser.add_argument('yachse', type=int, help='Anzahl der Spalten')
    host_parser.add_argument('personal_name', help='Name des Hosts')
    host_parser.add_argument('max_spieler', type=int, help='Maximale Anzahl an Spielern')

    #Subparser für Spieler
    player_parser = subparsers.add_parser('join', help='Tritt einer bestehenden Runde bei')
    player_parser.add_argument('personal_name', help='Dein Name')

    return parser.parse_args()


def lade_woerter(woerter_pfad, xachse, yachse):
    # Funktion zum Laden der Wörter aus der Wörter-Datei
    try:
        with open(woerter_pfad, 'r', encoding='utf-8') as file: #Öffne die Wörterdatei
            woerter = [line.strip() for line in file.readlines()]  #Liest alle Zeilen und entfernt Leerzeichen
            anz_woerter = xachse * yachse #Berechne die Anzahl der benötigten Wörter anhand der args --> Feldgroeße
            if len(woerter) < anz_woerter:
                raise ValueError("Nicht genug Wörter in der Datei.")
            zufaellige_woerter = random.sample(woerter, anz_woerter)
            return zufaellige_woerter
    except FileNotFoundError:
        raise FileNotFoundError('Die angegebene Datei konnte nicht gefunden werden')



def setup_pipes(): # Funktion: Einrichtung der Pipes für die IPC
    host_to_players_path = '/tmp/host_to_players' # Pfad für die Pipe vom Host zu den Spielern
    players_to_host_path = '/tmp/players_to_host'  # Pfad für die Pipe von den Spielern zum Host

    if os.path.exists(host_to_players_path):
        os.remove(host_to_players_path) # Entferne vorhandene Pipe, falls sie existiert [Fehlerbehebung]
    if os.path.exists(players_to_host_path):
        os.remove(players_to_host_path) # Same[Fehlerbehebung]

    os.mkfifo(host_to_players_path, mode=0o666)  #Erstelle FIFO-Pipe: Kommunikation vom Host zu den Spielern
    os.mkfifo(players_to_host_path, mode=0o666)  #Erstelle FIFO-Pipe: Kommunikation vom Host zu den Spielern
    #mode-Parameter definiert die Zugriffsberechtigungen:
                                #0o666 --> 6 für Lesen und Schreiben
    #                                      4 für Lesen
    #                                      2 für Schreiben


def cleanup_pipes():
    #Funktion: Entfernung der Pipes nach Benutzung [Fehlerbehebung]
    os.unlink('/tmp/host_to_players') #Entferne: Pipe Host --> Spielern
    os.unlink('/tmp/players_to_host') #Entferne: Pipe Spieler --> Host

def read_json_log():
    #Funktion: liest die JSON-Logs

    try:
        with open('log_data_host.json', 'r') as file: # Öffne die Log-Datei
            data = json.load(file)  # Lade die JSON-Daten
            if not isinstance(data, list):
                return []
            return data #Gib die Log-Daten zurück
    except (FileNotFoundError, json.JSONDecodeError):
        return [] #return leere Liste, wenn die Datei nicht gefunden wird
                    # oder ein JSON-Decode-Fehler auftritt



def write_json_log(data):
    # Funktion: schreibt JSON-Logs
    with open('log_data_host.json', 'w') as file: #Öffnet Log-Datei (w) zum Schreiben
        json.dump(data, file, indent=4) # Schreibe die JSON-Daten mit Einrückungen
                        #indent=4: Formatierung der JSON jedes verschachtelte Element
        #                           um 4 Leerzeichen weiter eingerückt wird


def clear_json_log():
    # Funktion: leert die Logs
    write_json_log([]) # Leere Log durch leere Liste []


def log_game_start(host_name, max_spieler):
    # Funktion: Loggt den Spielstart
    logs = read_json_log()  #liest die aktuelle Log
    start_data = {
        'host_name': host_name,
        'Event': "Spiel gestartet",
        'max_spieler': max_spieler,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(start_data) # w Startdaten --> Log
    write_json_log(logs)


def log_win(host_name):
    #Funktion: Loggt den Gewinner
    logs = read_json_log()
    win_data = {
        'Spieler_Name': host_name,
        'Event': "GEWONNEN",
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
    }
    logs.append(win_data)
    write_json_log(logs)


def pruefe_bingo(max_feld, logs):
    # Funktion:
    marked_positions = [(log.get('x_wert'), log.get('y_wert')) for log in logs
                        if log.get('button_text') == '---' or log.get('JOKER') == '---']

    # Überprüft horizontale Linien
    for i in range(max_feld):
        if all((i, j) in marked_positions for j in range(max_feld)):
            return True

    # Überprüft vertikale Linien
    for j in range(max_feld):
        if all((i, j) in marked_positions for i in range(max_feld)):
            return True

    # Überprüft diagonale Linien (von links oben nach rechts unten)
    if all((i, i) in marked_positions for i in range(max_feld)):
        return True

    # Überprüft diagonale Linien (von rechts oben nach links unten)
    if all((i, max_feld - 1 - i) in marked_positions for i in range(max_feld)):
        return True

    return False


def winner_screen(parent, personal_name):
    # Funktion: Zeigt den Gewinnerscreen an
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    win_root.raiseWidget()
    log_win(personal_name)  # Loggen des Gewinnereignisses
    win_root.show()

    name_root = ttk.TTkWindow(parent=parent, title=f"{personal_name} ist der Gewinner!", border=True, pos=(35, 20), size=(30, 10))
    name_root.raiseWidget()
    name_root.show()

    # Animation: Farbe des Titels wiederholt ändern (BONI)
    def animate_title():
        colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
                  ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
        index = 0
        while True:
            win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
            name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
            index += 1
            time.sleep(0.1)
            parent.update()

    #Starte die Animation in einem separaten Thread, um die GUI reaktionsfähig zu halten/ müsst man aber nicht so machen
    # Weil die Tasten nach dem Screen deaktiviert sind
    animation_thread = threading.Thread(target=animate_title, daemon=True)
    animation_thread.start()

game_over = False # globale Variable für die Prüfung ob das Spiel Vorbei ist

class GameApp:

    def __init__(self, args, player_name=None):
        self.args = args
        self.player_name = player_name
        self.player_name = player_name or args.personal_name
        self.woerter = lade_woerter(args.woerter_pfad, args.xachse, args.yachse)
        self.root = ttk.TTk()
        self.original_texts = {}
        print(f"DEBUG: GameApp initialisiert für {player_name}.")


    def run(self):
        grid_layout = ttk.TTkGridLayout(parent=self.root)
        self.root.setLayout(grid_layout)

        for i in range(self.args.xachse):
            for j in range(self.args.yachse):
                if i == self.args.xachse // 2 and j == self.args.yachse // 2:
                    button = ttk.TTkButton(parent=self.root, text='---', border=True, pos=(i, j))
                    grid_layout.addWidget(button, i, j)
                    self.log_joker('---', i, j, datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr'))
                else:
                    wort = self.woerter[i * self.args.yachse + j]
                    button = ttk.TTkButton(parent=self.root, text=wort, border=True, pos=(i, j))
                    self.original_texts[button] = button.text()
                    button.clicked.connect(lambda btn=button, x=i, y=j: self.button_click(btn, x, y))
                    grid_layout.addWidget(button, i, j)

        self.root.mainloop()

    def button_click(self, button, x_wert, y_wert):

        global game_over

        if game_over:
            return

        logs = read_json_log()
        if button.text() == "---":
            # Find the log entry corresponding to the button being reverted
            log_index = next(
                (index for (index, d) in enumerate(logs) if d.get("x_wert") == x_wert and d.get("y_wert") == y_wert),
                None)
            if log_index is not None and log_index == len(logs) - 1:
                logs.pop(log_index)  # Remove the log entry
                button.setText(self.original_texts[button])  # Set button text to original text
                write_json_log(logs)
        else:
            original_text = button.text()
            button.setText("---")
            auswahl_zeitpunkt = datetime.now().strftime('%d-%m-%Y %H:%M:%S Uhr')
            self.log_data_json(original_text, x_wert, y_wert, auswahl_zeitpunkt)
            log_data = {
                'spieler_name': self.player_name,
                'button_text': '---',
                'x_wert': x_wert,
                'y_wert': y_wert,
                'auswahl_zeitpunkt': auswahl_zeitpunkt
            }
            logs.append(log_data)
            write_json_log(logs)

        # Check for bingo
        if pruefe_bingo(self.args.xachse, logs):
            game_over = True
            winner_screen(self.root, self.player_name)

    def log_joker(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = read_json_log()
        logs.append({
            'Spieler_Name': self.player_name,
            'JOKER': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        write_json_log(logs)

    def log_data_json(self, button_text, x_wert, y_wert, auswahl_zeitpunkt):
        if isinstance(button_text, ttk.TTkString):
            button_text = str(button_text)
        elif not isinstance(button_text, str):
            button_text = repr(button_text)

        logs = read_json_log()
        logs.append({
            'host_name': self.player_name,
            'button_text': button_text,
            'x_wert': x_wert,
            'y_wert': y_wert,
            'auswahl_zeitpunkt': auswahl_zeitpunkt
        })
        write_json_log(logs)


def run_game_gui(player_name, xachse, yachse):
    # Funktion zum Starten der Spiel-GUI
    args = Namespace(
        woerter_pfad='woerter_datei',
        xachse=xachse,
        yachse=yachse,
        personal_name=player_name,
    )
    app = GameApp(args, player_name)
    app.run()
    print(f"GUI startet für Spieler {player_name} mit den Koordinaten ({xachse}, {yachse})")

def main(args):
    #Hauptfunktion zur Steuerung des Spiels
    print(f"DEBUG: main() aufgerufen mit args: {args}")
    if args.command == 'host' and args.newround:
        clear_json_log()
        log_game_start(args.personal_name, args.max_spieler)

        parent_conn, child_conn = Pipe() # Erstelle ein Pipe-Paar: ermöglicht bidirektionale Kommunikation zwischen Prozessen
        connection_process = Process(target=handle_host_connections, args=(args, child_conn)) # Erstelle einen neuen Prozess durch die Klasse Process aus dem MP Modul
        multiprocessing.set_start_method('fork', force=True)  #jetzt wird geforkt, kein Multithreading
                                                     #Setzt den Startmodus für Prozesse auf "fork" um threading zu vermeiden
        connection_process.start() #Starte den Verbindungsprozess

        if parent_conn.recv(): # Parent (Host) wartet auf Nachricht vom Child/Verbindungsprozess
            app = GameApp(args, args.personal_name)
            app.run()

        connection_process.join()  #wartet bis der Verbindungsprozess zu Ende ist
        print("DEBUG: Host-Verbindungsprozess beendet.")
    elif args.command == 'join':
        player_process(args.personal_name) # Starte den Spielerprozess
    else:
        print("Kein gültiges Argument zum Starten oder Beitreten einer Runde angegeben.")


def handle_host_connections(args, conn):
    # Funktion zur Handhabung der Host-Verbindungen
    print(f"Host-Prozess gestartet mit PID: {os.getpid()}")
    anz_spieler = args.max_spieler
    print(f"DEBUG: Warte auf {anz_spieler} Spieler...")
    setup_pipes() #Richte die Pipes ein
    connected_players = 0

    with open('/tmp/host_to_players', 'w') as h2p, open('/tmp/players_to_host', 'r') as p2h:
        while connected_players < anz_spieler:
            print("Warten auf READY-Nachricht von einem Spieler...")
            line = p2h.readline().strip() # Lese eine Zeile von den Spielern
            if line == 'READY':
                connected_players += 1
                print(f"Spieler {connected_players} verbunden.")
                print(f"Warte auf {anz_spieler - connected_players} Spieler...")

        print("Alle Spieler sind verbunden. Das Spiel beginnt!")
        for _ in range(anz_spieler):
            h2p.write(f'START {args.xachse} {args.yachse}\n') # Sende START-Nachricht an die Spieler
            h2p.flush() #schreibt alle gepufferten Daten sofort in die Pipe --> keine Verzögerung
            print(f"START-Nachricht an {connected_players} Spieler gesendet.")

        conn.send(True)  #Sende Nachricht an den Hauptprozess, dass das Spiel gestartet werden kann

    cleanup_pipes()  # Entferne die Pipes
    conn.close() # Schließe die Pipe-Verbindung



def player_process(player_name):
    print(f"Spieler-Prozess gestartet mit PID: {os.getpid()}")
    #hilfreich um später zu sehen, ob es tatsächliche Prozesse sind

    try:
        h2p = open('/tmp/host_to_players', 'r')
        p2h = open('/tmp/players_to_host', 'w')
    except Exception as e:
        print(f"Fehler beim Öffnen der Pipes: {e}")
        return

    print(f"Spieler {player_name} ist bereit.")

    try:
        p2h.write('READY\n') #Sende READY-Nachricht an den Host
        p2h.flush()
        print("DEBUG: READY-Nachricht an Host gesendet.")
    except Exception as e:
        print(f"DEBUG: Fehler beim Senden der READY-Nachricht: {e}")
        h2p.close()
        p2h.close()
        return

    while True:
        print("DEBUG: Warten auf START-Nachricht vom Host...")
        try:
            start_message = h2p.readline().strip()  #Lese START-Nachricht vom Host
            if start_message:
                print(f"Nachricht vom Host empfangen: {start_message}")
                if start_message.startswith('START'):
                    _, xachse, yachse = start_message.split()
                    xachse = int(xachse)
                    yachse = int(yachse)
                    print(f"DEBUG: Spiel beginnt für {player_name} mit den Koordinaten ({xachse}, {yachse})")
                    run_game_gui(player_name, xachse, yachse) # Starte die Spiel-GUI
                    break
            else:
                print("Keine Nachricht empfangen. Warten auf Nachricht...")
                time.sleep(1)
        except Exception as e:
            print(f"Fehler beim Lesen der START-Nachricht: {e}")
            break

    try:
        h2p.close()
        p2h.close()
    except Exception as e:
        print(f"Fehler beim Schließen der Pipes: {e}")


def game():
    args = parse_args()
    main(args)


if __name__ == "__main__":
    game()

#python3 multi.py host -n woerter_datei 5 5 HostName 3

#python3 multi.py join SpielerName1
#python3 multi.py join SpielerName2
#python3 multi.py join SpielerName3


#pstree -p | grep python3
#cd KhaledMohamed
#python3 multi.py host -n woerter_datei 5 5 khaled 1

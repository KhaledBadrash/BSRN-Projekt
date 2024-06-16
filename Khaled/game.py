import logging
from argparse import ArgumentParser, Namespace


def lade_woerter(woerter_pfad, info, xachse, yachse):

    try:
        with open(woerter_pfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            return woerter

    except FileNotFoundError:
        erorfile = 'Die angegebene Datei konnte nicht gefunden werden'
        return erorfile


def rechner_prog():

    parser = ArgumentParser()

    parser.add_argument('-s', '--start', required=True)
    parser.add_argument('-w', '--woerter_pfad', help='Worter_pfad')
    parser.add_argument('-r', '--runden_info', help='Datei für die loggs')
    parser.add_argument('-x', '--xachse', help='X-Achse', type=int)
    parser.add_argument('-x', '--yachse', help='Y-Achse', type=int)

    args: Namespace = parser.parse_args()





if __name__ == "__main__":

    rechner_prog()
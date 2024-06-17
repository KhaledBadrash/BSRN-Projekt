import logging
import random
from argparse import ArgumentParser, Namespace


def lade_woerter(woerter_pfad, xachse, yachse): #info

    try:
        with open(woerter_pfad, 'r', encoding='utf-8') as file:
            woerter = [line.strip() for line in file.readlines()]
            anz_woerter = xachse * yachse

            zufaellige_woerter = random.sample(woerter, anz_woerter)
            return print(zufaellige_woerter)

    except FileNotFoundError:
        erorfile = 'Die angegebene Datei konnte nicht gefunden werden'
        return erorfile


def rechner_prog():

    parser = ArgumentParser()

    parser.add_argument('-s', '--start')
    parser.add_argument('-w', '--woerter_pfad', help='Worter_pfad', required=True)
    #parser.add_argument('-r', '--runden_info', help='Datei für die loggs') --> brauch man net angeben
    parser.add_argument('-x', '--xachse', help='X-Achse', type=int)
    parser.add_argument('-y', '--yachse', help='Y-Achse', type=int)

    args: Namespace = parser.parse_args()

    if args.start == True:
        lade_woerter(args.woerter_pfad, args.x, args.y)






if __name__ == "__main__":

    rechner_prog()
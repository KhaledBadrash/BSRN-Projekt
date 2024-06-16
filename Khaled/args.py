from argparse import ArgumentParser, Namespace


def rechner_prog():

    parser = ArgumentParser()

    parser.add_argument('-s ', '--start ', required=False,
                        type=int, choices=[1, 2])
    parser.add_argument('zahl', help='Zahl', type=int)
    parser.add_argument('potenz', type=int)
    parser.add_argument('-t', '--text', help='Rechnung wird als Text angezeigt',
                        type=int, choices=[0, 1, 2])

    args: Namespace = parser.parse_args()

    if args.start == 1:
        if args.text == 0:
            print(f'ihre Zahl ist: {args.zahl}')
        elif args.text == 1:
            print(f'{args.zahl} ** {args.potenz} (Option 1)')
        elif args.text == 2:
            print(f'{args.zahl} hoch {args.potenz} ist: {args.zahl} ** {args.potenz}')

        else:
            while True:
                try:
                    args.hochzwei = int(input("Bitte geben Sie eine neue Zahl ein: "))
                    print(f'Neueingabe hochzwei ist: {args.hochzwei ** 2}')
                    break
                except ValueError:
                    print("Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")

    else:
        print('Auf Wiedersehen')


if __name__ == "__main__":

    rechner_prog()

    #    print('Um den Rechner zu starten koennen sie -s oder --start.\n'
    #      'Sie muessen aber 1 oder 2 angeben\n'
    #      '1 = Starte den Rechner\n'
    #      '2 = Starte den Rechner NICHT')
    #print('Gebe Sie Ganzzahl an welche du potenzieren willst an')
    #print('Gebe Sie die ganzzahlige Potenz an')
    #print('Um den den Text auszugeben zu starten koennen sie -t oder --text.\n'
    #      'Sie muessen aber 1,2 oder 3 angeben\n'
    #      '1 = Ausgabe Iher Zahl\n'
    #      '2 = Ausgabe der Lösung\n'
    #      '3 = Genaue Ausgabe der Lösung')

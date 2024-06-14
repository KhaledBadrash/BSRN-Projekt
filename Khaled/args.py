from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

parser.add_argument('eingabe')

args: Namespace = parser.parse_args()
print(args.eingabe)

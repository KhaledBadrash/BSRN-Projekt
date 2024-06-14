from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

parser.add_argument('echo', help='Echo message')

args: Namespace = parser.parse_args()
print(args.echo)

from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

parser.add_argument('hochzwei',help='hoch2',type=int)
parser.add_argument('-v','--verbose',help='verbose',action='store_true',required=True)
#-v gleiche wie --verbose
args: Namespace = parser.parse_args()

if args.verbose:
    print(f'{args.hochzwei} hochzwei ist: {args.hochzwei ** 2}')
else:
    print(args.hochzwei ** 2)


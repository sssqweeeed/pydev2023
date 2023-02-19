from argparse import ArgumentParser
import cowsay

parser = ArgumentParser(
    prog='Cowsay', description='Cowsay generates an ASCII picture of a cow saying something provided by the user. If run with no arguments, it accepts standard input, word-wraps the message given at about 40 columns, and prints the cow saying the given message on standard output.'
)
parser.add_argument(
    '-e', dest='eyes', action='store', default='oo',
    help="Selects the appearance of the cow's eyes, in which case the first two characters of the argument string eye_string will be used. The default eyes are 'oo'."
)
parser.add_argument(
    '-f', dest='cowfile', action='store', default='',
    help="specifies a particular cow picture file (''cowfile'') to use. If the cowfile spec contains '/' then it will be interpreted as a path relative to the current directory."
)
parser.add_argument(
    '-n', dest='wrap_text', action='store_false',
    help="If it is specified, the given message will not be word-wrapped."
)
parser.add_argument(
    '-l', dest='l', action='store_true',
    help="List all cowfiles on the current COWPATH"
)
parser.add_argument(
    '-T', dest='tongue', action='store', default='',
    help="The tongue is similarly configurable through -T and tongue_string; it must be two characters and does not appear by default. "
)
parser.add_argument(
    '-W', dest='width', action='store', default=40, type=int,
    help="Specifies roughly where the message should be wrapped."
)
parser.add_argument(
    '-b', dest='b', action='store_true',
    help="Initiates Borg mode"
)
parser.add_argument(
    '-d', dest='d', action='store_true',
    help="Causes the cow to appear dead"
)
parser.add_argument(
    '-g', dest='g', action='store_true',
    help="Invokes greedy mode"
)
parser.add_argument(
    '-p', dest='p', action='store_true',
    help="Causes a state of paranoia to come over the cow"
)
parser.add_argument(
    '-s', dest='s', action='store_true',
    help="Makes the cow appear thoroughly stoned"
)
parser.add_argument(
    '-t', dest='t', action='store_true',
    help="Yields a tired cow"
)
parser.add_argument(
    '-w', dest='w', action='store_true',
    help="Somewhat the opposite of -t, and initiates wired mode"
)
parser.add_argument(
    '-y', dest='y', action='store_true',
    help="Brings on the cow's youthful appearance"
)
parser.add_argument(
    'message', action='store', default=' ', nargs='?',
    help="A string to wrap in the text bubble"
)


if __name__ == '__main__':
    args = parser.parse_args()
    preset = ""
    for flag in "ywtspgdb":
        if args.__dict__[flag]:
            preset = flag
            break
    if args.l and args.message == " ":
        print(cowsay.list_cows())
    else:
        print(cowsay.cowsay(args.message,
                            eyes=args.eyes[0:2],
                            cowfile=args.cowfile if args.cowfile.find(
                                "/") != -1 else None,
                            wrap_text=args.wrap_text,
                            tongue=args.tongue[0:2],
                            width=args.width,
                            preset=preset,
                            cow=args.cowfile
                            if args.cowfile.find("/") == -1 and args.cowfile in cowsay.list_cows()
                            else 'default')
              )

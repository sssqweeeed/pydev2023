import cowsay
import cmd
import shlex


def complete_cowsay_and_cowthink(text, line, begidx, endidx):
    # print(text, line, begidx, endidx)
    args = shlex.split(line)
    args_num = len(args)
    eyes = ["OO", "XX", "QQ", "DD", "WW", "CC", "TT"]
    tongues = ["II", "VV", "UU", "JL"]

    if (text == args[-1] and args_num == 3 or not text == args[-1] and args_num == 2):
        return predict(text, cowsay.list_cows())
    elif (text == args[-1] and args_num == 4 or not text == args[-1] and args_num == 3):
        return predict(text, eyes)
    elif (text == args[-1] and args_num == 5 or not text == args[-1] and args_num == 4):
        return predict(text, tongues)


def mv_if_exists(src, idx, dst):
    try:
        dst = src[idx]
    except:
        pass


def predict(text, possible_list):
    return [pred for pred in possible_list if pred.startswith(text)]


def cowsay_and_cowthink(args):
    message, *options = shlex.split(args)
    cow = 'default'
    eyes = 'OO'
    tongue = 'II'

    mv_if_exists(cow, 0, options)
    mv_if_exists(eyes, 1, options)
    mv_if_exists(tongue, 2, options)

    return [message, eyes, tongue, cow]


class CmdCowSay(cmd.Cmd):
    intro = "Welcome to cow command line"
    prompt = "$ "

    def do_list_cows(self, arg):
        cowpath = None
        if arg:
            cowpath = shlex.split(arg)[0]
        print(*cowsay.list_cows(cowpath))

    def do_make_bubble(self, arg):
        message, *options = shlex.split(arg)
        wrap_text = True
        width = 30
        brackets = cowsay.THOUGHT_OPTIONS['cowsay']
        mv_if_exists(wrap_text, 0, options)
        mv_if_exists(width, 1, options)
        mv_if_exists(brackets, 2, options)

        print(cowsay.make_bubble(message, brackets=brackets,
              width=width, wrap_text=wrap_text))

    def complete_make_bubble(self, text, line, begidx, endidx):
        args = shlex.split(line)
        args_num = len(args)
        if (
            args_num == 2 and not args[-1] == text
            or args_num == 3 and args[-1] == text
        ):
            return [res for res in ['true', 'false'] if res.startswith(text.lower())]

    def do_cowsay(self, arg):
        message, eyes, tongue, cow = cowsay_and_cowthink(arg)
        print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))

    def complete_cowsay(self, text, line, begidx, endidx):
        return complete_cowsay_and_cowthink(text, line, begidx, endidx)

    def do_cowthink(self, arg):
        message, eyes, tongue, cow = cowsay_and_cowthink(arg)
        print(cowsay.cowthink(message, eyes=eyes, tongue=tongue, cow=cow))

    def complete_cowthink(self, text, line, begidx, endidx):
        return complete_cowsay_and_cowthink(text, line, begidx, endidx)

    def do_exit(self, arg):
        return 0


CmdCowSay().cmdloop()

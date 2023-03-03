import cowsay
import shlex
import cmd
import readline


COWSAY_DEFAULTS = COWTHINK_DEFAULTS = {"-e": (cowsay.Option.eyes, str),
                                       "-c": ("default", str),
                                       "-T": (cowsay.Option.tongue, str)}

MAKE_BUBBLE_DEFAULTS = {"-b": ("cowsay", str),
                        "-d": (40, int),
                        "-w": (True, bool)}

COWSAY_COMPLETE = COWTHINK_COMPLETE = {"-e": ["oo", "XX", "$$", "@@", "**", "--", "00", ".."],
                                       "-c": cowsay.list_cows(),
                                       "-T": ["  ", "U ", " U", "u ", " u", "||"]}

MAKE_BUBBLE_COMPLETE = {"-b": ["cowsay", "cowthink"], "-d": [], "-w": ["True", "False"]}

COMPLETE = {"cowsay": COWSAY_COMPLETE, "cowthink": COWTHINK_COMPLETE, "make_bubble": MAKE_BUBBLE_COMPLETE}


def parse(args):
    return shlex.split(args, comments=True)


def get_optional_args(args, default_values):
    i = 0
    opt_args = {key: val[0] for key, val in default_values.items()}
    while i < len(args):
        opt_args[args[i]] = default_values[args[i]][1](args[i + 1])
        i += 2

    return opt_args


def complete(text, line, begidx, endidx):
    key, command = shlex.split(line)[-1] if begidx == endidx else shlex.split(line)[-2], shlex.split(line)[0]
    return [s for s in COMPLETE[command][key] if s.startswith(text)]


class Cowsayer(cmd.Cmd):
    prompt = "(cowsay) "

    def do_list_cows(self, args):
        """
        Lists all cow file names in the given directory
        list_cows [cow_path]

        cow_path: path to the dir with cows
        """
        cow_path = parse(args)[0] if parse(args) else cowsay.COW_PEN
        print(*cowsay.list_cows(cow_path), sep="\n")

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        make_bubble text [-b cowsay | cowthink] [-d width] [-w wrap_text]

        text: text in bubble
        brackets=cowsay
        width=40
        wrap_text=True
        """
        message, *opt_args = parse(args)
        opt_args = get_optional_args(opt_args, MAKE_BUBBLE_DEFAULTS)
        print(cowsay.make_bubble(message,
                                 brackets=cowsay.THOUGHT_OPTIONS[opt_args["-b"]],
                                 width=opt_args["-d"],
                                 wrap_text=opt_args["-w"]))

    def complete_make_bubble(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_cowsay(self, args):
        '''
        Returns the resulting cowsay string
        cowsay message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: -c – the available cows can be found by calling list_cows
        eyes: -e or eye_string
        tongue: -T or tongue_string
        '''
        message, *opt_args = parse(args)
        opt_args = get_optional_args(opt_args, COWSAY_DEFAULTS)
        print(cowsay.cowsay(message, cow=opt_args["-c"], eyes=opt_args["-e"], tongue=opt_args["-T"]))

    def complete_cowsay(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_cowthink(self, args):
        """
        Returns the resulting cowthink string
        cowthink message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: -c – the available cows can be found by calling list_cows
        eyes: -e or eye_string
        tongue: -T or tongue_string
        """
        message, *opt_args = parse(args)
        opt_args = get_optional_args(opt_args, COWTHINK_DEFAULTS)
        print(cowsay.cowthink(message, cow=opt_args["-c"], eyes=opt_args["-e"], tongue=opt_args["-T"]))

    def complete_cowthink(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_exit(self, args):
        """Exits from cowsay command line"""
        return True

    def precmd(self, line):
        if line == 'EOF':
            return 'exit'
        return line

    def emptyline(self):
        pass


if __name__ == "__main__":
    Cowsayer().cmdloop()

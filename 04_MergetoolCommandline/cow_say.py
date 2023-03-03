import cowsay
import shlex
import cmd
import readline


def parse(args):
    return shlex.split(args, comments=True)


def get_optional_args(args, default_values):
    i = 0
    while i < len(args):
        default_values[args[i]] = args[i + 1]
        i += 2

    return default_values


class Cowsayer(cmd.Cmd):
    prompt = "(cowsay) "

    def do_list_cows(self, args):
        """
        Lists all cow file names in the given directory
        list_cows [cow_path]

        cow_path: path to the dir with cows
        """

        pass

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

        pass

    def do_cowsay(self, args):
        '''
        Returns the resulting cowsay string
        cowsay message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: -c – the available cows can be found by calling list_cows
        eyes: -e or eye_string
        tongue: -T or tongue_string
        '''
        # message, *opt_args = parse(args)
        # print(message, get_optional_args(opt_args, {"-e": "oo", "-c": "default", "tongue": "  "}))
        pass

    def do_cowthink(self, args):
        """
        Returns the resulting cowthink string
        cowthink message [-e eye_string] [-c cow] [-T tongue_string]

        message: The message to be displayed
        cow: -c – the available cows can be found by calling list_cows
        eyes: -e or eye_string
        tongue: -T or tongue_string
        """

        pass

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

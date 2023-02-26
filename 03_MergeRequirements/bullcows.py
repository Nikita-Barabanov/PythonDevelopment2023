import random
import argparse
import re
import urllib.request
import cowsay
import tempfile


smallcow = ['##\n', '## A small cow, artist unknown\n', '##\n', '$eyes = ".." unless ($eyes);\n', '$the_cow = <<EOC;\n',
            '       $thoughts   ,__,\n', '        $thoughts  ($eyes)____\n', '           (__)    )\\\\\n',
            '            $tongue||--|| *\n', 'EOC\n']


# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    secret_chrs = set(secret)
    for idx, c in enumerate(guess):
        if c == secret[idx]:
            bulls += 1
        elif c in secret_chrs:
            cows += 1

    return bulls, cows


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(cowsay.cowsay(prompt, cow=random.choice(cowsay.list_cows())))
    while valid and guess not in valid:
        guess = input(cowsay.cowsay(prompt, cow=random.choice(cowsay.list_cows())))
    return guess.strip()


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=random.choice(cowsay.list_cows())))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret, cnt = random.choice(words), 1
    print(secret)
    while (guess := ask("Введите слово: ", words)) != secret:
        cnt += 1
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))

    inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))
    return cnt


def main(words: str, length: int = 5) -> None:
    if re.match(regex, words) is not None:
        file_name, _ = urllib.request.urlretrieve(words)
    else:
        file_name = words

    try:
        with open(file_name) as file:
            words_list = [word.strip() for word in file.readlines() if len(word.strip()) == length]
    except OSError:
        print("Wrong path")
        return

    print(gameplay(ask, inform, words_list))




if __name__ == "__main__":
    smallcow_file = tempfile.NamedTemporaryFile().name
    with open(smallcow_file, "w") as scf:
        scf.writelines(smallcow)
    bullscows_parser = argparse.ArgumentParser(prog="bullscows")
    bullscows_parser.add_argument("words", type=str)
    bullscows_parser.add_argument("length", default=5, type=int, nargs="?")
    bullscows_args = bullscows_parser.parse_args()
    main(bullscows_args.words, bullscows_args.length)

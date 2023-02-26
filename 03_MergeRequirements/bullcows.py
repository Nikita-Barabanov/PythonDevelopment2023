import random


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
    guess = input(prompt)
    while valid and guess not in valid:
        guess = input(prompt)
    return guess.strip()


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret, cnt = random.choice(words), 1
    while (guess := ask("Введите слово: ", words)) != secret:
        cnt += 1
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))

    inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))
    return cnt

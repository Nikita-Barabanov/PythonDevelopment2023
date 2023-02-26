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
    if valid and guess not in valid:
        return ask(prompt, valid)
    return guess.strip()


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

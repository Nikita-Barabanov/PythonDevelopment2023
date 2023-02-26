def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    secret_chrs = set(secret)
    for idx, c in enumerate(guess):
        if c == secret[idx]:
            bulls += 1
        elif c in secret_chrs:
            cows += 1

    return bulls, cows
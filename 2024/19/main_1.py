from functools import cache

TOWELS: set[str] = set()
MAX_SIZE: int = 0


@cache
def is_possible(pattern: str) -> bool:
    if not pattern:
        return True

    for i in reversed(range(min(MAX_SIZE, len(pattern)))):
        current = pattern[: i + 1]
        if current not in TOWELS:
            continue
        remaining = pattern[i + 1 :]
        if not is_possible(pattern=remaining):
            continue
        return True
    return False


def main():
    global TOWELS, MAX_SIZE
    with open("input", "r") as f:
        content: list[str] = f.read().splitlines()

    TOWELS = {towel for towel in content[0].split(", ")}
    MAX_SIZE = max([len(towel) for towel in TOWELS])
    patterns: list[str] = content[2:]
    total: int = 0
    for index, pattern in enumerate(patterns):
        if is_possible(pattern=pattern):
            total += 1
    print(total)


if __name__ == "__main__":
    main()

from functools import cache

TOWELS: set[str] = set()
MAX_SIZE: int = 0


@cache
def nb_possible(pattern: str) -> int:
    if not pattern:
        return 1
    possible: int = 0
    for i in reversed(range(min(MAX_SIZE, len(pattern)))):
        current = pattern[: i + 1]
        if current not in TOWELS:
            continue
        remaining = pattern[i + 1 :]
        possible += nb_possible(remaining)
    return possible


def main():
    global TOWELS, MAX_SIZE
    with open("input", "r") as f:
        content: list[str] = f.read().splitlines()

    TOWELS = {towel for towel in content[0].split(", ")}
    MAX_SIZE = max([len(towel) for towel in TOWELS])
    patterns: list[str] = content[2:]
    total: int = 0
    for index, pattern in enumerate(patterns):
        total += nb_possible(pattern)
    print(total)


if __name__ == "__main__":
    # TOWELS = {"a"}
    # MAX_SIZE = 1
    # print(all_possible("a"))
    main()

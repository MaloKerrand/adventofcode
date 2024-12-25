from itertools import product


def main():
    with open("input", "r") as f:
        content: str = f.read()

    keys: list[list[int]] = []
    locks: list[list[int]] = []

    for block in content.split("\n\n"):
        lines: list[str] = block.splitlines()
        used: list[int] = [len([c for c in i if c == "#"]) - 1 for i in zip(*lines)]

        if block[0] == ".":
            keys.append(used)
        else:
            locks.append(used)

    matches = 0
    for key, lock in product(keys, locks):
        if all([k + l <= 5 for k, l in zip(key, lock)]):
            matches += 1

    print(matches)


if __name__ == "__main__":
    main()

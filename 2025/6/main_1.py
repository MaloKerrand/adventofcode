from functools import reduce
from pathlib import Path


def remove_duplicate_space(line: str) -> str:
    while "  " in line:
        line = line.replace("  ", " ")
    return line.strip(" ")


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    content_first, content_second = content.rsplit(sep="\n", maxsplit=1)
    numbers: list[list[str]] = []
    for line in content_first.splitlines():
        numbers.append(remove_duplicate_space(line.removesuffix("\n")).split(sep=" "))

    operations: list[str] = remove_duplicate_space(content_second).split(sep=" ")

    print(numbers)
    print(operations)

    sum_total = 0
    for index, operation in enumerate(operations):
        if operation == "*":
            initial_value = 1
            op = lambda x, y: int(x) * int(y)
        else:
            initial_value = 0
            op = lambda x, y: int(x) + int(y)

        sum_total += reduce(op, [nbs[index] for nbs in numbers], initial_value)

    print(sum_total)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

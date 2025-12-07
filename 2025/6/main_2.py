from pathlib import Path
from typing import Callable


def transpose(ll: list[str]) -> list[str]:
    return ["".join([ll[j][i] for j in range(len(ll))]) for i in range(len(ll[0]))]


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    columns: list[str] = transpose(content.splitlines())

    sum_total = 0
    current_total = 0
    op: Callable | None = None
    for index, column in enumerate(columns):
        column = column.strip(" ")
        if not column:
            op = None
            sum_total += current_total
            continue

        if op is None:
            column, operation = column[:-1], column[-1]
            if operation == "*":
                current_total = 1
                op = lambda x, y: int(x) * int(y)
            else:
                current_total = 0
                op = lambda x, y: int(x) + int(y)
        nb = column.strip(" ")
        current_total = op(current_total, nb)

    sum_total += current_total
    print(sum_total)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

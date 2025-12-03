from pathlib import Path
from typing import Literal


def main():
    current_file = Path(__file__)
    with open(file=current_file.parent / "input", mode="r", encoding="utf-8") as f:
        content = f.read().splitlines()

    nb_zero = 0
    current_number = 50
    for line in content:
        direction, steps = line[0], int(line[1:])
        direction_sign: Literal[-1, 1] = -1 if direction == "L" else 1
        old_number = current_number

        current_number += direction_sign * steps
        current_number = current_number % 100

        nb_zero += steps // 100
        if direction == "R" and current_number < old_number:
            nb_zero += 1
        if direction == "L" and (current_number > old_number or current_number == 0) and old_number != 0:
            nb_zero += 1

    print(nb_zero)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

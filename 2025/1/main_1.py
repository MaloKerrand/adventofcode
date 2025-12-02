from typing import Literal


def main():
    with open(file="input", mode="r", encoding="utf-8") as f:
        content = f.read().splitlines()

    nb_zero = 0
    current_number = 50
    for line in content:
        direction, steps = line[0], int(line[1:])
        direction_sign: Literal[-1, 1] = -1 if direction == "L" else 1
        current_number += direction_sign * steps
        current_number = current_number % 100
        if current_number == 0:
            nb_zero += 1

    print(nb_zero)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

from pathlib import Path


def get_ieme_max(numbers: list[int], ieme: int) -> tuple[int, int]:
    ieme_max = max(numbers[: -(ieme - 1)]) if ieme > 1 else max(numbers)
    index = numbers.index(ieme_max)
    return index, ieme_max


def main():
    current_file = Path(__file__)
    with open(file=current_file.parent / "input", mode="r", encoding="utf-8") as f:
        lines: list[list[int]] = [[int(i) for i in line.removesuffix("\n")] for line in f.readlines()]

    sum_max = 0
    for line in lines:
        numbers = line.copy()
        number = ""
        for i in range(12, 0, -1):
            index, m = get_ieme_max(numbers=numbers, ieme=i)
            number += str(m)
            numbers = numbers[index + 1 :]

        sum_max += int(number)

    print(sum_max)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

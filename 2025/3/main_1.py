from pathlib import Path


def double_max(numbers: list[int]) -> tuple[int, int]:
    first_max = max(numbers[:-1])
    index = numbers.index(first_max)
    return first_max, max(numbers[index + 1 :])


def main():
    current_file = Path(__file__)
    with open(file=current_file.parent / "input", mode="r", encoding="utf-8") as f:
        lines: list[list[int]] = [[int(i) for i in line.removesuffix("\n")] for line in f.readlines()]

    sum_max = 0
    for line in lines:
        m1, m2 = double_max(line)
        sum_max += int(str(m1) + str(m2))

    print(sum_max)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

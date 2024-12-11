def transform(x: int) -> list[int]:
    if x == 0:
        return [1]

    nb_digits = len(str(x))
    if nb_digits % 2 == 0:
        return [int(str(x)[: nb_digits // 2]), int(str(x)[nb_digits // 2 :])]

    return [x * 2024]


def blink(numbers: list[int]) -> list[int]:
    return [transform_number for number in numbers for transform_number in transform(number)]


def main():
    with open("input", "r") as f:
        numbers: list[int] = [int(number) for number in f.read().split(" ")]
    print(numbers)
    for _ in range(25):
        numbers = blink(numbers)
        # print(numbers)
    print(len(numbers))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

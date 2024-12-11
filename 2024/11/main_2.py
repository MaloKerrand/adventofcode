def transform(x: int) -> list[int]:
    if x == 0:
        return [1]

    nb_digits = len(str(x))
    if nb_digits % 2 == 0:
        return [int(str(x)[: nb_digits // 2]), int(str(x)[nb_digits // 2 :])]

    return [x * 2024]


def blink(number_to_occurrences: dict[int, int]) -> dict[int, int]:
    new_number_to_occurrences: dict[int, int] = {}
    for number, count in number_to_occurrences.items():
        for new_number in transform(number):
            new_number_to_occurrences.setdefault(new_number, 0)
            new_number_to_occurrences[new_number] += count
    return new_number_to_occurrences


def main():
    with open("input", "r") as f:
        numbers: list[int] = [int(number) for number in f.read().split(" ")]

    number_to_occurrences: dict[int, int] = {}
    for number in numbers:
        number_to_occurrences.setdefault(number, 0)
        number_to_occurrences[number] += 1

    for i in range(75):
        number_to_occurrences = blink(number_to_occurrences)

    print(sum(number_to_occurrences.values()))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

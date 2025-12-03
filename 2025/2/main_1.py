from pathlib import Path


def valid(id_int: int) -> bool:
    id_str = str(id_int)
    length = len(id_str)
    if length % 2 != 0:
        return True

    if id_str[: length // 2] != id_str[length // 2 :]:
        return True

    return False


def main():
    current_file = Path(__file__)
    with open(file=current_file.parent / "input", mode="r", encoding="utf-8") as f:
        lines: list[str] = f.read().split(",")

    invalid_sum = 0
    for line in lines:
        first, last = line.split("-")
        for index in range(int(first), int(last) + 1):
            if not valid(index):
                invalid_sum += int(index)

    print(invalid_sum)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

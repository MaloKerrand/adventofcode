def repeat(repeat_size: int, id_str: str) -> bool:
    pattern = id_str[:repeat_size]

    for index in range(0, len(id_str), repeat_size):
        if pattern != id_str[index : index + repeat_size]:
            return False
    return True


def valid(id_int: int) -> bool:
    id_str = str(id_int)
    length = len(id_str)
    for i in range(1, length // 2 + 1):
        if length % i != 0:
            continue
        if repeat(repeat_size=i, id_str=id_str):
            return False
    return True


def main():
    with open(file="input", mode="r", encoding="utf-8") as f:
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

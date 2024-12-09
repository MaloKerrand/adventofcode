def is_possible(result: int, current: int, values: list[int]) -> bool:
    if result < current:
        return False

    if not values:
        return result == current

    next_value, *next_values = values

    if is_possible(result, current + next_value, next_values):
        return True

    if is_possible(result, current * next_value, next_values):
        return True

    return False


def main():
    with open("input", "r") as f:
        content: str = f.read()
    operations: list[tuple[int, list[int]]] = []
    for line in content.splitlines():
        result, *numbers = line.split(" ")
        operations.append((int(result.removesuffix(":")), [int(number.removeprefix(" ")) for number in numbers]))

    print(
        sum(
            operation[0]
            for operation in operations
            if is_possible(result=operation[0], current=operation[1][0], values=operation[1][1:])
        )
    )


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

from functools import cmp_to_key

ELEMENT_TO_AFTER: dict[str, list[str]] = {}


def valid_order(order: list[str], element_to_after: dict[str, list[str]]) -> bool:
    for index, element in enumerate(order):
        for before in order[:index]:
            if before in element_to_after.get(element, []):
                print(element, before, element_to_after.get(element, []))
                return False
    return True


def smaller_eq(a: str, b: str) -> int:
    if a in ELEMENT_TO_AFTER.get(b, []):
        return 1
    if b in ELEMENT_TO_AFTER.get(a, []):
        return -1
    return 0


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    orders: list[list[str]] = []
    second_step = False
    for line in content:
        if line == "":
            second_step = True
            continue
        if not second_step:
            before, after = line.split("|")
            ELEMENT_TO_AFTER.setdefault(before, []).append(after)
            continue
        orders.append(line.split(","))

    total = 0
    for order in orders:
        sorted_order = sorted(order, key=cmp_to_key(smaller_eq))
        if sorted_order == order:
            total += int(order[int(len(order) / 2)])

    print(total)


if __name__ == "__main__":
    import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

import bisect

a = [1, 2, 4, 5]
bisect.insort(a, 3)


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    elements: list[str] = []
    element_2: dict[str, int] = {}
    for line in content:
        number_1, number_2 = line.split("   ")

        elements.append(number_1)

        element_2.setdefault(number_2, 0)
        element_2[number_2] += 1

    result = 0
    for element in elements:
        result += element_2.get(element, 0) * int(element)

    print(result)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit("main()", number=1000, globals=locals()))
    # main()

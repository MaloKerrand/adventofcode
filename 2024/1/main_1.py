def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    elements_1: list[int] = []
    elements_2: list[int] = []
    for line in content:
        number_1, number_2 = line.split("   ")

        elements_1.append(int(number_1))
        elements_2.append(int(number_2))

    elements_1.sort()
    elements_2.sort()

    result = 0
    for e1, e2 in zip(elements_1, elements_2):
        result += abs(e1 - e2)

    print(result)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

def number_xmas(x: int, y: int, content: list[str], size_x: int, size_y: int):
    number = 0
    for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        if (
            x + direction[1] * 3 < 0
            or x + direction[1] * 3 >= size_x
            or y + direction[0] * 3 < 0
            or y + direction[0] * 3 >= size_y
        ):
            continue

        if (
            content[y + direction[0]][x + direction[1]] != "M"
            or content[y + direction[0] * 2][x + direction[1] * 2] != "A"
            or content[y + direction[0] * 3][x + direction[1] * 3] != "S"
        ):
            continue
        number += 1
    return number


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    total = 0
    size_y = len(content)
    for y, line in enumerate(content):
        size_x = len(line)
        for x, char in enumerate(line):
            if char == "X":
                total += number_xmas(x=x, y=y, content=content, size_x=size_x, size_y=size_y)
    print(total)


if __name__ == "__main__":
    import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

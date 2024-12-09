def is_xmas(x: int, y: int, content: list[str]):
    return (
        content[y - 1][x - 1] in ["M", "S"]
        and content[y + 1][x + 1] in ["M", "S"]
        and content[y - 1][x - 1] != content[y + 1][x + 1]
        and content[y + 1][x - 1] in ["M", "S"]
        and content[y - 1][x + 1] in ["M", "S"]
        and content[y + 1][x - 1] != content[y - 1][x + 1]
    )


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    total = 0
    for y, line in enumerate(content[1:-1]):
        for x, char in enumerate(line[1:-1]):
            if char == "A" and is_xmas(x=x + 1, y=y + 1, content=content):
                total += 1
    print(total)


if __name__ == "__main__":
    import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

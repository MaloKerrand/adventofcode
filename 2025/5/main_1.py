from pathlib import Path


def in_ranges(number: int, ranges: list[range]) -> bool:
    for range_ in ranges:
        if number in range_:
            return True
    return False


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    content_first, content_second = content.split(sep="\n\n")
    ranges: list[range] = []
    for line in content_first.splitlines():
        start, end = line.split(sep="-")
        ranges.append(range(int(start), int(end) + 1))
    numbers: list[int] = [int(number) for number in content_second.splitlines()]

    nb_in_ranges = 0
    for number in numbers:
        if in_ranges(number=number, ranges=ranges):
            nb_in_ranges += 1

    print(nb_in_ranges)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

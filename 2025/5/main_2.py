from pathlib import Path


def in_ranges(number: int, ranges: list[range]) -> bool:
    for range_ in ranges:
        if number in range_:
            return True
    return False


def merge_overlapping_ranges(ranges: list[range]) -> list[range]:
    """Return the union of all currently intersecting ranges."""
    if not ranges:
        return []

    sorted_ranges: list[range] = sorted(ranges, key=lambda range_: range_.start)
    union_ranges: list[range] = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last: range = union_ranges[-1]
        if current.start < last.stop:
            union_ranges[-1] = range(last.start, max(last.stop, current.stop))
        else:
            union_ranges.append(current)
    return union_ranges


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    content_first, _ = content.split("\n\n")
    ranges: list[range] = []
    for line in content_first.splitlines():
        start, end = line.split(sep="-")
        ranges.append(range(int(start), int(end) + 1))

    union_ranges: list[range] = merge_overlapping_ranges(ranges)
    nb_index: int = sum(len(range_) for range_ in union_ranges)
    print(nb_index)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

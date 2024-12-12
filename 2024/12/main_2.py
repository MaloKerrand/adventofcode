CHECKED: list[tuple[int, int]] = []
KNOWN_REGIONS: list[list[tuple[int, int]]] = []


def in_map(x: int, y: int, garden: list[str]):
    return 0 <= x < len(garden[0]) and 0 <= y < len(garden)


def create_region(x: int, y: int, char: str, garden: list[str]) -> list[tuple[int, int]]:
    if (x, y) in CHECKED:
        return []
    if garden[y][x] != char:
        return []
    CHECKED.append((x, y))

    region: list[tuple[int, int]] = [(x, y)]
    for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        new_x, new_y = x + direction[0], y + direction[1]
        if not in_map(x=new_x, y=new_y, garden=garden):
            continue
        if sub_region := create_region(x=new_x, y=new_y, char=char, garden=garden):
            region += sub_region
    return region


def size(region: list[tuple[int, int]]) -> int:
    corner_to_origins: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for x, y in region:
        for direction in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            new_x, new_y = x + direction[0], y + direction[1]
            corner_to_origins.setdefault((new_x, new_y), []).append((x, y))

    total = 0
    for corner, origins in corner_to_origins.items():
        nb = len(origins)

        if nb == 4:
            continue
        if nb != 2:
            total += 1
            continue
        (x1, y1), (x2, y2) = origins
        if x1 != x2 and y1 != y2:
            total += 2

    return len(region) * total


def main():
    with open("input", "r") as f:
        garden: list[str] = f.read().splitlines()

    total_size = len(garden) * len(garden[0])
    current = 0
    for y, line in enumerate(garden):
        for x, char in enumerate(line):
            print(f"{100 * current / total_size: .2f} %")
            current += 1
            if region := create_region(x=x, y=y, char=char, garden=garden):
                KNOWN_REGIONS.append(region)

    total = 0
    for region in KNOWN_REGIONS:
        total += size(region)
    print(total)


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

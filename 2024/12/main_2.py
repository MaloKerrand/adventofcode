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
    area = len(region)
    fences: list[tuple[int, int, int, int, bool]] = []
    for x, y in region:
        for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_x, new_y = x + direction[0], y + direction[1]
            if (new_x, new_y) in region:
                continue
            fences.append((new_x, new_y, new_x + abs(direction[1]), new_y + abs(direction[0]), direction[0] == 0))
    nb_size = nb_side(fences)
    return area * nb_size


def nb_side(fences: list[tuple[int, int, int, int, bool]]) -> int:
    complete_fences: list[tuple[int, int, int, int, bool]] = []
    for fence in fences:
        complete_fences = add_fence(fences=complete_fences, new=fence)
    return len(complete_fences)


def add_fence(fences: list[tuple[int, int, int, int, bool]], new: tuple[int, int, int, int, bool]):
    aggregated_fence: tuple[int, int, int, int, bool] | None = None
    old_fences: list[tuple[int, int, int, int, bool]] | None = None
    for index, (x1, y1, x2, y2, face_x) in enumerate(fences):
        if face_x != new[4]:
            continue
        if (x1, y1) == (new[2], new[3]):
            aggregated_fence = (new[0], new[1], x2, y2, face_x)
            old_fences = fences[:index] + fences[index + 1 :]
            break
        if (x2, y2) == (new[0], new[1]):
            aggregated_fence = (x1, y1, new[2], new[3], face_x)
            old_fences = fences[:index] + fences[index + 1 :]
            break
    if aggregated_fence is None:
        return fences + [new]
    return add_fence(fences=old_fences, new=aggregated_fence)


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

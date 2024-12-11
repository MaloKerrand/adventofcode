def in_map(x: int, y: int, topographic_map: list[list[int]]):
    return 0 <= x < len(topographic_map[0]) and 0 <= y < len(topographic_map)


def reachable_nine(x: int, y: int, height: int, topographic_map: list[list[int]]) -> set[tuple[int, int]]:
    if height == 9:
        return {(x, y)}

    total: set[tuple[int, int]] = set()
    for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        new_x, new_y = x + direction[0], y + direction[1]
        if not in_map(x=new_x, y=new_y, topographic_map=topographic_map):
            continue
        if topographic_map[new_y][new_x] == height + 1:
            total |= reachable_nine(x=new_x, y=new_y, height=height + 1, topographic_map=topographic_map)
    return total


def main():
    with open("input_fake", "r") as f:
        topographic_map: list[list[int]] = [[int(e) for e in line] for line in f.read().splitlines()]

    nb = 0
    for y, line in enumerate(topographic_map):
        for x, height in enumerate(line):
            if height != 0:
                continue
            nb += len(reachable_nine(x=x, y=y, height=height, topographic_map=topographic_map))

    print(nb)


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

def get_antinode(x1: int, y1: int, x2: int, y2: int, max_x: int, max_y: int) -> set[tuple[int, int]]:
    antinodes = set()
    for n in range(-max(max_x, max_y), max(max_x, max_y) + 1):
        antinode = ((1 - n) * x1 + n * x2, (1 - n) * y1 + n * y2)
        if in_map(x=antinode[0], y=antinode[1], max_x=max_x, max_y=max_y):
            antinodes.add(antinode)
    return antinodes


def add_antinodes(
    antinodes: set[tuple[int, int]],
    nodes: list[tuple[int, int]],
    x: int,
    y: int,
    max_x: int,
    max_y: int,
) -> None:
    for node_x, node_y in nodes:
        antinodes |= get_antinode(x1=x, y1=y, x2=node_x, y2=node_y, max_x=max_x, max_y=max_y)


def in_map(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x < max_x and 0 <= y < max_y


def main():
    with open("input", "r") as f:
        _map: list[str] = f.read().splitlines()

    antinodes: set[tuple[int, int]] = set()
    char_to_x_y: dict[str, list[tuple[int, int]]] = {}
    max_x = len(_map[0])
    max_y = len(_map)
    for y, line in enumerate(_map):
        for x, char in enumerate(line):
            if char == ".":
                continue
            nodes = char_to_x_y.setdefault(char, [])
            add_antinodes(antinodes=antinodes, nodes=nodes, x=x, y=y, max_x=max_x, max_y=max_y)
            nodes.append((x, y))

    print(len(antinodes))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

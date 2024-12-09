def get_antinode(x1: int, y1: int, x2: int, y2: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return (2 * x1 - x2, 2 * y1 - y2), (2 * x2 - x1, 2 * y2 - y1)


def add_antinodes(antinodes: set[tuple[int, int]], nodes: list[tuple[int, int]], x: int, y: int) -> None:
    for node_x, node_y in nodes:
        antinode_1, antinode_2 = get_antinode(x, y, node_x, node_y)

        antinodes.add(antinode_1)
        antinodes.add(antinode_2)


def in_map(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x < max_x and 0 <= y < max_y


def main():
    with open("input", "r") as f:
        _map: list[str] = f.read().splitlines()
        # f.seek(0)
        # _map2: list[list[str]] = [[c for c in line] for line in f.read().splitlines()]

    antinodes: set[tuple[int, int]] = set()
    char_to_x_y: dict[str, list[tuple[int, int]]] = {}

    for y, line in enumerate(_map):
        for x, char in enumerate(line):
            if char == ".":
                continue
            nodes = char_to_x_y.setdefault(char, [])
            add_antinodes(antinodes=antinodes, nodes=nodes, x=x, y=y)
            nodes.append((x, y))

    # print(char_to_x_y)
    max_x = len(_map[0])
    max_y = len(_map)
    real_antinodes = {antinode for antinode in antinodes if in_map(antinode[0], antinode[1], max_x=max_x, max_y=max_y)}
    print(len(real_antinodes))

    # for antinode in real_antinodes:
    #     print(antinode)
    #     _map2[antinode[1]][antinode[0]] = "#"
    # for line in _map2:
    #     print("".join(line))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

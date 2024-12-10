from copy import deepcopy


def is_valid_position(x: int, y: int, _map: list[list[str]]) -> bool:
    return (0 <= x < len(_map)) and (0 <= y < len(_map[0]))


def get_position_in_way(x: int, y: int, _map: list[list[str]]) -> set[tuple[int, int]]:
    positions: set[tuple[int, int]] = set()
    new_position: tuple[int, int] = (x, y)
    guard_direction: tuple[int, int] = (0, -1)
    while True:
        if not is_valid_position(
            x=new_position[1] + guard_direction[1],
            y=new_position[0] + guard_direction[0],
            _map=_map,
        ):
            return positions

        if _map[new_position[1] + guard_direction[1]][new_position[0] + guard_direction[0]] == "#":
            match guard_direction:
                case (0, -1):
                    guard_direction = (1, 0)
                case (1, 0):
                    guard_direction = (0, 1)
                case (0, 1):
                    guard_direction = (-1, 0)
                case (-1, 0):
                    guard_direction = (0, -1)
            continue

        new_position = (new_position[0] + guard_direction[0], new_position[1] + guard_direction[1])
        positions.add(new_position)


def is_infinite_map(x: int, y: int, _map: list[list[str]]) -> bool:
    new_position: tuple[int, int] = (x, y)
    guard_direction: tuple[int, int] = (0, -1)
    know_path: set[tuple[tuple[int, int], tuple[int, int]]] = {(new_position, guard_direction)}
    while True:
        if not is_valid_position(
            x=new_position[1] + guard_direction[1],
            y=new_position[0] + guard_direction[0],
            _map=_map,
        ):
            return False

        if _map[new_position[1] + guard_direction[1]][new_position[0] + guard_direction[0]] == "#":
            match guard_direction:
                case (0, -1):
                    guard_direction = (1, 0)
                case (1, 0):
                    guard_direction = (0, 1)
                case (0, 1):
                    guard_direction = (-1, 0)
                case (-1, 0):
                    guard_direction = (0, -1)
            continue

        new_position = (new_position[0] + guard_direction[0], new_position[1] + guard_direction[1])

        if (new_position, guard_direction) in know_path:
            return True
        know_path.add((new_position, guard_direction))


def main():
    with open("input", "r") as f:
        _map: list[list[str]] = [[c for c in line] for line in f.read().splitlines()]

    for guard_y, line in enumerate(_map):
        try:
            guard_x = line.index("^")
            if guard_x != -1:
                _map[guard_y][guard_x] = "X"
                break
        except ValueError:
            pass

    total_vue = len(_map) * len(_map[0])
    total = 0
    vue = 0
    new_position = (guard_x, guard_y)
    positions = get_position_in_way(x=new_position[0], y=new_position[1], _map=_map)
    print(len(positions))
    for index_y, line in enumerate(_map):
        for index_x, c in enumerate(line):
            vue += 1
            if c != ".":
                continue

            if (index_x, index_y) not in positions:
                continue

            map_copy = deepcopy(_map)
            map_copy[index_y][index_x] = "#"
            if is_infinite_map(x=new_position[0], y=new_position[1], _map=map_copy):
                total += 1
            print((vue / total_vue) * 100)
    print(total)


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

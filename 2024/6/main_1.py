def is_valid_position(x: int, y: int, map: list[list[str]]) -> bool:
    return (0 <= x < len(map)) and (0 <= y < len(map[0]))


def main():
    with open("input", "r") as f:
        map: list[list[str]] = [[c for c in line] for line in f.read().splitlines()]

    for guard_y, line in enumerate(map):
        try:
            guard_x = line.index("^")
            if guard_x != -1:
                map[guard_y][guard_x] = "X"
                break
        except ValueError:
            pass
    guard_direction: tuple[int, int] = (0, -1)
    new_position = (guard_x, guard_y)
    while True:
        new_position = (
            new_position[0] + guard_direction[0],
            new_position[1] + guard_direction[1],
        )
        if not is_valid_position(x=new_position[0], y=new_position[1], map=map):
            break

        if (
            is_valid_position(x=new_position[1] + guard_direction[1], y=new_position[0] + guard_direction[0], map=map)
            and map[new_position[1] + guard_direction[1]][new_position[0] + guard_direction[0]] == "#"
        ):
            match guard_direction:
                case (0, -1):
                    guard_direction = (1, 0)
                case (1, 0):
                    guard_direction = (0, 1)
                case (0, 1):
                    guard_direction = (-1, 0)
                case (-1, 0):
                    guard_direction = (0, -1)

        map[new_position[1]][new_position[0]] = "X"

    print(len([c for line in map for c in line if c == "X"]))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

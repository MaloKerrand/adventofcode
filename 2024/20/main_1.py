def main():
    with open("input", "r") as f:
        maze: list[str] = f.read().splitlines()

    max_x = len(maze[0])
    max_y = len(maze)
    maze_values: list[list[int | None]] = [[None for _ in range(max_x)] for _ in range(max_y)]

    known_positions: list[tuple[int, int]] = []
    x, y = get_start(maze)
    cost = 0
    maze_values[y][x] = cost
    end = False
    while not end:
        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            new_x = x + dx
            new_y = y + dy
            if maze[new_y][new_x] not in [".", "E"]:
                continue

            if (new_x, new_y) in known_positions:
                continue
            known_positions.append((new_x, new_y))

            x += dx
            y += dy
            cost += 1
            maze_values[y][x] = cost

            if maze[y][x] == "E":
                end = True
            break

    gains: list[int] = []
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "#":
                values = [
                    maze_values[y + dy][x + dx]
                    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]
                    if in_maze(x=x + dx, y=y + dy, max_x=max_x, max_y=max_y)
                ]
                values = [v for v in values if v]
                if len(values) < 2:
                    continue
                gains.append(max(values) - min(values) - 2)

    gains.sort()
    print(gains)
    print(len([g for g in gains if g >= 100]))


def get_start(maze: list[str]) -> tuple[int, int]:
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "S":
                return x, y
    raise Exception("No 'S' in maze")


def in_maze(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x < max_x and 0 <= y < max_y


if __name__ == "__main__":
    main()

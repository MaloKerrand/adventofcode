from dataclasses import dataclass


@dataclass(frozen=True)
class Cheat:
    from_x: int
    from_y: int
    to_x: int
    to_y: int
    cost: int
    gain: int

    @property
    def real_gain(self) -> int:
        return self.gain - self.cost


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

    len_cheat = 20
    disc = get_disc(len_cheat)
    gains: set[Cheat] = set()
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "#":
                continue
            for dx, dy in disc:
                new_x = x + dx
                new_y = y + dy
                if not in_maze(x=new_x, y=new_y, max_x=max_x, max_y=max_y):
                    continue
                if maze[new_y][new_x] == "#":
                    continue

                cheat = Cheat(
                    from_x=x,
                    from_y=y,
                    to_x=new_x,
                    to_y=new_y,
                    cost=abs(dx) + abs(dy),
                    gain=maze_values[new_y][new_x] - maze_values[y][x],
                )

                if cheat.real_gain > 0:
                    gains.add(cheat)

    gains_to_nb: dict[int, int] = {}
    for g in gains:
        gains_to_nb.setdefault(g.real_gain, 0)
        gains_to_nb[g.real_gain] += 1

    print(len([g for g in gains if g.real_gain >= 100]))


def get_start(maze: list[str]) -> tuple[int, int]:
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == "S":
                return x, y
    raise Exception("No 'S' in maze")


def in_maze(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x < max_x and 0 <= y < max_y


def get_disc(radius: int = 20) -> list[tuple[int, int]]:
    disc: list[tuple[int, int]] = []
    for x in range(-radius, radius + 1):
        for y in range(-(radius - abs(x)), radius - abs(x) + 1):
            disc.append((x, y))
    return disc


if __name__ == "__main__":
    main()

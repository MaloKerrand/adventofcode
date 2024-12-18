import math
from bisect import insort
from dataclasses import dataclass

# MAX = 6
# LIMIT = 12
MAX = 70
LIMIT = 1024


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    cost: int
    distance: float

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class PriorityList:
    def __init__(self, elements: list[Position] | None = None):
        self.elements = elements or []

    def append(self, position: Position):
        insort(self.elements, position, key=lambda p: -(p.cost + p.distance))


def main():
    with open("input", "r") as f:
        bytes_list: list[tuple[int, int]] = [
            (int(line.split(",")[0]), int(line.split(",")[1])) for line in f.read().splitlines()
        ]

    maze: list[list[str]] = [["." for _ in range(MAX + 1)] for _ in range(MAX + 1)]
    for x, y in bytes_list[:LIMIT]:
        maze[y][x] = "#"

    for line in maze:
        print("".join(line))

    start_x, start_y = 0, 0
    end_x, end_y = MAX, MAX

    start = Position(x=0, y=0, cost=0, distance=math.dist((start_x, start_y), (end_x, end_y)))
    priority_list = PriorityList(elements=[start])
    known_positions: list[Position] = [start]
    while priority_list.elements:
        position = priority_list.elements.pop()
        for new_dx, new_dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            new_x = position.x + new_dx
            new_y = position.y + new_dy
            if not (0 <= new_x <= MAX and 0 <= new_y <= MAX):
                continue

            if maze[new_y][new_x] == "#":
                continue

            new_position = Position(
                x=new_x,
                y=new_y,
                cost=position.cost + 1,
                distance=math.dist((new_x, new_y), (end_x, end_y)),
            )

            if new_position in known_positions:
                continue
            known_positions.append(new_position)

            if (new_x, new_y) == (end_x, end_y):
                print("FOUND IT !", new_position.cost)
                return

            priority_list.append(new_position)

    print("Not found :<")


if __name__ == "__main__":
    main()

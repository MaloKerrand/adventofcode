import math
from bisect import insort
from copy import deepcopy
from dataclasses import dataclass


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


def is_possible(maze: list[list[str]]) -> bool:
    maximum = len(maze) - 1
    start_x, start_y = 0, 0
    end_x, end_y = maximum, maximum

    start = Position(x=0, y=0, cost=0, distance=math.dist((start_x, start_y), (end_x, end_y)))
    priority_list = PriorityList(elements=[start])
    known_positions: list[Position] = [start]
    while priority_list.elements:
        position = priority_list.elements.pop()
        for new_dx, new_dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            new_x = position.x + new_dx
            new_y = position.y + new_dy
            if not (0 <= new_x <= maximum and 0 <= new_y <= maximum):
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
                return True

            priority_list.append(new_position)
    return False


def generate_maze(maze: list[list[str]], bytes_list: list[tuple[int, int]]) -> list[list[str]]:
    new_maze = deepcopy(maze)
    for x, y in bytes_list:
        new_maze[y][x] = "#"
    return new_maze


def main():
    with open("input", "r") as f:
        bytes_list: list[tuple[int, int]] = [
            (int(line.split(",")[0]), int(line.split(",")[1])) for line in f.read().splitlines()
        ]

    # MAX = 6
    MAX = 70
    original_maze: list[list[str]] = [["." for _ in range(MAX + 1)] for _ in range(MAX + 1)]

    min_bytes: int = 0
    max_bytes: int = len(bytes_list)
    while min_bytes != max_bytes:
        size: int = (max_bytes + min_bytes) // 2
        maze = generate_maze(original_maze, bytes_list[: size + 1])

        if is_possible(maze):
            min_bytes = size + 1
        else:
            max_bytes = size

    print(",".join(str(i) for i in bytes_list[min_bytes]))


if __name__ == "__main__":
    main()

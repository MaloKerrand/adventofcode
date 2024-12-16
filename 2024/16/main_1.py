import math
from bisect import insort
from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    dx: int
    dy: int
    cost: int
    distance: float

    def __lt__(self, other: "Position"):
        if self.cost == other.cost:
            return self.distance < other.distance
        return self.cost < other.cost


class PriorityList:
    def __init__(self, elements: list[Position]|None = None):
        self.elements = elements or []

    def append(self, position: Position):
        insort(self.elements, position, key=lambda p: -p.cost)


MAZE: list[list[str]] = []


def main():
    global MAZE
    with open("input_fake_2", "r") as f:
        MAZE = [list(line) for line in f.read().splitlines()]

    start_x, start_y, end_x, end_y = get_start_end()
    priority_list = PriorityList(
        elements=[
            Position(
                x=start_x,
                y=start_y,
                dx=1,
                dy=0,
                cost=0,
                distance=math.dist((start_x, start_y), (end_x, end_y))
            )
        ]
    )
    while priority_list.elements:
        position = priority_list.elements.pop()
        print(priority_list.elements)
        print(position.x, position.y)
        show(position.x, position.y)
        input()
        for new_dx, new_dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            if new_dx == -position.dx and new_dy == -position.dy:
                continue
            new_x = position.x + new_dx
            new_y = position.y + new_dy

            if MAZE[new_y][new_x] == "#":
                continue

            new_cost = position.cost + (1 if new_dx == position.dx and new_dy == position.dy else 1001)
            new_position = Position(
                x=new_x,
                y=new_y,
                dx=new_dx,
                dy=new_dy,
                cost=new_cost,
                distance=math.dist((new_x, new_y), (end_x, end_y)),
            )

            if MAZE[new_y][new_x] == "E":
                print("FOUND IT !", new_position.cost)
                return

            priority_list.append(new_position)

    print("Not found :<")


def get_start_end() -> tuple[int, int, int, int]:
    found: tuple[int, int] | None = None
    for y, line in enumerate(MAZE):
        for x, char in enumerate(line):
            if char == "S":
                if found:
                    return x, y, found[0], found[1]
                found = (x, y)
            if char == "E":
                if found:
                    return found[0], found[1], x, y
                found = (x, y)

    raise Exception("No S")


def show(x, y):
    maze_2 = deepcopy(MAZE)
    maze_2[y][x] = "O"
    for line in maze_2:
        print("".join(line))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

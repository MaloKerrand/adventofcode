from bisect import insort
from copy import deepcopy
from dataclasses import dataclass
from functools import cache


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    dx: int
    dy: int
    cost: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dx == other.dx and self.dy == other.dy


class PriorityList:
    def __init__(self, elements: list[Position] | None = None):
        self.elements = elements or []

    def append(self, position: Position):
        insort(self.elements, position, key=lambda p: -p.cost)


MAZE: list[list[str]] = []


def main():
    global MAZE
    with open("input", "r") as f:
        MAZE = [list(line) for line in f.read().splitlines()]

    start_x, start_y, end_x, end_y = get_start_end()
    end_cost: int | None = None
    start_position = Position(
        x=start_x,
        y=start_y,
        dx=1,
        dy=0,
        cost=0,
    )
    priority_list = PriorityList(elements=[start_position])
    x_y_dx_dy_to_cost: dict[tuple[int, int, int, int], int] = {
        (start_position.x, start_position.y, start_position.dx, start_position.dy): 0
    }
    while priority_list.elements:
        position = priority_list.elements.pop()

        if end_cost is not None and position.cost > end_cost:
            break

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
            )

            if (new_x, new_y, new_dx, new_dy) in x_y_dx_dy_to_cost and new_position.cost > x_y_dx_dy_to_cost[
                (new_x, new_y, new_dx, new_dy)
            ]:
                continue
            x_y_dx_dy_to_cost[(new_x, new_y, new_dx, new_dy)] = new_position.cost

            if MAZE[new_y][new_x] == "E":
                print("FOUND IT !", new_position.cost)
                if end_cost is None:
                    end_cost = new_position.cost
                continue

            priority_list.append(new_position)

    print("Reverse search")
    x_y_to_positions: dict[tuple[int, int], list[Position]] = {}
    for (x, y, dx, dy), cost in x_y_dx_dy_to_cost.items():
        x_y_to_positions.setdefault((x, y), []).append(Position(x=x, y=y, dx=dx, dy=dy, cost=cost))

    @cache
    def older_positions(p: Position) -> set[tuple[int, int]]:
        positions: set[tuple[int, int]] = set()
        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            new_x = p.x - dx
            new_y = p.y - dy
            for old_position in x_y_to_positions.get((new_x, new_y), []):
                if (
                    old_position.x + old_position.dx == p.x
                    and old_position.y + old_position.dy == p.y
                    and old_position.cost + 1 != p.cost
                ):
                    continue
                if (
                    old_position.x + old_position.dx != p.x or old_position.y + old_position.dy != p.y
                ) and old_position.cost + 1001 != p.cost:
                    continue
                positions.add((old_position.x, old_position.y))
                positions |= older_positions(p=old_position)
        return positions

    best_positions: set[tuple[int, int]] = set()
    min_end_position = min(x_y_to_positions.get((end_x, end_y), []), key=lambda p: p.cost)
    for end_position in x_y_to_positions.get((end_x, end_y), []):
        if end_position.cost > min_end_position.cost:
            continue
        best_positions |= older_positions(p=end_position)

    show(list(best_positions))
    print(len(best_positions) + 1)


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


def show(positions: list[tuple[int, int]], positions_x: list[tuple[int, int]] = None):
    maze_2 = deepcopy(MAZE)
    for x, y in positions:
        maze_2[y][x] = "O"
    for x, y in positions_x or []:
        maze_2[y][x] = "X"
    for line in maze_2:
        print("".join(line))


if __name__ == "__main__":
    main()

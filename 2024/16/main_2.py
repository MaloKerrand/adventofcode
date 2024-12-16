from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    dx: int
    dy: int


MAZE: list[str] = []
POSITION_TO_COST: dict[Position, int] = {}
ALL_PATHS: list[list[Position]] = []

def main():
    global MAZE
    with open("input_fake_2", "r") as f:
        MAZE = [line for line in f.read().splitlines()]

    start_x, start_y, end_x, end_y = get_start_end()
    new_to_see: list[tuple[int, Position]] = [(0, Position(x=start_x, y=start_y, dx=1, dy=0))]
    while new_to_see:
        cost, position = new_to_see.pop()
        for new_dx, new_dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            if new_dx == -position.dx and new_dy == -position.dy:
                continue
            new_x = position.x + new_dx
            new_y = position.y + new_dy
            new_position = Position(x=new_x, y=new_y, dx=new_dx, dy=new_dy)

            if MAZE[new_y][new_x] == "#":
                continue

            new_cost = cost + (1 if new_dx == position.dx and new_dy == position.dy else 1001)
            if new_position in POSITION_TO_COST:
                POSITION_TO_COST[new_position] = min(new_cost, POSITION_TO_COST[new_position])
                continue
            POSITION_TO_COST[new_position] = new_cost

            if MAZE[new_y][new_x] == "E":
                continue
            new_to_see.append((new_cost, new_position))

    print("E")
    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        print(POSITION_TO_COST.get(Position(x=end_x, y=end_y, dx=dx, dy=dy)))

    print("****")
    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        print(POSITION_TO_COST.get(Position(x=end_x - 1, y=end_y, dx=dx, dy=dy)))


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


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

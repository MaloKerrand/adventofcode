import math
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Robot:
    x: int = None
    y: int = None
    dx: int = None
    dy: int = None

    def position(self, time: int, max_x: int, max_y: int) -> tuple[int, int]:
        return (self.x + time * self.dx) % max_x, (self.y + time * self.dy) % max_y

    @staticmethod
    def quadrant(x: int, y: int, max_x: int, max_y: int) -> int | None:
        if x < (max_x - 1) / 2 and y < (max_y - 1) / 2:
            return 0
        if x < (max_x - 1) / 2 and y > (max_y - 1) / 2:
            return 1
        if x > (max_x - 1) / 2 and y < (max_y - 1) / 2:
            return 2
        if x > (max_x - 1) / 2 and y > (max_y - 1) / 2:
            return 3
        return None


def main():
    with open("input", "r") as f:
        lines: list[str] = f.read().splitlines()

    positions: list[tuple[int, int]] = []
    # max_x = 11
    # max_y = 7
    max_x = 101
    max_y = 103
    for line in lines:
        p1, p23, p4 = line.split(",")
        p2, p3 = p23.split(" ")
        robot = Robot(x=int(p1.removeprefix("p=")), y=int(p2), dx=int(p3.removeprefix("v=")), dy=int(p4))
        positions.append(robot.position(time=100, max_x=max_x, max_y=max_y))

    quadrant_to_nb_robots: dict[int, int] = {}
    for x, y in positions:
        quadrant = Robot.quadrant(x=x, y=y, max_x=max_x, max_y=max_y)
        if quadrant is None:
            continue
        quadrant_to_nb_robots.setdefault(quadrant, 0)
        quadrant_to_nb_robots[quadrant] += 1

    # print(positions)
    # print(quadrant_to_nb_robots)
    print(math.prod(quadrant_to_nb_robots.values()))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

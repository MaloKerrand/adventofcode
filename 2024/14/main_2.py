from dataclasses import dataclass

MAX_X = 101
MAX_Y = 103


@dataclass(unsafe_hash=True)
class Robot:
    x: int = None
    y: int = None
    dx: int = None
    dy: int = None

    def position(self, time: int) -> tuple[int, int]:
        return (self.x + time * self.dx) % MAX_X, (self.y + time * self.dy) % MAX_Y

    @staticmethod
    def quadrant(x: int, y: int) -> int | None:
        if x < (MAX_X - 1) / 2 and y < (MAX_Y - 1) / 2:
            return 0
        if x < (MAX_X - 1) / 2 and y > (MAX_Y - 1) / 2:
            return 1
        if x > (MAX_X - 1) / 2 and y < (MAX_Y - 1) / 2:
            return 2
        if x > (MAX_X - 1) / 2 and y > (MAX_Y - 1) / 2:
            return 3
        return None


def show(positions: list[tuple[int, int]]):
    robot_map = [[" " for _ in range(MAX_X)] for _ in range(MAX_Y)]
    for x, y in positions:
        robot_map[y][x] = "*"

    for line in robot_map:
        print("".join(line))


def main():
    with open("input", "r") as f:
        lines: list[str] = f.read().splitlines()

    robots: list[Robot] = []
    for line in lines:
        p1, p23, p4 = line.split(",")
        p2, p3 = p23.split(" ")
        robots.append(Robot(x=int(p1.removeprefix("p=")), y=int(p2), dx=int(p3.removeprefix("v=")), dy=int(p4)))

    for i in range(100_000):
        positions: list[tuple[int, int]] = [robot.position(time=i) for robot in robots]
        x_to_nb: dict[int, int] = {}
        for x, _ in positions:
            x_to_nb.setdefault(x, 0)
            x_to_nb[x] += 1

        if max(x_to_nb.values()) > MAX_X / 3:
            show(positions)
            print(i, max(x_to_nb.values()))
            input()


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

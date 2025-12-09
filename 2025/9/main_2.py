from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def area(self, other: "Coordinate") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    coordinates: list[Coordinate] = []
    for line in content.splitlines():
        x, y = map(int, line.split(sep=","))
        coordinates.append(Coordinate(x=x, y=y))

    max_x = max(coordinate.x for coordinate in coordinates)
    max_y = max(coordinate.y for coordinate in coordinates)

    if max(max_x, max_y) > 100:
        raise ValueError("Max is too big")

    grid: list[list[str]] = [["."] * (max_x + 2) for _ in range(max_y + 2)]
    last_coordinate: Coordinate = coordinates[-1]
    for coordinate in coordinates:
        for x in range(min(coordinate.x, last_coordinate.x), max(coordinate.x, last_coordinate.x) + 1):
            for y in range(min(coordinate.y, last_coordinate.y), max(coordinate.y, last_coordinate.y) + 1):
                grid[y][x] = "X"
        grid[coordinate.y][coordinate.x] = "#"
        grid[last_coordinate.y][last_coordinate.x] = "#"
        last_coordinate = coordinate

    for line in grid:
        print("".join(line))


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

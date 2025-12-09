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

    max_area = 0
    for coordinate in coordinates:
        for other_coordinate in coordinates[coordinates.index(coordinate) + 1 :]:
            area = coordinate.area(other=other_coordinate)
            max_area = max(max_area, area)
    print(max_area)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def area(self, other: "Coordinate") -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


def get_borders(c1: Coordinate, c2: Coordinate) -> set[Coordinate]:
    min_x: int = min(c1.x, c2.x)
    max_x: int = max(c1.x, c2.x)
    min_y: int = min(c1.y, c2.y)
    max_y: int = max(c1.y, c2.y)
    borders: set[Coordinate] = set()
    for x in range(min_x + 1, max_x):
        borders.add(Coordinate(x=x, y=min_y))
        borders.add(Coordinate(x=x, y=max_y))
    for y in range(min_y + 1, max_y):
        borders.add(Coordinate(x=max_x, y=y))
        borders.add(Coordinate(x=min_x, y=y))
    return borders


def rectangle_in_polygon(
    c1: Coordinate,
    c2: Coordinate,
    horizontal_coordinates: set[Coordinate],
    vertical_coordinates: set[Coordinate],
    coordinates: list[Coordinate],
    y_to_vertical_xs: dict[int, list[int]],
    coordinate_to_in_polygon: dict[Coordinate, bool],
) -> bool:
    # if c1.x == 9 and c1.y == 5 and c2.x == 2 and c2.y == 3:
    #     print(get_borders(c1=c1, c2=c2))
    #     exit()
    borders: set[Coordinate] = get_borders(c1=c1, c2=c2)
    for index, border in enumerate(borders):
        print(f"Local progress: {100 * (index + 1) / len(borders): .2f} %")
        if border in coordinate_to_in_polygon:
            if not coordinate_to_in_polygon[border]:
                return False
            continue

        if (
            border not in horizontal_coordinates
            and border not in vertical_coordinates
            and border not in coordinates
            and not in_polygon(coordinate=border, y_to_vertical_xs=y_to_vertical_xs)
        ):
            coordinate_to_in_polygon[border] = False
            return False
        coordinate_to_in_polygon[border] = True
    return True


def in_polygon(coordinate: Coordinate, y_to_vertical_xs: dict[int, list[int]]) -> bool:
    xs: list[int] = y_to_vertical_xs[coordinate.y]
    if len(xs) % 2 != 0:
        print(coordinate, xs)
        return False
    for x1, x2 in zip(xs[::2], xs[1::2]):
        if x1 < coordinate.x < x2:
            return True
    print(coordinate, xs)
    return False


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    coordinates: list[Coordinate] = []
    for line in content.splitlines():
        x, y = map(int, line.split(sep=","))
        coordinates.append(Coordinate(x=x, y=y))

    # Calculate the horizontal and vertical borders
    horizontal_coordinates: set[Coordinate] = set()
    vertical_coordinates: set[Coordinate] = set()
    y_to_vertical_xs: dict[int, list[int]] = defaultdict(list)
    last_coordinate: Coordinate = coordinates[-1]
    for coordinate in coordinates:
        if coordinate.x == last_coordinate.x:
            for y in range(min(coordinate.y, last_coordinate.y) + 1, max(coordinate.y, last_coordinate.y)):
                vertical_coordinates.add(Coordinate(x=coordinate.x, y=y))
                y_to_vertical_xs[y].append(coordinate.x)
        else:
            for x in range(min(coordinate.x, last_coordinate.x) + 1, max(coordinate.x, last_coordinate.x)):
                horizontal_coordinates.add(Coordinate(x=x, y=coordinate.y))
            # the border are check differently so any x between last_coordinate.x and coordinate.x are ok
            y_to_vertical_xs[coordinate.y].append(coordinate.x)
        last_coordinate = coordinate

    for xs in y_to_vertical_xs.values():
        xs.sort()

    # Sort rectangles by area
    corners_to_area: dict[tuple[Coordinate, Coordinate], int] = {}
    for coordinate in coordinates:
        for other_coordinate in coordinates[coordinates.index(coordinate) + 1 :]:
            area = coordinate.area(other=other_coordinate)
            corners_to_area[(coordinate, other_coordinate)] = area
    sorted_corners: list[tuple[Coordinate, Coordinate]] = sorted(
        corners_to_area,
        key=lambda x: corners_to_area[x],
        reverse=True,
    )

    # Check if rectangles are in polygon by checking if all borders are in the polygon
    coordinate_to_in_polygon: dict[Coordinate, bool] = {}
    nb_rectangles: int = len(sorted_corners)
    for index, (c1, c2) in enumerate(sorted_corners):
        print(f"Global progress: {100 * (index + 1) / nb_rectangles: .2f} %")
        if rectangle_in_polygon(
            c1=c1,
            c2=c2,
            horizontal_coordinates=horizontal_coordinates,
            vertical_coordinates=vertical_coordinates,
            coordinates=coordinates,
            y_to_vertical_xs=y_to_vertical_xs,
            coordinate_to_in_polygon=coordinate_to_in_polygon,
        ):
            print(c1, c2)
            print(corners_to_area[(c1, c2)])
            return
        draw_grid(
            horizontal_coordinates=horizontal_coordinates,
            vertical_coordinates=vertical_coordinates,
            coordinates=coordinates,
            coordinate_to_in_polygon=coordinate_to_in_polygon,
        )
    raise ValueError("No rectangle found")


def draw_grid(
    horizontal_coordinates: set[Coordinate],
    vertical_coordinates: set[Coordinate],
    coordinates: list[Coordinate],
    coordinate_to_in_polygon: dict[Coordinate, bool],
) -> None:
    return
    max_x = max(coordinate.x for coordinate in coordinates)
    max_y = max(coordinate.y for coordinate in coordinates)
    if max(max_x, max_y) > 100:
        raise ValueError("Max is too big")
    grid: list[list[str]] = [["."] * (max_x + 1) for _ in range(max_y + 1)]
    for coordinate in horizontal_coordinates:
        grid[coordinate.y][coordinate.x] = "-"
    for coordinate in vertical_coordinates:
        grid[coordinate.y][coordinate.x] = "|"
    for coordinate in coordinates:
        grid[coordinate.y][coordinate.x] = "#"
    for coordinate, is_in_polygon in coordinate_to_in_polygon.items():
        grid[coordinate.y][coordinate.x] = "O" if is_in_polygon else "X"
    for line in grid:
        print("".join(line))
    print("")


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

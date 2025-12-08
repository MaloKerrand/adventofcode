from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
    z: int

    def distance(self, other: "Coordinate") -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz


def add_same_clique(c1: Coordinate, c2: Coordinate, cliques: list[set[Coordinate]]) -> None:
    """
    Update the cliques list by adding the two coordinates to the same clique if they are not already in the same clique.
    """
    c1_clique: set[Coordinate] | None = None
    c2_clique: set[Coordinate] | None = None
    for clique in cliques:
        if c1 in clique:
            c1_clique = clique
        if c2 in clique:
            c2_clique = clique

    if c1_clique is None and c2_clique is None:
        cliques.append({c1, c2})
        return

    if c1_clique is None:
        c2_clique.add(c1)
        return

    if c2_clique is None:
        c1_clique.add(c2)
        return

    if c1_clique == c2_clique:
        return

    cliques.remove(c1_clique)
    c2_clique.update(c1_clique)


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    coordinates: list[Coordinate] = []
    for line in content.splitlines():
        x, y, z = map(int, line.split(sep=","))
        coordinates.append(Coordinate(x=x, y=y, z=z))

    coordinates_to_distance: dict[tuple[Coordinate, Coordinate], int] = {}
    for index, coordinate in enumerate(coordinates):
        for other_coordinate in coordinates[index + 1 :]:
            coordinates_to_distance[(coordinate, other_coordinate)] = coordinate.distance(other=other_coordinate)

    coordinates_sorted_by_distance: list[tuple[Coordinate, Coordinate]] = sorted(
        coordinates_to_distance, key=lambda c: coordinates_to_distance[c]
    )

    last_distance = 0
    for key in coordinates_sorted_by_distance:
        if coordinates_to_distance[key] == last_distance:
            raise ValueError("Distance is not increasing")
        last_distance = coordinates_to_distance[key]

    cliques: list[set[Coordinate]] = []
    while True:
        if not coordinates_sorted_by_distance:
            raise ValueError("No more coordinates to process")
        c1, c2 = coordinates_sorted_by_distance.pop(0)
        add_same_clique(c1=c1, c2=c2, cliques=cliques)

        if len(cliques) == 1 and len(cliques[0]) == len(coordinates):
            print(c1.x * c2.x)
            break


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

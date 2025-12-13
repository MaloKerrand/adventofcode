import functools
from pathlib import Path


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    point_to_neighbors: dict[str, list[str]] = {}
    for line in content.splitlines():
        vertex, neighbors = line.split(sep=":")
        point_to_neighbors[vertex] = neighbors.strip().split(sep=" ")

    @functools.cache
    def nb_path_to_out(point: str) -> int:
        if point == "out":
            return 1
        return sum(nb_path_to_out(neighbor) for neighbor in point_to_neighbors.get(point, []))

    print(nb_path_to_out("you"))


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

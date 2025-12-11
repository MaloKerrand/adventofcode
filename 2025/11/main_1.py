from collections import defaultdict
from pathlib import Path


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    vertices: dict[str, list[str]] = {}
    for line in content.splitlines():
        vertex, neighbors = line.split(sep=":")
        vertices[vertex] = neighbors.strip().split(sep=" ")

    vertiex_to_nb_path: dict[str, int] = defaultdict(int)
    veticies_to_visit: list[str] = ["you"]
    while veticies_to_visit:
        vertex = veticies_to_visit.pop()
        for neighbor in vertices.get(vertex, []):
            vertiex_to_nb_path[neighbor] += 1
            veticies_to_visit.append(neighbor)
    print(vertiex_to_nb_path["out"])


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

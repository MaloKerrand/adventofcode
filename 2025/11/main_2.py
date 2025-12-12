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
    def nb_path(point_from: str, point_to: str) -> int:
        if point_from == point_to:
            return 1
        return sum(nb_path(neighbor, point_to) for neighbor in point_to_neighbors.get(point_from, []))

    svr_to_ftt = nb_path("svr", "fft")
    svr_to_dac = nb_path("svr", "dac")
    ftt_to_dac = nb_path("fft", "dac")
    dac_to_fft = nb_path("dac", "fft")
    dac_to_out = nb_path("dac", "out")
    ftt_to_out = nb_path("fft", "out")

    print(svr_to_ftt * ftt_to_dac * dac_to_out + svr_to_dac * dac_to_fft * ftt_to_out)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

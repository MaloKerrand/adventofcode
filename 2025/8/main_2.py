from collections import defaultdict
from pathlib import Path


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    lines = content.splitlines()

    max_coordinate = len(lines[0]) - 1
    current_coordinates_to_nb_split: dict[int, int] = {lines[0].index("S"): 1}
    for line in lines[1:]:
        new_coordinates_to_nb_split: dict[int, int] = defaultdict(int)
        for coordinate, nb_split in current_coordinates_to_nb_split.copy().items():
            tmp_new_coordinates = set()
            match line[coordinate]:
                case "^":
                    tmp_new_coordinates.add(coordinate - 1)
                    tmp_new_coordinates.add(coordinate + 1)
                case ".":
                    tmp_new_coordinates.add(coordinate)

            for new_coordinate in tmp_new_coordinates:
                if new_coordinate < 0:
                    continue
                if new_coordinate > max_coordinate:
                    continue
                new_coordinates_to_nb_split[new_coordinate] += nb_split
        current_coordinates_to_nb_split = new_coordinates_to_nb_split

    print(sum(current_coordinates_to_nb_split.values()))


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

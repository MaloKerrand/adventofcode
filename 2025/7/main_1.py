from pathlib import Path


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    lines = content.splitlines()

    max_coordinate = len(lines[0]) - 1
    current_coordinates: set[int] = {lines[0].index("S")}
    nb_split = 0
    for line in lines[1:]:
        new_coordinates: set[int] = set()
        for coordinate in current_coordinates:
            tmp_new_coordinates = set()
            match line[coordinate]:
                case "^":
                    nb_split += 1
                    tmp_new_coordinates.add(coordinate - 1)
                    tmp_new_coordinates.add(coordinate + 1)
                case ".":
                    tmp_new_coordinates.add(coordinate)
            for new_coordinate in tmp_new_coordinates:
                if new_coordinate < 0:
                    continue
                if new_coordinate > max_coordinate:
                    continue
                new_coordinates.add(new_coordinate)
        current_coordinates = new_coordinates
    print(nb_split)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

from pathlib import Path


def nb_adjacent(lines: list[list[int]], i: int, j: int, max_i: int, max_j: int) -> int:
    nb = 0
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_i = i + di
        new_j = j + dj
        if not (0 <= new_i < max_i and 0 <= new_j < max_j):
            continue
        if lines[new_i][new_j]:
            nb += 1
    return nb


def main():
    current_file = Path(__file__)
    with open(file=current_file.parent / "input", mode="r", encoding="utf-8") as f:
        lines: list[list[int]] = [[1 if i == "@" else 0 for i in line.removesuffix("\n")] for line in f.readlines()]

    max_i: int = len(lines)
    max_j: int = len(lines[0])
    nb_accessible: int = 0
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if not c:
                continue
            nb = nb_adjacent(lines=lines, i=i, j=j, max_i=max_i, max_j=max_j)
            if nb <= 3:
                nb_accessible += 1

    print(nb_accessible)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

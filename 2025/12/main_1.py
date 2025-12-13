from dataclasses import dataclass
from pathlib import Path


@dataclass
class Gift:
    coordinates: list[tuple[int, int]]

    def show(self) -> None:
        max_y: int = max(y for _, y in self.coordinates)
        max_x: int = max(x for x, _ in self.coordinates)
        for y in range(max_y + 1):
            line: list[str] = []
            for x in range(max_x + 1):
                if (x, y) in self.coordinates:
                    line.append("#")
                else:
                    line.append(".")
            print("".join(line))

    def size(self) -> int:
        return len(self.coordinates)


@dataclass
class Puzzle:
    max_x: int
    max_y: int
    gifts_quantities: list[int]

    def show(self) -> None:
        for _ in range(self.max_y + 1):
            print("".join("." * (self.max_x + 1)))

    def is_possible(self, gifts_sizes: list[int]) -> bool:
        if len(gifts_sizes) != len(self.gifts_quantities):
            raise ValueError("Number of gifts does not match")

        return (self.max_x + 1) * (self.max_y + 1) >= sum(
            [gifts_sizes[i] * self.gifts_quantities[i] for i in range(len(gifts_sizes))]
        )


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    gifts: list[Gift] = []
    puzzles: list[Puzzle] = []
    for block in content.split(sep="\n\n"):
        if block[1] == ":":
            coordinates: list[tuple[int, int]] = []
            for line_index, line in enumerate(block.splitlines()[1:]):
                line = line.strip()
                for char_index, char in enumerate(line):
                    if char == "#":
                        coordinates.append((char_index, line_index))
            gifts.append(Gift(coordinates=coordinates))
        else:
            for line in block.splitlines():
                size, *quantities = line.split(sep=" ")
                size_x, size_y = size.removesuffix(":").split(sep="x")
                puzzles.append(
                    Puzzle(
                        max_x=int(size_x) - 1,
                        max_y=int(size_y) - 1,
                        gifts_quantities=[int(quantity) for quantity in quantities],
                    )
                )

    gifts_sizes: list[int] = [gift.size() for gift in gifts]

    nb_possible = 0
    for puzzle in puzzles:
        if puzzle.is_possible(gifts_sizes=gifts_sizes):
            nb_possible += 1
    print(nb_possible)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

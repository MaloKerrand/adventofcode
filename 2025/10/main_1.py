from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np
from numpy._typing import NDArray


@dataclass
class Puzzle:
    lights: NDArray[np.int_]
    buttons: NDArray[np.int_]

    def minimal_nb_presses(self) -> int:
        minimal_nb_presses: int | None = None
        n = self.buttons.shape[1]
        for s in product([0, 1], repeat=n):
            # check if s is a valid solution buttons * s % 2== lights
            s: NDArray[np.int_] = np.array(s, dtype=np.int_)
            if np.all((np.matmul(self.buttons, s) % 2 == self.lights)):
                minimal_nb_presses = sum(s) if minimal_nb_presses is None else min(minimal_nb_presses, sum(s))
        if minimal_nb_presses is None:
            raise ValueError("No solution found")
        return minimal_nb_presses


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    puzzles: list[Puzzle] = []
    for line in content.splitlines():
        lights, *line_buttons, _ = line.split(sep=" ")
        puzzle_lights = np.array(
            [1 if l == "#" else 0 for l in lights.removeprefix("[").removesuffix("]")], dtype=np.int_
        )
        puzzle_buttons: NDArray[np.int_] = np.zeros((len(puzzle_lights), len(line_buttons)), dtype=np.int_)
        for button_index, button in enumerate(line_buttons):
            for light in button.removeprefix("(").removesuffix(")").split(sep=","):
                puzzle_buttons[int(light), button_index] = 1

        puzzles.append(
            Puzzle(
                lights=puzzle_lights,
                buttons=puzzle_buttons,
            )
        )

    nb_presses_total = 0
    for puzzle in puzzles:
        nb_presses_total += puzzle.minimal_nb_presses()
    print(nb_presses_total)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

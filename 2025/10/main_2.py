from collections import deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy._typing import NDArray


@dataclass
class Puzzle:
    objective: NDArray[np.int_]
    buttons: NDArray[np.int_]

    def nb_presses_to_solve(self) -> int:
        """Return the minimal number of non‑negative button presses to reach the objective."""
        target = tuple(int(v) for v in self.objective.tolist())
        m, n = self.buttons.shape

        # Quick sanity check: if any row is all zeros but objective is non‑zero, no solution.
        for row_idx in range(m):
            if np.all(self.buttons[row_idx, :] == 0) and target[row_idx] != 0:
                raise ValueError("No solution found")

        # Precompute column increments as tuples for faster updates.
        increments: list[tuple[int, ...]] = [tuple(int(v) for v in self.buttons[:, j].tolist()) for j in range(n)]

        start_state = tuple(0 for _ in range(m))
        if start_state == target:
            return 0

        visited: set[tuple[int, ...]] = {start_state}
        q: deque[tuple[tuple[int, ...], int]] = deque()
        q.append((start_state, 0))

        while q:
            state, presses = q.popleft()
            next_presses = presses + 1
            for inc in increments:
                # Compute next state; prune if we exceed the target on any coordinate.
                next_state_list: list[int] = []
                valid = True
                for cur, add, t in zip(state, inc, target):
                    v = cur + add
                    if v > t:
                        valid = False
                        break
                    next_state_list.append(v)
                if not valid:
                    continue

                next_state = tuple(next_state_list)
                if next_state == target:
                    return next_presses
                if next_state not in visited:
                    visited.add(next_state)
                    q.append((next_state, next_presses))

        raise ValueError("No solution found")


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    puzzles: list[Puzzle] = []
    for line in content.splitlines():
        _, *line_buttons, objective = line.split(sep=" ")
        objective_values = objective.removeprefix("{").removesuffix("}")
        puzzle_objective = np.array([int(v) for v in objective_values.split(",")], dtype=np.int_)
        puzzle_buttons: NDArray[np.int_] = np.zeros((len(puzzle_objective), len(line_buttons)), dtype=np.int_)
        for button_index, button in enumerate(line_buttons):
            for light in button.removeprefix("(").removesuffix(")").split(sep=","):
                puzzle_buttons[int(light), button_index] = 1

        puzzles.append(
            Puzzle(
                objective=puzzle_objective,
                buttons=puzzle_buttons,
            )
        )

    nb_presses_total = 0
    for puzzle in puzzles:
        nb_presses_total += puzzle.nb_presses_to_solve()
    print(nb_presses_total)


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

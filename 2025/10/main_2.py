from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
import pulp
from numpy._typing import NDArray


@dataclass(frozen=True)
class Puzzle:
    objective: NDArray[np.int_]
    buttons: NDArray[np.int_]  # shape: (n_lights, n_buttons)

    def min_presses(self) -> int:
        """
        Solve the non‑negative integer system A x = b minimizing sum(x) via MILP.
        """
        b = self.objective
        A = self.buttons
        n_lights, n_buttons = A.shape

        # Quick exit
        if np.all(b == 0):
            return 0

        prob = pulp.LpProblem("min_presses", pulp.LpMinimize)
        x_vars = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(n_buttons)]
        # Objective: minimize total presses
        prob += pulp.lpSum(x_vars)
        # Constraints: Ax = b
        for i in range(n_lights):
            prob += pulp.lpSum(A[i, j] * x_vars[j] for j in range(n_buttons)) == int(b[i])

        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            raise ValueError("No solution found")

        solution = [pulp.value(var) for var in x_vars]
        if any(v is None for v in solution):
            raise ValueError("No solution found")
        return int(round(sum(solution)))


def parse_input(path: Path) -> List[Puzzle]:
    puzzles: List[Puzzle] = []
    content = path.read_text(encoding="utf-8").splitlines()
    for line in content:
        if not line.strip():
            continue
        _, *btns, objective_str = line.split()
        objective = np.array([int(v) for v in objective_str[1:-1].split(",")], dtype=np.int_)
        n_lights = len(objective)
        n_buttons = len(btns)
        buttons = np.zeros((n_lights, n_buttons), dtype=np.int_)
        for j, btn in enumerate(btns):
            for light in btn[1:-1].split(","):
                if light:
                    buttons[int(light), j] = 1
        puzzles.append(Puzzle(objective=objective, buttons=buttons))
    return puzzles


def main() -> None:
    current_file = Path(__file__)
    puzzles = parse_input(current_file.parent / "input")

    total = 0
    for idx, puzzle in enumerate(puzzles):
        if len(puzzles) > 10:
            print(f"{100 * idx / len(puzzles):.2f}%")
        total += puzzle.min_presses()
    print(total)


if __name__ == "__main__":
    # Simple timeout wrapper to avoid long hangs
    import concurrent.futures
    import sys

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(main)
            fut.result(timeout=20)
    except concurrent.futures.TimeoutError:
        print("Timed out")
        sys.exit(1)

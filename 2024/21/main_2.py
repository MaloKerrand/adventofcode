from collections import deque
from functools import cache
from pathlib import Path
from typing import Iterable

NUMERIC_KEYPAD: list[list[str | None]] = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
NUMERIC_COORDS: dict[str, tuple[int, int]] = {
    value: (x, y) for y, row in enumerate(NUMERIC_KEYPAD) for x, value in enumerate(row) if value is not None
}

DIR_KEYPAD: list[list[str | None]] = [
    [None, "^", "A"],
    ["<", "v", ">"],
]
DIR_COORDS: dict[str, tuple[int, int]] = {
    value: (x, y) for y, row in enumerate(DIR_KEYPAD) for x, value in enumerate(row) if value is not None
}


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    codes: list[str] = content.splitlines()

    # Part 2: 25 directional keypads operated by robots.
    robot_layers = 25

    total = 0
    for code in codes:
        total += cost_code(code=code, robot_layers=robot_layers)
    print(total)


def neighbors(
    keypad: list[list[str | None]],
    coords: dict[str, tuple[int, int]],
    char: str,
) -> Iterable[tuple[str, int, int, str]]:
    """Yield possible moves (target_char, x, y, move_symbol) from current char."""
    x, y = coords[char]
    moves: dict[str, tuple[int, int]] = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0),
    }
    for move, (dx, dy) in moves.items():
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(keypad) and 0 <= nx < len(keypad[ny]):
            target: str | None = keypad[ny][nx]
            if target is not None:
                yield target, nx, ny, move


def all_shortest_paths(
    keypad: list[list[str | None]],
    coords: dict[str, tuple[int, int]],
    char_from: str,
    char_to: str,
) -> list[str]:
    """Return all shortest sequences of button presses (including final 'A')."""
    if char_from == char_to:
        return ["A"]

    queue: deque[tuple[str, str]] = deque()
    start_x, start_y = coords[char_from]
    queue.append((char_from, ""))

    best_dist: int | None = None
    results: list[str] = []
    visited: dict[tuple[int, int], int] = {(start_x, start_y): 0}

    while queue:
        char, path = queue.popleft()
        if best_dist is not None and len(path) > best_dist:
            break
        if char == char_to:
            best_dist: int = len(path) if best_dist is None else best_dist
            results.append(path + "A")
            continue
        for target, nx, ny, move in neighbors(keypad=keypad, coords=coords, char=char):
            next_len: int = len(path) + 1
            # Only keep exploring equally short routes.
            if best_dist is not None and next_len > best_dist:
                continue
            if visited.get((nx, ny), next_len) < next_len:
                continue
            visited[(nx, ny)] = next_len
            queue.append((target, path + move))

    return results


# Pre-compute all shortest paths for both keypads.
NUMERIC_PATHS: dict[tuple[str, str], list[str]] = {
    (a, b): all_shortest_paths(keypad=NUMERIC_KEYPAD, coords=NUMERIC_COORDS, char_from=a, char_to=b)
    for a in NUMERIC_COORDS
    for b in NUMERIC_COORDS
}
DIR_PATHS: dict[tuple[str, str], list[str]] = {
    (a, b): all_shortest_paths(keypad=DIR_KEYPAD, coords=DIR_COORDS, char_from=a, char_to=b)
    for a in DIR_COORDS
    for b in DIR_COORDS
}


@cache
def sequence_cost(sequence: str, depth: int) -> int:
    """Cost to type a whole sequence on a directional keypad with `depth` robots above."""
    current = "A"
    total = 0
    for char in sequence:
        total += move_cost("dir", depth, current, char)
        current = char
    return total


@cache
def move_cost(keypad_type: str, depth: int, char_from: str, char_to: str) -> int:
    """Minimal button presses on our keypad to press `char_to` from `char_from` at given depth."""
    if keypad_type == "num":
        paths = NUMERIC_PATHS[(char_from, char_to)]
        next_depth = depth - 1
    else:
        paths = DIR_PATHS[(char_from, char_to)]
        next_depth = depth - 1

    if depth == 0:
        return min(len(path) for path in paths)

    return min(sequence_cost(path, next_depth) for path in paths)


def cost_code(code: str, robot_layers: int) -> int:
    # Numeric part ignores trailing A and leading zeroes.
    code_value = int(code[:-1])

    total_presses = 0
    current_char = "A"
    for char in code:
        total_presses += move_cost("num", robot_layers, current_char, char)
        current_char = char
    return code_value * total_presses


if __name__ == "__main__":
    main()

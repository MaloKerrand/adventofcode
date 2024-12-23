from functools import cache


def main():
    with open("input", "r") as f:
        codes: list[str] = f.read().splitlines()

    total = 0
    for code in codes:
        complexity = cost_code(list(code))
        total += complexity
    print(total)


def n_code_to_d_code(n_code: list[str], nb_d_code: int) -> list[str]:
    d_code: list[str] = []
    current_char = "A"
    for char in n_code:
        sub_codes: list[list[str]] = n_to_d(char_from=current_char, char_to=char)
        d_d_sub_codes: list[list[str]] = [
            d_code_to_d_code(d_code=tuple(code), nb_d_code=nb_d_code) for code in sub_codes
        ]
        d_code += min(d_d_sub_codes, key=lambda c: len(c))
        current_char = char
    return d_code


@cache
def d_code_to_d_code(d_code: tuple[str], nb_d_code: int) -> list[str]:
    if nb_d_code == 0:
        return list(d_code)

    d_d_code: list[str] = []
    current_char = "A"
    for char in d_code:
        sub_codes: list[list[str]] = d_to_d(char_from=current_char, char_to=char)
        d_sub_codes: list[list[str]] = [
            d_code_to_d_code(d_code=tuple(code), nb_d_code=nb_d_code - 1) for code in sub_codes
        ]
        d_d_code += min(d_sub_codes, key=lambda c: len(c))
        current_char = char
    return d_d_code


@cache
def d_to_d(char_from: str, char_to: str) -> list[list[str]]:
    if char_from == char_to:
        return [["A"]]
    code_to_x_y: dict[str, tuple[int, int]] = {
        "A": (2, 0),
        "^": (1, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1),
    }
    keypad = [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]
    x_from, y_from = code_to_x_y[char_from]
    x_to, y_to = code_to_x_y[char_to]

    d_codes: list[list[str]] = []
    if x_from < x_to and keypad[y_from][x_from + 1] is not None:
        d_codes += [
            [">"] + l for l in d_to_d(keypad[y_from][x_from + 1], char_to=char_to) if (">" == l[0] or ">" not in l[1:])
        ]

    if y_from > y_to and keypad[y_from - 1][x_from] is not None:
        d_codes += [
            ["^"] + l for l in d_to_d(keypad[y_from - 1][x_from], char_to=char_to) if ("^" == l[0] or "^" not in l[1:])
        ]

    if y_from < y_to and keypad[y_from + 1][x_from] is not None:
        d_codes += [
            ["v"] + l for l in d_to_d(keypad[y_from + 1][x_from], char_to=char_to) if ("v" == l[0] or "v" not in l[1:])
        ]

    if x_from > x_to and keypad[y_from][x_from - 1] is not None:
        d_codes += [
            ["<"] + l for l in d_to_d(keypad[y_from][x_from - 1], char_to=char_to) if ("<" == l[0] or "<" not in l[1:])
        ]

    return d_codes


def n_to_d(char_from: str, char_to: str) -> list[list[str]]:
    if char_from == char_to:
        return [["A"]]
    code_to_x_y: dict[str, tuple[int, int]] = {
        "A": (2, 3),
        "0": (1, 3),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
    }
    keypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ]
    x_from, y_from = code_to_x_y[char_from]
    x_to, y_to = code_to_x_y[char_to]

    d_codes: list[list[str]] = []
    if x_from < x_to and keypad[y_from][x_from + 1] is not None:
        d_codes += [
            [">"] + l for l in n_to_d(keypad[y_from][x_from + 1], char_to=char_to) if (">" == l[0] or ">" not in l[1:])
        ]

    if y_from > y_to and keypad[y_from - 1][x_from] is not None:
        d_codes += [
            ["^"] + l for l in n_to_d(keypad[y_from - 1][x_from], char_to=char_to) if ("^" == l[0] or "^" not in l[1:])
        ]

    if y_from < y_to and keypad[y_from + 1][x_from] is not None:
        d_codes += [
            ["v"] + l for l in n_to_d(keypad[y_from + 1][x_from], char_to=char_to) if ("v" == l[0] or "v" not in l[1:])
        ]

    if x_from > x_to and keypad[y_from][x_from - 1] is not None:
        d_codes += [
            ["<"] + l for l in n_to_d(keypad[y_from][x_from - 1], char_to=char_to) if ("<" == l[0] or "<" not in l[1:])
        ]

    return d_codes


def cost_code(code: list[str]) -> int:
    code_value = int("".join(code).lstrip("0").rstrip("A"))
    last_code = n_code_to_d_code(n_code=code, nb_d_code=2)
    return code_value * len(last_code)


if __name__ == "__main__":
    main()

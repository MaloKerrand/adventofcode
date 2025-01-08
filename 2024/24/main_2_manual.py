import math
from collections import defaultdict
from itertools import product

good_keys: set[str] = set()


def main():
    with open("input", "r") as f:
        content: str = f.read()

    start, equations = content.split("\n\n")

    inputs: dict[str, bool] = defaultdict(lambda: False)

    unsolved: dict[str, tuple[str, str, str]] = {}
    for equation in equations.splitlines():
        n1, operation, n2, _, r = equation.split(" ")
        unsolved[r] = (n1, operation, n2)

    swaps_to_nb_errors: dict[tuple[str, ...], int | None] = {}
    current = 0
    total = math.comb(len(unsolved), 2)

    swaps: list[tuple[str, str]] = []
    n_with_errors(inputs=inputs, unsolved=unsolved, swaps=swaps)


def n_with_errors(
    inputs: dict[str, bool],
    unsolved: dict[str, tuple[str, str, str]],
    swaps: list[tuple[str, str]],
) -> int | None:
    switched_unsolved = unsolved.copy()
    for _s1, _s2 in swaps:
        switched_unsolved[_s1], switched_unsolved[_s2] = (
            switched_unsolved[_s2],
            switched_unsolved[_s1],
        )
    for n in range(45):
        if nb_errors(inputs=inputs, unsolved=switched_unsolved, max_n=n):
            print(f"Error on {n}")
            return n
    return None


def nb_errors(inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]], max_n: int = 45) -> int | None:
    # errors = test_max(inputs=inputs, unsolved=unsolved)
    # if errors is None:
    #     return None
    errors = 0
    for n in range(max_n):
        error = test_n(n=n, inputs=inputs, unsolved=unsolved)
        if error is None:
            return None
        errors += error
    return errors


def test_n(n: int, inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> int | None:
    original_input = inputs
    original_unsolved = unsolved
    errors = 0
    for x, y in product([True, False], [True, False]):
        inputs = original_input.copy()
        unsolved = original_unsolved.copy()
        inputs[f"x{n:02d}"] = x
        inputs[f"y{n:02d}"] = y

        try:
            resolve(key=f"z{n:02d}", inputs=inputs, unsolved=unsolved)
            resolve(key=f"z{n+1:02d}", inputs=inputs, unsolved=unsolved)
        except KeyError:
            return None

        if inputs[f"z{n:02d}"] != x ^ y:
            # print(n, f"{int(x)}+{int(y)}={int(inputs[f'z{n+1:02d}'])}{int(inputs[f'z{n:02d}'])}")
            errors += 1

        if inputs[f"z{n+1:02d}"] != x and y:
            # print(n, f"{int(x)}+{int(y)}={int(inputs[f'z{n+1:02d}'])}{int(inputs[f'z{n:02d}'])}")
            errors += 1

    return errors


def test_max(inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> int | None:
    inputs = inputs.copy()
    unsolved = unsolved.copy()
    for n in range(45):
        inputs[f"x{n:02d}"] = True
        inputs[f"y{n:02d}"] = True

    while unsolved:
        try:
            resolve(key=list(unsolved.keys())[0], inputs=inputs, unsolved=unsolved)
        except KeyError:
            return None

    result: dict[int, bool] = {}
    for name, value in inputs.items():
        if not name.startswith("z"):
            continue
        result[int(name.lstrip("z"))] = value

    max_z = max(result)
    r_string = "".join(reversed([str(int(result[i])) for i in range(max_z + 1)]))
    value = int(r_string, 2)
    return 0 if value == int("1" * 45, 2) else 1


def resolve(key: str, inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> bool:
    if key in inputs or key.startswith("x") or key.startswith("y"):
        return inputs[key]

    n1, op, n2 = unsolved.pop(key)
    v1 = resolve(key=n1, inputs=inputs, unsolved=unsolved)
    v2 = resolve(key=n2, inputs=inputs, unsolved=unsolved)

    v = calcul(v1=v1, op=op, v2=v2)

    inputs[key] = v
    return v


def calcul(v1: bool, op: str, v2: bool) -> bool:
    match op:
        case "AND":
            return v1 and v2
        case "OR":
            return v1 or v2
        case "XOR":
            return v1 ^ v2

    raise Exception(f"Unknown operation {op!r}")


def involve(key: str, unsolved: dict[str, tuple[str, str, str]]) -> set[str]:
    if key.startswith("x") or key.startswith("y"):
        return {key}

    n1, _, n2 = unsolved[key]
    return {key} | involve(key=n1, unsolved=unsolved) | involve(key=n2, unsolved=unsolved)


if __name__ == "__main__":
    main()
    # nqk <-> z07
    # fgt <-> pcp

import itertools
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

    print(nb_errors(inputs=inputs, unsolved=unsolved))

    swaps_to_nb_errors: dict[tuple[str, ...], int | None] = {}
    current = 0
    total = math.comb(len(unsolved), 2)
    for s1, s2 in itertools.combinations(iterable=unsolved.keys(), r=2):
        current += 1
        print(f"{100 * current/total:.2f} %")
        switched_unsolved = unsolved.copy()
        switched_unsolved[s1], switched_unsolved[s2] = (
            switched_unsolved[s2],
            switched_unsolved[s1],
        )
        swaps_to_nb_errors[tuple(sorted([s1, s2]))] = nb_errors(inputs=inputs, unsolved=switched_unsolved)

    swaps_2_to_nb_errors: dict[tuple[str, ...], int] = {
        (*s1, *s2): (swaps_to_nb_errors[s1] or 0) + (swaps_to_nb_errors[s2] or 0)
        for s1, s2 in itertools.combinations(iterable=swaps_to_nb_errors.keys(), r=2)
    }
    current = 0
    total = len(swaps_2_to_nb_errors)
    for s11, s12, s21, s22 in sorted(swaps_2_to_nb_errors.keys(), key=swaps_2_to_nb_errors.get):
        current += 1
        print(f"{100 * current / total:.2f} %")
        switched_unsolved = unsolved.copy()
        switched_unsolved[s11], switched_unsolved[s12] = (
            switched_unsolved[s12],
            switched_unsolved[s11],
        )
        switched_unsolved[s21], switched_unsolved[s22] = (
            switched_unsolved[s22],
            switched_unsolved[s21],
        )
        nb_error = nb_errors(inputs=inputs, unsolved=switched_unsolved)
        if nb_error == 0:
            print("Found it !")
            print((s11, s12), (s21, s22))
            return
    print("Not found :<")


def nb_errors(inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> int | None:
    errors = 0
    for n in range(45):
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

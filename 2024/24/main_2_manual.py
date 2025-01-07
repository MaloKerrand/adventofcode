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
    # for s1, s2 in itertools.combinations(iterable=unsolved.keys(), r=2):
    #     current += 1
    #     print(f"{100 * current/total:.2f} %")
    #     switched_unsolved = unsolved.copy()
    #     switched_unsolved[s1], switched_unsolved[s2] = (
    #         switched_unsolved[s2],
    #         switched_unsolved[s1],
    #     )
    #     nb_error = nb_errors(inputs=inputs, unsolved=switched_unsolved)
    #     if nb_error is None:
    #         continue
    #     swaps_to_nb_errors[tuple(sorted([s1, s2]))] = nb_errors(inputs=inputs, unsolved=switched_unsolved)

    # better: set[tuple[str, ...]] = {swap for swap, error in swaps_to_nb_errors.items() if error < 20}
    better = {
        ("mqq", "z07"),
        ("fpq", "jss"),
        ("z07", "z08"),
        ("nmq", "pcp"),
        ("jss", "tgs"),
        ("fpq", "qcs"),
        ("krv", "pcp"),
        ("nqk", "pcp"),
        ("fpq", "z24"),
        ("mqq", "qcs"),
        ("fgt", "pcp"),
        ("mqq", "z24"),
        ("nqk", "stq"),
        ("jss", "qcs"),
        ("jss", "krv"),
        ("jss", "z24"),
        ("fcg", "z17"),
        ("z17", "z18"),
        ("pcs", "z32"),
        ("pcp", "z17"),
        ("vjv", "z24"),
        ("gdb", "jss"),
        ("fgt", "nqk"),
        ("nqk", "z07"),
        ("z24", "z25"),
        ("fcg", "z07"),
        ("qcs", "z07"),
        ("pcp", "z07"),
        ("jss", "mqq"),
        ("qcs", "tgs"),
        ("fgt", "z07"),
        ("jnv", "pcp"),
        ("fcg", "jss"),
        ("krv", "qcs"),
        ("z07", "z24"),
        ("srn", "z07"),
        ("fgt", "jss"),
        ("nqk", "qcs"),
        ("krv", "z24"),
        ("fcg", "qcs"),
        ("tgs", "z07"),
        ("fcg", "z24"),
        ("stq", "z08"),
        ("fgt", "qcs"),
        ("pcp", "qcs"),
        ("fgt", "krv"),
        ("mqq", "pcp"),
        ("rgc", "z24"),
        ("pcp", "z24"),
        ("nqk", "z24"),
        ("jss", "z08"),
        ("jss", "pcp"),
        ("qcs", "z24"),
        ("fgt", "z24"),
        ("jss", "srn"),
        ("fcp", "pcp"),
        ("srn", "z32"),
        ("btq", "jss"),
        ("gtj", "z24"),
        ("srn", "z24"),
        ("krv", "mqq"),
        ("tgs", "z24"),
        ("nmp", "z24"),
        ("fcg", "mqq"),
        ("fpq", "z07"),
        ("mqq", "nqk"),
        ("fgt", "mqq"),
        ("jss", "nqk"),
        ("dsw", "jss"),
    }
    print(better)
    print(f"{len(better)=}")
    current = 0
    total = math.comb(len(better), 4)
    for s1, s2, s3, s4 in itertools.combinations(iterable=better, r=4):
        current += 1
        print(f"{100 * current / total:.2f} %")
        switched_unsolved = unsolved.copy()
        for _s1, _s2 in (s1, s2, s3, s4):
            switched_unsolved[_s1], switched_unsolved[_s2] = (
                switched_unsolved[_s2],
                switched_unsolved[_s1],
            )
        nb_error = nb_errors(inputs=inputs, unsolved=switched_unsolved)
        if nb_error == 0:
            print("Found it !")
            print((s1, s2, s3, s4))
            return
    print("Not found :<")


def nb_errors(inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> int | None:
    errors = test_max(inputs=inputs, unsolved=unsolved)
    if errors is None:
        return None
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

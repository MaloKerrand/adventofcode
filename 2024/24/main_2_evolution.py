import random
from collections import defaultdict
from itertools import product

NB_PER_BATCH = 1000
NB_SWITCH = 4
NB_BIT = 45
TESTED: set[tuple[str, ...]] = set()


def main():
    with open("input", "r") as f:
        content: str = f.read()

    start, equations = content.split("\n\n")

    inputs: dict[str, bool] = defaultdict(lambda: False)

    unsolved: dict[str, tuple[str, str, str]] = {}
    for equation in equations.splitlines():
        n1, operation, n2, _, r = equation.split(" ")
        unsolved[r] = (n1, operation, n2)

    batch: list[list[str]] = [random.sample(list(unsolved.keys()), 2 * NB_SWITCH) for _ in range(NB_PER_BATCH)]
    # batch.append(["srn", "z32", "tgs", "z24", "fgt", "pcp", "nqk", "z07"])

    for generation in range(10_000):
        print(f"Generation {generation}")
        result: list[tuple[list[str], int]] = []
        for index, permutation in enumerate(batch):
            TESTED.add(tuple(permutation))
            switched_unsolved = unsolved.copy()
            for s1, s2 in zip(permutation[::2], permutation[1::2]):
                switched_unsolved[s1], switched_unsolved[s2] = (
                    switched_unsolved[s2],
                    switched_unsolved[s1],
                )
            nb_error = nb_errors(inputs=inputs, unsolved=switched_unsolved) or 4 * NB_BIT
            if nb_error == 0:
                print("Found it !")
                print(permutation)
                return
            result.append((permutation, nb_error))

        result.sort(key=lambda x: x[1])
        batch = []
        for _ in range(NB_PER_BATCH):
            candidate = result[random.randint(0, NB_PER_BATCH // 100)][0].copy()
            for _ in range(100):
                if tuple(candidate) not in TESTED:
                    break
                new = random.choice(list(unsolved.keys()))
                for _ in range(100):
                    if new not in candidate:
                        break
                    new = random.choice(list(unsolved.keys()))
                candidate[random.randint(0, 2 * NB_SWITCH - 1)] = new

            batch.append(candidate)
        batch.append(result[0][0])
        print(f"Best is {result[0]}")
    print("Found nothing")


def nb_errors(inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> int | None:
    errors = test_max(inputs=inputs, unsolved=unsolved)
    if errors is None:
        return None
    for n in range(NB_BIT):
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


if __name__ == "__main__":
    main()

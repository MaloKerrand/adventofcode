def main():
    with open("input", "r") as f:
        content: str = f.read()

    start, equations = content.split("\n\n")

    inputs: dict[str, bool] = {}
    for line in start.splitlines():
        name, value = line.split(": ")
        inputs[name] = value == "1"

    unsolved: dict[str, tuple[str, str, str]] = {}
    for equation in equations.splitlines():
        n1, operation, n2, _, r = equation.split(" ")
        unsolved[r] = (n1, operation, n2)

    while unsolved:
        resolve(key=list(unsolved.keys())[0], inputs=inputs, unsolved=unsolved)

    result: dict[int, bool] = {}
    for name, value in inputs.items():
        if not name.startswith("z"):
            continue
        result[int(name.lstrip("z"))] = value

    max_z = max(result)
    r_string = "".join(reversed(["1" if result[i] else "0" for i in range(max_z + 1)]))
    print(int(r_string, 2))


def resolve(key: str, inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> bool:
    if key in inputs:
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

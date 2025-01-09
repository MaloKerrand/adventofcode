"""
                      ____________________XOR-(Zn)________
                     /                                     \
         ________OR-(ORn)________                      Xn-XOR-(XORn)-Yn
        /                        \
ORn1-AND-XORn1               Xn1-AND-Yn1
"""
import math
from collections import defaultdict
from dataclasses import dataclass
from itertools import product

good_keys: set[str] = set()


@dataclass
class Equation:
    left: str
    op: str
    right: str


def main():
    with open("input", "r") as f:
        content: str = f.read()

    _, equations_raw = content.split("\n\n")

    equations: dict[str, Equation] = {}
    for equation in equations_raw.splitlines():
        n1, operation, n2, _, r = equation.split(" ")
        equations[r] = Equation(left=n1, op=operation, right=n2)

    swaps = solve(equations)
    print(",".join(sorted(s for swap in swaps for s in swap)))


def solve(equations: dict[str, Equation]) -> list[tuple[str, str]]:
    swaps: list[tuple[str, str]] = []
    or_n1: str | None = None
    xor_n1: str | None = None

    for n in range(45):
        zn = f"z{n:02d}"
        zn_equation = equations[zn]

        if n == 0:
            zn_equation_expected = Equation(left="x00", op="XOR", right="y00")
            if zn_equation != zn_equation_expected:
                print("z00 wrong")
                real_zn = equation_to_name(equation=zn_equation_expected, equations=equations)
                swaps.append((zn, real_zn))
                equations[zn], equations[real_zn] = equations[real_zn], equations[zn]
            continue

        if n == 1:
            left_equation_expected = Equation(left="x00", op="AND", right="y00")
            left_expected = equation_to_name(equation=left_equation_expected, equations=equations)
            right_equation_expected = Equation(left="x01", op="XOR", right="y01")
            right_expected = equation_to_name(equation=right_equation_expected, equations=equations)
            zn_equation_expected = Equation(left=left_expected, op="XOR", right=right_expected)
            if zn_equation.op != zn_equation_expected:
                print("z01 wrong")
                possible_swaps: list[tuple[str, Equation]] = [
                    (zn, zn_equation_expected),
                    (zn_equation.left, zn_equation_expected),
                ]
                for name, equation in possible_swaps:
                    real_name = equation_to_name(equation=equation, equations=equations)
                    if real_name == name:
                        continue
                    swaps.append((name, real_name))
                    equations[name], equations[real_name] = equations[real_name], equations[name]
                    break

            left_equation = equations[zn_equation.left]
            right_equation = equations[zn_equation.right]
            or_n1 = None
            xor_n1 = None
            continue

        or_n: str | None = None
        xor_n: str | None = None

        or_n1 = or_n
        xor_n1 = xor_n

    return


def equation_to_name(equation: Equation, equations: dict[str, Equation]) -> str | None:
    for name, _equation in equations.items():
        if equation == _equation:
            return name
    return None


def resolve(key: str, inputs: dict[str, bool], unsolved: dict[str, tuple[str, str, str]]) -> bool:
    if key in inputs or key.startswith("x") or key.startswith("y"):
        return inputs[key]

    n1, op, n2 = unsolved.pop(key)
    v1 = resolve(key=n1, inputs=inputs, unsolved=unsolved)
    v2 = resolve(key=n2, inputs=inputs, unsolved=unsolved)

    v = calcul(v1=v1, op=op, v2=v2)

    inputs[key] = v
    return v


def involve(key: str, unsolved: dict[str, tuple[str, str, str]]) -> set[str]:
    if key.startswith("x") or key.startswith("y"):
        return {key}

    n1, _, n2 = unsolved[key]
    return {key} | involve(key=n1, unsolved=unsolved) | involve(key=n2, unsolved=unsolved)


if __name__ == "__main__":
    main()

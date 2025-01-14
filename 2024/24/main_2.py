from dataclasses import dataclass

good_keys: set[str] = set()


@dataclass
class Equation:
    left: str
    op: str
    right: str

    def __eq__(self, other):
        if not isinstance(other, Equation):
            raise TypeError(f"Cannot compare Equation object to {type(other)}")
        return self.op == other.op and (
            (self.left == other.left and self.right == other.right)
            or (self.left == other.right and self.right == other.left)
        )


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
        match n:
            case 0:
                swaps += z_0(equations)
                continue
            case 1:
                s, or_n1, xor_n1 = z_1(equations)
                swaps += s
            case _:
                s, or_n1, xor_n1 = z_n(n=n, equations=equations, or_n1=or_n1, xor_n1=xor_n1)
                swaps += s

    return swaps


def z_0(equations: dict[str, Equation]) -> list[tuple[str, str]]:
    """x00-XOR-(z00)-y00"""
    zn = "z00"
    zn_equation = equations[zn]
    zn_equation_expected = Equation(left="x00", op="XOR", right="y00")
    if zn_equation == zn_equation_expected:
        return []

    print("z00 wrong")
    real_zn = equation_to_name(equation=zn_equation_expected, equations=equations)
    equations[zn], equations[real_zn] = equations[real_zn], equations[zn]
    return [(zn, real_zn)]


def z_1(equations: dict[str, Equation]) -> tuple[list[tuple[str, str]], str, str]:
    """
          ________XOR-(z01)________
         /                         \
    x00-AND-y00               x01-XOR-y01
    """
    swaps = []
    zn = "z01"
    zn_equation = equations[zn]
    left_equation_expected = Equation(left="x00", op="AND", right="y00")
    left_expected = equation_to_name(equation=left_equation_expected, equations=equations)
    right_equation_expected = Equation(left="x01", op="XOR", right="y01")
    right_expected = equation_to_name(equation=right_equation_expected, equations=equations)
    zn_equation_expected = Equation(left=left_expected, op="XOR", right=right_expected)
    if zn_equation != zn_equation_expected:
        print("z01 wrong")
        real_name = equation_to_name(equation=zn_equation_expected, equations=equations)
        if real_name is not None:
            swaps.append((zn, real_name))
            equations[zn], equations[real_name] = equations[real_name], equations[zn]
            return swaps, left_expected, right_expected

        if zn_equation.op != zn_equation_expected.op:
            raise Exception("z01 op wrong and cannot find replacement")

        if zn_equation.left == left_expected:
            expected_switch = (zn_equation.right, right_equation_expected)
        elif zn_equation.left == right_expected:
            expected_switch = (zn_equation.right, left_equation_expected)
        elif zn_equation.right == right_expected:
            expected_switch = (zn_equation.left, left_equation_expected)
        elif zn_equation.right == left_expected:
            expected_switch = (zn_equation.left, right_equation_expected)
        else:
            raise Exception("z01 left and right wrong and cannot find replacement")

        real_name = equation_to_name(equation=expected_switch[1], equations=equations)
        if real_name is None:
            raise Exception(f"Failed to find replacement for {expected_switch[0]}")
        old_name = expected_switch[0]
        swaps.append((old_name, real_name))
        equations[old_name], equations[real_name] = (equations[real_name], equations[old_name])

    or_n1 = equation_to_name(equation=left_equation_expected, equations=equations)
    xor_n1 = equation_to_name(equation=right_equation_expected, equations=equations)

    return swaps, or_n1, xor_n1


def z_n(n: int, equations: dict[str, Equation], or_n1: str, xor_n1: str) -> tuple[list[tuple[str, str]], str, str]:
    """
                          ____________________XOR-(Zn)________
                         /                                     \
             ________OR-(ORn)________                      Xn-XOR-(XORn)-Yn
            /                        \
    ORn1-AND-XORn1               Xn1-AND-Yn1
    """
    swaps = []
    zn = f"z{n:02d}"
    zn_equation = equations[zn]

    or_n_left_equation_expected = Equation(left=or_n1, op="AND", right=xor_n1)
    or_n_left_expected: str = equation_to_name(equation=or_n_left_equation_expected, equations=equations)

    or_n_right_equation_expected = Equation(left=f"x{n-1:02d}", op="AND", right=f"y{n-1:02d}")
    or_n_right_expected: str = equation_to_name(equation=or_n_right_equation_expected, equations=equations)

    or_n_equation_expected = Equation(left=or_n_left_expected, op="OR", right=or_n_right_expected)
    or_n_expected: str = equation_to_name(equation=or_n_equation_expected, equations=equations)

    xor_n_equation_expected = Equation(left=f"x{n:02d}", op="XOR", right=f"y{n:02d}")
    xor_n_expected: str = equation_to_name(equation=xor_n_equation_expected, equations=equations)

    zn_equation_expected = Equation(left=or_n_expected, op="XOR", right=xor_n_expected)

    # Case all ok
    if zn_equation == zn_equation_expected:
        return [], or_n_expected, xor_n_expected

    print(f"{zn} wrong")
    # Case zn swaps
    real_name = equation_to_name(equation=zn_equation_expected, equations=equations)
    if real_name is not None:
        equations[zn], equations[real_name] = equations[real_name], equations[zn]
        return [(zn, real_name)], or_n_expected, xor_n_expected

    if zn_equation.op != zn_equation_expected.op:
        raise Exception(f"{zn} op wrong and cannot find replacement")

    # Case or_n and xor_n swaps
    if zn_equation.left == or_n_expected:
        expected_switch = (zn_equation.right, xor_n_equation_expected)
    elif zn_equation.left == xor_n_expected:
        expected_switch = (zn_equation.right, or_n_equation_expected)
    elif zn_equation.right == xor_n_expected:
        expected_switch = (zn_equation.left, or_n_equation_expected)
    elif zn_equation.right == or_n_expected:
        expected_switch = (zn_equation.left, xor_n_equation_expected)
    else:
        raise Exception(f"{zn} left and right wrong and cannot find replacement")

    real_name = equation_to_name(equation=expected_switch[1], equations=equations)
    # case or_n_left_expected or or_n_right_expected swaps
    if real_name is None:
        or_n_equation = equations[expected_switch[0]]
        if or_n_equation.left == or_n_left_expected:
            expected_switch = (or_n_equation.right, or_n_right_equation_expected)
        elif or_n_equation.left == or_n_right_expected:
            expected_switch = (or_n_equation.right, or_n_left_equation_expected)
        elif or_n_equation.right == or_n_right_expected:
            expected_switch = (or_n_equation.left, or_n_left_equation_expected)
        elif or_n_equation.right == or_n_left_expected:
            expected_switch = (or_n_equation.left, or_n_right_equation_expected)
        else:
            raise Exception(f"{zn} xor_n left and right wrong and cannot find replacement")

    real_name = equation_to_name(equation=expected_switch[1], equations=equations)
    old_name = expected_switch[0]
    swaps.append((old_name, real_name))
    equations[old_name], equations[real_name] = (equations[real_name], equations[old_name])

    # After swaps
    or_n_left_equation = Equation(left=or_n1, op="AND", right=xor_n1)
    or_n_left: str = equation_to_name(equation=or_n_left_equation, equations=equations)

    or_n_right_equation = Equation(left=f"x{n-1:02d}", op="AND", right=f"y{n-1:02d}")
    or_n_right: str = equation_to_name(equation=or_n_right_equation, equations=equations)

    or_n_equation = Equation(left=or_n_left, op="OR", right=or_n_right)
    or_n: str = equation_to_name(equation=or_n_equation, equations=equations)

    xor_n_equation = Equation(left=f"x{n:02d}", op="XOR", right=f"y{n:02d}")
    xor_n: str = equation_to_name(equation=xor_n_equation, equations=equations)

    return swaps, or_n, xor_n


def equation_to_name(equation: Equation, equations: dict[str, Equation]) -> str | None:
    for name, _equation in equations.items():
        if equation == _equation:
            return name
    return None


if __name__ == "__main__":
    main()

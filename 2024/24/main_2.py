class Equation:
    def __init__(self, left: "Equation | str", right: "Equation | str", op: str):
        self.raw_left = left
        self.raw_right = right
        self.op = op

    @staticmethod
    def z_n(n: int):
        if n == 0:
            return Equation(left="x00", right="y00", op="XOR")
        left = Equation(left=f"x{n:02d}", right=f"y{n:02d}", op="XOR")
        right = Equation.r_n(n - 1)
        return Equation(left=left, right=right, op="XOR")

    @staticmethod
    def r_n(n: int):
        if n == 0:
            return Equation(left="x00", right="y00", op="AND")
        left = Equation()
        right = Equation()
        return Equation(left=left, right=right, op="OR")

    def __eq__(self, other: "Equation"):
        if not isinstance(other, Equation):
            return False

        if self.op != other.op:
            return False

        if (self.left == other.left and self.right == other.right) or (
            self.left == other.right and self.right == other.left
        ):
            return True

        # Case (a and b) or (c and d) or (e and f)
        if (
            isinstance(self.right, str)
            or isinstance(self.left, str)
            or isinstance(other.right, str)
            or isinstance(other.left, str)
        ):
            return False

        if not (self.right.op == self.left.op == other.right.op == other.left.op):
            return False

        return False

    @property
    def left(self):
        if isinstance(self.raw_left, str) and not self.raw_left.startswith("x") and not self.raw_left.startswith("y"):
            self.raw_left = EQUATIONS[self.raw_left]
        return self.raw_left

    @property
    def right(self):
        if (
            isinstance(self.raw_right, str)
            and not self.raw_right.startswith("x")
            and not self.raw_right.startswith("y")
        ):
            self.raw_right = EQUATIONS[self.raw_right]
        return self.raw_right

    def __str__(self):
        return f"Equation(left={self.left!r}, right={self.right!r}, op={self.op!r})"

    def __repr__(self):
        return str(self)

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if isinstance(self.right, str) and isinstance(self.left, str):
            line = f"{self.left}-{self.op}-{self.right}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if isinstance(self.right, str):
            lines, n, p, x = self.left._display_aux()
            s = f"{self.op}-{self.right}"
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if isinstance(self.left, str):
            lines, n, p, x = self.right._display_aux()
            s = f"{self.left}-{self.op}"
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = "%s" % self.op
        u = len(s)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


EQUATIONS: dict[str, Equation] = {}


def main():
    with open("input", "r") as f:
        content: str = f.read()

    _, equations_raw = content.split("\n\n")

    for equation in equations_raw.splitlines():
        n1, operation, n2, _, r = equation.split(" ")
        EQUATIONS[r] = Equation(left=n1, right=n2, op=operation)

    EQUATIONS["z03"].display()

    # for n in range(46):
    #     print(n, EQUATIONS[f"z{n:02d}"] == Equation.z_n(n))
    #     print(EQUATIONS[f"z{n:02d}"])
    #     print(Equation.z_n(n))


if __name__ == "__main__":
    main()

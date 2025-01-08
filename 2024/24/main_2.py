class Equation:
    def __init__(self, left: "Equation | str", right: "Equation | str", op: str, name: str):
        self.raw_left = left
        self.raw_right = right
        self.op = op
        self.name = name

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

    def display(self, depth: int | None = None):
        lines, *_ = self._display_aux(depth)
        for line in lines:
            print(line)

    def _display_aux(self, depth: int | None = None):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # Depth 0
        if depth == 0:
            left = self.left if isinstance(self.left, str) else self.left.name
            right = self.right if isinstance(self.right, str) else self.right.name
            line = f"{left}-{self.op}-({self.name})-{right}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # No child.
        if isinstance(self.right, str) and isinstance(self.left, str):
            line = f"{self.left}-{self.op}-({self.name})-{self.right}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if isinstance(self.right, str):
            lines, n, p, x = self.left._display_aux(depth - 1 if depth is not None else None)
            s = f"{self.op}-({self.name})-{self.right}"
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if isinstance(self.left, str):
            lines, n, p, x = self.right._display_aux(depth - 1 if depth is not None else None)
            s = f"{self.left}-{self.op}-({self.name})"
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux(depth - 1 if depth is not None else None)
        right, m, q, y = self.right._display_aux(depth - 1 if depth is not None else None)
        s = f"{self.op}-({self.name})"
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
        EQUATIONS[r] = Equation(left=n1, right=n2, op=operation, name=r)

    for n in range(25):
        print(f"---- z{n:02d} -----")
        EQUATIONS[f"z{n:02d}"].display(depth=2)


if __name__ == "__main__":
    main()

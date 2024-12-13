import math
from dataclasses import dataclass
from functools import cache


@dataclass(unsafe_hash=True)
class Machine:
    Xa: int = None
    Ya: int = None
    Xb: int = None
    Yb: int = None
    Xp: int = None
    Yp: int = None

    def is_solution(self, nb_a: int, nb_b: int) -> bool:
        return nb_a * self.Xa + nb_b * self.Xb == self.Xp and nb_a * self.Ya + nb_b * self.Yb == self.Yp

    @staticmethod
    def price(nb_a: int, nb_b: int) -> int:
        return 3 * nb_a + nb_b

    def solution(self) -> tuple[int, int] | None:
        nb_b: float = (self.Xa * self.Yp - self.Xp * self.Ya) / (self.Yb * self.Xa - self.Xb * self.Ya)
        nb_a: float = (self.Xb * self.Yp - self.Xp * self.Yb) / (self.Ya * self.Xb - self.Xa * self.Yb)
        if nb_a.is_integer() and nb_b.is_integer():
            return int(round(nb_a)), int(round(nb_b))
        return None


def main():
    with open("input", "r") as f:
        lines: list[str] = f.read().splitlines()
    machines: list[Machine] = []
    machine = Machine()
    for index, line in enumerate(lines):
        match index % 4:
            case 0:
                _, _, x, y = line.split(" ")
                machine.Xa = int(x.removeprefix("X+").removesuffix(","))
                machine.Ya = int(y.removeprefix("Y+").removesuffix(","))
            case 1:
                _, _, x, y = line.split(" ")
                machine.Xb = int(x.removeprefix("X+").removesuffix(","))
                machine.Yb = int(y.removeprefix("Y+").removesuffix(","))
            case 2:
                _, x, y = line.split(" ")
                machine.Xp = int(x.removeprefix("X=").removesuffix(",")) + 10000000000000
                machine.Yp = int(y.removeprefix("Y=").removesuffix(",")) + 10000000000000
                machines.append(machine)
            case 3:
                machine = Machine()

    total = 0
    nb_machines = len(machines)
    for current, machine in enumerate(machines):
        print(f"{100 * current / nb_machines: .2f} %")
        solution = machine.solution()
        if solution is not None:
            total += machine.price(nb_a=solution[0], nb_b=solution[1])

    print(total)


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()
    # print(Machine(Xa=1, Ya=1, Xb=1, Yb=1, Xp=1, Yp=1).minimum_price())

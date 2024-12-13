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

    def result(self, nb_a: int, nb_b: int) -> tuple[int, int]:
        return (nb_a * self.Xa + nb_b * self.Xb), (nb_a * self.Ya + nb_b * self.Yb)

    @staticmethod
    def price(nb_a: int, nb_b: int) -> int:
        return 3 * nb_a + nb_b

    @cache
    def minimum_price(self, target_x: int = None, target_y: int = None) -> int | None:
        if target_x is None:
            target_x = self.Xp
        if target_y is None:
            target_y = self.Yp

        if target_x < 0 or target_y < 0:
            return None

        if target_x == 0 and target_y == 0:
            return 0

        price_a = None
        if target_x >= self.Xa and target_y >= self.Ya:
            price = self.minimum_price(target_x=target_x - self.Xa, target_y=target_y - self.Ya)
            if price is not None:
                price_a = 3 + price

        price_b = None
        if target_x >= self.Xb and target_y >= self.Yb:
            price = self.minimum_price(target_x=target_x - self.Xb, target_y=target_y - self.Yb)
            if price is not None:
                price_b = 1 + price

        if price_b is None and price_a is None:
            return None

        if price_a is None:
            return price_b

        if price_b is None:
            return price_a

        return min(price_a, price_b)


def main():
    with open("input_fake", "r") as f:
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
        total += machine.minimum_price() or 0

    print(total)


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()
    # print(Machine(Xa=1, Ya=1, Xb=1, Yb=1, Xp=1, Yp=1).minimum_price())

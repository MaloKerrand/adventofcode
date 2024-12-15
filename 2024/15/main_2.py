from dataclasses import dataclass
from enum import Enum


class Entity(Enum):
    ROBOT = "robot"
    WALL = "wall"
    BOX_L = "box_l"
    BOX_R = "box_r"


@dataclass(unsafe_hash=True)
class Warehouse:
    robot_x: int = None
    robot_y: int = None
    walls: list[tuple[int, int]] = None
    boxes: list[tuple[int, int]] = None

    @staticmethod
    def from_string(string: str) -> "Warehouse":
        warehouse = Warehouse()
        for y, line in enumerate(string.splitlines()):
            for x, char in enumerate(line):
                match char:
                    case "@":
                        warehouse.robot_x = 2 * x
                        warehouse.robot_y = y
                    case "#":
                        if warehouse.walls is None:
                            warehouse.walls = []
                        warehouse.walls.append((2 * x, y))
                        warehouse.walls.append((2 * x + 1, y))
                    case "O":
                        if warehouse.boxes is None:
                            warehouse.boxes = []
                        warehouse.boxes.append((2 * x, y))
        warehouse.show()
        return warehouse

    def compute_step(self, dx: int, dy: int) -> None:
        self.move(x=self.robot_x, y=self.robot_y, dx=dx, dy=dy)

    def move(self, x: int, y: int, dx: int, dy: int) -> None:
        if not self.can_move(x=x, y=y, dx=dx, dy=dy):
            return

        new_x: int = x + dx
        new_y: int = y + dy
        entity: Entity | None = self.get_entity(x=x, y=y)
        match (entity, dx, dy):
            case Entity.ROBOT, _, _:
                self.move(x=new_x, y=new_y, dx=dx, dy=dy)
                self.robot_x += dx
                self.robot_y += dy

            case Entity.BOX_L, 1, _:
                self.move(x=new_x + 1, y=new_y, dx=dx, dy=dy)
                index = self.boxes.index((x, y))
                self.boxes[index] = (new_x, new_y)

            case Entity.BOX_L, -1, _:
                raise Exception("No possible")

            case Entity.BOX_L, 0, _:
                self.move(x=new_x, y=new_y, dx=dx, dy=dy)
                self.move(x=new_x + 1, y=new_y, dx=dx, dy=dy)
                index = self.boxes.index((x, y))
                self.boxes[index] = (new_x, new_y)

            case Entity.BOX_R, 1, _:
                raise Exception("No possible")

            case Entity.BOX_R, -1, _:
                self.move(x=new_x - 1, y=new_y, dx=dx, dy=dy)
                index = self.boxes.index((x - 1, y))
                self.boxes[index] = (new_x - 1, new_y)

            case Entity.BOX_R, 0, _:
                self.move(x=new_x, y=new_y, dx=dx, dy=dy)
                self.move(x=new_x - 1, y=new_y, dx=dx, dy=dy)
                index = self.boxes.index((x - 1, y))
                self.boxes[index] = (new_x - 1, new_y)

    def can_move(self, x: int, y: int, dx: int, dy: int) -> bool:
        new_x: int = x + dx
        new_y: int = y + dy
        entity: Entity | None = self.get_entity(x=x, y=y)
        match (entity, dx, dy):
            case Entity.WALL, _, _:
                return False
            case Entity.ROBOT, _, _:
                return self.can_move(x=new_x, y=new_y, dx=dx, dy=dy)

            case Entity.BOX_L, 1, _:
                return self.can_move(x=new_x + 1, y=new_y, dx=dx, dy=dy)

            case Entity.BOX_L, -1, _:
                raise Exception("No possible")

            case Entity.BOX_L, 0, _:
                return (
                    self.can_move(x=new_x, y=new_y, dx=dx, dy=dy)
                    and self.can_move(x=new_x + 1, y=new_y, dx=dx, dy=dy)
                )

            case Entity.BOX_R, 1, _:
                raise Exception("No possible")

            case Entity.BOX_R, -1, _:
                return self.can_move(x=new_x - 1, y=new_y, dx=dx, dy=dy)

            case Entity.BOX_R, 0, _:
                return (
                    self.can_move(x=new_x, y=new_y, dx=dx, dy=dy)
                    and self.can_move(x=new_x - 1, y=new_y, dx=dx, dy=dy)
                )
        return True

    def get_entity(self, x: int, y: int) -> Entity | None:
        if self.robot_x == x and self.robot_y == y:
            return Entity.ROBOT

        if (x, y) in self.walls:
            return Entity.WALL

        if (x, y) in self.boxes:
            return Entity.BOX_L

        if (x - 1, y) in self.boxes:
            return Entity.BOX_R

        return None

    def show(self) -> None:
        max_x = max(wall[0] for wall in self.walls)
        max_y = max(wall[1] for wall in self.walls)
        _map = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        _map[self.robot_y][self.robot_x] = "@"
        for x, y in self.walls:
            _map[y][x] = "#"
        for x, y in self.boxes:
            _map[y][x] = "["
            _map[y][x + 1] = "]"

        for line in _map:
            print("".join(line))

    def sum_gps(self) -> int:
        return sum(100 * box[1] + box[0] for box in self.boxes)


def step_to_direction(step: str) -> tuple[int, int]:
    match step:
        case "<":
            return -1, 0
        case "^":
            return 0, -1
        case ">":
            return 1, 0
        case "v":
            return 0, 1
    raise Exception(f"Unknown step {step!r}")


def main():
    with open("input", "r") as f:
        content: str = f.read()
    p1, p2 = content.split("\n\n")
    warehouse: Warehouse = Warehouse.from_string(p1)
    steps: str = p2.replace("\n", "")

    print(steps)
    for step in steps:
        dx, dy = step_to_direction(step)
        warehouse.compute_step(dx=dx, dy=dy)
        # print(step)
        # warehouse.show()
    warehouse.show()

    print(warehouse.sum_gps())


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

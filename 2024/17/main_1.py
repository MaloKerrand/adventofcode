import math
from bisect import insort
from copy import deepcopy
from dataclasses import dataclass

register_a = 0
register_b = 0
register_c = 0
instruction = 0
output: list[int] = []


def operand_to_value(operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register_a
        case 5:
            return register_b
        case 6:
            return register_c
    raise Exception("opcode not supported")


def opcode_to_value(opcode: int, literal_operand: int) -> None:
    global register_a, register_b, register_c, instruction
    combo_operand_value = operand_to_value(literal_operand)
    match opcode:
        case 0:  # adv
            register_a = register_a // (2**combo_operand_value)
        case 1:  # bxl
            register_b = register_b ^ literal_operand
        case 2:  # bst
            register_b = (combo_operand_value % 8) & 0b111
        case 3:  # jmz
            if register_a == 0:
                return
            instruction += literal_operand  # -2 ?
        case 4:  # bxc
            register_b = register_b ^ register_c
        case 5:  # out
            output.append((combo_operand_value % 8) & 0b111)
        case 6:  # bdv
            register_b = register_a // (2**combo_operand_value)
        case 7:  # cdv
            register_c = register_a // (2**combo_operand_value)


def main():
    with open("input", "r") as f:
        MAZE = [list(line) for line in f.read().splitlines()]


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

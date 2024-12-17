def operand_to_value(operand: int, register_a: int, register_b: int, register_c: int) -> int | None:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register_a
        case 5:
            return register_b
        case 6:
            return register_c
    return None


def compute(program: list[int], register_a: int,  register_b: int, register_c: int) -> list[int] | None:
    output: list[int] = []
    instruction = 0
    while instruction < len(program):
        opcode = program[instruction]
        literal_operand = program[instruction + 1]
        # print(instruction, opcode, literal_operand, register_a, register_b, register_c)

        combo_operand_value: int | None = operand_to_value(
            operand=literal_operand,
            register_a=register_a,
            register_b=register_b,
            register_c=register_c
        )
        match opcode:
            case 0:  # adv
                register_a = register_a // (2 ** combo_operand_value)
            case 1:  # bxl
                register_b = register_b ^ literal_operand
            case 2:  # bst
                register_b = (combo_operand_value % 8) & 0b111
            case 3:  # jmz
                if register_a != 0:
                    instruction = literal_operand - 2  # -2 ?
            case 4:  # bxc
                register_b = register_b ^ register_c
            case 5:  # out
                output.append((combo_operand_value % 8) & 0b111)
                # if output != program[:len(output)]:
                #     return None
            case 6:  # bdv
                register_b = register_a // (2 ** combo_operand_value)
            case 7:  # cdv
                register_c = register_a // (2 ** combo_operand_value)

        instruction += 2
    return output


def smaller_a(
    program: list[int],
    index: int,
    a_list: list[int],
    register_b: int,
    register_c: int
) -> list[int] | None:
    register_a = a_list.copy()
    if index == -1:
        return register_a

    possibles: set[int] = set()
    for i in range(0, 8):
        register_a[index] = i
        a = sum(i * 8 ** index for index, i in enumerate(register_a))
        output = compute(program=program, register_a=a, register_b=register_b, register_c=register_c)
        if len(output) == len(program) and output[index] == program[index]:
            possibles.add(i)

    for i in sorted(possibles):
        register_a[index] = i
        small_a = smaller_a(
            program=program,
            index=index - 1,
            a_list=register_a,
            register_b=register_b,
            register_c=register_c
        )
        if small_a is not None:
            return small_a
    return None


def main():
    with open("input", "r") as f:
        content: list[str] = f.read().splitlines()

    # register_a: int = int(content[0].split(" ")[2])
    register_b: int = int(content[1].split(" ")[2])
    register_c: int = int(content[2].split(" ")[2])

    program: list[int] = [int(e) for e in content[4].split(" ")[1].split(",")]
    a_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    a_list = smaller_a(
        program=program,
        index=len(a_list) - 1,
        a_list=a_list,
        register_b=register_b,
        register_c=register_c
    )
    a = sum(i * 8 ** index for index, i in enumerate(a_list))
    print(a)


if __name__ == "__main__":
    main()

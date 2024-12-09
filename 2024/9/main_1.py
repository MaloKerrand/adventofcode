def main():
    with open("input", "r") as f:
        disk_map: str = f.read()

    disk: list[str] = []
    for index, nb in enumerate(disk_map):
        if index % 2 == 0:
            disk += [str(index // 2) for _ in range(int(nb))]
        else:
            disk += ["." for _ in range(int(nb))]

    nb_empty: int = disk.count(".")
    char_to_move: list[str] = [char for char in disk[-nb_empty:] if char != "."]

    new_disk: list[str] = []
    for index in range(len(disk) - nb_empty):
        if disk[index] == ".":
            new_disk.append(char_to_move.pop())
        else:
            new_disk.append(disk[index])

    print(sum(index * int(char) for index, char in enumerate(new_disk)))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

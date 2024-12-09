from copy import deepcopy


def empty(file_id: str, disk: list[tuple[str, int]]) -> None:
    for index, (space_id, space) in enumerate(disk):
        if space_id == file_id:
            disk[index] = (".", space)


def insert(file_id: str, file_size: int, disk: list[tuple[str, int]]) -> list[tuple[str, int]]:
    final_disk = deepcopy(disk)
    for index, (space_id, space) in enumerate(disk):
        if space_id == file_id:
            return disk
        if space_id != ".":
            continue
        if space < file_size:
            continue

        empty(file_id=file_id, disk=final_disk)

        if space == file_size:
            final_disk[index] = (file_id, file_size)
        else:
            final_disk[index] = (space_id, space - file_size)
            final_disk = final_disk[:index] + [(file_id, file_size)] + final_disk[index:]

        return final_disk
    return final_disk


def main():
    with open("input", "r") as f:
        disk_map: str = f.read()

    # (id, space)
    original_disk: list[tuple[str, int]] = []
    for index, nb in enumerate(disk_map):
        if index % 2 == 0:
            original_disk.append((str(index // 2), int(nb)))
        else:
            original_disk.append((".", int(nb)))

    final_disk: list[tuple[str, int]] = deepcopy(original_disk)
    total_size = len(original_disk)
    current = 0
    for file_id, file_size in reversed(original_disk):
        current += 1
        print(f"{100 * current / total_size: .2f} %")
        if file_id == ".":
            continue
        final_disk = insert(file_id=file_id, file_size=file_size, disk=final_disk)

    final_disk_2 = [file_id for file_id, file_size in final_disk for _ in range(file_size)]
    print("".join(final_disk_2))
    print(sum(index * int(char) for index, char in enumerate(final_disk_2) if char != "."))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

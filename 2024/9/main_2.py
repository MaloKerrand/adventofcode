from copy import deepcopy


def insert(file_id: str, file_size: int, disk: list[tuple[str, int]]):
    final_disk = deepcopy(disk)
    for index, (space_id, space) in enumerate(disk):
        if space_id != ".":
            continue
        if space < file_size:
            continue

        if space == file_size:
            final_disk[index] = (file_id, file_size)
        else:
            final_disk[index] = (space_id, space - file_size)
            final_disk = final_disk[:index] + [(file_id, file_size)] + final_disk[index + 1 :]

        return final_disk
    return final_disk


def main():
    with open("input_fake", "r") as f:
        disk_map: str = f.read()

    # (id, space)
    original_disk: list[tuple[str, int]] = []
    for index, nb in enumerate(disk_map):
        if index % 2 == 0:
            original_disk.append((str(index // 2), int(nb)))
        else:
            original_disk.append((".", int(nb)))

    print(original_disk)
    # (id, space)
    disk: list[tuple[str, int]] = deepcopy(original_disk)
    final_disk: list[tuple[str, int]] = []
    while disk:
        file_id, file_size = disk.pop()
        final_disk = insert(file_id=file_id, file_size=file_size, disk=final_disk)
    print(final_disk)

    final_disk = [file_id for file_id, file_size in final_disk for _ in range(file_size)]
    print(sum(file_size * int(file_id) for file_id, file_size in final_disk if file_id != "."))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

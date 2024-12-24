from collections import defaultdict


def main():
    with open("input", "r") as f:
        all_connections: list[list[str]] = [line.split("-") for line in f.read().splitlines()]

    computer_to_connected: dict[str, set[str]] = defaultdict(set)
    for c1, c2 in all_connections:
        computer_to_connected[c1].add(c2)
        computer_to_connected[c2].add(c1)

    three_connected: set[tuple[str, ...]] = set()
    for c1, connections in computer_to_connected.items():
        if not c1.startswith("t"):
            continue

        for c2 in connections:
            intersection = computer_to_connected[c2].intersection(connections)
            for c3 in intersection:
                three_connected.add(tuple(sorted([c1, c2, c3])))
    print(three_connected)
    print(len(three_connected))


if __name__ == "__main__":
    main()

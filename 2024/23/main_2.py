from collections import defaultdict


def main():
    with open("input", "r") as f:
        all_connections: list[list[str]] = [line.split("-") for line in f.read().splitlines()]

    computer_to_connected: dict[str, set[str]] = defaultdict(set)
    for c1, c2 in all_connections:
        computer_to_connected[c1].add(c2)
        computer_to_connected[c2].add(c1)

    cliques: set[tuple[str, ...]] = {(computer,) for computer in computer_to_connected}
    for i in range(1, 1000):
        print(i, len(cliques))
        new_cliques = n_plus_1_cliques(cliques=cliques, graph=computer_to_connected)

        if new_cliques:
            cliques = new_cliques
            continue

        print(i, len(cliques), cliques)
        print(",".join(cliques.pop()))
        break


def n_plus_1_cliques(cliques: set[tuple[str, ...]], graph: dict[str, set[str]]) -> set[tuple[str, ...]]:
    new_cliques: set[tuple[str, ...]] = set()
    for clique in cliques:
        for c, connections in graph.items():
            if c in clique:
                continue
            if len(set(clique).difference(connections)) != 0:
                continue
            new_cliques.add(tuple(sorted((*clique, c))))
    return new_cliques


if __name__ == "__main__":
    main()

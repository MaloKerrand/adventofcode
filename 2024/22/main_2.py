def main():
    with open("input", "r") as f:
        secrets: list[int] = [int(s) for s in f.read().splitlines()]

    all_sequence_to_price: list[dict[tuple[int, int, int, int], int]] = []

    for secret in secrets:
        prices: list[int] = [int(str(secret)[-1])]
        prices_diff: list[int] = []
        for _ in range(2000):
            secret = new_secret(secret)
            new_price = int(str(secret)[-1])
            prices_diff.append(new_price - prices[-1])
            prices.append(new_price)

        sequence_to_price: dict[tuple[int, int, int, int], int] = {}
        for d1, d2, d3, d4, price in zip(prices_diff, prices_diff[1:], prices_diff[2:], prices_diff[3:], prices[4:]):
            if (d1, d2, d3, d4) in sequence_to_price:
                continue
            sequence_to_price[(d1, d2, d3, d4)] = price
        all_sequence_to_price.append(sequence_to_price)

    sequences: set[tuple[int, int, int, int]] = {s for ss in all_sequence_to_price for s in ss}
    sequence_to_price: dict[tuple[int, int, int, int], int] = {
        s: sum(sequence_to_price.get(s, 0) for sequence_to_price in all_sequence_to_price) for s in sequences
    }
    max_bananas = max(sequence_to_price.values())
    print(max_bananas)


def new_secret(secret: int) -> int:
    r = secret * 64
    secret = secret ^ r
    secret = secret % 16777216
    r = secret // 32
    secret = secret ^ r
    secret = secret % 16777216
    r = secret * 2048
    secret = secret ^ r
    return secret % 16777216


if __name__ == "__main__":
    main()

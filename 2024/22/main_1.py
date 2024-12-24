def main():
    with open("input", "r") as f:
        secrets: list[int] = [int(s) for s in f.read().splitlines()]

    total = 0
    for secret in secrets:
        for _ in range(2000):
            secret = new_secret(secret)
        total += secret
    print(total)


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

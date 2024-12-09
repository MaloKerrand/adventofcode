def is_safe(report: list[int], nb_remove: int = 0):
    increasing = False
    decreasing = False
    old_value = report[0]
    for index, x in enumerate(report[1:]):
        if not (0 < abs(x - old_value) < 4) or (increasing and x < old_value) or (decreasing and x > old_value):
            if nb_remove > 0:
                return False
            return any(is_safe(report[:i] + report[i + 1 :], nb_remove + 1) for i in range(len(report)))
        increasing = x > old_value
        decreasing = x < old_value
        old_value = x
    return True


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    total = sum(is_safe([int(x) for x in report.split(" ")]) for report in content)
    print(total)


if __name__ == "__main__":
    import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

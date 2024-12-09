def is_safe(report: str):
    increasing = False
    decreasing = False
    report_int = [int(x) for x in report.split(" ")]
    old_value = report_int[0]
    for x in report_int[1:]:
        if not (0 < abs(x - old_value) < 4):
            return False
        if increasing and x < old_value:
            return False
        if decreasing and x > old_value:
            return False
        increasing = x > old_value
        decreasing = x < old_value
        old_value = x
    return True


def main():
    with open("input", "r") as f:
        content = f.read().splitlines()

    total = sum(is_safe(x) for x in content)
    print(total)


if __name__ == "__main__":
    import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()

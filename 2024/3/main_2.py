import re


def main():
    with open("input", "r") as f:
        content = f.read()
    content = "do()" + content

    result_1 = re.findall(pattern=r"do\(\)((?:(?:(?!don't).)*mul\([0-9]+,[0-9]+\))+)", string=content, flags=re.DOTALL)
    somme = 0
    for elem in result_1:
        result = re.findall(pattern=r"mul\(([0-9]+,[0-9]+)\)", string=elem)
        for i in result:
            number_1, number_2 = i.split(",")
            somme += int(number_1) * int(number_2)
    print(somme)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit("main()", number=1000, globals=locals()))

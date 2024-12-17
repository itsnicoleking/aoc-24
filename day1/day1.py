from pathlib import Path
import re

p = Path(__file__).with_name("input.txt")

left, right = [], []

def setup():
    # Read
    with open(p, 'r') as file:
        lineList = list(filter(None,re.split(r'[\s\n]+', file.read(), flags=re.MULTILINE)))

    # Split
    i = 0
    while i < len(lineList):
        if i % 2 == 0:
            left.append(int(lineList[i]))
        else:
            right.append(int(lineList[i]))
        i += 1

    if len(left) != len(right):
        raise ValueError()

    # Sort
    left.sort()
    right.sort()


def part1() -> int:
    distance = 0
    i = 0
    while i < len(left):
        distance += abs(left[i] - right[i])
        i += 1

    return distance


def part2() -> int:
    similarity = 0

    for e in left:
        similarity += e * right.count(e)

    return similarity


if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

from pathlib import Path

p = Path(__file__).with_name("input.txt")

reports = []

def setup():
    global reports
    # Read
    with open(p, 'r') as file:
        reports = [line.strip().split(' ') for line in file]
        reports = [[int(level) for level in line] for line in reports]

    if len(reports) < 1:
        raise ValueError()

def isAscending(list: list) -> bool:
    return all(list[i] < list[i + 1] for i in range(len(list) - 1))

def isDescending(list: list) -> bool:
    return all(list[i] > list[i + 1] for i in range(len(list) - 1))

def areAdjacentLevelsValid(list: list) -> bool:
    i = 0
    while i < len(list) - 1:
        diff = abs(list[i] - list[i+1])
        if diff == 0 or diff > 3:
            return False
        i += 1
    return True

def part1() -> int:
    numSafe = 0

    for report in reports:
        if len(report) < 2:
            raise ValueError()
        if (isAscending(report) or isDescending(report)) and areAdjacentLevelsValid(report):
            numSafe += 1
    return numSafe

def part2() -> int:
    numSafe = 0

    for report in reports:
        if len(report) < 2:
            raise ValueError()
        if (isAscending(report) or isDescending(report)) and areAdjacentLevelsValid(report):
            numSafe += 1
        else:
            # run it with a level removed until it works
            i = 0
            while i < len(report):
                removed = report.pop(i)
                if (isAscending(report) or isDescending(report)) and areAdjacentLevelsValid(report):
                    numSafe += 1
                    report.insert(i, removed)
                    break
                report.insert(i, removed)

                i += 1

    return numSafe

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

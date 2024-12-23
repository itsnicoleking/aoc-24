from pathlib import Path
import re

p = Path(__file__).with_name("input.txt")

def getOps(regex: str) -> list:
    ops = []

    with open(p, 'r') as file:
        ops = re.findall(regex, file.read())

    return ops

def part1() -> int:
    res = 0
    mulOps = getOps(r'{}'.format("(?:mul)\([0-9]{1,3}\,[0-9]{1,3}\)"))

    for mul in mulOps:
        nums = re.findall(r'[0-9]{1,3}', mul)
        res += int(nums[0]) * int(nums[1])

    return res

def part2() -> int:
    res = 0
    ops = getOps(r'{}'.format("(?:mul)\([0-9]{1,3}\,[0-9]{1,3}\)|(?:do\(\))|(?:don\'t\(\))"))

    do = True
    for op in ops:
        if "do" in op:
            do = True
        if "don't" in op:
            do = False
        if "mul" in op and do:
            nums = re.findall(r'[0-9]{1,3}', op)
            res += int(nums[0]) * int(nums[1])

    return res

if __name__ == "__main__":
    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

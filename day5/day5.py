from math import ceil
from pathlib import Path

rules = []
updates = []

def setup():
    global rules, updates

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        allLines = [line.strip() for line in file]

    splitIdx = allLines.index('')
    rules = [rule.split('|') for rule in allLines[:splitIdx]]
    updates = [update.split(',') for update in allLines[splitIdx+1:]]

def doesPassAllRules(update: list) -> bool:
    for rule in rules:
        if rule[0] in update and rule[1] in update and update.index(rule[0]) > update.index(rule[1]):
            return False

    return True

def fixUpdatePerRules(update: list) -> list:
    for rule in rules:
        if rule[0] in update and rule[1] in update and update.index(rule[0]) > update.index(rule[1]):
            idx0 = update.index(rule[0])
            idx1 = update.index(rule[1])
            update[idx0], update[idx1] = update[idx1], update[idx0]

    return update

def part1() -> int:
    res = 0

    for update in updates:
        if doesPassAllRules(update):
            res += int(update[ceil(len(update) / 2) - 1])

    return res

def part2( )-> int:
    res = 0

    for update in updates:
        if not doesPassAllRules(update):
            while not doesPassAllRules(update):
                update = fixUpdatePerRules(update)
            res += int(update[ceil(len(update) / 2) - 1])

    return res

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

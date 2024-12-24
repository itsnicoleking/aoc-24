import sys
from pathlib import Path
from typing import TextIO

sys.path.append('{}/utils'.format(Path(__file__).parent.parent.resolve()))
from grid import Grid, Point


class GuardMap(Grid):
    DIRECTIONS = [
        Point(0, -1),  # north
        Point(1, 0),  # east
        Point(0, 1),  # south
        Point(-1, 0)  # west
    ]
    BLOCKAGE = '#'

    def __init__(self, file: TextIO):
        super().__init__([line.strip() for line in file])

        # Get starting location and direction
        for point in self.points:
            if self.getValueAtPoint(point) == '^':
                self._startPos = point
                self._startDirIdx = 0
                break
            if self.getValueAtPoint(point) == '>':
                self._startPos = point
                self._startDirIdx = 1
                break
            if self.getValueAtPoint(point) == 'v':
                self._startPos = point
                self._startDirIdx = 2
                break
            if self.getValueAtPoint(point) == '<':
                self._startPos = point
                self._startDirIdx = 3
                break
        # Init copies to modify as path is traversed
        self._guardPos = self._startPos
        self._guardDirIdx = self._startDirIdx

        self._visited = []  # Point
        # where int is direction index
        self._visitedWithDir = set(tuple[Point, int])

        self._isLoop = False
        self._extraBlockages = []  # Point

        # Visit the starting location
        self._visit

    @property
    def visitedPoints(self):
        return self._visited

    @property
    def isLoop(self):
        return self._isLoop

    def reset(self):
        self._guardPos = self._startPos
        self._guardDirIdx = self._startDirIdx

        self._visited = []
        self._visitedWithDir = set()

        self._isLoop = False

        self._visit()
        self._clearBlockages()

    def addBlockage(self, point: Point):
        self._extraBlockages.append((point, self.getValueAtPoint(point)))
        self.setValueAtPoint(point, GuardMap.BLOCKAGE)

    def step(self) -> bool:
        while True:
            # Get the next position in direction of travel
            next = self._guardPos + GuardMap.DIRECTIONS[self._guardDirIdx]

            # Stop if off the grid
            if not self.isValidPoint(next):
                return False

            # If next position is a block, reorient and try step again
            if self.getValueAtPoint(next) == GuardMap.BLOCKAGE:
                self._guardDirIdx = (self._guardDirIdx +
                                     1) % len(GuardMap.DIRECTIONS)
                continue

            # Valid step, move to this position
            self._guardPos = next
            self._visit()
            return True

    def stepUntilFalse(self):
        while self.step():
            pass

    def _visit(self):
        # Save every visited position
        self._visited.append(self._guardPos)

        # Save (position, direction) in set if it's the first visit
        config = (self._guardPos, self._guardDirIdx)
        if config in self._visitedWithDir:
            self._isLoop = True
            return
        else:
            self._visitedWithDir.add(config)

    def _clearBlockages(self):
        for point, originalVal in self._extraBlockages:
            self.setValueAtPoint(point, originalVal)

        self._extraBlockages = []


gm: GuardMap


def setup():
    global gm

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        gm = GuardMap(file)


def part1() -> int:
    gm.reset()
    gm.stepUntilFalse()
    return len(set(gm.visitedPoints))


def part2() -> int:
    gm.reset()

    # Unique route waypoints on first pass, throw away start pos
    gm.stepUntilFalse()
    route = [pos for pos in list(set(gm.visitedPoints[1:]))]

    numLoops = 0
    for pos in route:
        gm.reset()
        gm.addBlockage(pos)
        while gm.step():
            if gm.isLoop:
                numLoops += 1
                break

    return numLoops


if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

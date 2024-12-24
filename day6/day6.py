from pathlib import Path
from typing import TextIO

gm = None

class GuardMap:
    map = []
    rows = 0
    cols = 0
    posX, posY = 0, 0 # col, row
    dirIdx = 0
    directions = [
        (0, -1), # north
        (1, 0), # east
        (0, 1), # south
        (-1, 0) # west
    ]

    def __init__(self, file: TextIO):
        self.map = [line.strip() for line in file]

        if len(set(map(len, self.map))) != 1:
            raise ValueError("Disparate number of characters per line")

        self.rows = len(self.map)
        self.cols = len(self.map[0])

        i = 0
        while i < len(self.map):
            line = self.map[i]
            if '^' in line:
                self.posX, self.posY = line.index('^'), i
                self.dirIdx = 0
            elif '>' in line:
                self.posX, self.posY = line.index('>'), i
                self.dirIdx = 1
            elif 'v' in line:
                self.posX, self.posY = line.index('v'), i
                self.dirIdx = 2
            elif '<' in line:
                self.posX, self.posY = line.index('<'), i
                self.dirIdx = 3
            i += 1

    def isValidCoordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def numDistinctPositions(self) -> int:
        positions = set()

        while self.isValidCoordinates(self.posX, self.posY):
            # Current position is visited and valid
            positions.add((self.posX, self.posY))

            # Convenience
            dirX = self.directions[self.dirIdx][0]
            dirY = self.directions[self.dirIdx][1]

            # Provided the next step is in the map
            if self.isValidCoordinates(self.posX + dirX, self.posY + dirY):
                # If is has a blockage, turn 90
                if self.map[self.posY + dirY][self.posX + dirX] == '#':
                    self.dirIdx = (self.dirIdx + 1) % 4

            # Update position for next round
            self.posX += self.directions[self.dirIdx][0]
            self.posY += self.directions[self.dirIdx][1]

        return len(positions)

def setup():
    global gm

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        gm = GuardMap(file)

def part1() -> int:
    return gm.numDistinctPositions()

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    # print("Part 2:\t", part2())

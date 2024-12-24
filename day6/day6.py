from pathlib import Path
from typing import TextIO

gm = None

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        totalStr = ""

        current = self.head
        while current != None:
            totalStr += f"{str(current)}, "
            current = current.next

        return totalStr

    def insertAtEnd(self, data):
        newNode = Node(data)
        if self.head == None:
            self.head = newNode
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = newNode

    def existsWithNext(self, data, nextData) -> bool:
        if self.head == None:
            return False

        current = self.head
        while current != None and current.next != None:
            if current.data == data and current.next.data == nextData:
                return True
            current = current.next

        return False

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

    def getDistinctPositions(self) -> int:
        positions = set()

        posX = self.posX
        posY = self.posY
        dirIdx = self.dirIdx

        while self.isValidCoordinates(posX, posY):
            # Current position is visited and valid
            positions.add((posX, posY))

            # Convenience
            dirX = self.directions[dirIdx][0]
            dirY = self.directions[dirIdx][1]

            # Provided the next step is in the map
            if self.isValidCoordinates(posX + dirX, posY + dirY):
                # If is has a blockage, turn 90
                if self.map[posY + dirY][posX + dirX] == '#':
                    dirIdx = (dirIdx + 1) % 4

            # Update position for next round
            posX += self.directions[dirIdx][0]
            posY += self.directions[dirIdx][1]

        return positions

    def doesMapLoop(self, blockageX: int, blockageY: int) -> bool:
        positions = LinkedList()

        posX = self.posX
        posY = self.posY
        dirIdx = self.dirIdx

        while self.isValidCoordinates(posX, posY):
            # Convenience
            dirX = self.directions[dirIdx][0]
            dirY = self.directions[dirIdx][1]

            # If current position exists with same next, there is a cycle
            if positions.existsWithNext((posX, posY), (posX + dirX, posY + dirY)):
                return True
            else:
                positions.insertAtEnd((posX, posY))

            # Provided the next step is in the map
            if self.isValidCoordinates(posX + dirX, posY + dirY):
                # If is has a blockage, turn 90
                if self.map[posY + dirY][posX + dirX] == '#' or \
                    (posX + dirX == blockageX and posY + dirY == blockageY):
                    dirIdx = (dirIdx + 1) % 4

            # Update position for next round
            posX += self.directions[dirIdx][0]
            posY += self.directions[dirIdx][1]

        return False

def setup():
    global gm

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        gm = GuardMap(file)

def part1() -> int:
    return len(gm.getDistinctPositions())

def part2() -> int:
    numMapsWithLoop = 0

    originalDistinctPath = gm.getDistinctPositions()

    for x, y in originalDistinctPath:
        if gm.map[y][x] != '#' and gm.doesMapLoop(x, y):
            numMapsWithLoop += 1

    return numMapsWithLoop

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2()) # at what cost...

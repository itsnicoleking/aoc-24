from pathlib import Path
from typing import TextIO

ws = None

class WordSearch:
    board = [] # 2D: board[row][column]
    rows = 0
    cols = 0

    def __init__(self, file: TextIO):
        self.board = [line.strip() for line in file]

        if len(set(map(len, self.board))) != 1:
            raise ValueError("Disparate number of characters per line")

        self.rows = len(self.board)
        self.cols = len(self.board[0])


    def numOccurrencesByWord(self, word: str) -> int:
        res = 0

        directions = [
            (1, 0), # east
            (1, 1), # north-east
            (0, 1), # north
            (-1, 1), # north-west
            (-1, 0), # west
            (-1, -1), # south-west
            (0, -1), # south
            (1, -1) # south-east
        ]

        for i in range(self.rows): # Y-axis
            for j in range(self.cols): # X-axis
                # Start of the target word
                if word[0] == self.board[i][j]:
                    for dirX, dirY in directions:
                        res = (res + 1) if self.searchDirectionally(word, 0, j, i, dirX, dirY) else (res)

        return res

    def isValidCoordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def searchDirectionally(self, word: str, idx: int, x: int, y: int, dirX: int, dirY: int) -> bool:
        if idx == len(word):
            return True

        if self.isValidCoordinates(x, y) and word[idx] == self.board[y][x]:
            return self.searchDirectionally(word, idx+1, x+dirX, y+dirY, dirX, dirY)

def setup():
    global ws

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        ws = WordSearch(file)

def part1() -> int:
    return ws.numOccurrencesByWord("XMAS")

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    # print("Part 2:\t", part2())

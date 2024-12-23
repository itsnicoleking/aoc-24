from math import ceil
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
                        res = (res + 1) if self.searchDirectionally(word, 0, True, j, i, dirX, dirY) else (res)

        return res

    def numCrossedWords(self, word: str) -> int:
        if len(word) % 2 != 1:
            raise ValueError("word must contain odd number of characters")
        if len(word) < 3:
            raise ValueError("word must contain minimum of three characters")

        res = 0

        middleIdx = ceil(len(word) / 2) - 1
        directions = [
            [(1, 1), (-1, -1), (-1, 1), (1, -1)], # NE/SW & NW/SE
            [(1, 1), (-1, -1), (1, -1), (-1, 1)], # NE/SW & SE/NW
            [(-1, -1), (1, 1), (-1, 1), (1, -1)], # SW/NE & NW/SE
            [(-1, -1), (1, 1), (1, -1), (-1, 1)] # SW/NE & SE/NW
        ]

        for i in range(self.rows):
            for j in range(self.cols):
                # Middle of target word
                if word[middleIdx] == self.board[i][j]:
                    for dirSet in directions:
                        if self.searchDirectionally(word, middleIdx, True, j, i, dirSet[0][0], dirSet[0][1]) and \
                            self.searchDirectionally(word, middleIdx, False, j, i, dirSet[1][0], dirSet[1][1]) and \
                            self.searchDirectionally(word, middleIdx, True, j, i, dirSet[2][0], dirSet[2][1]) and \
                            self.searchDirectionally(word, middleIdx, False, j, i, dirSet[3][0], dirSet[3][1]):
                            res += 1

        return res

    def isValidCoordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def searchDirectionally(self, word: str, idx: int, toWordEnd: bool, x: int, y: int, dirX: int, dirY: int) -> bool:
        if idx == len(word) or idx == -1:
            return True

        if self.isValidCoordinates(x, y) and word[idx] == self.board[y][x]:
            if toWordEnd:
                newIdx = idx + 1
            else:
                newIdx = idx - 1
            return self.searchDirectionally(word, newIdx, toWordEnd, x+dirX, y+dirY, dirX, dirY)

def setup():
    global ws

    p = Path(__file__).with_name("input.txt")
    with open(p, 'r') as file:
        ws = WordSearch(file)

def part1() -> int:
    return ws.numOccurrencesByWord("XMAS")

def part2() -> int:
    return ws.numCrossedWords("MAS")

if __name__ == "__main__":
    setup()

    print("Part 1:\t", part1())
    print("Part 2:\t", part2())

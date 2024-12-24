from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"Point({self.x},{self.y})"


Point.__add__ = lambda self, other: Point(self.x + other.x, self.y + other.y)
Point.__sub__ = lambda self, other: Point(self.x - other.x, self.y - other.y)


class Grid:
    def __init__(self, data: list) -> None:
        self._grid = [list(row) for row in data[:]]

        if len(set(map(len, self._grid))) != 1:
            raise ValueError("Disparate number of characters per line")

        self._width = len(self._grid[0])
        self._height = len(self._grid)

        self._points = [Point(x, y) for y in range(self._height)
                        for x in range(self._width)]

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._grid)

    @property
    def points(self):
        return self._points

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def cols(self):
        return list(zip(*self._grid))

    @property
    def rows(self):
        return self._grid

    def isValidCoordinates(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def isValidPoint(self, point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def getValueAtPoint(self, point: Point):
        return self._grid[point.y][point.x]

    def setValueAtPoint(self, point: Point, value):
        self._grid[point.y][point.x] = value

    def colsAsStr(self):
        return ["".join(str(char) for char in col) for col in self.cols]

    def rowsAsStr(self):
        return ["".join(str(char) for char in row) for row in self._grid]

from graphics import Rectangle, Point
from button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics import GraphWin


class Grid:
    def __init__(self, window: "GraphWin") -> None:
        """Constructs the game grid"""
        self.width, self.height = window.getWidth(), window.getHeight()
        self.window = window
        self.grid = []
        self.squareWidth = self.squareHeight = 50

        self.drawGrid()

    def drawGrid(self) -> None:
        """Draws the grid"""

        # Hide intro screen dominoes
        rect = Rectangle(Point(0, 0), Point(self.width, self.height))
        rect.draw(self.window)
        rect.setOutline("gray")
        rect.setFill("gray")

        for x in range(1, 11):
            row = []
            for y in range(1, 10):
                square = self.buildSquare(x, y, self.squareWidth, self.squareHeight)
                square.draw(self.window)
                square.setFill("black")
                square.setOutline("white")
                row.append(square)
            self.grid.append(row)

        self.quitB = Button(
            self.window,
            Point(self.width / 2, self.height - 30),
            50,
            40,
            "Quit",
            inverse=True,
        )

    def buildSquare(self, x: int, y: int, width: int, height: int) -> Rectangle:
        offsetW, offsetH = 0.22 * self.width, 0.05 * self.height
        halfW, halfH = width * 0.5, height * 0.5
        return Rectangle(
            Point((x * width - halfW) + offsetW, (y * height - halfH) + offsetH),
            Point((x * width + halfW) + offsetW, (y * height + halfH) + offsetH),
        )

    def getWin(self) -> "GraphWin":
        """returns the graphical window"""
        return self.window

    def getQuitB(self) -> Button:
        """returns the quit Button"""
        return self.quitB

    def gridPoint(self, x: int, y: int) -> Point:
        """returns the centerpoint of a given grid square"""
        return self.grid[x][y].getCenter()

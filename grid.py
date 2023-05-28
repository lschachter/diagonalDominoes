from graphics import Rectangle, Point
from ButtonClass import Button


class Grid:
    def __init__(self, window):
        """Constructs the game grid"""
        self.width = window.getWidth()
        self.height = window.getHeight()
        self.window = window
        self.window.setCoords(0, 600, 1000, 0)
        self.grid = []
        self.squareWidth = 50
        self.squareHeight = 50

    def drawGrid(self):
        """Draws the grid"""
        rect = Rectangle(Point(0, 0), Point(1000, 600))
        rect.draw(self.window)
        rect.setOutline("gray")
        rect.setFill("gray")
        for x in range(1, 11):
            row = []
            for y in range(1, 10):
                square = Rectangle(
                    Point(
                        (x * self.squareWidth - self.squareWidth * 0.5)
                        + 0.22 * self.width,
                        (y * self.squareHeight - self.squareHeight * 0.5)
                        + self.height * 0.05,
                    ),
                    Point(
                        (x * self.squareWidth + self.squareWidth * 0.5)
                        + 0.22 * self.width,
                        (y * self.squareHeight + self.squareHeight * 0.5)
                        + self.height * 0.05,
                    ),
                )
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
            "black",
            "Quit",
        )
        self.quitB.setTextColor("white")

    def getWin(self):
        """returns the graphical window"""
        return self.window

    def getQuitB(self):
        """returns the quit button"""
        return self.quitB

    def gridPoint(self, x, y):
        """returns the centerpoint of a given grid square"""
        return self.grid[x][y].getCenter()

    def moveGrid(self):
        """moves the grid so a different portion of the board is shown"""
        for row in self.grid:
            for square in row:
                for i in range(20):
                    square.move(-5, 5)

    def closeGrid(self):
        """closes the grid"""
        self.window.close()

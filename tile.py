from graphics import Point, Rectangle

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics import GraphWin


class Tile:
    def __init__(self, color1: str, color2: str, window: "GraphWin") -> None:
        """Constructs a tile object"""
        self.window = window
        self.squareWidth = self.squareHeight = 50
        self.objects = []
        self.colors = [color1, color2]
        self.mark = 0

    def drawTile(self, pt1: Point, pt2: Point) -> None:
        """Draws the tile and appends each piece of it to self.objects"""
        self.p1 = pt1
        self.p2 = pt2
        x1 = pt1.getX()
        x2 = pt2.getX()
        y1 = pt1.getY()
        y2 = pt2.getY()

        rectX1 = min(x1, x2) - 25
        rectY1 = max(y1, y2) + 25
        rectX2 = max(x1, x2) + 25
        rectY2 = min(y1, y2) - 25

        def drawObject(object, fillColor):
            object.draw(self.window)
            object.setFill(fillColor)
            object.setOutline("brown")
            self.objects.append(object)

        def buildTileColor(offset):
            rectX, rectY = (rectX1, rectY1) if offset == 1 else (rectX2, rectY2)
            color = self.colors[0] if offset == 1 else self.colors[1]
            half = Rectangle(
                Point(rectX + (3 * offset), rectY - (3 * offset)),
                Point(rectX + (47 * offset), rectY - (47 * offset)),
            )
            drawObject(half, color)
            return half

        self.box = Rectangle(Point(rectX1, rectY1), Point(rectX2, rectY2))
        drawObject(self.box, "brown")
        self.half1 = buildTileColor(1)
        self.half2 = buildTileColor(-1)

    def __str__(self) -> str:
        """allows the tile object to print out readably"""
        return "[" + self.colors[0] + ", " + self.colors[1] + "]"

    def switch(self) -> None:
        """Switches the colors of the tile, as if the player
        flipped the tile over"""
        self.colors.reverse()
        self.half1.setFill(self.colors[0])
        self.half2.setFill(self.colors[1])

    def placeTile(self, pt1) -> None:
        """animates placing the tile on the board"""
        xDist = abs(self.p1.getX() - pt1.getX())
        yDist = abs(self.p1.getY() - pt1.getY())
        if self.p1.getX() > pt1.getX():
            xDist = -xDist
        if self.p1.getY() > pt1.getY():
            yDist = -yDist
        self.moveTile(xDist, yDist, 50)

    def moveTile(self, x, y, dist) -> None:
        """Moves a tile"""
        for _ in range(dist):
            for item in self.objects:
                item.move(x / 50, y / 50)

    def getName(self) -> str:
        """returns the name of the tile"""
        return self.colors[0][0] + self.colors[1][0]

    def getMark(self) -> int:
        """returns the tile's mark"""
        return self.mark

    def updateMark(self, num) -> None:
        """updates the tile's mark:
        0 == unused
        1 == used in the current AI check
        2 == used on the board
        """
        self.mark = num

    def undraw(self) -> None:
        """undraws each piece of the tile"""
        for item in self.objects:
            item.undraw()

    def getColor1(self) -> str:
        """returns the left color of the tile"""
        return self.colors[0]

    def getColor2(self) -> str:
        """returns the right color of the tile"""
        return self.colors[1]

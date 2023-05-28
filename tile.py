from graphics import Point, Rectangle

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics import GraphWin


class Tile:
    def __init__(self, color1: str, color2: str, window: "GraphWin"):
        """Constructs a tile object"""
        self.color1 = color1
        self.color2 = color2
        self.window = window
        self.squareWidth = 50
        self.squareHeight = 50
        self.p1 = Point(0, 0)
        self.p2 = Point(0, 0)
        self.objects = []
        self.colors = [self.color1, self.color2]
        self.name = self.color1[0] + self.color2[0]
        self.mark = 0

    def drawTile(self, pt1: Point, pt2: Point):
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
        self.box = Rectangle(Point(rectX1, rectY1), Point(rectX2, rectY2))
        self.box.draw(self.window)
        self.box.setFill("brown")
        self.box.setOutline("brown")
        self.objects.append(self.box)

        def buildTileColor(offset):
            rectX, rectY = (rectX1, rectY1) if offset == 1 else (rectX2, rectY2)
            color = self.color1 if offset == 1 else self.color2
            half = Rectangle(
                Point(rectX + (3 * offset), rectY - (3 * offset)),
                Point(rectX + (47 * offset), rectY - (47 * offset)),
            )
            half.draw(self.window)
            half.setFill(color)
            half.setOutline("brown")
            self.objects.append(half)
            return half

        self.half1 = buildTileColor(1)
        self.half2 = buildTileColor(-1)

    def __str__(self):
        """allows the tile object to print out readably"""
        return "[" + self.color1 + ", " + self.color2 + "]"

    def switch(self):
        """Switches the colors of the tile, as if the player
        flipped the tile over"""
        self.color1, self.color2 = self.color2, self.color1
        self.half1.setFill(self.color1)
        self.half2.setFill(self.color2)
        self.name = self.name[1] + self.name[0]

    def placeTile(self, pt1):
        """animates placing the tile on the board"""
        x1 = self.p1.getX()
        x2 = pt1.getX()
        xDist = abs(x1 - x2)
        y1 = self.p1.getY()
        y2 = pt1.getY()
        yDist = abs(y1 - y2)
        if x1 > x2:
            xDist = -xDist
        if y1 > y2:
            yDist = -yDist
        self.moveTile(xDist, yDist, 50)

    def moveTile(self, x, y, dist):
        """Moves a tile"""
        for _ in range(dist):
            for item in self.objects:
                item.move(x / 50, y / 50)

    def getName(self):
        """returns the name of the tile"""
        return self.name

    def getMark(self):
        """returns whether or not the tile is marked"""
        return self.mark

    def updateMark(self, num):
        """updates whether or not the tile is marked"""
        self.mark = num

    def undraw(self):
        """undraws each piece of the tile"""
        for item in self.objects:
            item.undraw()

    def getColor1(self):
        """returns the left color of the tile"""
        return self.color1

    def getColor2(self):
        """returns the right color of the tile"""
        return self.color2

from graphics import Point, Rectangle

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from graphics import GraphWin


class Tile:
    def __init__(self, color1: str, color2: str, window: "GraphWin") -> None:
        """Constructs a tile object"""
        self.window = window
        self.squareWidth = self.squareHeight = 50
        self.objects = []
        self.colors = [color1, color2]
        self.isUnused = True

    def drawTile(self, pt1: Point, pt2: Point) -> None:
        """Draws the tile and appends each piece of it to self.objects"""
        self.p1 = pt1
        self.p2 = pt2

        rectX1 = min(pt1.getX(), pt2.getX()) - 25
        rectY1 = max(pt1.getY(), pt2.getY()) + 25
        rectX2 = max(pt1.getX(), pt2.getX()) + 25
        rectY2 = min(pt1.getY(), pt2.getY()) - 25

        def drawObject(object, fillColor: str) -> None:
            object.draw(self.window)
            object.setFill(fillColor)
            object.setOutline("brown")
            self.objects.append(object)

        def buildTileColor(dir: int) -> Rectangle:
            rectX, rectY = (rectX1, rectY1) if dir == 1 else (rectX2, rectY2)
            color = self.colors[0] if dir == 1 else self.colors[1]
            up, down = 3 * dir, 47 * dir
            half = Rectangle(
                Point(rectX + up, rectY - up), Point(rectX + down, rectY - down)
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

    def placeTile(self, pt1: Point) -> None:
        """animates placing the tile on the board"""
        xDist = self.getDist(self.p1.getX(), pt1.getX())
        yDist = self.getDist(self.p1.getY(), pt1.getY())
        self.moveTile(xDist, yDist, 50)

    def getDist(self, a: int, b: int) -> int:
        dist = abs(a - b)
        return dist if a <= b else -dist

    def moveTile(self, x: int, y: int, dist: int) -> None:
        """Moves a tile"""
        for _ in range(dist):
            for item in self.objects:
                item.move(x / 50, y / 50)

    def getName(self) -> str:
        """returns the name of the tile"""
        return self.colors[0][0] + self.colors[1][0]

    def isAvailable(self) -> bool:
        """returns the tile's availability"""
        return self.isUnused

    def updateAvailability(self) -> None:
        """update the tile's availability: true if unused, false if not"""
        self.isUnused = not self.isUnused

    def undraw(self) -> None:
        """undraws each piece of the tile"""
        for item in self.objects:
            item.undraw()

    def getColors(self) -> List[str]:
        return self.colors

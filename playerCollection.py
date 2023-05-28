from graphics import *
from random import randrange
from tile import *
from ButtonClass import *


class PlayerCollection:
    def __init__(self, window, top, player):
        """Constructs a player's collection of tiles
        and prints their information on the screen"""
        self.window = window
        self.top = top
        self.x = self.top.getX()
        self.player = player
        self.set = []
        self.choiceButtons = []
        self.squareWidth = 50
        self.squareHeight = 50
        self.left = []
        color = ["green", "blue", "red", "yellow"]
        cs = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
        ]
        for i in range(5):
            index = randrange(len(cs))
            col1, col2 = cs[index][0], cs[index][1]
            c1 = color[col1]
            c2 = color[col2]
            cs.remove(cs[index])
            tile = Tile(c1, c2, self.window)
            self.set.append(tile)
            self.left.append(tile)

        info = Text(self.top, "Player " + str(self.player) + " Collection")
        info.setSize(25)
        info.draw(self.window)

    def displayTiles(self):
        """Displays the collection of tiles on the screen
        as well as the polygon to cover the tiles should
        the game go so long as to require the board to shift"""
        y = self.top.getY() + 50
        for tile in self.set:
            tile.drawTile(Point(self.x - 25, y), Point(self.x + 25, y))
            y += 80

    def humanSetup(self):
        """Creates the buttons needed for a human player"""
        self.switchB = Button(
            self.window,
            Point(self.x - 35, self.window.getHeight() - 100),
            12,
            10,
            "white",
            "Switch Tile \nOrientation",
        )
        self.switchB.offSet(0, 25)
        self.switchB.deactivate()
        self.placeB = Button(
            self.window,
            Point(self.x + 35, self.window.getHeight() - 100),
            12,
            10,
            "white",
            "Place Tile",
        )
        self.placeB.offSet(0, 25)
        self.placeB.deactivate()
        y = self.top.getY() + 85
        for _ in self.set:
            button = Button(self.window, Point(self.x, y), 10, 8, "white", "Choose")
            button.offSet(0, 10)
            button.activate()
            self.choiceButtons.append(button)
            y += 80

    def getTileSet(self):
        """returns the set of tiles"""
        return self.set

    def getButtonSet(self):
        """returns the set of buttons used to choose the next tile"""
        return self.choiceButtons

    def getMoveSet(self):
        """returns the switch and placement tiles"""
        return self.switchB, self.placeB

    def getPlayer(self):
        """returns the number associated with the player"""
        return self.player

    def getLeft(self):
        """returns the tiles left in the player's hand"""
        return self.left

    def updateLeft(self, tile):
        """updates the tiles left in the player's hand"""
        self.left.remove(tile)

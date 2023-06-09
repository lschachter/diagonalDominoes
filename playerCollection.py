from random import randrange

from graphics import Point, Text
from tile import Tile
from button import Button

from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from graphics import GraphWin


class PlayerCollection:
    def __init__(self, window: "GraphWin", top: Point, playerId: int) -> None:
        """Constructs a player's collection of tiles
        and prints their information on the screen"""
        self.window = window
        self.top = top
        self.playerId = playerId
        self.tiles = []
        self.choiceButtons = []
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
        for _ in range(5):
            index = randrange(len(cs))
            col1, col2 = cs[index][0], cs[index][1]
            cs.remove(cs[index])
            tile = Tile(color[col1], color[col2], self.window)
            self.tiles.append(tile)
            self.left.append(tile)

        info = Text(self.top, f"Player {str(self.playerId)} Collection")
        info.setSize(25)
        info.draw(self.window)

    def displayTiles(self) -> None:
        """Displays the collection of tiles on the screen
        as well as the polygon to cover the tiles should
        the game go so long as to require the board to shift"""
        y = self.top.getY() + 50
        for tile in self.tiles:
            tile.drawTile(
                Point(self.top.getX() - 25, y), Point(self.top.getX() + 25, y)
            )
            y += 80

    def humanSetup(self) -> None:
        """Creates the buttons needed for a human player"""
        self.switchB = self.setUpButton("Switch Tile \nOrientation", -1)
        self.placeB = self.setUpButton("Place Tile", 1)

        y = self.top.getY() + 85
        for _ in self.tiles:
            button = Button(self.window, Point(self.top.getX(), y), 10, 8, "Choose")
            button.offSet(0, 10)
            button.activate()
            self.choiceButtons.append(button)
            y += 80

    def setUpButton(self, label: str, shift: int) -> Button:
        pt = Point(self.top.getX() + (35 * shift), self.window.getHeight() - 100)
        button = Button(self.window, pt, 12, 10, label)
        button.offSet(0, 25)
        button.deactivate()
        return button

    def getTiles(self) -> List[Tile]:
        """returns the set of tiles"""
        return self.tiles

    def getButtonSet(self) -> List[Button]:
        """returns the set of buttons used to choose the next tile"""
        return self.choiceButtons

    def getMoveSet(self) -> Tuple[Button, Button]:
        """returns the switch and placement tiles"""
        return self.switchB, self.placeB

    def getLeft(self) -> List[Tile]:
        """returns the tiles left in the player's hand"""
        return self.left

    def updateLeft(self, tile: Tile) -> None:
        """updates the tiles left in the player's hand"""
        self.left.remove(tile)

    def getPlayerId(self) -> int:
        return self.playerId

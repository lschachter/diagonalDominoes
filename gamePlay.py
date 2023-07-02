from graphics import Point
from gameTree import GameTree
from gNode import GNode
from button import WinButton, InfoBox
from playerCollection import PlayerCollection

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from grid import Grid
    from graphics import GraphWin
    from tile import Tile


class GamePlay:
    def __init__(
        self,
        window: "GraphWin",
        grid: "Grid",
    ) -> None:
        """constructs the instance for game play"""
        self.window = window
        self.grid = grid
        self.winButton = None
        self.buildPlayerCollections()

    def buildPlayerCollections(self) -> None:
        # sets up each player collection
        self.player1 = PlayerCollection(self.window, Point(120, 50), 1)
        self.player1.humanSetup()

        self.buttons = self.player1.getChoiceButtons()
        self.humanTiles = self.player1.getTiles()
        self.switch, self.place = self.player1.getMoveSet()

        self.player2 = PlayerCollection(self.window, Point(880, 50), 2)

        self.startX = 0
        self.startY = 8

        self.numClicked = 0

    def playGame(self) -> None:
        """begins the game"""
        pt = self.window.getMouse()
        startingNode = None

        while not self.grid.getQuitB().isClicked(pt):
            startingNode = self.startUp(pt)
            if startingNode or self.winButton:
                break

            pt = self.window.getMouse()

        if startingNode:
            self.humanMove(pt, startingNode)
        else:
            self.window.close()

    def startUp(self, pt: Point) -> Optional[GNode]:
        """Waits for the first tile to be picked by player1, then uses it to
        call to populate the tree"""
        self.checkTileButtons(pt)

        if self.switch.isClicked(pt):
            self.humanTiles[self.numClicked].switch()
        elif self.place.isClicked(pt):
            self.placeHumanTile()
            return self.computerSetUp(self.humanTiles[self.numClicked])

    def placeHumanTile(self) -> None:
        self.switch.deactivate()
        self.buttons[self.numClicked].die()

        gridPoint = self.grid.gridPoint(self.startX, self.startY)
        self.humanTiles[self.numClicked].placeTile(gridPoint)
        self.place.deactivate()
        self.humanTiles[self.numClicked].updateUseState(2)
        for button in self.buttons:
            button.deactivate()
        self.startX += 1
        self.startY -= 1

    def computerSetUp(self, rootTile: "Tile") -> Optional[GNode]:
        """creates an instance of the game tree and calls to populate it,
        then runs the rollback analysis"""
        root = GNode(rootTile)
        self.tree = GameTree(root, [self.player1, self.player2])
        self.tree.printTree()  # UNCOMMENT LINE TO SEE TREE PRINT

        return self.computerMove(root)

    def computerMove(self, node: GNode) -> Optional[GNode]:
        """chooses the computer's next move based on payoff, then places it"""
        gridPoint = self.grid.gridPoint(self.startX, self.startY)
        self.startX += 1
        self.startY -= 1

        if node.isEmpty():
            self.winButton = WinButton(self.window, "1")
            return None

        childrenByPay = {child.getPayoff(): child for child in node.getChildren()}
        newNode = childrenByPay[max(childrenByPay)]

        if newNode.getColors()[0] != node.getColors()[1]:
            newNode.getTile().switch()
        newNode.getTile().placeTile(gridPoint)

        if newNode.isEmpty():
            self.winButton = WinButton(self.window, "2")
            return None

        for button in self.buttons:
            button.activate()

        return newNode

    def humanMove(self, pt: Point, node: GNode) -> None:
        """gets clicks until player places tile correctly"""
        while not self.grid.getQuitB().isClicked(pt):
            if self.winButton and self.winButton.isClicked(pt):
                self.restartGame()

            if self.grid.getQuitB().isClicked(pt):
                break

            # Check if a tile was selected
            self.checkTileButtons(pt)

            if self.switch.isClicked(pt):
                self.humanTiles[self.numClicked].switch()
            elif self.place.isClicked(pt):
                node = self.processPlaceTileClick(node)

            pt = self.window.getMouse()
        self.window.close()

    def processPlaceTileClick(self, node: GNode) -> GNode:
        placedColor = node.getColors()[1]
        if placedColor == self.humanTiles[self.numClicked].getColors()[1]:
            self.humanTiles[self.numClicked].switch()

        if placedColor != self.humanTiles[self.numClicked].getColors()[0]:
            msg = "That move is invalid.\nChoose a tile whose left color corresponds\nto the rightmost tile-color on the board."
            errorRect = InfoBox(self.window, Point(496, 225), 500, 250, msg, size=26)
            self.window.getMouse()
            errorRect.delete()
        else:
            self.placeHumanTile()
            if self.player1.isEmpty():
                self.winButton = WinButton(self.window, "1")
            else:
                for child in node.getChildren():
                    if child.getTile() == self.humanTiles[self.numClicked]:
                        break
                node = self.computerMove(child)

        return node

    def checkTileButtons(self, pt: Point) -> None:
        for button in self.buttons:
            if button.isClicked(pt):
                self.buttons[self.numClicked].unchoose()
                button.choose()
                self.switch.activate()
                self.place.activate()
                self.numClicked = self.buttons.index(button)
                return

    def restartGame(self) -> None:
        self.clearGame()
        self.buildPlayerCollections()
        self.playGame()

    def clearGame(self) -> None:
        for player in [self.player1, self.player2]:
            for tile in player.getTiles():
                tile.undraw()

        for button in self.buttons:
            button.die()

        self.winButton.die()

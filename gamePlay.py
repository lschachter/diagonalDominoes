from graphics import Point
from gameTree import GameTree
from gNode import GNode
from button import WinButton, InfoBox

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from grid import Grid
    from playerCollection import PlayerCollection
    from graphics import GraphWin
    from button import Button
    from tile import Tile


class GamePlay:
    def __init__(
        self,
        window: "GraphWin",
        grid: "Grid",
        player1: "PlayerCollection",
        player2: "PlayerCollection",
    ) -> None:
        """constructs the instance for game play"""
        self.window = window
        self.grid = grid
        self.player1 = player1
        self.player2 = player2
        self.startX = 0
        self.startY = 8
        self.quitB = self.grid.getQuitB()
        self.buttons = player1.getButtonSet()
        self.humanTiles = player1.getTiles()
        self.switch, self.place = player1.getMoveSet()
        self.numClicked = 0

    def playGame(self) -> None:
        """begins the game"""
        pt = self.window.getMouse()
        startingNode = None

        while not self.quitB.isClicked(pt):
            startingNode = self.startUp(pt)
            if startingNode:
                break

            pt = self.window.getMouse()

        if startingNode:
            self.humanMove(pt, startingNode, 2)
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
        self.humanTiles[self.numClicked].updateMark(2)
        self.player1.updateLeft(self.humanTiles[self.numClicked])
        for button in self.buttons:
            button.deactivate()
        self.startX += 1
        self.startY -= 1

    def computerSetUp(self, rootTile: "Tile") -> Optional[GNode]:
        """creates an instance of the game tree and calls to populate it,
        then runs the rollback analysis"""
        self.root = GNode(rootTile, 0)
        self.tree = GameTree(self.root, [self.player1, self.player2])
        self.tree.populateTree()
        self.tree.setPayoffs()
        # self.tree.printTree()  # UNCOMMENT LINE TO SEE TREE PRINT

        return self.computerMove(self.root)

    def computerMove(self, node: GNode) -> Optional[GNode]:
        """chooses the computer's next move based on payoff, then places it"""
        gridPoint = self.grid.gridPoint(self.startX, self.startY)
        self.startX += 1
        self.startY -= 1

        if node.isEmpty():
            WinButton(self.window, "1")
            return None

        pays = []
        for child in node.getChildren():
            pays.append(child.getPayoff())
        index = pays.index(min(pays))
        newNode = node.getChildren()[index]
        if newNode.getTile().getColor1() != node.getTile().getColor2():
            newNode.getTile().switch()
        newNode.getTile().placeTile(gridPoint)
        self.player2.updateLeft(newNode.getTile())

        if node.getChildren()[index].isEmpty():
            WinButton(self.window, "2")
            return None

        for button in self.buttons:
            button.activate()

        return newNode

    def humanMove(self, pt: Point, node: GNode, depth: int) -> None:
        """gets clicks until player places tile correctly"""
        while not self.quitB.isClicked(pt):
            if self.quitB.isClicked(pt):
                break

            # Check if a tile was selected
            self.checkTileButtons(pt)

            if self.switch.isClicked(pt):
                self.humanTiles[self.numClicked].switch()
            elif self.place.isClicked(pt):
                placedColor = node.getTile().getColor2()
                if placedColor == self.humanTiles[self.numClicked].getColor2():
                    self.humanTiles[self.numClicked].switch()

                if placedColor != self.humanTiles[self.numClicked].getColor1():
                    errorRect = InfoBox(
                        self.window,
                        Point(496, 225),
                        500,
                        250,
                        "That move is invalid.\nChoose a tile whose left color corresponds\nto the rightmost tile-color on the board.",
                        size=26,
                    )
                    self.window.getMouse()
                    errorRect.delete()
                else:
                    self.placeHumanTile()
                    if depth == 8:
                        WinButton(self.window, "1")
                    else:
                        for iNode in node.getChildren():
                            if iNode.getTile() == self.humanTiles[self.numClicked]:
                                newNode = iNode
                                break
                        node = self.computerMove(newNode)
                        depth += 2

            pt = self.window.getMouse()
        self.window.close()

    def checkTileButtons(self, pt: Point) -> None:
        for button in self.buttons:
            if button.isClicked(pt):
                self.buttons[self.numClicked].unchoose()
                button.choose()
                self.switch.activate()
                self.place.activate()
                self.numClicked = self.buttons.index(button)

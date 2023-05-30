from graphics import Point
from gameTree import GameTree
from gNode import GNode
from button import WinButton, InfoBox

from typing import TYPE_CHECKING

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
        quitB: "Button",
    ):
        """constructs the instance for game play"""
        self.window = window
        self.grid = grid
        self.player1 = player1
        self.player2 = player2
        self.startX = 0
        self.startY = 8
        self.quitB = quitB
        self.buttons = player1.getButtonSet()
        self.tiles1 = player1.getTiles()
        self.switch, self.place = player1.getMoveSet()
        self.usedTiles = []
        self.numClicked = 0
        self.isOver = False

    def playGame(self):
        """begins the game"""
        pt = self.window.getMouse()
        start = False
        while start == False or not self.quitB.isClicked(pt):
            if self.quitB.isClicked(pt):
                self.window.close()
                break

            start = self.startUp(pt)
            if start != False:
                break

            pt = self.window.getMouse()

        self.humanMove(pt, start, 2)

    def startUp(self, pt: Point):
        """Waits for the first tile to be picked by player1, then uses it to
        call to populate the tree"""
        self.checkTileButtons(pt)

        if self.switch.isClicked(pt):
            self.tiles1[self.numClicked].switch()
        elif self.place.isClicked(pt):
            self.placeHumanTile()
            return self.computerSetUp(self.tiles1[self.numClicked])

        # returns false so that the while loop gets another click
        return False

    def placeHumanTile(self):
        self.switch.deactivate()
        self.buttons[self.numClicked].die()

        gridPoint = self.grid.gridPoint(self.startX, self.startY)
        self.tiles1[self.numClicked].placeTile(gridPoint)
        self.place.deactivate()
        self.tiles1[self.numClicked].updateMark(2)
        self.player1.updateLeft(self.tiles1[self.numClicked])
        for button in self.buttons:
            button.deactivate()
        self.startX += 1
        self.startY -= 1

    def computerSetUp(self, rootTile: "Tile"):
        """creates an instance of the game tree and calls to populate it,
        then runs the rollback analysis"""
        self.root = GNode(rootTile, 0)
        self.tree = GameTree(self.root, rootTile, [self.player1, self.player2])
        self.tree.populateTree()
        self.tree.setPayoffs()
        # self.tree.printTree() # UNCOMMENT LINE TO SEE TREE PRINT

        g1 = self.grid.gridPoint(self.startX, self.startY)
        self.startX += 1
        self.startY -= 1

        if self.root.isEmpty():
            WinButton(self.window, "1")
            self.isOver = True
            return False

        pays = []
        for node in self.root.getOutgoing():
            pays.append(node.getPayoff())
        index = pays.index(min(pays))
        newNode = self.root.getOutgoing()[index]
        tile = newNode.getTile()

        if tile.getColor1() != self.root.getTile().getColor2():
            tile.switch()
        tile.placeTile(g1)
        self.player2.updateLeft(tile)

        if newNode.isEmpty():
            self.isOver = True
            WinButton(self.window, "2")
        for button in self.buttons:
            button.activate()
        return newNode

    def computerMove(self, node: GNode):
        """chooses the computer's next move based on payoff, then places it"""
        g1 = self.grid.gridPoint(self.startX, self.startY)
        self.startX += 1
        self.startY -= 1

        if node.isEmpty():
            return False

        pays = []
        for child in node.getOutgoing():
            pays.append(child.getPayoff())
        index = pays.index(min(pays))
        newNode = node.getOutgoing()[index]
        if newNode.getTile().getColor1() != node.getTile().getColor2():
            newNode.getTile().switch()
        newNode.getTile().placeTile(g1)
        self.player2.updateLeft(newNode.getTile())
        if node.getOutgoing()[index].isEmpty():
            return True

        for button in self.buttons:
            button.activate()
        return newNode

    def humanMove(self, pt: Point, node: GNode, depth: int) -> None:
        """gets clicks until player places tile correctly"""
        while not self.quitB.isClicked(pt) or not self.isOver:
            if self.quitB.isClicked(pt):
                break

            # Check if a tile was selected
            self.checkTileButtons(pt)

            if self.switch.isClicked(pt):
                self.tiles1[self.numClicked].switch()
            elif self.place.isClicked(pt):
                placedColor = node.getTile().getColor2()
                if placedColor == self.tiles1[self.numClicked].getColor2():
                    self.tiles1[self.numClicked].switch()

                if placedColor != self.tiles1[self.numClicked].getColor1():
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
                        self.isOver = True
                        WinButton(self.window, "1")
                    else:
                        for iNode in node.getOutgoing():
                            if iNode.getTile() == self.tiles1[self.numClicked]:
                                newNode = iNode
                                break
                        tile, node = self.computerMove(
                            newNode, self.tiles1[self.numClicked]
                        )
                        depth += 2
                        if tile == False:
                            self.isOver = True
                            WinButton(self.window, "1")
                        elif tile == True:
                            self.isOver = True
                            WinButton(self.window, "2")

            pt = self.window.getMouse()
        self.window.close()

    def checkTileButtons(self, pt):
        for button in self.buttons:
            if button.isClicked(pt):
                self.buttons[self.numClicked].unchoose()
                button.choose()
                self.switch.activate()
                self.place.activate()
                self.numClicked = self.buttons.index(button)

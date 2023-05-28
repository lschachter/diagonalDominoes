from graphics import Rectangle, Point, Text
from GameTree import GameTree
from gNode import GNode
from button import WinButton


class GamePlay:
    def __init__(self, window, grid, player1, player2, quitB):
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
            else:
                start = self.startUp(pt)
            if start != False:
                break
            pt = self.window.getMouse()

        self.humanMove(pt, start, start.getTile(), 2)

    def startUp(self, pt):
        """Waits for the first tile to be picked by player1, then uses it to
        call to populate the tree"""
        for button in self.buttons:
            if button.isClicked(pt):
                self.buttons[self.numClicked].unchoose()
                button.choose()
                self.switch.activate()
                self.place.activate()
                self.numClicked = self.buttons.index(button)
        if self.switch.isClicked(pt):
            self.tiles1[self.numClicked].switch()
        elif self.place.isClicked(pt):
            self.switch.deactivate()
            self.buttons[self.numClicked].die()

            g1 = self.grid.gridPoint(self.startX, self.startY)
            g2 = self.grid.gridPoint(self.startX + 1, self.startY)
            self.tiles1[self.numClicked].placeTile(g1, g2)
            self.place.deactivate()
            self.tiles1[self.numClicked].updateMark(2)
            self.player1.updateLeft(self.tiles1[self.numClicked])
            for button in self.buttons:
                button.deactivate()
            self.startX += 1
            self.startY -= 1
            return self.computerSetUp(self.tiles1[self.numClicked])

        # returns false so that the while loop gets another click
        return False

    def computerSetUp(self, rootTile):
        """creates an instance of the game tree and calls to populate it,
        then runs the rollback analysis"""
        self.root = GNode(rootTile, 1, 0)
        self.tree = GameTree(self.root, rootTile)
        self.tree.populateTree(self.player1, self.player2)
        self.tree.setPayoffs()
        # self.tree.printTree() # UNCOMMENT LINE TO SEE TREE PRINT

        g1 = self.grid.gridPoint(self.startX, self.startY)
        g2 = self.grid.gridPoint(self.startX + 1, self.startY)
        self.startX += 1
        self.startY -= 1

        if self.root.isEmpty():
            WinButton(self.window, "1")
            self.isOver = True
            return False
        else:
            pays = []
            for node in self.root.getOutgoing():
                pays.append(node.getPayoff())
            index = pays.index(min(pays))
            newNode = self.root.getOutgoing()[index]
            tile = newNode.getTile()
        if tile.getColor1() != self.root.getTile().getColor2():
            tile.switch()
        tile.placeTile(g1, g2)
        self.player2.updateLeft(tile)
        if newNode.isEmpty():
            self.isOver = True
            WinButton(self.window, "2")
        for button in self.buttons:
            button.activate()
        return newNode

    def computerMove(self, node, tile, depth):
        """chooses the computer's next move based on payoff, then places it"""
        g1 = self.grid.gridPoint(self.startX, self.startY)
        g2 = self.grid.gridPoint(self.startX + 1, self.startY)
        self.startX += 1
        self.startY -= 1

        if node.isEmpty():
            return False, False
        else:
            pays = []
            for child in node.getOutgoing():
                pays.append(child.getPayoff())
            index = pays.index(min(pays))
            newNode = node.getOutgoing()[index]
            newTile = newNode.getTile()
            if newTile.getColor1() != tile.getColor2():
                newTile.switch()
            newTile.placeTile(g1, g2)
            self.player2.updateLeft(newTile)
            if node.getOutgoing()[index].isEmpty():
                return True, True
            for button in self.buttons:
                button.activate()
            return newTile, newNode

    def humanMove(self, pt, node, tile, depth):
        """gets clicks until player places tile correctly"""
        while not self.quitB.isClicked(pt) or not self.isOver:
            if self.quitB.isClicked(pt):
                break
            for button in self.buttons:
                if button.isClicked(pt):
                    self.buttons[self.numClicked].unchoose()
                    button.choose()
                    self.switch.activate()
                    self.place.activate()
                    self.numClicked = self.buttons.index(button)
            if self.switch.isClicked(pt):
                self.tiles1[self.numClicked].switch()
            elif self.place.isClicked(pt):
                if tile.getColor2() != self.tiles1[self.numClicked].getColor1():
                    errorRect = Rectangle(Point(249, 100), Point(748, 350))
                    errorRect.setFill("white")
                    errorRect.draw(self.window)
                    errorMess = Text(
                        Point(500, 200),
                        "That move is invalid.\nChoose a tile whose left color corresponds\nto the rightmost tile-color on the board.",
                    )
                    errorMess.draw(self.window)
                    errorMess.setSize(26)
                    self.window.getMouse()
                    errorRect.undraw()
                    errorMess.undraw()
                else:
                    self.switch.deactivate()
                    self.buttons[self.numClicked].die()

                    g1 = self.grid.gridPoint(self.startX, self.startY)
                    g2 = self.grid.gridPoint(self.startX + 1, self.startY)
                    self.tiles1[self.numClicked].placeTile(g1, g2)
                    self.place.deactivate()
                    self.tiles1[self.numClicked].updateMark(2)
                    self.player1.updateLeft(self.tiles1[self.numClicked])
                    for button in self.buttons:
                        button.deactivate()
                    self.startX += 1
                    self.startY -= 1
                    if depth == 8:
                        self.isOver = True
                        WinButton(self.window, "1")
                    else:
                        for iNode in node.getOutgoing():
                            if iNode.getTile() == self.tiles1[self.numClicked]:
                                newNode = iNode
                        tile, node = self.computerMove(
                            newNode, self.tiles1[self.numClicked], depth
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

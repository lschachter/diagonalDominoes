from collections import defaultdict
from gNode import GNode

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from tile import Tile
    from playerCollection import PlayerCollection


class GameTree:
    """creates and populates a tree of possibilities for the game,
    as well as does the rollback analysis"""

    def __init__(
        self, root: GNode, rootTile: "Tile", players: List["PlayerCollection"]
    ):
        """constructs the tree with the given root tile"""
        self.rootTile = rootTile
        self.root = root
        self.tree = defaultdict(list)
        self.tree[0].append(self.root)
        self.players = players

    def getRoot(self):
        """returns the root"""
        return self.root

    def getStruct(self):
        """returns actual dictionary"""
        return self.tree

    def populateTree(self):
        """gives the player tile collections and relevant info to the recursive
        function 'nextMove' to populate the tree"""
        self.nextMove(self.players[1], 1, self.root, self.rootTile.getColor2())

    def nextMove(self, player, depth, node, prevCol):
        """a recursive function that finds each possible next move"""
        for tile in player.getLeft():
            if prevCol == tile.getColor2():
                tile.switch()
            if prevCol == tile.getColor1() and tile.getMark() == 0:
                tile.updateMark(1)
                newNode = GNode(tile, depth)
                node.addOutgoing(newNode)
                self.tree[node.getDepth()].append(node)
                self.nextMove(
                    self.players[player.getPlayerNum() % 2],
                    depth + 1,
                    newNode,
                    tile.getColor2(),
                )
                tile.updateMark(0)
                if newNode.isEmpty():
                    if newNode.getDepth() == 9 or newNode.getDepth() % 2 == 0:
                        newNode.updatePayoff(1)
                    else:
                        newNode.updatePayoff(-1)

    def getTile(self, node: GNode):
        """returns the tile associated with the node"""
        return node.getTile()

    def payoffAt(self, node: GNode):
        """calculates payoffs based on how likely the human is to win
        given the children of the node"""
        if node.isEmpty():
            return node.getPayoff()

        childPays = []
        for child in node.getOutgoing():
            childPays.append(child.getPayoff())
        if node.getDepth() % 2 == 0:  # then these are your choices
            return min(childPays)
        else:
            numPos = 1
            numNeg = 1
            for num in childPays:
                if num <= 0:
                    numNeg += 1
                else:
                    numPos += 1
            pay = numPos / numNeg
            if pay > 1:
                return numNeg / numPos
            elif pay == 1:
                return 0
            else:
                return -pay

    def setPayoffs(self):
        """sets the payoffs for all nodes"""
        tuples = list(self.tree.items())
        tuples.sort(reverse=True)
        for layer in tuples:
            for node in layer[1]:
                node.updatePayoff(self.payoffAt(node))

    def printTree(self):
        """prints the tree by depth"""
        for level in list(self.tree.items()):
            print(level[0])
            for node in level[1]:
                print(node)
                print("payoff: ", node.getPayoff())

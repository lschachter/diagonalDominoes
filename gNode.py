from graphics import *


class GNode:
    """a GNode is just an object that holds a tile and all the tiles
    that that tile can reach"""

    def __init__(self, tile, player, depth):
        """constructs the node"""
        self.tile = tile
        self.outgoing = []
        self.player = player
        self.depth = depth
        self.payOff = 0
        self.items = ""

    def getTileName(self):
        """returns the name of the tile"""
        return self.self.tile.getName()

    def getTile(self):
        return self.tile

    def getDepth(self):
        """returns the depth of the node"""
        return self.depth

    def updatePayoff(self, num):
        """updates the node's payoff"""
        self.payOff = num

    def getPayoff(self):
        """returns the node's payoff"""
        return self.payOff

    def isEmpty(self):
        """returns true if leaf, false if not"""
        if self.outgoing == []:
            return True
        else:
            return False

    def getOutgoing(self):
        return self.outgoing

    def addOutgoing(self, gNode):
        """adds a node to the list of nodes reachable by this one,
        and adds the name of that node's tile to a string"""
        self.outgoing.append(gNode)
        self.items += gNode.getTileName() + " "

    def __str__(self):
        """allows the node to be printed out readably as the tile
        and all nodes it can reach"""
        return "{" + self.tile.getName() + ": " + self.items + "}"

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from tile import Tile


class GNode:
    """a GNode is just an object that holds a tile and all the tiles
    that that tile can reach"""

    def __init__(self, tile: "Tile", depth: int):
        """constructs the node"""
        self.tile = tile
        self.children = []
        self.depth = depth
        self.payOff = 0

    def getTile(self) -> "Tile":
        return self.tile

    def getDepth(self) -> int:
        """returns the depth of the node"""
        return self.depth

    def updatePayoff(self, num: int) -> None:
        """updates the node's payoff"""
        self.payOff = num

    def getPayoff(self) -> int:
        """returns the node's payoff"""
        return self.payOff

    def isEmpty(self) -> bool:
        """returns true if leaf, false if not"""
        return len(self.children) == 0

    def getChildren(self) -> List["GNode"]:
        return self.children

    def addChild(self, gNode: "GNode") -> None:
        """adds a node to the list of nodes reachable by this one,
        and adds the name of that node's tile to a string"""
        self.children.append(gNode)

    def __str__(self) -> str:
        """allows the node to be printed out readably as the tile
        and all nodes it can reach"""
        children = ", ".join([node.getTile().getName() for node in self.children])
        return f"[{self.tile.getName()}: {children}]"

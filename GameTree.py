from collections import defaultdict
from gNode import GNode

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from playerCollection import PlayerCollection


class GameTree:
    """creates and populates a tree of possibilities for the game,
    as well as does the rollback analysis"""

    def __init__(self, root: GNode, players: List["PlayerCollection"]) -> None:
        """constructs the tree with the given root tile"""
        self.root = root
        self.tree = defaultdict(set)
        self.players = players

    def populateTree(self) -> None:
        """gives the player tile collections and relevant info to the recursive
        function 'nextMove' to populate the tree"""
        self.nextMove(self.players[1], 1, self.root, self.root.getTile().getColor2())

    def nextMove(
        self, player: "PlayerCollection", depth: int, node: GNode, prevCol: str
    ) -> None:
        """a recursive function that finds each possible next move"""
        self.tree[node.getDepth()].add(node)

        for tile in player.getLeft():
            colors = tile.getColors()
            if prevCol not in colors or tile.getMark() != 0:
                # Ignore tiles that don't match the color or that have been used
                continue

            tile.updateMark(1)
            newNode = GNode(tile, depth)
            node.addChild(newNode)

            newColor = colors[0] if colors[0] != prevCol else colors[1]
            newPlayerId = player.getPlayerId() % 2
            self.nextMove(self.players[newPlayerId], depth + 1, newNode, newColor)

            tile.updateMark(0)

    def setPayoff(self, node: GNode) -> int:
        """calculates payoffs based on how likely the human is to win
        given the children of the node"""
        if node.isEmpty():
            # If it's a leaf node, set the payoff as user win (0) or loss (100)
            if node.getDepth() == 9 or node.getDepth() % 2 == 0:
                node.updatePayoff(0)
            else:
                node.updatePayoff(100)
            return

        childPays = [child.getPayoff() for child in node.getChildren()]
        if node.getDepth() % 2 == 0:
            # Then these are the computer's choices, so pick the best one
            node.updatePayoff(max(childPays))
        else:
            # Otherwise, average together the user's options
            node.updatePayoff(sum(childPays) / len(childPays))

    def setPayoffs(self) -> None:
        """sets the payoffs for all nodes"""
        tuples = list(self.tree.items())
        tuples.sort(reverse=True)
        for _, nodes in tuples:
            for node in nodes:
                self.setPayoff(node)

    def printTree(self) -> None:
        """prints the tree by depth"""
        for level, nodes in list(self.tree.items()):
            print(level)
            for node in nodes:
                print(node)
                print("payoff: ", node.getPayoff())

from gNode import GNode

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from playerCollection import PlayerCollection


class GameTree:
    """creates and populates a tree of possibilities for the game,
    as well as does the rollback analysis"""

    def __init__(self, root: GNode, players: List["PlayerCollection"]) -> None:
        """constructs the tree with the given root tile"""
        self.maxDepth = 9
        self.root = root
        self.players = players

        self.nextMove(self.players[1], 1, self.root, self.root.getTile().getColors()[1])

    def nextMove(
        self, player: "PlayerCollection", depth: int, node: GNode, prevCol: str
    ) -> None:
        """a recursive function that finds each possible next move"""
        for tile in player.getTiles():
            # Ignore tiles that don't match the color or that have been used
            if tile.getUseState() != 0 or prevCol not in tile.getColors():
                continue

            tile.updateUseState(1)
            newNode = GNode(tile, depth)
            node.addChild(newNode)

            colors = tile.getColors()
            newColor = colors[0] if colors[0] != prevCol else colors[1]
            newPlayerId = player.getPlayerId() % 2
            self.nextMove(self.players[newPlayerId], depth + 1, newNode, newColor)

            tile.updateUseState(0)

        self.setPayoff(node)

    def setPayoff(self, node: GNode) -> int:
        """calculates payoffs based on how likely the human is to win
        given the children of the node"""
        if node.isEmpty():
            # If it's a leaf node, set the payoff as user win (0) or loss (100)
            if node.getDepth() == self.maxDepth or node.getDepth() % 2 == 0:
                node.updatePayoff(0)
            else:
                # Multiply by (max depth - node.depth) to prioritize faster wins
                node.updatePayoff(100 * (self.maxDepth - node.getDepth()))
            return

        # Otherwise, the payoff depends on those of the node's children
        childPays = [child.getPayoff() for child in node.getChildren()]
        if node.getDepth() % 2 == 0:
            # Then these are the computer's choices, so pick the best one
            node.updatePayoff(max(childPays))
        else:
            # Otherwise, average together the user's options
            node.updatePayoff(sum(childPays) / len(childPays))

    def printTree(self) -> None:
        """prints the tree by depth"""
        queue = [self.root]

        while queue:
            node = queue.pop(0)
            print(node)
            print("payoff: ", node.getPayoff())
            for child in node.getChildren():
                queue.append(child)

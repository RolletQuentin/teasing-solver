from Teasing import Teasing


class Node:

    def __init__(self, parent: Teasing, game: Teasing, cost: int) -> None:
        self.parent = parent
        self.game = game
        self.cost = cost

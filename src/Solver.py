from src.Teasing import Teasing
from src.Node import Node
from typing import List
import numpy as np
from time import monotonic


class Solver:

    def __init__(self, geometry: str):
        self.geometry: str = geometry
        self.open_list: List(Node) = []
        self.close_list: List(Node) = []

    def manhattan_geometry(self, game: Teasing):
        res = 0
        for i in range(game.x):
            for j in range(game.y):
                if not (game.board[i, j] == 0):
                    x0 = (game.board[i, j] - 1) // game.x
                    y0 = (game.board[i, j] - 1) % game.y
                    res += abs(x0-i) + (y0-j)

        return res

    def hamming_geometry(self, game: Teasing):
        res = game.x * game.y - 1
        for i in range(game.x):
            for j in range(game.y):
                if game.board[i, j] == game.solution[i, j] and not (game.board[i, j] == 0):
                    res -= 1

        return res

    def cost(self, game: Teasing):
        cost: int = 0
        if self.geometry == "hamming":
            cost = self.hamming_geometry(game)
        elif self.geometry == "manhattan":
            cost = self.manhattan_geometry(game)

        return cost

    def is_in_open_list(self, node: Node) -> int:
        index = -1
        i = 0
        while i < len(self.open_list) and index == -1:
            if self.open_list[i].game == node.game:
                index = i
            else:
                i += 1

        return index

    def is_in_close_list(self, node: Node) -> int:
        index = -1
        i = 0
        while i < len(self.close_list) and index == -1:
            if self.close_list[i].game == node.game:
                index = i
            else:
                i += 1

        return index

    def update_node_in_open_list(self, node: Node, index: int):
        if node.cost < self.open_list[index].cost:
            self.open_list.pop(index)
            self.add_node_to_open_list(node)

    def add_node_to_open_list(self, node: Node):
        i = 0
        added = False
        while not (added) and i < len(self.open_list):
            if node.cost < self.open_list[i].cost:
                self.open_list.insert(i, node)
                added = True
            else:
                i += 1

        if not (added):
            self.open_list.append(node)

    def a_star(self, game: Teasing):
        number_of_iteration: int = 0
        start_time = monotonic()

        # add root to the open_list
        root: Node = Node(None, game, self.cost(game))
        self.open_list.append(root)

        while len(self.open_list) > 0 and not (self.open_list[0].game.win()):
            node: Node = self.open_list[0]

            # 1. watch near nodes
            zero_index = np.where(node.game.board == 0)
            x0, y0 = zero_index[0][0], zero_index[1][0]

            # up
            self.move(node, (x0-1, y0), (x0, y0))
            # down
            self.move(node, (x0+1, y0), (x0, y0))
            # left
            self.move(node, (x0, y0-1), (x0, y0))
            # right
            self.move(node, (x0, y0+1), (x0, y0))

            self.open_list.remove(node)
            self.close_list.append(node)
            number_of_iteration += 1

            # print("open_list :")
            # for e in self.open_list:
            #     print(e.game)
            # print("close_list :")
            # for e in self.close_list:
            #     print(e.game)
            # print(node.game)

        if len(self.open_list) == 0:
            solution = []
            print("No solutions")

        else:
            solution = self.list_optimal_solution(self.open_list[0])
            for e in solution:
                print(e.game)

            print(f"Solution find in {len(solution)} moves !")
            print(
                f"Number of iterations to find the solution: {number_of_iteration}")

        end_time = monotonic()
        return {
            'solution': solution,
            'elapsed_time': end_time - start_time
        }

    def move(self, node: Node, initial_position, reset_position):
        moving: int = 0
        moving = node.game.move(initial_position)
        if moving == 1:
            new_node = Node(node, node.game.copy(), self.cost(node.game))
            node.game.move(reset_position)
            if self.is_in_close_list(new_node) == -1:
                index_same_node = self.is_in_open_list(new_node)

                if index_same_node != -1:
                    self.update_node_in_open_list(new_node, index_same_node)
                else:
                    self.add_node_to_open_list(new_node)

    def list_optimal_solution(self, node: Node):
        res = []
        while node.parent is not None:
            res.append(node)
            node = node.parent

        res.reverse()

        return res


if __name__ == "__main__":
    game = Teasing(x=3, y=3, seed=-1)
    solver = Solver("hamming")
    print(game)
    print(solver.a_star(game))

    # open_list: list((Teasing, int)) = [
    #     (None, 1), (None, 3), (None, 5), (None, 9)]
    # print(solver.add_to_list_sort(open_list, (None, 10)))

    # open_list = []
    # game.move((1, 1))
    # open_list.append((game.copy(), solver.manhattan_geometry(game)))
    # game.move((2, 1))

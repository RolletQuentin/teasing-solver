from Teasing import Teasing
import numpy as np


class Solver:

    def __init__(self, geometry):
        self.geometry = geometry

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

    # doesn't work
    def greedy(self, game: Teasing):
        moves = 0
        while not (game.win()):
            # calculate possible grid
            zero_index = np.where(game.board == 0)
            x0 = zero_index[0][0]
            y0 = zero_index[1][0]
            moving = 0  # 1 if we move, else 0
            geometries = []

            # for each side, we calculate the geometry
            # up
            moving = game.move((x0-1, y0))
            if moving == 1:
                if self.geometry == "hamming":
                    geometries.append(
                        ((x0-1, y0), self.hamming_geometry(game)))
                # we cancel the move
                game.move((x0, y0))

            # down
            moving = game.move((x0+1, y0))
            if moving == 1:
                if self.geometry == "hamming":
                    geometries.append(
                        ((x0+1, y0), self.hamming_geometry(game)))
                # we cancel the move
                game.move((x0, y0))

            # left
            moving = game.move((x0, y0-1))
            if moving == 1:
                if self.geometry == "hamming":
                    geometries.append(
                        ((x0, y0-1), self.hamming_geometry(game)))
                # we cancel the move
                game.move((x0, y0))

            # right
            moving = game.move((x0, y0+1))
            if moving == 1:
                if self.geometry == "hamming":
                    geometries.append(
                        ((x0, y0+1), self.hamming_geometry(game)))
                # we cancel the move
                game.move((x0, y0))

            # select the best moves
            best_moves = []
            minimum = geometries[0][1]
            for e in geometries:
                # e : ((x,y), distance)
                if e[1] == minimum:
                    best_moves.append(e[0])
                elif e[1] < minimum:
                    minimum = e[1]
                    best_moves = [e[0]]

            # print(f"geometries : {geometries}")
            # print(f"Best moves : {best_moves}")
            # print(game)
            # print()

            # choose a random move in the best moves
            game.move(best_moves[np.random.randint(len(best_moves))])
            moves += 1

        return moves

    def a_star(self, game: Teasing):
        open_list: list((Teasing, int)) = []
        close_list: list((Teasing, int)) = []
        moves: int = 0

        # add the current node to the list
        if self.geometry == "hamming":
            open_list.append((game.copy(), self.hamming_geometry(game)))
        elif self.geometry == "manhattan":
            open_list.append((game.copy(), self.manhattan_geometry(game)))

        while len(open_list) > 0 and not (open_list[0][0].win()):
            current_game: Teasing = open_list[0][0]

            # 1. watch near nodes
            zero_index = np.where(current_game.board == 0)
            x0 = zero_index[0][0]
            y0 = zero_index[1][0]

            # up
            (open_list, close_list) = self.move(
                current_game, open_list, close_list, x0-1, y0, x0, y0)

            # down
            (open_list, close_list) = self.move(
                current_game, open_list, close_list, x0+1, y0, x0, y0)

            # left
            (open_list, close_list) = self.move(
                current_game, open_list, close_list, x0, y0-1, x0, y0)

            # right
            (open_list, close_list) = self.move(
                current_game, open_list, close_list, x0, y0+1, x0, y0)

            # 5. put the node from open_list to close_list
            close_list.append(open_list.pop(0))

            moves += 1

            # print(f"open_list : {open_list}")
            # print(f"close_list : {close_list}")
            # print(current_game)
            # print()

        if len(open_list) == 0:
            print("No solutions")

        else:
            print(open_list[0][0])
        return moves

    def move(self, current_game: Teasing, open_list: list((Teasing, int)), close_list: list((Teasing, int)), x0: int, y0: int, x1: int, y1: int):
        moving: int = 0  # 1 if we move, else 0
        moving = current_game.move((x0, y0))
        if moving == 1:
            # 2. if it is in close_list, forget it
            is_in_close_list = False
            i = 0
            while i < len(close_list) and not (is_in_close_list):
                is_in_close_list = np.array_equal(
                    current_game.board, close_list[i][0].board)
                i += 1

            if not (is_in_close_list):
                new_game = current_game.copy()

                # we cancel the move
                current_game.move((x1, y1))
                if self.geometry == "hamming":
                    open_list = self.add_node(
                        open_list, (new_game, self.hamming_geometry(new_game)))
                elif self.geometry == "manhattan":
                    open_list = self.add_node(
                        open_list, (new_game, self.manhattan_geometry(new_game)))

            # we cancel the move (it doesn't matter if the move is already cancel)
            current_game.move((x1, y1))

        return (open_list, close_list)

    def add_node(self, open_list: list, node: (Teasing, int)):
        is_in_list = False
        i = 0
        while i < len(open_list) and not (is_in_list):
            is_in_list = np.array_equal(node[0].board, open_list[i][0].board)
            i += 1

        # 3. if the node is not in the open list, add it into the list
        if not (is_in_list):
            open_list = self.add_to_list_sort(open_list, node)

        return open_list

    def add_to_list_sort(self, open_list: list((Teasing, int)), node: (Teasing, int)):
        i = 0
        added = False
        while not (added) and i < len(open_list):
            if node[1] < open_list[i][1]:
                open_list.insert(i, node)
                added = True
            i += 1

        if not (added):
            open_list.append(node)

        return open_list


if __name__ == "__main__":
    game = Teasing(x=3, y=3, seed=1)
    solver = Solver("manhattan")
    print(game)
    print(solver.a_star(game))

    # open_list: list((Teasing, int)) = [
    #     (None, 1), (None, 3), (None, 5), (None, 9)]
    # print(solver.add_to_list_sort(open_list, (None, 10)))

    # open_list = []
    # game.move((1, 1))
    # open_list.append((game.copy(), solver.manhattan_geometry(game)))
    # game.move((2, 1))

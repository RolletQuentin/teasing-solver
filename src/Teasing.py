import numpy as np


class Teasing:
    """
    This is the implementation of the teasing game.

    ...

    Attributes
    ----------
    board : array
        the board of the game

    Methods
    -------

    """

    def __init__(self, x=3, y=3, seed=-1, board=None, solution=None):
        """Constructs all the necessary attributes for the person object.

        Args:
            seed (str, optional): The seed for how the teasing game is set. -1 is for a random seed. Defaults to -1.
        """
        self.x = x
        self.y = y
        self.seed = seed

        if solution is None:
            # generate the solution
            solution = np.arange(1, self.x*self.y)
            solution = np.append(solution, 0)
            self.solution = solution.reshape((self.x, self.y))
        else:
            self.solution = solution

        if board is None:
            # generate random board
            self.board = self.solution.copy()
            self.random_teasing_board()
        else:
            self.board = board

    def __eq__(self, value: object) -> bool:
        return np.array_equal(self.board, value.board)

    def __str__(self):
        horizontal_line = "----"*self.y + "-\n"

        # first line
        result = horizontal_line
        for i in range(self.x):
            # Replace 0 with space
            row_str = "| " + " | ".join(" " if x == 0 else str(x)
                                        for x in self.board[i]) + " |\n"
            result += row_str
            result += horizontal_line

        return result

    def copy(self):
        return Teasing(
            x=self.x,
            y=self.y,
            seed=self.seed,
            board=self.board.copy(),
            solution=self.solution)

    def random_teasing_board(self):
        """Generate a random board for the teasing game. If the seed is -1, a random seed will be used.

        Args:
            seed (int, optional): Seed for random number generation. If not provided or set to -1, a random seed will be used.

        Returns:
            numpy.ndarray: A 2D NumPy array representing the random teasing board.
        """
        if self.seed == -1:
            np.random.seed()
        else:
            np.random.seed(self.seed)

        for _ in range(50*self.x*self.y):
            zero_index = np.where(self.board == 0)
            x0 = zero_index[0][0]
            y0 = zero_index[1][0]
            # we take a zone arround the empty case where we click
            match np.random.randint(4):
                case 0:
                    self.move((x0-1, y0))
                case 1:
                    self.move((x0+1, y0))
                case 2:
                    self.move((x0, y0-1))
                case 3:
                    self.move((x0, y0+1))

    def win(self):
        """Return True if the game is finished, else False
        """
        return np.array_equal(self.board, self.solution)

    def move(self, pos):
        """Move one box

        Args:
            pos (tuple(int, int)):
                the position of the box
        """

        (i, j) = pos

        if i >= 0 and i < self.x and j >= 0 and j < self.y:
            # if the empty case is up to the selected box
            if i > 0 and self.board[i-1, j] == 0:
                self.board[i-1, j] = self.board[i, j]
                self.board[i, j] = 0
                return 1

            # if the empty case is below to the selected box
            if i < self.x-1 and self.board[i+1, j] == 0:
                self.board[i+1, j] = self.board[i, j]
                self.board[i, j] = 0
                return 1

            # if the empty case is left to the selected box
            if j > 0 and self.board[i, j-1] == 0:
                self.board[i, j-1] = self.board[i, j]
                self.board[i, j] = 0
                return 1

            # if the empty case is right to the selected box
            if j < self.y-1 and self.board[i, j+1] == 0:
                self.board[i, j+1] = self.board[i, j]
                self.board[i, j] = 0
                return 1

            return 0
        return 0


if __name__ == "__main__":
    game = Teasing(x=9, y=8, seed=1)
    game2 = Teasing(x=9, y=9, seed=1)
    # game.move((8, 8))
    print(game)
    print(game == game2)

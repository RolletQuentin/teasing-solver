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

    def __init__(self, seed=-1):
        """Constructs all the necessary attributes for the person object.

        Args:
            seed (str, optional): The seed for how the teasing game is set. -1 is for a random seed. Defaults to -1.
        """
        self.board = self.random_teasing_board(seed)

    def __str__(self):
        horizontal_line = "-------------\n"

        # first line
        result = horizontal_line
        for i in range(3):
            # Replace 0 with space
            row_str = "| " + " | ".join(" " if x == 0 else str(x)
                                        for x in self.board[i]) + " |\n"
            result += row_str
            result += horizontal_line

        return result

    def random_teasing_board(self, seed=-1):
        """Generate a random board for the teasing game. All numbers from 0 to 8 will appear once on the board, and the shape of the board is (3,3). If the seed is -1, a random seed will be used.

        Args:
            seed (int, optional): Seed for random number generation. If not provided or set to -1, a random seed will be used.

        Returns:
            numpy.ndarray: A 2D NumPy array representing the random teasing board.
        """
        if seed == -1:
            np.random.seed()
        else:
            np.random.seed(seed)

        numbers = np.arange(9)
        np.random.shuffle(numbers)

        teasing_board = numbers.reshape((3, 3))
        return teasing_board

    def win(self):
        """Return True if the game is finished, else False
        """

        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def move(self, pos, direction):
        """Move one box

        Args:
            pos (tuple(int, int)):
                the position of the box

            direction (string):
                take one of the following values : "right", "left", "up" or "down"
        """

        i, j = pos
        if direction == "up" and i != 0 and self.board[i-1, j] == 0:
            self.board[i-1, j] = self.board[i, j]
            self.board[i, j] = 0

        if direction == "down" and i != 2 and self.board[i+1, j] == 0:
            self.board[i+1, j] = self.board[i, j]
            self.board[i, j] = 0

        if direction == "left" and j != 0 and self.board[i, j-1] == 0:
            self.board[i, j-1] = self.board[i, j]
            self.board[i, j] = 0

        if direction == "right" and j != 2 and self.board[i, j+1] == 0:
            self.board[i, j+1] = self.board[i, j]
            self.board[i, j] = 0


if __name__ == "__main__":
    game = Teasing(seed=1)
    game.move((2, 2), "up")
    game.move((1, 2), "up")
    game.move((2, 1), "right")
    game.move((1, 1), "down")
    game.move((1, 2), "left")
    print(game)

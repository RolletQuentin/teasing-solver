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


if __name__ == "__main__":
    game = Teasing()
    print(game)

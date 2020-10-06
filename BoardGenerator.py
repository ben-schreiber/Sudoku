from typing import List

from Board import Board
from random import randint


class BoardGenerator:
    """
    This class houses the algorithms necessary for generating a solvable Sudoku board.
    The class only needs to be instantiated once, and then the generate_new_board() method
    can be called to continue producing new Board objects
    """

    def __init__(self, size=(9, 9)):
        self.height, self.width = size

    def generate_new_board(self) -> Board:
        """When called, will return a new Board object containing an unsolved Sudoku grid"""
        board_object = Board((self.height, self.width))
        new_board = self.create_empty_board(board_object)
        board_object.set_board(new_board)
        return board_object

    def create_empty_board(self, board: Board) -> List[List[int]]:
        """Used to create a 2D python array containing the board info"""
        pass

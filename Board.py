from math import sqrt
from copy import deepcopy


class Board:

    ERROR = -1

    def __init__(self, size=(9, 9)):
        self.height, self.width = size
        self.board = self.__init_board()
        self.initial_board = deepcopy(self.board)
        self.mini_box_height = int(sqrt(self.height))
        self.mini_box_width = int(sqrt(self.width))
        self.valid_nums = [num for num in range(1, self.mini_box_width * self.mini_box_height + 1)]
        default_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 1, 6, 0],
            [0, 6, 7, 0, 3, 5, 0, 0, 4],
            [6, 0, 8, 1, 2, 0, 9, 0, 0],
            [0, 9, 0, 0, 8, 0, 0, 3, 0],
            [0, 0, 2, 0, 7, 9, 8, 0, 6],
            [8, 0, 0, 6, 9, 0, 3, 5, 0],
            [0, 2, 6, 0, 0, 0, 0, 9, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        # default_board = [
        #     [4, 8, 9, 2, 6, 1, 5, 7, 3],
        #     [2, 3, 5, 8, 4, 7, 1, 6, 9],
        #     [1, 6, 7, 9, 3, 5, 2, 8, 4],
        #     [6, 7, 8, 1, 2, 3, 9, 4, 5],
        #     [5, 9, 1, 4, 8, 6, 7, 3, 2],
        #     [3, 4, 2, 5, 7, 9, 8, 1, 6],
        #     [8, 1, 4, 6, 9, 2, 3, 5, 7],
        #     [7, 2, 6, 3, 5, 8, 4, 9, 1],
        #     [9, 5, 3, 7, 1, 4, 6, 2, 0]
        # ]
        self.set_board(default_board)

    def __str__(self):
        output = ''
        for row in range(self.height):
            if row % self.mini_box_height == 0 and row > 0:
                output += ' - ' * (self.width - 2) + '\n'
            for col in range(self.width):
                if col % self.mini_box_width == 0 and col > 0:
                    output += '| '
                output += str(self.board[row][col])
                output += ' '
            output += '\n'
        return output

    def is_legal(self, row, col, num):
        """
        Given the cell coordinates and attempted number, returns whether or not
        the number can legally be placed there. Does not account for if the desired cell is already occupied
        :param row: The row
        :param col: The column
        :param num: The number
        :return: True iff legal placement
        """
        # Check the rest of the row
        for other_col_coordinate in range(self.width):
            if other_col_coordinate != col and self.board[row][other_col_coordinate] == num:
                return False

        # Check the rest of the column
        for other_row_coordinate in range(self.height):
            if other_row_coordinate != row and self.board[other_row_coordinate][col] == num:
                return False

        # Check the mini box that the cell resides in
        col_shift = col // self.mini_box_width
        row_shift = row // self.mini_box_height

        for _row in range(self.mini_box_height):
            for _col in range(self.mini_box_width):
                if (_row != row or _col != col) and self.board[row_shift * self.mini_box_height + _row][col_shift * self.mini_box_width + _col] == num:
                    return False

        return True

    def apply_move(self, row, col, num):
        """
        Attempts to apply the given number to the given cell.
        Will only apply the move if the cell was unoccupied on the initial board.
        If num == 0, the desired cell will be cleared
        Returns True iff successful
        :param row: The row
        :param col: The column
        :param num: The number
        :return: True iff successful
        """
        if 0 <= row < self.height \
                and 0 <= col < self.width \
                and (num in self.valid_nums or num == 0) \
                and self.initial_board[row][col] == 0:
            self.board[row][col] = num
            return True
        return False

    def reset_cell(self, row, col):
        """Resets the given (row, col) cell to contain the default val. Returns True iff successful"""
        return self.apply_move(row, col, 0)

    def find_empty_cell(self):
        """Returns an empty cell in the board. If none exist, return (Board.ERROR, Board.ERROR)"""
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
                    return row, col
        return Board.ERROR, Board.ERROR

    def __init_board(self):
        """Initializes a board"""
        board = []
        for row in range(self.height):
            new_row = []
            for col in range(self.width):
                new_row.append(0)
            board.append(new_row)
        return board

    def set_board(self, board):
        """Sets the board to the given board (a 2D array). Does not check for validity
        and does not update other internal variables connected to the board.
        Useful only for setting the board before the game begins"""
        self.board = board
        self.initial_board = deepcopy(self.board)

    def valid_complete_board(self):
        """Returns True iff the board has been solved"""
        for row in range(self.height):
            for col in range(self.width):
                if not self.is_legal(row, col, self.board[row][col]):
                    return False
        return True

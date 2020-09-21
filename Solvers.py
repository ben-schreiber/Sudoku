from Board import Board
from copy import deepcopy


class Solver:

    BACKTRACKING_SOLVER = 'backtracking'
    SOLVERS = [BACKTRACKING_SOLVER]

    def __init__(self, board: Board):
        self.board = board
        self.original_board = deepcopy(board)
        self.solved = False
        self.steps = []  # Stores all of the steps

    def solve_board(self):
        """
        Solves the board stored in memory if possible. Will update the Solver object accordingly if the board was solved
        :return: The board object after solving if a solution is possible; otherwise, returns original board
        """
        pass

    def was_solved(self):
        """Returns False unless a solution was found when calling self.solve_board()"""
        return self.solved

    def get_steps(self):
        """Returns all of the steps used to find a solution. Each step is a (row, col, num) triplet"""
        return self.steps

    def record_step(self, step):
        """
        Records a step as the solver solves the board
        :param step: A (row, col, num) tuple triplet
        """
        self.steps.append(step)


class BacktrackingSolver(Solver):

    def __init__(self, board: Board):
        super().__init__(board)

    def solve_board(self):
        if self.solve_board_helper():
            self.solved = True
            return self.board
        else:
            return self.original_board

    def solve_board_helper(self):
        """A helper function. Actually performs the solving"""
        row, col = self.board.find_empty_cell()
        if row == self.board.ERROR:  # If there are no more empty cells
            return True
        for num in self.board.valid_nums:
            if self.board.is_legal(row, col, num) and self.original_board.board[row][col] == 0:
                self.board.apply_move(row, col, num)  # Set the number
                self.record_step((row, col, num))
                if self.solve_board_helper():
                    return True
                self.board.reset_cell(row, col)  # Undo the setting
                self.record_step((row, col, 0))


def get_solver(solver_name, board):
    """Given the string input representing the name of the solver, return the Solver object"""
    if solver_name == Solver.BACKTRACKING_SOLVER:
        return BacktrackingSolver(board)

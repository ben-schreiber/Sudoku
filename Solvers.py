from Board import Board
from copy import deepcopy
from time import time
import heapq
import abc


class PriorityQueue:
    """
    Implements a priority queue data structure.
    The queue will store each item with a paired priority. That way,
    when the pop() method is called, the queue will return the item with
    the lowest priority
    """

    def __init__(self):
        self.list = []

    def push(self, item, priority=None):
        pair = (priority, item)
        heapq.heappush(self.list, pair)

    def pop(self):
        priority, item = heapq.heappop(self.list)
        return item

    def is_empty(self):
        """Returns True iff the data structure is free of any item"""
        return len(self.list) == 0

    def get_sorted_list(self):
        """Returns a sorted list containing the elements of the heap"""
        in_order = []
        while not self.is_empty():
            item = self.pop()
            in_order.append(item)
        return in_order


class Solver(abc.ABC):

    LCV_SOLVER = 'lcv'
    BACKTRACKING_SOLVER = 'backtracking'
    MRV_SOLVER = 'mrv'
    FORWARD_CHECKING_SOLVER = 'fcs'

    SOLVERS = [BACKTRACKING_SOLVER, MRV_SOLVER, LCV_SOLVER, FORWARD_CHECKING_SOLVER]

    def __init__(self, board: Board):
        self.board = board
        self.original_board = deepcopy(board)
        self.solved = False
        self.steps = []  # Stores all of the steps
        self.time_used = 0

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

    def get_time_used_to_solve(self):
        """Returns the amount of time needed to solve the board"""
        return self.time_used

    def get_cell(self):
        """Returns a cell to attempt to fill"""
        return self.board.ERROR, self.board.ERROR

    def get_vals_for_cell(self, row, col):
        """
        Returns a list of possible values for the given (row, col) pair
        """
        return []

    def solve_board(self):
        """
        Solves the board stored in memory if possible. Will update the Solver object accordingly if the board was solved
        :return: The board object after solving if a solution is possible; otherwise, returns original board
        """
        start = time()
        if self.solve_board_helper():
            self.time_used = time() - start
            self.solved = True
            return self.board
        else:
            self.time_used = time() - start
            return self.original_board

    def solve_board_helper(self):
        row, col = self.get_cell()
        if row == self.board.ERROR:  # If there are no more empty cells
            return True
        for num in self.get_vals_for_cell(row, col):
            if self.board.is_legal(row, col, num) and self.original_board.board[row][col] == 0:
                self.do_move(row, col, num)
                # print(f'Row={row}, Col={col}, Num={num}, Setting_num=True')

                if self.solve_board_helper():
                    return True

                # print(f'Row={row}, Col={col}, Num={num}, Setting_num=False')
                self.do_move(row, col, num, setting_num=False)

    @abc.abstractmethod
    def do_move(self, row, col, num, setting_num=True):
        pass


class BacktrackingSolver(Solver):

    def __init__(self, board: Board):
        super().__init__(board)

    def get_cell(self):
        return self.board.find_empty_cell()

    def get_vals_for_cell(self, row, col):
        return self.board.valid_nums

    def do_move(self, row, col, num, setting_num=True):
        if setting_num:
            self.board.apply_move(row, col, num)
            self.record_step((row, col, num))
        else:
            self.board.apply_move(row, col, 0)
            self.record_step((row, col, 0))


class LegalValuesParent(Solver):

    def __init__(self, board: Board):
        super().__init__(board)
        self.legal_values = dict()
        self.__init_legal_values()

    def __init_legal_values(self):
        """
        Initializes the legal_values dictionary
        At first, each empty cell can have all nums; each non-empty cell can have no nums
        """
        for row in range(self.board.height):
            for col in range(self.board.width):
                if self.board.initial_board[row][col] == 0:
                    self.legal_values[(row, col)] = self.board.get_legal_nums_for_cell(row, col)

    def get_vals_for_cell(self, row, col):
        return self.legal_values[(row, col)]

    def get_cell(self):
        return self.board.find_empty_cell()

    def do_move(self, row, col, num, setting_num=True):
        if setting_num:
            self.board.apply_move(row, col, num)
            self.record_step((row, col, num))
        else:
            self.board.apply_move(row, col, 0)
            self.record_step((row, col, 0))
        self.update_legal_values(row, col, num, setting_num)

    def update_legal_values(self, row, col, num, removing=True):
        """
        Updates the legal_values dict. If removing is set to True, that means we just placed a number on the board. If removing is
        set to False, that means we just reset the cell
        :param row: The row of the cell
        :param col: The column of the cell
        :param num: The number placed in the cell
        :param removing: Boolean if we are setting{=True} or resetting{=False} the cell
        """

        # Update legal values for the current cell
        if removing:
            self.legal_values.pop((row, col), None)
        else:
            self.legal_values[(row, col)] = [num]

        # Update legal values for all other cells in the same row
        for other_col in range(self.board.width):
            if other_col != col:
                vals = self.board.get_legal_nums_for_cell(row, other_col)
                if len(vals) == 0:
                    self.legal_values.pop((row, other_col), None)
                else:
                    self.legal_values[(row, other_col)] = vals

        # Update legal values for all other cells in the same column
        for other_row in range(self.board.height):
            if other_row != row:
                vals = self.board.get_legal_nums_for_cell(other_row, col)
                if len(vals) == 0:
                    self.legal_values.pop((other_row, col), None)
                else:
                    self.legal_values[(other_row, col)] = vals

        # Update legal values for all other cells in the same mini box that are not in the same row or col
        width_mini = col // self.board.mini_box_width
        height_mini = row // self.board.mini_box_height

        for other_row in range(self.board.mini_box_height * height_mini, (self.board.mini_box_height + 1) * height_mini + 1):
            for other_col in range(self.board.mini_box_width * width_mini, (self.board.mini_box_width + 1) * width_mini + 1):
                if other_col != col and other_row != row:

                    vals = self.board.get_legal_nums_for_cell(other_row, other_col)
                    if len(vals) == 0:
                        self.legal_values.pop((other_row, other_col), None)
                    else:
                        self.legal_values[(other_row, other_col)] = vals


class MinimumRemainingValuesSolver(LegalValuesParent):

    def __init__(self, board):
        super().__init__(board)

    def get_cell(self):
        """Given the current state of the board, returns the (row, col) pair with the minimum remaining number of possible values"""
        min_cell = self.board.ERROR, self.board.ERROR
        min_value = float('inf')
        for cell in self.legal_values.keys():
            if len(self.legal_values[cell]) < min_value:
                min_value = len(self.legal_values[cell])
                min_cell = cell
        check_row, check_col = self.board.find_empty_cell()
        if min_cell[0] == self.board.ERROR and check_row != self.board.ERROR:
            return check_row, check_col
        return min_cell


class LeastConstrainingValueSolver(LegalValuesParent):
    """
    This Solver uses the Least Constraining Value to determine which value to try next.
    The heuristic chooses the value that rules out the fewest values in the remaining variables
    """

    def __init__(self, board):
        super().__init__(board)

    def get_vals_for_cell(self, row, col):
        if (row, col) not in self.legal_values:
            return []
        legal_vals = self.legal_values[(row, col)]
        min_heap = PriorityQueue()

        for num in legal_vals:
            count = 0

            # Count the number of cells in the same row that this num can be placed in
            for other_col in range(self.board.width):
                if other_col != col and (row, other_col) in self.legal_values and num in self.legal_values[(row, other_col)]:  # If the number we are assigning to (row, col) could have been assigned to (row, other_col)
                    count += 1

            # Count the number of cells in the same column that this num can be placed in
            for other_row in range(self.board.height):
                if other_row != row and (other_row, col) in self.legal_values and num in self.legal_values[(other_row, col)]:  # If the number we are assigning to (row, col) could have been assigned to (other_row, col)
                    count += 1

            # Count the number of cells in the same mini box that this num can be placed in
            width_mini = col // self.board.mini_box_width
            height_mini = row // self.board.mini_box_height

            for other_row in range(self.board.mini_box_height * height_mini, (self.board.mini_box_height + 1) * height_mini + 1):
                for other_col in range(self.board.mini_box_width * width_mini, (self.board.mini_box_width + 1) * width_mini + 1):
                    if other_col != col and other_row != row and (other_row, other_col) in self.legal_values and num in self.legal_values[(other_row, other_col)]:  # If the number we are assigning to (row, col) could have been assigned to (other_row, other_col)
                        count += 1

            min_heap.push(num, count)

        return min_heap.get_sorted_list()


class ForwardCheckingSolver(LegalValuesParent):
    """
    This Solver will use forward checking in order to detect failed constraints
    early. It does so by keeping track of all legal values for each cell at all
    times. When it detects that a move in one cell will eliminate all remaining
    possible values in another cell, it will skip that value.
    """

    def __init__(self, board: Board):
        super().__init__(board)


    # def get_vals_for_cell(self, row, col):
    #     values = self.legal_values[(row, col)]
    #     output = []
    #     for value in values:
    #         for _row in range(self.board.height):
    #             for _col in range(self.board.width):
    #                 if self.board.board[_row][_col] == 0 and (_row, _col) not in self.legal_values:

    def solve_board_helper(self):
        row, col = self.get_cell()
        if row == self.board.ERROR:  # If there are no more empty cells
            return True
        for num in self.get_vals_for_cell(row, col):
            if self.board.is_legal(row, col, num) and self.original_board.board[row][col] == 0:
                if not self.do_move(row, col, num):
                    continue
                # print(f'Row={row}, Col={col}, Num={num}, Setting_num=True')

                if self.solve_board_helper():
                    return True

                # print(f'Row={row}, Col={col}, Num={num}, Setting_num=False')
                self.do_move(row, col, num, setting_num=False)

    def do_move(self, row, col, num, setting_num=True):
        if not setting_num:
            self.board.apply_move(row, col, 0)
            self.record_step((row, col, 0))
        else:
            self.board.apply_move(row, col, num)
            self.update_legal_values(row, col, num, setting_num)

            proceed = True
            if num != 0:
                for _row in range(self.board.height):
                    for _col in range(self.board.width):
                        if self.board.board[_row][_col] == 0 and (_row, _col) not in self.legal_values:
                            proceed = False
                            break
                    if not proceed:
                        break
            if proceed:
                self.record_step((row, col, num))
            else:
                self.board.apply_move(row, col, 0)
                self.update_legal_values(row, col, num, removing=False)
                self.record_step((row, col, 0))
            return proceed
    #
    # def get_vals_for_cell(self, row, col):
    #     if (row, col) not in self.legal_values:
    #         return []
    #     output_vals = self.legal_values[(row, col)]
    #     output = []
    #     for val in output_vals:
    #         valid_num = True
    #
    #         for _row in range(self.board.height):
    #             if row != _row and (_row, col) in self.legal_values:
    #                 values = self.legal_values[(_row, col)]
    #                 if len(values) == 1 and val in values:
    #                     valid_num = False
    #                     break
    #
    #         if valid_num:
    #             for _col in range(self.board.width):
    #                 if col != _col and (row, _col) in self.legal_values:
    #                     values = self.legal_values[(row, _col)]
    #                     if len(values) == 1 and val in values:
    #                         valid_num = False
    #                         break
    #
    #         if valid_num:
    #             width_mini = col // self.board.mini_box_width
    #             height_mini = row // self.board.mini_box_height
    #
    #             for other_row in range(self.board.mini_box_height * height_mini, (self.board.mini_box_height + 1) * height_mini + 1):
    #                 for other_col in range(self.board.mini_box_width * width_mini, (self.board.mini_box_width + 1) * width_mini + 1):
    #                     if other_col != col and other_row != row and (other_row, other_col) in self.legal_values:
    #                         values = self.legal_values[(other_row, other_col)]
    #                         if len(values) == 1 and val in values:
    #                             valid_num = False
    #                             break
    #
    #         if valid_num:
    #             output.append(val)
    #
    #     return output


def get_solver(solver_name, board):
    """Given the string input representing the name of the solver, return the Solver object"""
    if solver_name == Solver.BACKTRACKING_SOLVER:
        return BacktrackingSolver(board)
    elif solver_name == Solver.MRV_SOLVER:
        return MinimumRemainingValuesSolver(board)
    elif solver_name == Solver.LCV_SOLVER:
        return LeastConstrainingValueSolver(board)
    elif solver_name == Solver.FORWARD_CHECKING_SOLVER:
        return ForwardCheckingSolver(board)


if __name__ == '__main__':
    board = Board()
    # solver = get_solver(Solver.BACKTRACKING_SOLVER, board)
    # solver = get_solver(Solver.LCV_SOLVER, board)
    # solver = get_solver(Solver.MRV_SOLVER, board)
    solver = get_solver(Solver.FORWARD_CHECKING_SOLVER, board)

    solved_board = solver.solve_board()
    print(f'Solved Board:\n{solved_board}')
    print(f'Solved in {solver.get_time_used_to_solve()} seconds')
    print(f'Successfully solved = {solver.was_solved()}')
    print(f'Steps taken were \n{solver.get_steps()}')
    print(f'Number of steps taken were {len(solver.get_steps())}')

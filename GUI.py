from copy import deepcopy

import pygame as pg
from Solvers import BacktrackingSolver, MinimumRemainingValuesSolver


class GUI:
    TITLE_MESSAGE = 'Sudoku'
    WINDOW_SIZE = (570, 460)
    CELL_BG_COLOR = (0, 0, 0)
    CELL_CLICKED_COLOR = (208, 208, 208)
    CHECK_BOARD_COLOR = (153, 204, 255)
    SOLVER_COLOR = (255, 153, 51)
    SQUARE_SIZE = 50
    DIVIDER_SIZE = 5
    FPS = 30
    VALID_NUMS = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_BACKSPACE]
    ARROW_KEYS = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]

    def __init__(self, board):
        pg.init()
        self.window = pg.display.set_mode(GUI.WINDOW_SIZE)
        pg.display.set_caption(GUI.TITLE_MESSAGE)
        self.clock = pg.time.Clock()

        self.board = board
        self.height, self.width = self.board.height, self.board.width
        self.playing = True
        self.won = False
        self.wrong = False
        self.cells = []
        self.highlighted_cell = None
        self.check_button = None
        self.backtracking_button = None
        self.mrv_button = None
        self.board_solution = self.get_solution()
        # print(self.board_solution)

    def run_game(self):
        """Manages the logic of the game"""
        pg.event.clear()
        self.draw_all(init=True)
        expecting_input = False

        while self.playing:

            self.clock.tick(GUI.FPS)
            event = pg.event.wait()
            if event.type == pg.QUIT:
                self.playing = False

            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                clicked_cell = [cell for cell in self.cells if cell.collidepoint(pos)]

                if len(clicked_cell) == 1:  # If the user clicked on a cell on the board
                    if clicked_cell[0] == self.highlighted_cell:  # If the user clicked on an already highlighted cell
                        self.highlighted_cell = None
                        expecting_input = False
                    else:  # If the user clicked on a non-highlighted cell
                        self.highlighted_cell = clicked_cell[0]
                        expecting_input = True

                elif self.check_button.collidepoint(pos):  # The user clicked the 'Check Board' button
                    if self.check_board():  # If the board is full and correct
                        self.won = True
                    else:
                        self.wrong = True

                elif self.backtracking_button.collidepoint(pos):  # The user clicked on the 'Backtracking' button
                    self.animate_backtracking_solution()
                    self.won = True

                elif self.mrv_button.collidepoint(pos):  # The user clicked on the 'mrv' button
                    self.animate_mrv_solution()
                    self.won = True

                else:  # If the user clicked on something other than a cell
                    self.highlighted_cell = None
                    expecting_input = False

            elif event.type == pg.KEYDOWN and expecting_input:  # If the user hits a key on the keyboard while a cell is highlighted
                if event.key in GUI.VALID_NUMS:  # If the user hit a number key
                    col, row, *_ = self.highlighted_cell
                    row, col = self.convert_row_col_from_pixel(row, col)
                    self.board.apply_move(row, col, self.convert_pg_number(event.key))
                elif event.key in GUI.ARROW_KEYS:  # If the user hit an arrow key
                    self.move_highlighted_cell(event.key)

            self.draw_all()

        pg.quit()

    def move_highlighted_cell(self, event_key):  # TODO
        """
        Moves the highlighted cell according to the user's input
        :param event_key: A pygame constant representing one of the four arrow keys
        """
        col, row, _x, _y = self.highlighted_cell
        _row, _col = self.convert_row_col_from_pixel(row, col)
        if event_key == pg.K_UP and _row > 0:
            _row = _row - 1
        elif event_key == pg.K_DOWN and _row < self.board.height - 1:
            _row = _row + 1
        elif event_key == pg.K_RIGHT and _col < self.board.width - 1:
            _col = _col + 1
        elif event_key == pg.K_LEFT and _col > 0:
            _col = _col - 1
        row, col = self.convert_row_col_to_pixel(_row, _col)
        self.highlighted_cell = (col, row, _x, _y)

    def check_board(self):
        """Checks the current board against the solution. Will return True iff the current board is both full and correct"""
        for row in range(self.height):
            for col in range(self.width):
                if self.board.board[row][col] != self.board_solution.board[row][col]:
                    return False
        return True

    def general_animation(self, solver):
        solver.solve_board()
        steps = solver.get_steps()

        for row, col, num in steps:
            events = pg.event.get()  # Needs to be here; otherwise, python will think the program crashed because we aren't checking for event inputs
            self.clock.tick(GUI.FPS)
            pixel_row, pixel_col = self.convert_row_col_to_pixel(row, col)
            self.highlighted_cell = (pixel_col, pixel_row, GUI.SQUARE_SIZE, GUI.SQUARE_SIZE)
            self.board.apply_move(row, col, num)
            self.draw_all()
            pg.time.delay(50)

    def animate_backtracking_solution(self):
        """Will solve the board using backtracking and then animate the steps required to find the solution"""
        solver = BacktrackingSolver(deepcopy(self.board))
        self.general_animation(solver)

    def animate_mrv_solution(self):
        """Will solve the board using mrv and then animate the steps required to find the solution"""
        solver = MinimumRemainingValuesSolver(deepcopy(self.board))
        self.general_animation(solver)

    def get_solution(self):
        """Calculates and returns the solution to the board"""
        solver = BacktrackingSolver(deepcopy(self.board))
        return solver.solve_board()

    def convert_row_col_to_pixel(self, row, col):
        """Converts the (row, col) pair from Sudoku board units to pixel units"""
        num_row_dividers = row // self.board.mini_box_height
        _row = GUI.SQUARE_SIZE * row + num_row_dividers * GUI.DIVIDER_SIZE

        num_col_dividers = col // self.board.mini_box_width
        _col = GUI.SQUARE_SIZE * col + num_col_dividers * GUI.DIVIDER_SIZE

        return _row, _col

    def convert_row_col_from_pixel(self, row, col):
        """Converts the (row, col) pair from pixel units to the Sudoku board units"""
        return_row, return_col = 0, 0

        for board_row in range(self.height):
            num_row_dividers = board_row // self.board.mini_box_height
            if GUI.SQUARE_SIZE * board_row + num_row_dividers * GUI.DIVIDER_SIZE == row:
                return_row = board_row

        for board_col in range(self.width):
            num_col_dividers = board_col // self.board.mini_box_width
            if GUI.SQUARE_SIZE * board_col + num_col_dividers * GUI.DIVIDER_SIZE == col:
                return_col = board_col

        return return_row, return_col

    @staticmethod
    def convert_pg_number(num):
        """Converts a Pygame number constant to its corresponding int. Works for 0-9"""
        if num == pg.K_1:
            return 1
        elif num == pg.K_2:
            return 2
        elif num == pg.K_3:
            return 3
        elif num == pg.K_4:
            return 4
        elif num == pg.K_5:
            return 5
        elif num == pg.K_6:
            return 6
        elif num == pg.K_7:
            return 7
        elif num == pg.K_8:
            return 8
        elif num == pg.K_9:
            return 9
        elif num == pg.K_0 or num == pg.K_BACKSPACE:
            return 0

    def draw_grid(self, init=False):
        """Draws the grid onto the window. If drawing for the first time, set init to True"""
        self.window.fill((255, 255, 255))
        for row in range(self.height):
            num_row_dividers = row // self.board.mini_box_height
            for col in range(self.width):
                num_col_dividers = col // self.board.mini_box_width
                cell = pg.draw.rect(
                    self.window,
                    GUI.CELL_BG_COLOR,
                    (GUI.SQUARE_SIZE * col + num_col_dividers * GUI.DIVIDER_SIZE,
                     GUI.SQUARE_SIZE * row + num_row_dividers * GUI.DIVIDER_SIZE,
                     GUI.SQUARE_SIZE,
                     GUI.SQUARE_SIZE),
                    1
                )
                if init:
                    self.cells.append(cell)

    def draw_check_board_button(self):
        """Draws the 'Check Board' button on the right of the board"""
        cell = pg.draw.rect(
            self.window,
            GUI.CHECK_BOARD_COLOR,
            (465, 5, 100, 30)
        )
        self.check_button = cell
        font = pg.font.SysFont('times new roman', 17)
        text = font.render('Check Board', 1, (0, 0, 0))
        self.window.blit(text, (468, 10))

    def draw_backtracking_button(self):
        """Draws the 'Backtracking' button on the right of the board"""
        cell = pg.draw.rect(
            self.window,
            GUI.SOLVER_COLOR,
            (465, 40, 100, 30)
        )
        self.backtracking_button = cell
        font = pg.font.SysFont('times new roman', 17)
        text = font.render('Backtracking', 1, (0, 0, 0))
        self.window.blit(text, (468, 45))

    def draw_mrv_button(self):
        """Draws the 'MRV' button on the right of the board"""
        cell = pg.draw.rect(
            self.window,
            GUI.SOLVER_COLOR,
            (465, 75, 100, 30)
        )
        self.mrv_button = cell
        font = pg.font.SysFont('times new roman', 17)
        text = font.render('MRV', 1, (0, 0, 0))
        self.window.blit(text, (468, 80))

    def draw_numbers(self):
        """Draws the numbers onto the board"""
        font_init_board = pg.font.SysFont('times new roman', 22, bold=True)
        font_user_board = pg.font.SysFont('times new roman', 22)
        text_x_padding = 20
        text_y_padding = 13
        for row in range(self.height):
            num_row_dividers = row // self.board.mini_box_height
            for col in range(self.width):
                num_col_dividers = col // self.board.mini_box_width
                if self.board.board[row][col] != 0:  # If there is a number in the desired cell
                    num_text = font_user_board.render(str(self.board.board[row][col]), 1, (0, 0, 0))
                    if self.board.initial_board[row][col] != 0:  # If that number is part of the original board
                        num_text = font_init_board.render(str(self.board.board[row][col]), 1, (0, 0, 0))
                    self.window.blit(num_text, (GUI.SQUARE_SIZE * col + num_col_dividers * GUI.DIVIDER_SIZE + text_x_padding,
                                                GUI.SQUARE_SIZE * row + num_row_dividers * GUI.DIVIDER_SIZE + text_y_padding))

    def draw_vertical_lines(self):
        """Draws the vertical block lines for the board layout"""
        for col_bar in range(self.board.mini_box_width - 1):
            wid = self.board.mini_box_width * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, 0), (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, GUI.WINDOW_SIZE[0]),
                GUI.DIVIDER_SIZE * 2
            )

    def draw_horizontal_lines(self):
        """Draws the horizontal block lines for the board layout"""
        for row_bar in range(self.board.mini_box_height - 1):
            wid = self.board.mini_box_height * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (0, wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE), (GUI.WINDOW_SIZE[1], wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE),
                GUI.DIVIDER_SIZE * 2
            )

    def draw_highlighted_cell(self):
        """Draws the highlight on the desired cell if a cell should be highlighted"""
        if self.highlighted_cell:
            pg.draw.rect(
                self.window,
                GUI.CELL_CLICKED_COLOR,
                self.highlighted_cell
            )

    def draw_winner_overlay(self):
        """Draws an overlay when the user wins the game"""
        # Draw transparent overlay
        surface = pg.Surface(GUI.WINDOW_SIZE, pg.SRCALPHA)
        surface.fill((255, 255, 255, 170))
        self.window.blit(surface, (0, 0))

        # Draw message
        font = pg.font.SysFont('times new roman', 72)
        text = font.render('You Won!', 1, (0, 0, 0))
        self.window.blit(text, (120, 150))

    def draw_incorrect_board_overlay(self):
        """Draws an overlay on the board when the user wrongly hits the 'check board' button"""
        surface = pg.Surface(GUI.WINDOW_SIZE, pg.SRCALPHA)
        surface.fill((253, 100, 100, 170))
        self.window.blit(surface, (0, 0))

    def draw_all(self, init=False):
        """Draws the graphics onto the window. If drawing for the first time, set init to 'True'"""
        self.draw_grid(init)
        self.draw_highlighted_cell()
        self.draw_vertical_lines()
        self.draw_horizontal_lines()
        self.draw_numbers()
        self.draw_check_board_button()
        self.draw_backtracking_button()
        self.draw_mrv_button()

        # Draw an overlay if applicable
        if self.won:
            self.draw_winner_overlay()
            pg.display.update()
            pg.time.delay(1000)
            self.won = False
        elif self.wrong:
            self.draw_incorrect_board_overlay()
            pg.display.update()
            pg.time.delay(200)
            self.wrong = False

        pg.display.update()

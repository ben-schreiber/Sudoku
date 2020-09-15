import pygame as pg


class GUI:

    TITLE_MESSAGE = 'Sudoku'
    WINDOW_SIZE = (460, 460)
    CELL_BG_COLOR = (0, 0, 0)
    CELL_CLICKED_COLOR = (208, 208, 208)
    SQUARE_SIZE = 50
    DIVIDER_SIZE = 5
    FPS = 30

    def __init__(self, board):
        pg.init()
        self.window = pg.display.set_mode(GUI.WINDOW_SIZE)
        pg.display.set_caption(GUI.TITLE_MESSAGE)
        self.clock = pg.time.Clock()

        self.board = board
        self.height, self.width = self.board.height, self.board.width
        self.playing = True
        self.cells = []
        self.highlighted_cell = None

    def run_game(self):
        """Manages the logic of the game"""
        pg.event.clear()
        self.draw(init=True)
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
                    else:  # If the user clicked on a non-highlighted cell
                        self.highlighted_cell = clicked_cell[0]

            self.draw()

        pg.quit()

    def draw(self, init=False):
        """Draws the graphics onto the window"""
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

        # Highlight a clicked cell if relevant
        if self.highlighted_cell:
            pg.draw.rect(
                self.window,
                GUI.CELL_CLICKED_COLOR,
                self.highlighted_cell
            )

        # Draw the vertical block lines
        for col_bar in range(self.board.mini_box_width - 1):
            wid = self.board.mini_box_width * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, 0), (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, GUI.WINDOW_SIZE[0]),
                GUI.DIVIDER_SIZE * 2
                         )

        # Draw the horizontal block lines
        for row_bar in range(self.board.mini_box_height - 1):
            wid = self.board.mini_box_height * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (0, wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE), (GUI.WINDOW_SIZE[1], wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE),
                GUI.DIVIDER_SIZE * 2
                         )

        # Draw on the numbers to the board
        font_init_board = pg.font.SysFont('arial', 22, bold=True)
        font_user_board = pg.font.SysFont('arial', 22)
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

        pg.display.update()

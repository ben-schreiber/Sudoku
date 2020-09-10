import pygame as pg


class GUI:

    TITLE_MESSAGE = 'Sudoku'
    WINDOW_SIZE = (460, 460)
    CELL_BG_COLOR = (0, 0, 0)
    SQUARE_SIZE = 50
    DIVIDER_SIZE = 5

    def __init__(self, board):
        pg.init()
        self.window = pg.display.set_mode(GUI.WINDOW_SIZE)
        pg.display.set_caption(GUI.TITLE_MESSAGE)
        self.clock = pg.time.Clock()

        self.board = board
        self.height, self.width = self.board.height, self.board.width
        self.playing = True

    def run_game(self):
        """Manages the logic of the game"""
        while self.playing:

            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False

            self.draw()

        pg.quit()

    def draw(self):
        """Draws the graphics onto the window"""
        self.window.fill((255, 255, 255))
        for row in range(self.height):
            for col in range(self.width):
                num_col_dividers = col // self.board.mini_box_width
                num_row_dividers = row // self.board.mini_box_height
                pg.draw.rect(
                    self.window,
                    GUI.CELL_BG_COLOR,
                    (GUI.SQUARE_SIZE * col + num_col_dividers * GUI.DIVIDER_SIZE,
                     GUI.SQUARE_SIZE * row + num_row_dividers * GUI.DIVIDER_SIZE,
                     GUI.SQUARE_SIZE,
                     GUI.SQUARE_SIZE),
                    1
                )

        for col_bar in range(self.board.mini_box_width - 1):
            wid = self.board.mini_box_width * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, 0), (wid * (col_bar + 1) + col_bar * GUI.DIVIDER_SIZE, GUI.WINDOW_SIZE[0]),
                GUI.DIVIDER_SIZE * 2
                         )

        for row_bar in range(self.board.mini_box_height - 1):
            wid = self.board.mini_box_height * GUI.SQUARE_SIZE
            pg.draw.line(
                self.window,
                GUI.CELL_BG_COLOR,
                (0, wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE), (GUI.WINDOW_SIZE[1], wid * (row_bar + 1) + row_bar * GUI.DIVIDER_SIZE),
                GUI.DIVIDER_SIZE * 2
                         )

        pg.display.update()

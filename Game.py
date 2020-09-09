from Board import Board


class Game:

    INPUT_ROW_MSG = 'Please choose a row...'
    INPUT_COL_MSG = 'Please choose a column...'
    INPUT_NUM_MSG = 'Please choose a number...'
    INVALID_ROW_MSG = 'Invalid row choice. Please try again'
    INVALID_COL_MSG = 'Invalid column choice. Please try again'
    INVALID_NUM_MSG = 'Invalid number choice. Please try again'

    def __init__(self, size=(9, 9)):
        self.board = Board(size)

    def __is_valid_input(self, row, col, num):
        """Returns True iff the user_input is a valid input. Does not check for validity of move"""
        output_bool = True
        if row < 1 or row > self.board.height:
            print(Game.INVALID_ROW_MSG)
            output_bool = False
        if col < 1 or col > self.board.width:
            print(Game.INVALID_COL_MSG)
            output_bool = False
        if num not in self.board.valid_nums:
            print(Game.INVALID_NUM_MSG)
            output_bool = False
        return output_bool

    def get_input(self):
        """
        Gets, validates, and returns the user's input. Will keep requesting an input until a valid one is given
        :return : (row, col, num)
        """
        while True:
            row_input = int(input(Game.INPUT_ROW_MSG))
            col_input = int(input(Game.INPUT_COL_MSG))
            num_input = int(input(Game.INPUT_NUM_MSG))
            if self.__is_valid_input(row_input, col_input, num_input):
                return row_input - 1, col_input - 1, num_input

    def one_turn(self):
        """Runs one turn from the user"""
        row, col, num = self.get_input()
        self.board.apply_move(row, col, num)
        print(self.board)

    def run_game_from_cli(self):
        """Runs an entire game to be played from the command line"""
        print(self.board)
        while True:
            self.one_turn()


if __name__ == '__main__':
    game = Game()
    game.run_game_from_cli()
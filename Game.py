from Board import Board


class Game:

    QUIT = 'q'
    INPUT_PROMPT = 'Please provide a "row col num" input or type "q" to quit:\n'
    INVALID_ROW_MSG = 'Invalid row choice. Please try again'
    INVALID_COL_MSG = 'Invalid column choice. Please try again'
    INVALID_NUM_MSG = 'Invalid number choice. Please try again'

    def __init__(self, size=(9, 9)):
        self.board = Board(size)
        self.playing = True

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
        while self.playing:
            user_input = input(Game.INPUT_PROMPT)
            split_input = user_input.split(' ')
            if len(split_input) == 1 and split_input[0].lower() == Game.QUIT:
                print('Ending game...')
                self.playing = False
                return Game.QUIT, None, None
            elif len(split_input) == 3:
                row_input, col_input, num_input = split_input
                row_input, col_input, num_input = int(row_input), int(col_input), int(num_input)
                if self.__is_valid_input(row_input, col_input, num_input):
                    return row_input - 1, col_input - 1, num_input

    def one_turn(self):
        """Runs one turn from the user"""
        row, col, num = self.get_input()
        if row == Game.QUIT:
            return
        self.board.apply_move(row, col, num)
        print(self.board)

    def run_game_from_cli(self):
        """Runs an entire game to be played from the command line"""
        print(self.board)
        while self.playing:
            self.one_turn()


if __name__ == '__main__':
    game = Game()
    game.run_game_from_cli()
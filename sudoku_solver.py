import numpy as np

def donothing():
    pass

def convert_string_to_table(string):
    return np.array([int(i)-1 if int(i)!=0 else None for i in string]).reshape(9,9)


class sudoku():
    """
    Sudoku generator and solver to test the effectivity of an algorithm

    Sudokus are made in the form of 9x9 grids with digits 0-8, where unfilled
    elements are set to None values.
    """
    def __init__(self):
        pass

    
    def create_solved_board(self):
        self.solved_board = np.zeros((9,9))
        base = np.arange(1,10)
        np.random.shuffle(base)

        self.solved_board[0,:] = base
        for i in range(1, 9):
            if i%3 == 0:
                base = np.roll(base, 1)
            else:
                base = np.roll(base, 3)
            self.solved_board[i,:] = base


        return self.solved_board


    def _get_rest_of_cell(self, board, x_in, y_in):
        x = x_in//3*3
        y = y_in//3*3

        cell = board[x:x+3,y:y+3]
        cell[x_in%3,y_in%3] = None

        return cell


    def validate_board(self, board=None):
        if board is None:
            board = self.create_solved_board()

        # Validate shape:
        assert(board.shape==(9,9))

        # Validate rows:
        for i in range(9):
            assert(len(set(board[i,:])) == 9)

        # Validate columns:
        for i in range(9):
            assert(len(set(board[:,i])) == 9)

        # Validate cells:
        for i in range(0,9,3):
            for ii in range(0,9,3):
                cell = board[i:i+3,ii:ii+3]
                assert(len(set(cell.flatten())) == 9)
            

    def solve(self, board_in):
        full_set = set(range(9))
        none_set = set([None])
        possibles_array = board_in.copy()
        board = board_in.copy()

        # First I check that possibles_array contains exclusively sets and None
        for i in range(9):
            for ii in range(9):
                if board[i, ii] is not None:
                    possibles_array[i,ii] = set([board[i,ii]])

        changing = 3
        while changing > 0:
            changing -= 1
            for i in range(9):
                for ii in range(9):
                    if board[i, ii] is not None:
                        possibles_array[i,ii] = set([board[i,ii]])
                        continue
                        # This element is already solved

                    # Check what numbers an element can/cannot have by
                    # looking at its cell, row, and column
                    impossibles = set.union(
                        set(self._get_rest_of_cell(board, i, ii).flatten()),
                        set(board[i,:ii]), set(board[i,ii:]),
                        set(board[:i,ii]), set(board[i:,ii])
                    )

                    possibles = full_set - impossibles - none_set
                    possibles_array[i,ii] = possibles

                    # If there is only one possible input, i.e. 8 impossible
                    # ones, the input is input to the board
                    if len(possibles) == 1:
                        board[i,ii]  = [item for item in possibles][0]
                        changing = 3
        
        return board





if __name__ == "__main__":
    sud = sudoku()

    test_sudoku = np.array((
        (None,    3,    5,         0, None,    8,          1, None, None),
        (None, None,    1,      None,    5,    3,       None, None, None),
        (None, None,    0,         2,    4,    1,          7, None, None),

        (None, None,    7,      None, None, None,       None,    3,    1),
        (None, None,    2,         7, None, None,          4,    6,    8),
        (None,    5,    8,      None, None, None,       None, None, None),

        (   5, None,    6,      None,    8,    7,       None, None, None),
        (None, None, None,      None,    0,    2,       None, None, None),
        (   8,    0, None,         3, None, None,       None, None,    5)
    ))

    solved_board = sud.solve(test_sudoku)
    sud.validate_board(solved_board)
    print(test_sudoku)
    print(solved_board)

    # golden_nugget = np.array((
    #     (None, None, None,      None, None, None,       None,    2,    8),
    #     (None, None, None,      None,    0, None,       None, None,    4),
    #     (None, None,    2,      None, None,    4,          7, None, None),

    #     (None, None,    7,      None, None,    8,       None, None,    5),
    #     (None,    6, None,      None,    1, None,       None, None, None),
    #     (   0, None, None,         3, None, None,       None, None, None),

    #     (None, None,    8,      None, None,    7,       None,    4, None),
    #     (None,    1, None,      None, None, None,          5, None, None),
    #     (   3, None, None,         6, None, None,       None, None, None)
    # ))
    # I wrote this in before writing the conversion function and I want to 
    # keep it for sentimental reasons, lol

    # http://www.sudokusnake.com/goldennugget.php
    golden_nugget = convert_string_to_table("000000039000010005003005800008009006070020000100400000009008050020000600400700000")

    solved_nugget = sud.solve(golden_nugget)
    print(solved_nugget)
    # sud.validate_board(solved_nugget)
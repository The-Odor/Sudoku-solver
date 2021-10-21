import numpy as np

def donothing():
    # Visual Studio Code won't let me put stops on empty lines
    # or pass-lines, so I use this function while debugging
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
        self.full_set = set(range(9))
        self.none_set = set([None])

    
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


    def _get_cell(self, board, x_in, y_in):
        x = x_in//3*3
        y = y_in//3*3

        return board.copy()[x:x+3,y:y+3].flatten()

    def _get_rest_of_cell(self, board, x_in, y_in):
        cell_index = x_in*9 + y_in
        x = x_in//3*3
        y = y_in//3*3

        cell = board.copy()[x:x+3,y:y+3]
        cell = cell.flatten()
        cell = np.concatenate((cell[:cell_index], cell[cell_index+1:]))

        return cell


    def validate_board(self, board=None):
        if board is None:
            board = self.create_solved_board()

        # Validate shape:
        if not (board.shape==(9,9)):
            return False

        # Validate rows:
        for i in range(9):
            if not (len(set(board[i,:])) == 9):
                return False

        # Validate columns:
        for i in range(9):
            if not (len(set(board[:,i])) == 9):
                return False

        # Validate cells:
        for i in range(0,9,3):
            for ii in range(0,9,3):
                cell = board[i:i+3,ii:ii+3]
                if not (len(set(cell.flatten())) == 9):
                    return False

        return True
            

    def pointing_pair(self, board, possibles_board):
        return board, possibles_board
        for iv in range(9):
            # Only intersections between cells and rows/columns
            # need to be checked, as intersections between rows and
            # columns will be caught by method 1.
            row = possibles_array[:,iv]
            col = possibles_array[iv,:]

            # Separated out for readability
            cel_row = [row[3*v:3*(v+1)] for v in range(3)]
            cel_col = [col[3*v:3*(v+1)] for v in range(3)]

            cel_row = [set.union(*cel) for cel in cel_row]
            cel_col = [set.union(*cel) for cel in cel_col]

            for cel_n in range(3):
                for possibility in cel_row[cel_n]:
                    if possibility not in cel_row[cel_n-1] and possibility not in cel_row[cel_n-2]:
                        # possibility can now be safely removed
                        # from rest of cell
                        x = iv//3*3
                        y = cel_n*3
                        cel = possibles_array[x:x+3, y:y+3]


                        # is that you _think_ I'd say, bitch
                        # I have _no_ fucking clue what's happening
                        for x in range(3):
                            for y in range(3):
                                if y == iv%3:
                                    continue
                                if possibility in cel[x,y]:
                                    donothing()
                                # cel[x,y] -= set([possibility])
                                pass


    def _naked_pair_recursion(self, remainder, set_recursive, recursion_layer):
        if len(remainder) == 0:
            return len(set_recursive) == recursion_layer 

        own_set = remainder[0]
        if len(own_set) == 0:
            return False

        for i in range(1, len(remainder)):
            if self._naked_pair_recursion(remainder[i:], own_set + set_recursive, recursion_layer+1)




    def naked_pair(self, board, possibles_array):
        # return board, possibles_array
            
        for group_i in range(9):
            row = possibles_array[:,group_i]
            col = possibles_array[group_i,:]
            cel_ind_1 = group_i//3
            cel_ind_2 = group_i%3
            cel = possibles_array[cel_ind_1, cel_ind_2]

            for i in range(9):
                




    def solve(self, board_in):
        possibles_array = board_in.copy()
        board = board_in.copy()

        # First I check that possibles_array contains exclusively sets and None
        for i in range(9):
            for ii in range(9):
                if board[i, ii] is None:
                    possibles_array[i,ii] = self.full_set
                else:
                    possibles_array[i,ii] = set([board[i,ii]])
                

        changing = 3
        while changing > 0:
            changing -= 1
            for i in range(9):
                for ii in range(9):
                    
                    # ------- Method 1 ------- #
                    # This is already solved
                    if board[i, ii] is not None:
                        possibles_array[i,ii] = set([board[i,ii]])
                        continue
                        # This element is already solved


                    # ------- Method 2 ------- #
                    # Most naive method (other than an element already solved).
                    # Elements are compared against other elements in a group,
                    # and if they are already solved in those groups, they 
                    # cannot be in this element. When only one possibility is
                    # available, the element is solved.
                    impossibles = set.union(
                        set(self._get_rest_of_cell(board, i, ii)),
                        set(board[i,:ii]), set(board[i,ii+1:]),
                        set(board[:i,ii]), set(board[i+1:,ii])
                    )

                    possibles = possibles_array[i,ii] - impossibles - self.none_set
                    possibles_array[i,ii] = possibles

                    if len(possibles) == 1:
                        board[i,ii]  = [item for item in possibles][0]
                        changing = 3
                        continue

                    # ------- Method 3 ------- #
                    # If a possible number in an element could not be anywhere 
                    # else within its groups, it must be in this element, hence
                    # solving it
                    cel = self._get_rest_of_cell(possibles_array, i, ii)
                    row = possibles_array[i,:ii], possibles_array[i,ii+1:]
                    col = possibles_array[:i,ii], possibles_array[i+1:,ii]

                    cel = set.union(*cel)
                    row = np.concatenate((np.array([]), *row))
                    row = set.union(*row)
                    col = np.concatenate((np.array([]), *col))
                    col = set.union(*col)

                    # celrowcol = np.concatenate((cel, row, col))
                    celrowcol = set.union(cel, row, col)

                    # A quick temporary sanity check to make sure that
                    # this leaves only one possible solution
                    checkmultiples = False

                    for possibility in possibles:
                        # if possibility not in celrowcol:
                        if possibility not in cel or possibility not in row or possibility not in col:
                            if checkmultiples:
                                pass
                                # raise Exception("Method 3 is is not uniquely determined")
                            checkmultiples = True

                            board[i,ii] = possibility
                            possibles_array[i,ii] = set([possibility])
                            changing = 3
                            continue

                    
                    if changing > 1:
                        # The following methods are slower and are to be run
                        # only when required to. I don't know the game well 
                        # enough to know when to apply these following methods,
                        # nor whether one should be applied before another,
                        # so they all come as a group when methods 1-3 fail.
                        continue


                    # I don't trust the following methods yet


                    # ------- Method 4 ------- #
                    # I believe this method is referred to as "pointing pair".
                    # the method implies that if a possibility is contained
                    # within the intersections of two groups (the elements of a
                    # column contained within a cell for example), but is 
                    # non-overlap area of one of the groups, it can be removed
                    # from the other group.
                    

                    board, possibles_array = self.pointing_pair(board, possibles_array)
                                    
                                    

                    # ------- Method 5 ------- #
                    # I believe this method is referred to as "naked pair",
                    # but I refer to it as "n possibilities within n elements
                    # within a group". If there are n numbers within as many 
                    # elements within a group, then those numbers, of that 
                    # grouping, must be within that section, and can be safely
                    # removed from the remainder of the group.


                    board, possibles_array = self.naked_pair(board, possibles_array)



            for i in range(9):
                for ii in range(9):
                    cel = self._get_cell(possibles_array, i//3, i%3)
                    row = possibles_array[i,:]
                    col = possibles_array[:,i]

                    cel = set.union(*cel)
                    row = set.union(*row)
                    col = set.union(*col)
                    if ii not in cel or ii not in row or ii not in col:
                        print("This board is not solvable")
                        break

                else:
                    continue
                break
            else:
                continue
            break                       

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
    if sud.validate_board(solved_board):
        print("Test sudoku succeeded")
    else:
        print("Test sudoku failed")
    # print(test_sudoku)
    # print(solved_board)

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
    if sud.validate_board(solved_nugget):
        print("Golden Nugget solved")
    else:
        print("Golden Nugget failed")
    

    # Challenges:

    solveThis1 = np.array(( #Just normal strategy to solve so it becomes solved
    ( None,None,4,None,None,6,None,5,None ),
    ( 2,1,None,5,4,None,None,3,None ),
    ( None,None,None,None,None,1,4,None,8 ),
    ( None,None,5,None,None,None,None,1,None ),
    ( None,None,2,4,1,5,6,None,None ),
    ( None,3,None,None,None,None,5,None,None ),
    ( 8,None,0,1,None,None,None,None,None ),
    ( None,2,None,None,5,7,None,6,4 ),
    ( None,4,None,3,None,None,2,None,None )
    ))
    solveThis2 = np.array((  #Needing pointing pair to be solved
    ( None,None,None,None,5,6,3,8,None ),
    ( None,8,None,None,None,None,1,None,5 ),
    ( None,None,None,4,None,None,None,7,None ),
    ( None,None,4,None,None,7,None,None,None ),
    ( 6,None,None,None,8,None,None,None,7 ),
    ( None,None,None,3,None,None,2,None,None ),
    ( None,5,None,None,None,3,None,None,None ),
    ( 4,None,3,None,None,None,None,5,None ),
    ( None,7,2,0,4,None,None,None,None )
    ))
    solveThis3 = np.array(( #Unsolvable Sudoku 
    ( 0,6,2,7,None,None,8,4,None ),
    ( 7,None,None,6,4,None,None,None,None ),
    ( None,None,None,None,None,None,None,3,None ),
    ( None,None,None,4,2,None,None,None,None ),
    ( 1,None,None,None,8,None,2,None,None ),
    ( 4,None,5,None,7,None,None,None,None ),
    ( None,None,6,None,None,3,None,None,4 ),
    ( None,5,None,None,1,None,None,None,8 ),
    ( 2,4,None,None,None,None,3,5,None )
    ))
    solveThis4 = np.array(( #Alot of naked pairs
    ( None,7,None,None,8,None,None,2,None ),
    ( None,2,None,None,None,None,None,5,8 ),
    ( 8,None,1,None,5,2,0,4,7 ),
    ( None,1,None,7,None,3,4,8,None ),
    ( 7,4,0,8,None,6,None,3,5 ),
    ( 2,8,3,5,None,4,7,6,None ),
    ( 4,5,2,None,3,None,8,7,6 ),
    ( 1,None,None,None,None,None,None,0,4 ),
    ( None,0,None,None,4,None,None,1,None ),
    ))

    for i, solve_this in enumerate([eval("solveThis"+str(i+1)) for i in range(4)]):
        solved_this = sud.solve(solve_this)
        if sud.validate_board(solved_this):
            print("Challenge {} succeeded".format(i+1))
        else:
            print("Challenge {} failed".format(i+1))
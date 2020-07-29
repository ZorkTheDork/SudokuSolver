''' Takes in a board 2D array array and solves it by recursively
calling itself, placing a number on the board in an empty cell. 
Backtracks to available changes to continue to solve it. Returns 
True when board is solved, false otherwise. '''
def solve(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    else:
        row, col = empty_cell

    for i in range(9):
        if check_board(board, i+1, (row, col)):
            board[row][col] = i+1

            if solve(board):
                return True

            board[row][col] = 0

    return False

''' Takes in the board 2D array, the number to be checked, and
 the position it is to be placed on the board. Checks the sudoku 
 board to make sure none of the rules have been broken. 
 Returns False when a rule is broken, and True if rules 
are still being met. '''
def check_board(board, num, pos):
    # Check row
    for i in range(9):
        if board[pos[0]][i] == num and (pos[0], i) != pos:
            return False

    # Check column
    for i in range(9):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

''' Runs through the board 2D array and finds an empty cell. 
 If an empty cell is found, the position on the board is returned,
 or None is returned if there are no more empty cells.'''
def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

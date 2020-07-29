from solver import check_board, find_empty_cell, solve
from copy import deepcopy
from sys import exit
import pygame
import time
import random
pygame.init()

BOARD_SIZE = 9
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_RED = (255, 0, 0)
C_GREEN = (34, 139, 34)
C_PURPLE = (186,85,211)
C_GREY = (128, 128, 128)

'''
Randomly generates a valid sudoku board to be passed to the GUI.
Returns the board.
'''
def generate_board():
    #return breaks the infinite loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if random.randint(1,10) >= 5: #Add in a difficulty 
                    board[i][j] = random.randint(1, BOARD_SIZE)
                    if check_board(board, board[i][j], (i, j)):
                        continue
                    else:
                        board[i][j] = 0
        partialBoard = deepcopy(board) #copy of board so solve doesn't modify it
        if solve(board):
            return partialBoard

class Board:
    ''' Board class to contain the 2D array representation of the board,
    a copy of the solved version of the board, the tiles for the GUI and
    the GUI window'''
    def __init__(self, window):
        self.board = generate_board()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        self.window = window

    ''' Board method that draws the lines and tiles of the board onto the window '''
    def draw_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                #vertical lines
                if j%3 == 0 and j != 0:
                    pygame.draw.line(self.window, C_BLACK, ((j//3)*180, 0), ((j//3)*180, 540), 4)

                #horizontal lines
                if i%3 == 0 and i != 0:
                    pygame.draw.line(self.window, C_BLACK, (0, (i//3)*180), (540, (i//3)*180), 4)

                self.tiles[i][j].draw_tile(C_BLACK, 1)

                #only display numbers 1-9, dont display 0
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display_value(self.tiles[i][j].value, (21+(j*60), (16+(i*60))), C_BLACK)
        #footer line        
        pygame.draw.line(self.window, C_BLACK, (0, ((i+1)//3)*180), (540, ((i+1)//3)*180), 4)

    ''' Board method that deselects a tile on the board '''
    def deselect(self, tile):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    ''' Board method that redraws the board to show correct, incorrect,
    selected tiles, as well as the time and number of wrong guesses '''
    def redraw(self, keys, wrong, time):
        self.window.fill((255,255,255))
        self.draw_board()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.tiles[j][i].selected:
                    self.tiles[j][i].draw_tile(C_PURPLE, 4)

                elif self.tiles[i][j].correct:
                    self.tiles[j][i].draw_tile(C_GREEN, 4)

                elif self.tiles[i][j].incorrect:
                    self.tiles[j][i].draw_tile(C_RED, 4)

        #displays user entered value until enter key is pressed
        if len(keys) != 0:
            for value in keys:
                self.tiles[value[0]][value[1]].display_value(keys[value], (21+(value[0]*60), (16+(value[1]*60))), C_GREY)

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30)
            text = font.render('X', True, C_RED)
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40)
            text = font.render(str(wrong), True, C_BLACK)
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40)
        text = font.render(str(time), True, C_BLACK)
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    ''' Board method that solves the board on the GUI version
    of the board '''
    def solve_gui(self, wrong, time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        empty = find_empty_cell(self.board)
        if not empty:
            return True

        for num in range(9):
            if check_board(self.board, num+1, (empty[0], empty[1])):
                self.board[empty[0]][empty[1]] = num+1
                self.tiles[empty[0]][empty[1]].value = num+1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(50) #time delay to allow for easy visualization
                self.redraw({}, wrong, time)

                if self.solve_gui(wrong, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(50) #time delay to allow for easy visualization
                self.redraw({}, wrong, time)
            

class Tile:
    ''' Tile Class that contains the value in the tile, 
    the window to be drawn on, the tiles position/size, 
    and if it is selected, correct, or incorrect '''
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    ''' Tile method that draws the tile on the window'''
    def draw_tile(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    ''' Tile method to display the value in the tile'''
    def display_value(self, value, position, color):
        font = pygame.font.SysFont('lato', 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    ''' Tile method that returnss the coordinates of the tile clicked'''
    def tile_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
        return self.selected



def main():
    window = pygame.display.set_mode((540, 590))
    window.fill(C_WHITE)
    pygame.display.set_caption("Sudoku Solver")

    pygame.display.flip()

    wrong = 0
    board = Board(window)
    selected = -1, -1
    keyDict = {}
    running = True
    startTime = time.time()

    while running:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        if board.board == board.solvedBoard:
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    board.tiles[i][j].selected = False
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()                

            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        if board.tiles[i][j].tile_clicked(mousePos):
                            selected = i, j
                            board.deselect(board.tiles[i][j])

            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7
                    
                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]
                        
                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]:
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                break

                            board.tiles[selected[1]][selected[0]].value = keyDict[selected]
                            board.board[selected[1]][selected[0]] = keyDict[selected]
                            del keyDict[selected]

                #start solver
                if event.key == pygame.K_SPACE:
                    for i in range(BOARD_SIZE):
                        for j in range(BOARD_SIZE):
                            board.tiles[i][j].selected = False
                    keyDict = {}
                    board.solve_gui(wrong, passedTime)
                    for i in range(BOARD_SIZE):
                        for j in range(BOARD_SIZE):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    running = False

        board.redraw(keyDict, wrong, passedTime)
    #allows for window to remain until user exits
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

main()
pygame.quit()
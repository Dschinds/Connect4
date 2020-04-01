import numpy as np
import pygame
import sys
import math
import time
ROW_COUNT = 6
COL_COUNT = 7
SQUARE_SIZE = 100
WHITE = (255,255,255)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
RADIUS = int(SQUARE_SIZE / 2.25)
def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def is_valid_location(board,col):
    if col == -1:
        print("Hover over a column and drop a piece")
        return False
    if board[0][col] != 0:
        return False
    else:
        return True

def play_move(board,col,player):
    row = 0
    for row in reversed(range(ROW_COUNT)):
        if board[row][col] == 0:
            board[row][col] = player
            return board, row
    return board, row

def check_win(board,row,col):
    player = board[row][col]
    # Horizonal Check
    count = 1
    idx = col - 1
    while idx >=0 and board[row][idx] == player:
        count += 1
        idx -= 1
    idx = col + 1
    while idx < COL_COUNT and board[row][idx] == player:
        idx += 1
        count += 1
    if count == 4:
        return True
    # Vertical Check
    count = 1
    idx = row - 1
    while idx >= 0 and board[idx][col] == player:
        count += 1
        idx -= 1
    idx = row + 1
    while idx < ROW_COUNT and board[idx][col] == player:
        idx += 1
        count += 1
    if count == 4:
        return True
    #Diagonal top right
    count = 1
    idxrow = row - 1
    idxcol = col - 1
    while idxrow >= 0 and idxcol >= 0 and board[idxrow][idxcol] == player:
        count += 1
        idxrow -= 1
        idxcol -= 1

    idxrow = row + 1
    idxcol = col + 1
    while idxrow < ROW_COUNT and idxcol < COL_COUNT and board[idxrow][idxcol] == player:
        count += 1
        idxrow += 1
        idxcol += 1
    if count == 4:
        return True
    # Diagonal top left
    count = 1
    idxrow = row + 1
    idxcol = col - 1
    while idxrow < ROW_COUNT and idxcol >= 0 and board[idxrow][idxcol] == player:
        count += 1
        idxrow += 1
        idxcol -= 1

    idxrow = row - 1
    idxcol = col + 1
    while idxrow >= 0 and idxcol < COL_COUNT and board[idxrow][idxcol] == player:
        count += 1
        idxrow -= 1
        idxcol += 1
    if count == 4:
        return True
    return False


def draw_board(board):

    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            pygame.draw.rect(screen,BLUE,(col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[row][col] == 0:
                pygame.draw.circle(screen,BLACK,(int(col*SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),RADIUS)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, RED, (
                int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            else:
                pygame.draw.circle(screen, GREEN, (
                int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)

    pygame.display.update()



pygame.init()
width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
size = (width,height)
screen = pygame.display.set_mode(size)


def main():
    board = create_board()
    draw_board(board)
    game_over = False
    starting_player = 0
    turn = starting_player
    excluding = ""
    col = 0
    row = 0
    font = pygame.font.Font(None, 62)
    while not game_over:
        player = turn % 2 + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
                posx = event.pos[0]
                if player == 1:
                    pygame.draw.circle(screen, RED, (
                        posx, int(SQUARE_SIZE / 2)),
                                   RADIUS)
                else:
                    pygame.draw.circle(screen, GREEN, (
                        posx, int(SQUARE_SIZE / 2)),
                                   RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                # Player 1 input
                if turn % 2 == 0:
                    print("Player 1 move, player anywhere from (0-6) excluting {}".format(excluding))
                    posx = event.pos[0]
                    col = math.floor(posx / SQUARE_SIZE)
                    remainder = posx % SQUARE_SIZE
                    if remainder <= 3:
                        col = -1
                    if is_valid_location(board, col):
                        board, row = play_move(board, col, player)
                        draw_board(board)
                        turn += 1
                        if check_win(board, row, col):
                            print("Congrats player {} won ".format(player))
                            game_over = True
                            # If game over is true, draw game over
                            text = font.render("Player {} wins!! Click to play again".format(player), True, WHITE)
                            text_rect = text.get_rect()
                            text_x = screen.get_width() / 2 - text_rect.width / 2
                            text_y = screen.get_height() / 2 - text_rect.height / 2
                            screen.blit(text, [text_x, text_y])
                            pygame.display.update()



                        print(board)
                    else:
                        if col != -1:
                            excluding += "{},".format(col)
                        print("Invalid col pick again excluding {} ".format(excluding))




                else:
                    print("Player   2 move, player anywhere from (0-6) excluting {}".format(excluding))
                    posx = event.pos[0]
                    col = math.floor(posx / SQUARE_SIZE)
                    remainder = posx % SQUARE_SIZE
                    if remainder <= 3:
                        col = -1
                    if is_valid_location(board, col):
                        board, row = play_move(board, col, player)
                        draw_board(board)
                        turn += 1
                        if check_win(board, row, col):
                            print("Congrats player {} won ".format(player))
                            game_over = True
                            text = font.render("Player {} wins!! Click to play again".format(player), True, WHITE)
                            text_rect = text.get_rect()
                            text_x = screen.get_width() / 2 - text_rect.width / 2
                            text_y = screen.get_height() / 2 - text_rect.height / 2
                            screen.blit(text, [text_x, text_y])
                            pygame.display.update()

                        print(board)
                    else:
                        if col != -1:
                            excluding += "{},".format(col)
                        print("Invalid col pick again excluding {} ".format(excluding))

                if game_over:
                    starting_player = (starting_player + 1) % 2
                    waiting = True
                    while waiting:
                        for event1 in pygame.event.get():
                            if event1.type == pygame.QUIT:
                                pygame.quit()
                            if event1.type == pygame.MOUSEBUTTONDOWN:
                                waiting = False
                                game_over = False
                                board = create_board()
                                draw_board(board)
                                turn = starting_player







        #Player 2 input




if __name__ == '__main__':
    main()

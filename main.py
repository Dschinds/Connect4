import numpy as np
import pygame
import sys
import math
import random
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
WINDOW_LENGTH = 4
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
def create_board():
    board = np.zeros((ROW_COUNT,COL_COUNT),dtype=int)
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

def check_win(board,row,col,player):
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


def draw_board(board,screen):

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

def score_move(board,player,row, col):
    #score row
    score = 0
    row_array = board[row]
    if col == int(COL_COUNT / 2) and board[row][col] == player:
        score += 5
    for coliter in range(COL_COUNT - 3):
        if coliter <= col < coliter + 4:
            window = row_array[coliter:coliter+WINDOW_LENGTH]
            score += score_window(window,player)

    #score col

    col_array = board[:,col]
    for rowiter in range(ROW_COUNT -3):
        if rowiter <= row < rowiter + 4:
            window = col_array[rowiter:rowiter + 4]
            score += score_window(window,player)

    #Top right bottom left diagonal
    top_right,index_right, top_left,index_left = extract_diagonals(board,row,col)
    for diagiter in range(len(top_right) - 3):
        if diagiter <= index_right < diagiter + 4:
            window = top_right[diagiter:diagiter + 4]
            score += score_window(window,player)

    #Top left bottom right diagonal
    for diagiter in range(len(top_left) - 3):
        if diagiter <= index_left < diagiter + 4:
            window = top_left[diagiter:diagiter + 4]
            score += score_window(window,player)





    return score
def extract_diagonals(board,row,col):
    top_right = []
    top_left = []
    index_row = row
    index_col = col
    index_top_right = 0
    index_top_left = 0
    #Bottom Left to top right
    while(index_row < ROW_COUNT - 1 and index_col >= 0):
        index_row += 1
        index_col -= 1
    while(index_row >= 0 and index_col < COL_COUNT):
        val = board[index_row][index_col]
        top_right.append(val)
        if(index_row == row and index_col == col):
            index_top_right = len(top_right) - 1
        index_row -= 1
        index_col += 1
    #Bottom Right to top left
    index_row = row
    index_col = col
    while(index_row < ROW_COUNT - 1 and index_col < COL_COUNT - 1):
        index_row += 1
        index_col += 1
    while(index_row >=0 and index_col >=0):
        val = board[index_row][index_col]
        top_left.append(val)
        if (index_row == row and index_col == col):
            index_top_left = len(top_right) - 1
        index_row -= 1
        index_col -= 1
    return top_right,index_top_right, top_left,index_top_left

def score_window(window,player):
    if player == 1:
        opponent = 2
    else:
        opponent = 1
    score = 0
    unique, counts = np.unique(window, return_counts=True)
    count_dict = dict(zip(unique, counts))
    if player in count_dict:
        if EMPTY in count_dict and count_dict[player] == 3 and count_dict[EMPTY] == 1:
            score += 15
        elif EMPTY in count_dict and count_dict[player] == 2 and count_dict[EMPTY] == 2:
            score += 10
        elif opponent in count_dict and count_dict[player] == 1 and count_dict[opponent] == 3:
            score += 100
        elif opponent in count_dict and EMPTY in count_dict and count_dict[EMPTY] == 1 and count_dict[opponent] == 3:
            score -= 100

    return score


def get_valid_cols(board):
    col_array = []
    for col in range(COL_COUNT):
        if(is_valid_location(board,col)):
            col_array.append(col)
    return col_array

def play_best_move(board,player):
    valid_locations = get_valid_cols(board)
    best_score = 0
    move = random.choice(valid_locations)

    for col in valid_locations:
        copy_board = board.copy()
        copy_board, row = play_move(copy_board,col,player)
        score = score_move(copy_board,player,row,col)
        if score > best_score:
            move = col
            best_score = score
    return move
def check_all_winning_moves(board, piece):
    # Check horizontal locations for win
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def score_all_positions(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COL_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 10
    for r in range(len(center_array)- 3):
        window = center_array[r: r + WINDOW_LENGTH]
        score += (score_window(window,piece) * 10)
    ## Score Horizontal
    multiplier = 1
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COL_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += score_window(window, piece) * multiplier
        multiplier = r + 1

    ## Score Vertical
    multiplier = 1
    for c in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += score_window(window, piece) * multiplier
        if(c < COL_COUNT // 2):
            multiplier += 1
        else:
            multiplier -= 1

    ## Score posiive sloped diagonal
    multiplier = 1
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece) * multiplier
        multiplier = r + 1
    multiplier = 1
    for r in range(ROW_COUNT-3):
        for c in range(COL_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += score_window(window, piece) * multiplier
        multiplier = r + 1

    return score



def is_terminal_node(board):
    return check_all_winning_moves(board,PLAYER1) or check_all_winning_moves(board,PLAYER2) or len(get_valid_cols(board)) == 0

def minimax(board,depth,alpha,beta,maximizing_player,current_player):
    if current_player == 1:
        opponent = 2
    else:
        opponent = 1
    valid_locations = get_valid_cols(board)
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if check_all_winning_moves(board,current_player):
                return 100000000000000, None
            elif check_all_winning_moves(board,opponent):
                return -100000000000000000, None
            else:
                return 0, None
        else:
            return score_all_positions(board,current_player), None
    column = random.choice(valid_locations)
    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            board_copy = board.copy()
            board_copy, _ = play_move(board_copy,col,current_player)
            new_score, _ = minimax(board_copy,depth - 1,alpha,beta, False,current_player)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha,value)
            if(beta <= alpha):
                break
        return value, column
    else:
        value = math.inf
        for col in valid_locations:
            board_copy = board.copy()
            board_copy, _ = play_move( board_copy, col, opponent)
            new_score, _ = minimax(board_copy, depth - 1,alpha,beta, True,current_player)
            if(new_score < value):
                value = new_score
                column = col
            beta = min(beta,value)
            if(beta <= alpha):
                break
        return value, column






def main():
    print("Welcome to connect four press 1 for two players 2 for a player and an ai and 3 for 3 ai's")
    game_mode = 0
    while game_mode != 1 and game_mode != 2 and game_mode !=3:
        game_mode = int(input('Enter 1 for two players 2 for a player and ai 3 for two ai\'s: '))
    pygame.init()
    width = COL_COUNT * SQUARE_SIZE
    height = (ROW_COUNT + 1) * SQUARE_SIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    board = create_board()
    draw_board(board,screen)
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
            if event.type == pygame.MOUSEMOTION and game_mode != 3:
                pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
                posx = event.pos[0]
                if player == 1:
                    pygame.draw.circle(screen, RED, (
                        posx, int(SQUARE_SIZE / 2)),
                                   RADIUS)
                elif game_mode == 1:
                    pygame.draw.circle(screen, GREEN, (
                        posx, int(SQUARE_SIZE / 2)),
                                   RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and game_mode != 3:
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
                        draw_board(board,screen)
                        turn += 1
                        if check_win(board, row, col,player):
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




                elif game_mode == 1:
                    print("Player   2 move, player anywhere from (0-6) excluting {}".format(excluding))
                    posx = event.pos[0]
                    col = math.floor(posx / SQUARE_SIZE)
                    remainder = posx % SQUARE_SIZE
                    if remainder <= 3:
                        col = -1
                    if is_valid_location(board, col):
                        board, row = play_move(board, col, player)
                        draw_board(board,screen)
                        turn += 1
                        if check_win(board, row, col,player):
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
        if game_mode == 2 and player == 2:


            score, col = minimax(board,6,-math.inf,math.inf,True, player)
            board,row = play_move(board,col,player)
            draw_board(board,screen)

            if check_win(board, row, col,player):
                print("Congrats ai {} won ".format(player))
                game_over = True
                # If game over is true, draw game over
                text = font.render("AI {} wins!! Click to play again".format(player), True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
                pygame.display.update()
            turn += 1
        if game_mode == 3:
            difficulty = 7

            score, col = minimax(board, difficulty, -math.inf, math.inf, True, player)
            print("Score for player {} is {} with col {}".format(player,score, col))
            board, row = play_move(board, col, player)
            draw_board(board, screen)
            pygame.time.wait(3000)
            if len(get_valid_cols(board)) == 0:
                print("Draw ")
                game_over = True
                text = font.render("Draw click to play again", True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
                pygame.display.update()
            elif check_win(board, row, col, player) :
                print("Congrats ai {} won ".format(player))
                game_over = True
                # If game over is true, draw game over
                text = font.render("AI {} wins!! Click to play again".format(player), True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
                pygame.display.update()
            turn += 1

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
                        draw_board(board,screen)
                        turn = starting_player







        #Player 2 input




if __name__ == '__main__':
    main()

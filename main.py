import numpy
import pygame
import sys
import math
import random

BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

row_number = 6
column_number = 7
board = numpy.zeros((row_number, column_number))
game_over = False
userPiece = 1
AIPiece = -1
EMPTY = 0
WINNING_LENGTH = 4


def random_value():
    temp = random.randrange(0, 100)
    print("temp", temp)
    if temp % 2 == 0:
        return False
    else:
        return True


flip = random_value()


def columnChecker (board, userChoise):
    if userChoise>=0 and userChoise <=6:
        if board[row_number - 1][userChoise] == 0:
            return True
        else:
            return False
    else: return False


def printBoard(board):
    print(numpy.flip(board, 0))


printBoard(board)


def winCheck(board, piece):
    for c in range(column_number-3):
        for r in range(row_number):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(column_number):
        for r in range(row_number-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(column_number-3):
        for r in range(row_number-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    for c in range(column_number-3):
        for r in range(3, row_number):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def get_row_number(board, column):
    for row in range(row_number):
        if board[row][column] == 0:
            return row


def get_column_number(board):
    valid_column = []
    for c in range(column_number):
        if columnChecker(board, c):
            valid_column.append(c)
    return valid_column


def evaluate_window(window, piece):
    score = 0
    opponent = userPiece
    if piece == userPiece:
        opponent = AIPiece
    if window.count(piece) == 4:
        score += 1000000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4
    if window.count(opponent) == 4:
        score -= 100000
    elif window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 8

    return score


def score_position(board, piece):

    score = 0

    center = [int(i) for i in list(board[:, column_number//2])]
    center_count = center.count(piece)
    score += center_count * 6

    for r in range(row_number):
        row = [int(i) for i in list(board[r, :])]
        for c in range(column_number-3):
            window = row[c:c+WINNING_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(column_number):
        column = [int(i) for i in list(board[:, c])]
        for r in range(row_number-3):
            window = column[r:r+WINNING_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(row_number-3):
        for c in range(column_number-3):
            window = [board[r+i][c+i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(row_number-3):
        for c in range(column_number-3):
            window = [board[r+3-i][c+i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_leaf_node(board):
    return winCheck(board, userPiece) or winCheck(board, AIPiece) or len(get_column_number(board)) == 0


def minimax(board, depth, alpha, beta, maximizing_value):
    valid_column = get_column_number(board)
    is_leaf = is_leaf_node(board)
    if depth == 0 or is_leaf:
        return None, score_position(board, AIPiece)

    if maximizing_value:
        value = -math.inf
        column = random.choice(valid_column)
        for col in valid_column:
            row = get_row_number(board, col)
            temp_board = board.copy()
            temp_board[row][col] = AIPiece
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_column)
        for col in valid_column:
            row = get_row_number(board, col)
            temp_board = board.copy()
            temp_board[row][col] = userPiece
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


SQUARE_SIZE = 100
width = column_number * SQUARE_SIZE
height = (row_number+1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)


def draw_board(board):
    for c in range(column_number):
        for r in range(row_number):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def checkDraw(board):
    print("check_draw!!")
    for c in range(column_number-1):
        for r in range(row_number-1):
            if board[c][r] == 0:
                return False
    return True


pygame.init()
tempBoard = numpy.flip(board, 0)
draw_board(tempBoard)
pygame.display.update()

gameFont = pygame.font.SysFont("monospace", 60)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if flip:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            if flip:
                posx = event.pos[0]
                userChoise = int(math.floor(posx / SQUARE_SIZE))
                if columnChecker(board, userChoise):
                    for i in range(row_number):
                        if board[i][userChoise] == 0:
                            board[i][userChoise] = userPiece
                            break
                else: continue

                if winCheck(board, 1):
                    label = gameFont.render("Player Win!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                elif checkDraw(board):
                    label = gameFont.render("Draw!!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over = True

                flip = False

                tempBoard = numpy.flip(board, 0)
                draw_board(tempBoard)
                printBoard(board)

    if not flip and not game_over:
        # userChoise= best_move(board, AIPiece)
        userChoise, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
        print("userChoice : ", userChoise)
        print("minimax value: ", minimax_score)
        if columnChecker(board, userChoise):
            for i in range(row_number):
                if board[i][userChoise] == 0:
                    board[i][userChoise] = AIPiece
                    break
        else:
            continue

        if winCheck(board, -1):
            label = gameFont.render("AI Win!!", 1, YELLOW)
            screen.blit(label, (40, 10))
            game_over = True

        elif checkDraw(board):
            label = gameFont.render("Draw!!", 1, BLUE)
            screen.blit(label, (40, 10))
            game_over = True

        flip = True

        tempBoard = numpy.flip(board, 0)
        draw_board(tempBoard)
        printBoard(board)

    if game_over:
        pygame.time.wait(3000)




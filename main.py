import numpy
import pygame
import sys
import math
import random
from pygame.locals import *

# define colours
BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
bg_color = (178, 190, 181)


row_number = 6
column_number = 7
board = numpy.zeros((row_number, column_number))
userPiece = 1
AIPiece = -1
EMPTY = 0
WINNING_LENGTH = 4

pygame.init()
pygame.display.set_caption('Connect Four')

# font for button
font = pygame.font.SysFont('Constantia', 30)

# define global variable
clicked = False


class Button:

    # colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = BLACK
    width = 200
    height = 80

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action

# chose turn
def random_value():
    temp = random.randrange(0, 100)
    print("temp", temp)
    if temp % 2 == 0:
        return False
    else:
        return True


# assign the turn value
flip = random_value()


# check valid column to drop the disk
def columnChecker (board, userChoise):
    if userChoise>=0 and userChoise <=6:
        if board[row_number - 1][userChoise] == 0:
            return True
        else:
            return False
    else: return False


# reverse the array
def printBoard(board):
    print(numpy.flip(board, 0))


# check draw
def checkDraw(board):
    print("check_draw!!")
    for c in range(column_number-1):
        for r in range(row_number-1):
            if board[c][r] == 0:
                return False
    return True


# check win
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


# get the row of a specific column
def get_row_number(board, column):
    for row in range(row_number):
        if board[row][column] == 0:
            return row


# get the valid column array where player can drop the disk
def get_column_number(board):
    valid_column = []
    for c in range(column_number):
        if columnChecker(board, c):
            valid_column.append(c)
    return valid_column


# Evaluation function
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


# calculate total score for an specific node of the tree
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


# check win or draw
def is_leaf_node(board):
    return winCheck(board, userPiece) or winCheck(board, AIPiece) or len(get_column_number(board)) == 0


# minimax function with alpha beta pruning
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


# screen variable
SQUARE_SIZE = 100
width = column_number * SQUARE_SIZE
height = (row_number+1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)


# drawing the board
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


# font for the game board
gameFont = pygame.font.SysFont("monospace", 60)
textFont = pygame.font.SysFont("monospace", 20)
is_home_page = True
is_level_selection = False
game_over = True
game_over_2 = True

# Defined button for home page
single = Button(250, 250, 'Single Player')
double = Button(250, 400, 'Two Player')

# Home page
while is_home_page:
    screen.fill(bg_color)

    if single.draw_button():
        is_level_selection = True
        is_home_page = False

    if double.draw_button():
        screen.fill(BLACK)
        game_over_2 = False
        is_home_page = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()

# depth of game tree
depth = 0


# Defined button for level selection
easy = Button(250, 200, 'Easy')
medium = Button(250, 300, 'Medium')
hard = Button(250, 400, 'Hard')

# Level selection
while is_level_selection:

    screen.fill(bg_color)

    if easy.draw_button():
        screen.fill(BLACK)
        depth = 1
        game_over = False
        is_level_selection = False

    if medium.draw_button():
        screen.fill(BLACK)  # for gui
        depth = 3
        game_over = False
        is_level_selection = False

    if hard.draw_button():
        screen.fill(BLACK)  # for gui
        depth = 5
        game_over = False
        is_level_selection = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()


# Playing against AI
while not game_over:
    # showing turn
    tempBoard = numpy.flip(board, 0)
    draw_board(tempBoard)
    if flip:
        label = textFont.render("Your turn", 1, RED)
        screen.blit(label, (550, 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if flip:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                label = textFont.render("Your turn", 1, RED)
                screen.blit(label, (550, 10))
            else:
                label = textFont.render("AI turn", 1, YELLOW)
                screen.blit(label, (550, 10))
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
        # showing turn
        label = textFont.render("AI turn", 1, YELLOW)
        screen.blit(label, (550, 10))
        pygame.display.update()

        # minimax function call
        userChoise, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
        print("userChoice : ", userChoise)
        print("minimax value: ", minimax_score)

        # delay according to the level
        if depth == 1:
            pygame.time.wait(1000)
        elif depth == 3:
            pygame.time.wait(800)

        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
        pygame.display.update()

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

    pygame.display.update()

    if game_over:
        pygame.time.wait(3000)


# Two player game
while not game_over_2:
    tempBoard = numpy.flip(board, 0)
    draw_board(tempBoard)
    if flip:
        label = textFont.render("Player 1 turn", 1, RED)
        screen.blit(label, (500, 10))
    else:
        label = textFont.render("Player 2 turn", 1, YELLOW)
        screen.blit(label, (500, 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if flip:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                label = textFont.render("Player 1 turn", 1, RED)
                screen.blit(label, (500, 10))
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                label = textFont.render("Player 2 turn", 1, YELLOW)
                screen.blit(label, (500, 10))
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

                if winCheck(board, userPiece):
                    label = gameFont.render("Player 1 Win!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over_2 = True

                elif checkDraw(board):
                    label = gameFont.render("Draw!!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over_2 = True

                flip = False

                tempBoard = numpy.flip(board, 0)
                draw_board(tempBoard)
                printBoard(board)

            else:
                posx = event.pos[0]
                userChoise = int(math.floor(posx / SQUARE_SIZE))
                if columnChecker(board, userChoise):
                    for i in range(row_number):
                        if board[i][userChoise] == 0:
                            board[i][userChoise] = AIPiece
                            break
                else: continue

                if winCheck(board, AIPiece):
                    label = gameFont.render("Player 2 Win!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over_2 = True

                elif checkDraw(board):
                    label = gameFont.render("Draw!!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    game_over_2 = True

                flip = True

                tempBoard = numpy.flip(board, 0)
                draw_board(tempBoard)
                printBoard(board)
        pygame.display.update()

    if game_over_2:
        pygame.time.wait(3000)




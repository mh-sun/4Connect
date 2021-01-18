import numpy
import pygame
import sys
import math
import random

BLUE = (135, 206, 235)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

row_number = 6
column_number = 7
board = numpy.zeros((row_number, column_number))
game_over = False
flip = True
userPiece = 1
AIPiece = -1


def columnChecker (board, userChoise):
    if userChoise>=0 and userChoise <=7 :
        if  board[row_number - 1][userChoise] == 0 :
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


SQUARESIZE = 100
width = column_number * SQUARESIZE
height = (row_number+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)


def draw_board(board):
    for c in range(column_number):
        for r in range(row_number):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
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
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if flip:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
            if flip:
                posx = event.pos[0]
                userChoise = int(math.floor(posx/SQUARESIZE))
                if columnChecker(board, userChoise) :
                    for i in range(6):
                        if board[i][userChoise] == 0:
                                board[i][userChoise] = userPiece
                                break
                else: continue
                if winCheck(board, 1):
                    label = gameFont.render("Player 1 Win!!", 1, RED)
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
            userChoise= random.randrange(0,7)
            print("userChoice : ",userChoise)
            if columnChecker(board, userChoise):
                pygame.time.wait(500)
                for i in range(6):
                    if board[i][userChoise] == 0:
                        board[i][userChoise] = AIPiece
                        break
            else:
                continue
            if winCheck(board, -1):
                label = gameFont.render("Player 2 Win!!", 1, YELLOW)
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
        pygame.time.wait(5000)



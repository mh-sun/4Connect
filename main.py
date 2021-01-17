import numpy

row_number=6
colomn_number=7
board = numpy.zeros((row_number,colomn_number))
game_over=False
flip=True
userPiece=1
AIPiece=-1

def colomnChecker(board,userChoise):
    if(board[row_number-1][userChoise]==0):
        return True
    else:return False

def printBoard(board):
    tempboard=numpy.zeros((row_number,colomn_number))
    for i in range(6):
        for j in range(7):
            tempboard[i][j]=board[5-i][j]
    print(tempboard)


printBoard(board)
while not game_over:
    if(flip):
        userChoise=int(input())-1
        if(colomnChecker(board,userChoise)):
            for i in range(6):
                if(board[i][userChoise]==0):
                    board[i][userChoise]=userPiece
                    break
        else:pass

        flip=False
    else:
        userChoise = int(input())-1
        if (colomnChecker(board, userChoise)):
            for i in range(6):
                if (board[i][userChoise] == 0):
                    board[i][userChoise] = AIPiece
                    break

        flip =True
    printBoard(board)





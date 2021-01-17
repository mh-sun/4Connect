import numpy

row_number=6
colomn_number=7
board = numpy.zeros((row_number,colomn_number))

game_over=False

while not game_over:
    userChoise=int(input())
    print(userChoise)
    print(type(userChoise))
print(board)

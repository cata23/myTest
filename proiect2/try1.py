import pygame
from pygame.locals import *

# declare our global variables for the game
XO = "X"  # track whose turn it is; X goes first
grid = [[None, None, None],
        [None, None, None],
        [None, None, None]]

winner = None

lastRow = None
lastCol = None


# initialize the board and return it as a variable
# ttt - display mode (width and high)
def initBoard(ttt):
    # set up the background surface
    background = pygame.Surface(ttt.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # draw the grid lines
    # vertical lines
    pygame.draw.line(background, (0, 0, 0), (0, 0), (0, 300), 2)
    pygame.draw.line(background, (0, 0, 0), (298, 0), (298, 300), 2)
    pygame.draw.line(background, (0, 0, 0), (100, 0), (100, 300), 2)
    pygame.draw.line(background, (0, 0, 0), (200, 0), (200, 300), 2)

    # horizontal lines
    pygame.draw.line(background, (0, 0, 0), (0, 0), (300, 0), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 298), (300, 298), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 100), (300, 100), 2)
    pygame.draw.line(background, (0, 0, 0), (0, 200), (300, 200), 2)

    # return the board
    return background


# draw position
# enable - True  -> draw red square
#        - False -> draw white square
def drawPosition(board, boardRow, boardCol, enable):
    if boardRow is not None and boardCol is not None:
        # determinate the square
        startPointX = ((boardCol) * 100)
        startPointY = ((boardRow) * 100)

        color = None
        red = (255, 0, 0)
        white = (255, 255, 255)

        if enable:
            color = red
        else:
            color = white

        # vertical lines
        pygame.draw.line(board, color, (startPointX + 2, startPointY + 2), (startPointX + 2, startPointY + 100 - 2), 2)
        pygame.draw.line(board, color, (startPointX + 100 - 2, startPointY + 2),
                         (startPointX + 100 - 2, startPointY + 100 + 2), 2)

        # horizontal lines
        # red
        pygame.draw.line(board, color, (startPointX + 2, startPointY + 2),
                         (startPointX + 100 - 2, startPointY + 2), 2)
        pygame.draw.line(board, color, (startPointX + 2, startPointY + 100 - 2),
                         (startPointX + 100 - 2, startPointY + 100 - 2), 2)


# draw the status (i.e., player turn, etc) at the bottom of the board
# board : the initialized game board surface where the status will
def drawStatus(board):
    # get access to global variables
    global XO, winner

    # determine the status message
    if winner is None:
        message = XO + "'s turn"
    else:
        message = winner + " won!"

    # render the status message
    font = pygame.font.Font(None, 24)
    text = font.render(message, 1, (10, 10, 10))

    # copy the rendered message onto the board
    board.fill((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (10, 300))


# redraw the game board on the display
def showBoard(ttt, board):
    drawStatus(board)
    ttt.blit(board, (0, 0))
    pygame.display.flip()


# given a set of coordinates from the mouse, determine which board space
def boardPos(mouseX, mouseY):
    # determine the row the user clicked
    if mouseY < 100:
        row = 0
    elif mouseY < 200:
        row = 1
    else:
        row = 2

    # determine the column the user clicked
    if mouseX < 100:
        col = 0
    elif mouseX < 200:
        col = 1
    else:
        col = 2

    # return the pair containing the row & column
    return row, col


# draw an X or O on the board in boardRow, boardCol
def drawMove(board, boardRow, boardCol, Piece):
    if winner is None:
        global lastRow, lastCol

        # determine the center of the square
        centerX = (boardCol * 100) + 50
        centerY = (boardRow * 100) + 50

        # draw the appropriate piece
        if Piece == 'O':
            pygame.draw.circle(board, (0, 0, 0), (centerX, centerY), 44, 2)
        else:
            pygame.draw.line(board, (0, 0, 0), (centerX - 22, centerY - 22), \
                             (centerX + 22, centerY + 22), 2)
            pygame.draw.line(board, (0, 0, 0), (centerX + 22, centerY - 22), \
                             (centerX - 22, centerY + 22), 2)

        # delete last position
        drawPosition(board, lastRow, lastCol, False)
        # draw new position
        drawPosition(board, boardRow, boardCol, True)

        lastRow = boardRow
        lastCol = boardCol
        # mark the space as used
        grid[boardRow][boardCol] = Piece


# determine where the user clicked and if the space is not already
def clickBoard(board):
    # get access to global variable
    global grid, XO

    (mouseX, mouseY) = pygame.mouse.get_pos()
    (row, col) = boardPos(mouseX, mouseY)

    # make sure no one's used this space
    if (grid[row][col] == "X") or (grid[row][col] == "O"):
        # this space is in use
        return

    # draw an X or O
    drawMove(board, row, col, XO)

    # next player
    if (XO == "X"):
        XO = "O"
    else:
        XO = "X"


# determine if anyone has won the game
def gameWon(board):
    global grid, winner

    # check for winning rows
    for row in range(0, 3):
        if ((grid[row][0] == grid[row][1] == grid[row][2]) and \
                (grid[row][0] is not None)):
            # this row won
            winner = grid[row][0]
            pygame.draw.line(board, (250, 0, 0), (0, (row + 1) * 100 - 50), \
                             (300, (row + 1) * 100 - 50), 2)
            break

    # check for winning columns
    for col in range(0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and \
                (grid[0][col] is not None):
            # this column won
            winner = grid[0][col]
            pygame.draw.line(board, (250, 0, 0), ((col + 1) * 100 - 50, 0),
                             ((col + 1) * 100 - 50, 300), 2)
            break

    # check for diagonal winners
    if (grid[0][0] == grid[1][1] == grid[2][2]) and \
            (grid[0][0] is not None):
        # game won diagonally left to right
        winner = grid[0][0]
        pygame.draw.line(board, (250, 0, 0), (50, 50), (250, 250), 2)

    if (grid[0][2] == grid[1][1] == grid[2][0]) and \
            (grid[0][2] is not None):
        # game won diagonally right to left
        winner = grid[0][2]
        pygame.draw.line(board, (250, 0, 0), (250, 50), (50, 250), 2)


# --------------------------------------------------------------------
# initialize pygame and our window
pygame.init()
ttt = pygame.display.set_mode((300, 400))
pygame.display.set_caption('X & 0')

# create the game board
board = initBoard(ttt)

# main event loop
running = 1

while running == 1:
    for event in pygame.event.get():
        if event.type is QUIT:
            running = 0
        elif event.type is MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            clickBoard(board)

        # check for a winner
        gameWon(board)

        # update the display
        showBoard(ttt, board)

#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
# here
# import smbus
import pygame

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stuff about gesture sensor !!!!!!!!!!!!!!!!!!!!!!!!!!!
# i2c address
from builtins import object

from pygame.constants import QUIT

PAJ7620U2_I2C_ADDRESS = 0x73
# Register Bank select
PAJ_BANK_SELECT = 0xEF  # Bank0== 0x00,Bank1== 0x01
PAJ_INT_FLAG1 = 0x43  # Gesture detection interrupt flag

# Gesture detection interrupt flag
PAJ_UP = 0x01
PAJ_DOWN = 0x02
PAJ_LEFT = 0x04
PAJ_RIGHT = 0x08
PAJ_FORWARD = 0x10
PAJ_BACKWARD = 0x20
PAJ_CLOCKWISE = 0x40
PAJ_COUNT_CLOCKWISE = 0x80
PAJ_WAVE = 0x100

# Power up initialize array
Init_Register_Array = (
    (0xEF, 0x00),
    (0x37, 0x07),
    (0x38, 0x17),
    (0x39, 0x06),
    (0x41, 0x00),
    (0x42, 0x00),
    (0x46, 0x2D),
    (0x47, 0x0F),
    (0x48, 0x3C),
    (0x49, 0x00),
    (0x4A, 0x1E),
    (0x4C, 0x20),
    (0x51, 0x10),
    (0x5E, 0x10),
    (0x60, 0x27),
    (0x80, 0x42),
    (0x81, 0x44),
    (0x82, 0x04),
    (0x8B, 0x01),
    (0x90, 0x06),
    (0x95, 0x0A),
    (0x96, 0x0C),
    (0x97, 0x05),
    (0x9A, 0x14),
    (0x9C, 0x3F),
    (0xA5, 0x19),
    (0xCC, 0x19),
    (0xCD, 0x0B),
    (0xCE, 0x13),
    (0xCF, 0x64),
    (0xD0, 0x21),
    (0xEF, 0x01),
    (0x02, 0x0F),
    (0x03, 0x10),
    (0x04, 0x02),
    (0x25, 0x01),
    (0x27, 0x39),
    (0x28, 0x7F),
    (0x29, 0x08),
    (0x3E, 0xFF),
    (0x5E, 0x3D),
    (0x65, 0x96),
    (0x67, 0x97),
    (0x69, 0xCD),
    (0x6A, 0x01),
    (0x6D, 0x2C),
    (0x6E, 0x01),
    (0x72, 0x01),
    (0x73, 0x35),
    (0x74, 0x00),
    (0x77, 0x01),
)
# Gesture register initializes array
Init_Gesture_Array = (
    (0xEF, 0x00),
    (0x41, 0x00),
    (0x42, 0x00),
    (0xEF, 0x00),
    (0x48, 0x3C),
    (0x49, 0x00),
    (0x51, 0x10),
    (0x83, 0x20),
    (0x9F, 0xF9),
    (0xEF, 0x01),
    (0x01, 0x1E),
    (0x02, 0x0F),
    (0x03, 0x10),
    (0x04, 0x02),
    (0x41, 0x40),
    (0x43, 0x30),
    (0x65, 0x96),
    (0x66, 0x00),
    (0x67, 0x97),
    (0x68, 0x01),
    (0x69, 0xCD),
    (0x6A, 0x01),
    (0x6B, 0xB0),
    (0x6C, 0x04),
    (0x6D, 0x2C),
    (0x6E, 0x01),
    (0x74, 0x00),
    (0xEF, 0x00),
    (0x41, 0xFF),
    (0x42, 0x01),
)


class PAJ7620U2(object):
    def __init__(self, address=PAJ7620U2_I2C_ADDRESS):
        self._address = address
        # here
        # self._bus = smbus.SMBus(1)
        time.sleep(0.5)
        if self._read_byte(0x00) == 0x20:
            print("\nGesture Sensor OK\n")
            for num in range(len(Init_Register_Array)):
                self._write_byte(Init_Register_Array[num][0], Init_Register_Array[num][1])
        else:
            print("\nGesture Sensor Error\n")
        self._write_byte(PAJ_BANK_SELECT, 0)
        for num in range(len(Init_Gesture_Array)):
            self._write_byte(Init_Gesture_Array[num][0], Init_Gesture_Array[num][1])

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_u16(self, cmd):
        LSB = self._bus.read_byte_data(self._address, cmd)
        MSB = self._bus.read_byte_data(self._address, cmd + 1)
        return (MSB << 8) + LSB

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)

    def check_gesture(self):
        Gesture_Data = self._read_u16(PAJ_INT_FLAG1)
        if Gesture_Data == PAJ_UP:
            print("Up\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_DOWN:
            print("Down\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_LEFT:
            print("Left\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_RIGHT:
            print("Right\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_FORWARD:
            print("Forward\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_BACKWARD:
            print("Backward\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_CLOCKWISE:
            print("Clockwise\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_COUNT_CLOCKWISE:
            print("AntiClockwise\r\n")
            return Gesture_Data
        elif Gesture_Data == PAJ_WAVE:
            print("Wave\r\n")
            return Gesture_Data
        else:
            return None


class gameClass(object):
    XO = "X"  # track whose turn it is; X goes first
    grid = [[None, None, None],
            [None, None, None],
            [None, None, None]]
    # exist or not a winner
    winner = XO
    # hold current position on the board
    currentRow = 0
    currentCol = 0
    # hold the last position on the board
    lastRow = None
    lastCol = None
    # game is runnig or not
    runnig = 1
    # mode for windows (wight and height)
    ttt = None
    # board to be displayed
    board = None

    def __init__(self):
        pygame.init()
        self.ttt = pygame.display.set_mode((300, 400))
        pygame.display.set_caption('X & 0')

    def initBoard(self):
        # set up the background surface
        self.board = pygame.Surface(self.ttt.get_size())
        self.board = self.board.convert()
        self.board.fill((250, 250, 250))

        # draw the grid lines
        # vertical lines
        pygame.draw.line(self.board, (0, 0, 0), (0, 0), (0, 300), 2)
        pygame.draw.line(self.board, (0, 0, 0), (298, 0), (298, 300), 2)
        pygame.draw.line(self.board, (0, 0, 0), (100, 0), (100, 300), 2)
        pygame.draw.line(self.board, (0, 0, 0), (200, 0), (200, 300), 2)

        # horizontal lines
        pygame.draw.line(self.board, (0, 0, 0), (0, 0), (300, 0), 2)
        pygame.draw.line(self.board, (0, 0, 0), (0, 298), (300, 298), 2)
        pygame.draw.line(self.board, (0, 0, 0), (0, 100), (300, 100), 2)
        pygame.draw.line(self.board, (0, 0, 0), (0, 200), (300, 200), 2)

    def displayBoard(self):
        self.ttt.blit(self.board, (0, 0))
        pygame.display.flip()

    # draw the status (i.e., player turn, etc) at the bottom of the board
    def drawStatus(self):
        if self.winner in "X":
            message = self.XO + "'s turn"
        else:
            message = self.winner + " won!"

        # render the status message
        font = pygame.font.Font(None, 24)
        text = font.render(message, 1, (10, 10, 10))

        # copy the rendered message on the board
        self.board.fill((250, 250, 250), (0, 300, 300, 25))
        self.board.blit(text, (10, 300))

    # draw X or 0 (piece) on the board in boardRaw, boardCol
    def drawMove(self, boardRow, boardCol, piece):
        if self.winner is None:
            # determine the center of the square
            centerX = (boardCol * 100) + 50
            centerY = (boardRow * 100) + 50

            # draw the appropriate piece
            if piece == 'O':
                pygame.draw.circle(self.board, (0, 0, 0), (centerX, centerY), 44, 2)
            else:
                pygame.draw.line(self.board, (0, 0, 0), (centerX - 22, centerY - 22), \
                                 (centerX + 22, centerY + 22), 2)
                pygame.draw.line(self.board, (0, 0, 0), (centerX + 22, centerY - 22), \
                                 (centerX - 22, centerY + 22), 2)

            # mark the space as used
            self.grid[boardRow][boardCol] = piece

    # verify if "click" is possible
    def clickBoard(self):
        if self.grid[self.currentRow][self.currentCol] is "X" or \
                self.grid[self.currentRow][self.currentCol] is "O":
            return

        # draw "X" or "0" on the board in current position
        self.drawMove(self.currentRow, self.currentCol, self.XO)

        # go to next payer
        if self.XO is "X":
            self.XO = "O"
        else:
            self.XO = "X"

    # determine if anyone has won the game
    def gameWon(self):
        # check for winning rows
        for row in range(0, 3):
            if ((self.grid[row][0] == self.grid[row][1] == self.grid[row][2]) and \
                    (self.grid[row][0] is not None)):
                # this row won
                self.winner = self.grid[row][0]
                pygame.draw.line(self.board, (250, 0, 0), (0, (row + 1) * 100 - 50), \
                                 (300, (row + 1) * 100 - 50), 2)
                break

        # check for winning columns
        for col in range(0, 3):
            if (self.grid[0][col] == self.grid[1][col] == self.grid[2][col]) and \
                    (self.grid[0][col] is not None):
                # this column won
                self.winner = self.grid[0][col]
                pygame.draw.line(self.board, (250, 0, 0), ((col + 1) * 100 - 50, 0),
                                 ((col + 1) * 100 - 50, 300), 2)
                break

        # check for diagonal winners
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) and \
                (self.grid[0][0] is not None):
            # game won diagonally left to right
            self.winner = self.grid[0][0]
            pygame.draw.line(self.board, (250, 0, 0), (50, 50), (250, 250), 2)

        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0]) and \
                (self.grid[0][2] is not None):
            # game won diagonally right to left
            self.winner = self.grid[0][2]
            pygame.draw.line(self.board, (250, 0, 0), (250, 50), (50, 250), 2)

    def drawConture(self, startPointX, startPointY, color):
        # vertical lines
        pygame.draw.line(self.board, color,
                         (startPointX + 2, startPointY + 2),
                         (startPointX + 2, startPointY + 100 - 2), 2)
        pygame.draw.line(self.board, color,
                         (startPointX + 100 - 2, startPointY + 2),
                         (startPointX + 100 - 2, startPointY + 100 + 2), 2)

        # horizontal lines
        # red
        pygame.draw.line(self.board, color,
                         (startPointX + 2, startPointY + 2),
                         (startPointX + 100 - 2, startPointY + 2), 2)
        pygame.draw.line(self.board, color,
                         (startPointX + 2, startPointY + 100 - 2),
                         (startPointX + 100 - 2, startPointY + 100 - 2), 2)

    # draw new position
    # delete last position
    # enable - True  -> draw red square
    #        - False -> draw white square
    def drawPosition(self):
        red = (255, 0, 0)
        white = (255, 255, 255)
        if self.currentRow is not None and self.currentCol is not None:
            # determinate the square
            startPointXNew = (self.currentRow * 100)
            startPointYNew = (self.currentCol * 100)
            self.drawConture(startPointXNew, startPointYNew, red)
        if self.lastRow is not None and self.lastCol is not None:
            startPointXOld = (self.lastRow * 100)
            startPointYOld = (self.lastCol * 100)
            self.drawConture(startPointXOld, startPointYOld, white)

    def executeGestEvent(self, gest):
        print("Something")
        if gest == PAJ_UP:
            print("Up\r\n")
            if 0 < self.currentRow < 3:
                self.currentRow -= 1
                self.drawPosition()

        elif gest == PAJ_DOWN:
            print("Down\r\n")
            if 0 <= self.currentRow < 2:
                self.currentRow += 1
                self.drawPosition()

        elif gest == PAJ_LEFT:
            print("Left\r\n")
            if 0 < self.currentCol <= 2:
                self.currentCol -= 1
                self.drawPosition()

        elif gest == PAJ_RIGHT:
            print("Right\r\n")
            if 0 <= self.currentCol < 2:
                self.currentCol += 1
                self.drawPosition()

        elif gest == PAJ_FORWARD:
            print("Forward\r\n")
        elif gest == PAJ_BACKWARD:
            print("Backward\r\n")
        elif gest == PAJ_CLOCKWISE:
            print("Clockwise\r\n")
        elif gest == PAJ_COUNT_CLOCKWISE:
            print("AntiClockwise\r\n")
        elif gest == PAJ_WAVE:
            print("Wave\r\n")

if __name__ == '__main__':
    print("\nStart Test Program ...\n")
    # init game
    game = gameClass()
    game.initBoard()
    # init sensor
    # paj7620u2 = PAJ7620U2()
    game.drawStatus()
    # initial position
    game.drawPosition()
    game.displayBoard()
    while game.runnig is 1:
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type is QUIT:
                game.runnig = 0
        # get gesture
        # gesture = paj7620u2.check_gesture()
        gesture = None
        if gesture is not None:
            game.executeGestEvent(gesture)
            game.drawStatus()
            game.displayBoard()

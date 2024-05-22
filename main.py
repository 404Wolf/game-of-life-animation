from utils import Board, Printer
from sys import stdout
import time
import os

DELAY = 0.01

def main():
    board = Board.from_random(*os.get_terminal_size())
    printer = Printer(str(board))
    for _ in board:
        printer.redraw_frame(str(board))
        time.sleep(DELAY)

if __name__ == "__main__":
    main()

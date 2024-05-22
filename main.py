from utils import Board, Printer
from sys import stdout
import time

DELAY = 0.3

def main():
    board = Board.from_random(100, 7)
    printer = Printer(str(board))
    for _ in board:
        printer.redraw_frame(str(board))
        time.sleep(DELAY)

if __name__ == "__main__":
    main()

from utils import Board
from sys import stdout

def main():
    board = Board.from_random(100, 7)
    i = 0
    for live_cell_count in board:
        print(f"Generation {i}")
        board.print()
        i += 1
        # if i == 2:
        #     break

if __name__ == "__main__":
    main()

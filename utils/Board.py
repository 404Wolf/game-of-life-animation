from functools import cache
from enum import Enum
from random import randint, choices
from dataclasses import dataclass

class CellState(Enum):
    DEAD = "◯" # "⠀" "■"
    ALIVE = "●" # "█" "□"

# All of the indices of the adjacent cells of a given cell
ADJACENT_CELLS = ((-1, -1), (-1, 0), (-1, 1),
                  (0,  -1),          (0,  1),
                  (1,  -1), (1,  0), (1,  1))

@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Board:
    def __init__(
        self,
        width: int, 
        height: int, 
        live_cells: frozenset[Cell]
    ):
        self._width = width
        self._height = height

        # Make sure that width and height are nonnegative
        if width < 0 or height < 0:
            raise ValueError(f"Width/height must be nonnegative, got {width}")

        # Check if live cells are within bounds
        for cell in live_cells:
            if cell.x < 0 or cell.x >= width:
                raise ValueError(f"Cell {cell} is out of bounds")
            
            if cell.x < 0 or cell.y >= height:
                raise ValueError(f"Cell {cell} is out of bounds")

        self._live_cells = live_cells 

    @classmethod
    def from_random(self, width: int=None, height: int=None):
        width = width or randint(10, 200)
        height = height or randint(10, 200)
        assert isinstance(width, int) and isinstance(height, int), f"Width and height must be integers, got {width}, {height}"

        # We only need to deal with live cells so we must first figure out how many there should be
        number_of_live_cells = randint(int(width * height * 0.1), int(width * height * 0.5))
        live_cells = frozenset(Cell(*cell) for cell in zip(choices(range(width), k=number_of_live_cells), 
            choices(range(height), k=number_of_live_cells)))
                        
        return Board(width, height, live_cells)

    def __str__(self) -> str:
        frame = ""
        for y in range(self._height):
            for x in range(self._width):
                # End means that we resume from the last printed character
                frame += CellState.ALIVE.value if Cell(x, y) in self._live_cells else CellState.DEAD.value 
            frame += "\n"
        return frame

    def _generate_next_state(self, live_cells: frozenset[Cell]):
        assert isinstance(live_cells, frozenset), f"live_cells is not of type frozenset {live_cells}"
        assert all(isinstance(cell, Cell) for cell in live_cells), f"live_cells contains non-Cell elements {live_cells}"
 
        # Count the number of live neighbors
        def count_live_neighbors(cell: Cell) -> int:
            assert isinstance(cell, Cell), f"cell is not of type Cell. Got '{cell}'"
            count = 0
            for dx, dy in ADJACENT_CELLS:
                if Cell(cell.x + dx, cell.y + dy) in live_cells:
                    count += 1
            return count

        # Compute the next state
        next_live_cells = set()
        for live_cell in live_cells:
            count = count_live_neighbors(live_cell)

            # If the cell is alive and has 2 or 3 live neighbors it stays alive
            if count in (2, 3):
                next_live_cells.add(live_cell)

            # If the cell is dead and has 3 live neighbors it becomes alive
            for dx, dy in ADJACENT_CELLS:
                neighbor = Cell(live_cell.x + dx, live_cell.y + dy)
                if count_live_neighbors(neighbor) == 3 and neighbor not in live_cells:
                    next_live_cells.add(neighbor)

        return frozenset(next_live_cells)

    def __iter__(self):
        return self

    def __next__(self):
        self._live_cells = self._generate_next_state(self._live_cells)
        return len(self._live_cells)
    
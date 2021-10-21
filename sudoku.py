from __future__ import annotations
from typing import Iterable, Sequence
from functools import lru_cache
import numpy as np


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[str] = []
        self._array_grid: list[[int]] = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)


    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        row = self._grid[y]
        new_row = ""

        for i in range(9):
            if i == x:
                new_row += str(value)
            else:
                new_row += row[i]

        self._grid[y] = new_row

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        row = self._grid[y]
        new_row = row[:x] + "0" + row[x + 1:]
        self._grid[y] = new_row

    # @lru_cache(maxsize=128)
    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = -1

        for i in range(9):
            for j in range(9):
                if i == x and j == y:
                    row = self._grid[y]
                    value = int(row[x])

        return value

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for row in self._grid:
            for number in row:
                if number == '0' and next_x == -1 and next_y == -1:
                    next_x, next_y = row.index('0'), self._grid.index(row)

        return next_x, next_y

    def row_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th row."""
        values = list(map(int, self._grid[i]))

        return values

    def column_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th column."""
        values = [int(item[i]) for item in self._grid]

        return values

    def block_values(self, i: int) -> Sequence[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        sudoku = []

        for row in self._grid:
            array_row = list(map(int, row))
            sudoku.append(array_row)

        blocks = [[sudoku[int(m / 3) * 3 + i][(m % 3) * 3 + j] for i in range(3) for j in range(3)] for m in range(9)]
        values = blocks[i]

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
    
        result = True

        if any('0' in row for row in self._grid):
            result = False

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
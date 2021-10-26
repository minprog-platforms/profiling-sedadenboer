# sudoku.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# Contains Sudoku class to solve sudoku's.
# Has to be paired with solve.py and puzzle files.
# Methods and attributes:
# - grid
# - place, unplace
# - value_at, options_at, next_empty_index
# - row_values, column_values, block_values
# - is_solved
# - function to print the sudoku

from __future__ import annotations
from typing import Iterable, Sequence
from functools import lru_cache


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        # list in which sudoku rows will be appended
        self._grid: list[str] = []

        # loop through puzzle file to retrieve rows
        for puzzle_row in puzzle:
            row = ""

            # get sudoku values and make row strings
            for element in puzzle_row:
                row += str(element)

            # add rows to the sudoku grid
            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        # get y'th
        row = self._grid[y]
        new_row = ""

        # insert value into row at place x
        for i in range(9):
            if i == x:
                new_row += str(value)
            else:
                new_row += row[i]

        self._grid[y] = new_row

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        # remove a number and replace with '0'
        row = self._grid[y]
        new_row = row[:x] + "0" + row[x + 1:]
        self._grid[y] = new_row

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        # get value at x,y with sudoku grid
        value = int(self._grid[y][x])

        return value

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)
        
        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        # intialize next index values
        next_x, next_y = -1, -1

        # search for empty spot '0' by looping over rows
        for row in self._grid:
            if '0' in row and next_x == -1 and next_y == -1:
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
        values = []

        # get starting coördinates for a block
        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        # get block values
        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        result = True

        # sudoku is solved if there are no empty spots left
        if any('0' in row for row in self._grid):
            result = False

        return result

    def __str__(self) -> str:
        representation = ""
        
        # print sudoku in a neat way
        for row in self._grid:
            representation += row + "\n"

        return representation.strip()

@lru_cache(maxsize=128)
def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)

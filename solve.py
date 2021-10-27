# solve.py
#
# Course: programmeerplatform
# Name: Seda den Boer
# Student number: 12179981
#
# Premade file from the assignment.
# Solves a sudoku by calling functions from sudoku.py.

from __future__ import annotations
from typing import Union

import argparse
import os
import sys

from sudoku import Sudoku, load_from_file


def solve(sudoku: Sudoku) -> Union[Sudoku, None]:
    """
    Solve a Sudoku puzzle using Depth First Search (DFS).
    Returns a Sudoku puzzle if the puzzle is solvable, None otherwise.
    """
    # if sudoku is solved, nothing to be done
    if sudoku.is_solved():
        return sudoku

    # otherwise, find an empty spot
    x, y = sudoku.next_empty_index()

    # for each possible option at the empty spot
    for option in sudoku.options_at(x, y):

        # place that option in the sudoku
        sudoku.place(option, x, y)

        # try to solve the remaining sudoku
        if solve(sudoku):
            return sudoku

        # if that option did not lead to a solution, unplace
        sudoku.unplace(x, y)

    return None


if __name__ == "__main__":
    # create a command line argument parser
    parser = argparse.ArgumentParser(description='Solve a sudoku puzzle.')
    parser.add_argument("puzzle", type=int, help="identifier of the puzzle to be solved")
    parser.add_argument("-n", type=int, default=1, dest="number_of_runs", help="number of runs")

    # parse the command line arguments
    args = parser.parse_args()

    puzzle_path = f"puzzles/{args.puzzle}.csv"

    # if the puzzle does not exist, exit
    if not os.path.exists(puzzle_path):
        print(f"puzzle {args.puzzle} does not exist")
        sys.exit(1)

    # load the puzzle
    sudoku = load_from_file(puzzle_path)

    # show the puzzle to the user
    print(sudoku)
    print()

    # solve the puzzle args.number_of_runs times
    print("SOLVING...")
    for i in range(args.number_of_runs):
        solved_sudoku = solve(sudoku)

        # if this is not the last run, reload the puzzle
        if i < args.number_of_runs - 1:
            sudoku = load_from_file(puzzle_path)

    print("DONE SOLVING")

    # show the solution
    print()
    print(solved_sudoku)

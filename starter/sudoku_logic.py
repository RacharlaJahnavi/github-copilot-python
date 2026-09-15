import copy
import random

SIZE = 9
EMPTY = 0


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):

            if board[row][col] == EMPTY:

                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)

                for candidate in possible:

                    if is_safe(board, row, col, candidate):

                        board[row][col] = candidate

                        if fill_board(board):
                            return True

                        board[row][col] = EMPTY

                return False

    return True


def find_empty_cell(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col

    return None


def _has_valid_givens(board):
    if len(board) != SIZE or any(len(row) != SIZE for row in board):
        return False

    for row in board:
        values = [value for value in row if value != EMPTY]
        if any(value not in range(1, SIZE + 1) for value in values):
            return False
        if len(values) != len(set(values)):
            return False

    for col in range(SIZE):
        values = [board[row][col] for row in range(SIZE)]
        values = [value for value in values if value != EMPTY]
        if len(values) != len(set(values)):
            return False

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            values = [
                board[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
                if board[row][col] != EMPTY
            ]
            if len(values) != len(set(values)):
                return False

    return True


def count_solutions(board, max_solutions=2):
    """
    Count the number of possible solutions.
    Stops after finding max_solutions.
    """

    if max_solutions < 1:
        raise ValueError("max_solutions must be at least 1")

    if not _has_valid_givens(board):
        return 0

    board = deep_copy(board)
    solutions = 0

    def backtrack():

        nonlocal solutions

        if solutions >= max_solutions:
            return

        empty = find_empty_cell(board)

        if not empty:
            solutions += 1
            return

        row, col = empty

        for num in range(1, SIZE + 1):

            if is_safe(board, row, col, num):

                board[row][col] = num

                backtrack()

                board[row][col] = EMPTY

                if solutions >= max_solutions:
                    return

    backtrack()

    return solutions


def remove_cells(board, clues):
    """
    Remove cells while keeping exactly one solution.
    """

    if not isinstance(clues, int) or not 17 <= clues <= SIZE * SIZE:
        raise ValueError("clues must be an integer between 17 and 81")

    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)

    for row, col in cells:
        if sum(value != EMPTY for row in board for value in row) <= clues:
            return

        if board[row][col] == EMPTY:
            continue

        original_value = board[row][col]

        board[row][col] = EMPTY

        # Keep the removal only if there is exactly one solution
        if count_solutions(board, max_solutions=2) != 1:
            board[row][col] = original_value

    if sum(value != EMPTY for row in board for value in row) > clues:
        raise RuntimeError("Unable to generate a puzzle with the requested clues")


def generate_puzzle(clues=35):
    """
    Generate a Sudoku puzzle and its solution.
    """

    if not isinstance(clues, int) or not 17 <= clues <= SIZE * SIZE:
        raise ValueError("clues must be an integer between 17 and 81")

    # Create completely solved board
    board = create_empty_board()

    if not fill_board(board):
        raise RuntimeError("Unable to generate a complete Sudoku solution")

    # Save the solution
    solution = deep_copy(board)

    # Remove numbers while keeping one solution
    remove_cells(board, clues)

    # Save puzzle
    puzzle = deep_copy(board)

    if count_solutions(puzzle, max_solutions=2) != 1:
        raise RuntimeError("Generated Sudoku puzzle does not have a unique solution")

    return puzzle, solution
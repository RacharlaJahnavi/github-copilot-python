import pytest
import sudoku_logic


SOLVED_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(value == sudoku_logic.EMPTY for row in board for value in row)


def test_deep_copy_is_independent():
    copied_board = sudoku_logic.deep_copy(SOLVED_BOARD)
    copied_board[0][0] = 0

    assert SOLVED_BOARD[0][0] == 5
    assert copied_board[0][0] == 0


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][1] = 5
    board[1][0] = 6
    board[1][1] = 7

    assert sudoku_logic.is_safe(board, 0, 0, 5) is False
    assert sudoku_logic.is_safe(board, 0, 0, 6) is False
    assert sudoku_logic.is_safe(board, 0, 0, 7) is False
    assert sudoku_logic.is_safe(board, 0, 0, 4) is True


def test_fill_board_completes_an_empty_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert sudoku_logic.find_empty_cell(board) is None
    assert sudoku_logic.count_solutions(board) == 1


def test_find_empty_cell_returns_first_empty_position():
    board = sudoku_logic.deep_copy(SOLVED_BOARD)
    board[2][4] = sudoku_logic.EMPTY

    assert sudoku_logic.find_empty_cell(board) == (2, 4)


def test_count_solutions_counts_solved_and_ambiguous_boards():
    solved_board = sudoku_logic.deep_copy(SOLVED_BOARD)
    ambiguous_board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(solved_board) == 1
    assert sudoku_logic.count_solutions(ambiguous_board, max_solutions=2) == 2


def test_count_solutions_rejects_invalid_givens():
    invalid_board = sudoku_logic.deep_copy(SOLVED_BOARD)
    invalid_board[0][1] = invalid_board[0][0]

    assert sudoku_logic.count_solutions(invalid_board) == 0


def test_generate_puzzle_rejects_unsupported_clue_count():
    with pytest.raises(ValueError):
        sudoku_logic.generate_puzzle(clues=16)


def test_remove_cells_keeps_requested_clues_and_unique_solution():
    puzzle = sudoku_logic.deep_copy(SOLVED_BOARD)
    sudoku_logic.remove_cells(puzzle, clues=80)

    assert sum(value != sudoku_logic.EMPTY for row in puzzle for value in row) == 80
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_generate_puzzle_returns_unique_puzzle_and_matching_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=80)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert solution != puzzle
    assert all(
        puzzle[row][col] in (sudoku_logic.EMPTY, solution[row][col])
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )
    assert sum(value != sudoku_logic.EMPTY for row in puzzle for value in row) == 80
    assert sudoku_logic.count_solutions(puzzle) == 1

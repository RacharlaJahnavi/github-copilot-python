import pytest
import app as app_module


SOLUTION = [
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

PUZZLE = [
    [5, 0, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def start_fixed_game(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "generate_puzzle",
        lambda clues: ([row[:] for row in PUZZLE], [row[:] for row in SOLUTION]),
    )


def test_home_renders_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku Game" in response.data


@pytest.mark.parametrize(
    ("difficulty", "expected_clues"),
    [("easy", 45), ("medium", 35), ("hard", 25)],
)
def test_new_game_uses_requested_difficulty_and_clue_count(
    client, monkeypatch, difficulty, expected_clues
):
    calls = []

    def fake_generate_puzzle(clues):
        calls.append(clues)
        return PUZZLE, SOLUTION

    monkeypatch.setattr(app_module, "generate_puzzle", fake_generate_puzzle)

    response = client.get(f"/new?difficulty={difficulty}")

    assert response.status_code == 200
    assert response.get_json() == {"puzzle": PUZZLE, "difficulty": difficulty}
    assert calls == [expected_clues]


def test_new_game_defaults_unknown_difficulty_to_medium_clues(client, monkeypatch):
    calls = []
    monkeypatch.setattr(
        app_module,
        "generate_puzzle",
        lambda clues: (calls.append(clues) or (PUZZLE, SOLUTION)),
    )

    response = client.get("/new?difficulty=unknown")

    assert response.status_code == 200
    assert response.get_json()["difficulty"] == "unknown"
    assert calls == [35]


def test_hint_requires_a_started_game(client):
    response = client.get("/hint")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Please start a new game first."}


def test_hint_fills_first_empty_cell(client, monkeypatch):
    start_fixed_game(monkeypatch)
    client.get("/new")
    before_hint = [row[:] for row in app_module.current_puzzle]

    response = client.get("/hint")

    assert response.status_code == 200
    assert response.get_json() == {"row": 0, "col": 1, "value": 3}
    assert app_module.current_puzzle[0][1] == 3
    assert app_module.current_puzzle[0][1] == app_module.current_solution[0][1]
    changed_cells = [
        (row, col)
        for row in range(9)
        for col in range(9)
        if before_hint[row][col] != app_module.current_puzzle[row][col]
    ]
    assert changed_cells == [(0, 1)]


def test_hint_fills_one_new_cell_on_each_request(client, monkeypatch):
    start_fixed_game(monkeypatch)
    client.get("/new")
    app_module.current_puzzle[1][1] = 0

    first_hint = client.get("/hint").get_json()
    second_hint = client.get("/hint").get_json()

    assert (first_hint["row"], first_hint["col"]) != (
        second_hint["row"],
        second_hint["col"],
    )
    assert first_hint["value"] == app_module.current_solution[
        first_hint["row"]
    ][first_hint["col"]]
    assert second_hint["value"] == app_module.current_solution[
        second_hint["row"]
    ][second_hint["col"]]


def test_hint_reports_when_no_empty_cells_remain(client):
    app_module.current_puzzle = [row[:] for row in SOLUTION]
    app_module.current_solution = [row[:] for row in SOLUTION]

    response = client.get("/hint")

    assert response.status_code == 200
    assert response.get_json() == {"error": "There are no empty cells left."}


def test_check_rejects_missing_board(client):
    response = client.post("/check", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid board data."}


def test_check_rejects_malformed_board_shape(client):
    app_module.current_puzzle = [row[:] for row in PUZZLE]
    app_module.current_solution = [row[:] for row in SOLUTION]

    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid board data."}


def test_check_requires_a_started_game(client):
    response = client.post("/check", json={"board": PUZZLE})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Please start a new game first."}


def test_check_reports_incomplete_board(client):
    app_module.current_puzzle = [row[:] for row in PUZZLE]
    app_module.current_solution = [row[:] for row in SOLUTION]

    response = client.post("/check", json={"board": PUZZLE})

    assert response.status_code == 200
    assert response.get_json() == {
        "incorrect": [],
        "incomplete": [[0, 1]],
        "complete": False,
        "message": "Please fill all the cells.",
    }


def test_check_reports_incorrect_values(client):
    app_module.current_puzzle = [row[:] for row in PUZZLE]
    app_module.current_solution = [row[:] for row in SOLUTION]
    board = [row[:] for row in SOLUTION]
    board[0][1] = 9

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {
        "incorrect": [[0, 1]],
        "incomplete": [],
        "complete": False,
        "message": "Some cells are incorrect.",
    }


def test_check_reports_multiple_incorrect_editable_values_without_flagging_clues(
    client,
):
    app_module.current_puzzle = [row[:] for row in PUZZLE]
    app_module.current_puzzle[1][1] = 0
    app_module.current_solution = [row[:] for row in SOLUTION]
    board = [row[:] for row in SOLUTION]
    board[0][1] = 9
    board[1][1] = 8
    board[0][0] = 9

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {
        "incorrect": [[0, 1], [1, 1]],
        "incomplete": [],
        "complete": False,
        "message": "Some cells are incorrect.",
    }


def test_check_accepts_string_numbers_and_complete_solution(client):
    app_module.current_puzzle = [row[:] for row in PUZZLE]
    app_module.current_solution = [row[:] for row in SOLUTION]
    board = [[str(value) for value in row] for row in SOLUTION]

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.get_json() == {
        "incorrect": [],
        "incomplete": [],
        "complete": True,
        "message": "Congratulations! You solved it!",
    }

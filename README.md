# Flask Sudoku Game

A browser-based Sudoku game built with Flask, Python, HTML, CSS, and JavaScript. The application generates uniquely solvable puzzles, supports three difficulty levels, provides hints and answer checking, tracks completion time, and stores a local Top 10 leaderboard in the browser.

## Features

- Generates valid Sudoku puzzles with exactly one solution.
- Supports three difficulty levels:
  - Easy: 45 prefilled cells
  - Medium: 35 prefilled cells
  - Hard: 25 prefilled cells
- Keeps prefilled cells locked.
- Provides one correct hint at a time and locks hinted cells.
- Checks user-entered values against the current puzzle solution.
- Gives immediate feedback for incorrect editable values.
- Shows incomplete, incorrect, and completed puzzle states.
- Stops the timer when the puzzle is completed.
- Displays a completion message containing elapsed time and hints used.
- Stores the Top 10 fastest completed games in browser `localStorage`.
- Stores player name, completion time, difficulty, and hint count for each score.
- Defaults a blank player name to `Guest`.
- Supports light and dark themes with persisted theme preference.
- Uses alternating styling for the nine 3x3 regions.
- Provides responsive desktop and mobile layouts.
- Includes keyboard focus styling and touch-friendly mobile controls.

## Technologies

- Python 3
- Flask
- pytest
- HTML5
- CSS3
- JavaScript
- Browser `localStorage`

## Project Structure

```text
.
├── README.md
├── pytest.ini
└── starter/
    ├── app.py
    ├── instruction.md
    ├── requirements.txt
    ├── sudoku_logic.py
    ├── static/
    │   ├── main.js
    │   └── styles.css
    ├── templates/
    │   └── index.html
    └── tests/
        ├── conftest.py
        ├── test_app.py
        └── test_sudoku_logic.py
```

## Installation

From the repository root, create and activate a virtual environment in the `starter` directory:

### Windows PowerShell

```powershell
cd starter
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation for the current process, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
cd starter
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

With the virtual environment active:

```bash
python -m pip install -r requirements.txt
```

The requirements include Flask and pytest.

## Run the Application

From the `starter` directory, with the virtual environment active:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

The application exposes these routes:

- `GET /` renders the game page.
- `GET /new?difficulty=easy|medium|hard` creates a new puzzle.
- `GET /hint` fills and locks one correct empty cell.
- `POST /check` checks a submitted 9x9 board.

## Run the Tests

From the repository root:

```bash
pytest -q
```

Or from the `starter` directory:

```bash
python -m pytest -q
```

The current project result is:

```text
28 passed
```

The exact runtime may vary by machine. The tests cover Sudoku board operations, solution counting, unique puzzle generation, difficulty mapping, hints, board checking, malformed board handling, and completion behavior.

## GitHub Copilot Usage

GitHub Copilot was used to review the existing starter project, establish the pytest baseline, implement and verify Sudoku uniqueness, add difficulty behavior, strengthen hint and check flows, implement timer and leaderboard behavior, improve dark mode and responsive styling, and review the project against its requirements.

Copilot was used as a coding and review assistant. Changes were kept focused on the existing Flask architecture, and each implementation step was checked with the project test suite or a relevant syntax or behavior check.

## Design Decisions

- **Unique solutions:** A randomized backtracking solver creates a complete board. Cells are removed only when the resulting puzzle still has exactly one solution. Solution counting stops after two solutions because the distinction needed is zero, one, or multiple.
- **Difficulty:** Difficulty is represented by clue counts: 45, 35, and 25 prefilled cells for Easy, Medium, and Hard.
- **Client-side leaderboard:** Scores are stored in browser `localStorage` because the project requirement calls for persistence between browser sessions without a database. The list is sorted by elapsed seconds and truncated to the fastest 10 entries.
- **Game timing:** The browser starts the timer after a new puzzle is received and records elapsed time from a timestamp. It stops after a correct completion.
- **Server validation:** The Flask `/check` endpoint compares editable cells with the stored solution and validates that incoming boards are 9x9. Prefilled cells are protected in the browser and excluded from user-entry checking.
- **Responsive UI:** The Sudoku board uses a fixed 9x9 grid with a responsive square size, while controls and score tables adapt to narrow screens.
- **Current state model:** The active puzzle and solution are held in application memory. This is suitable for the local starter application, but a multi-user deployment would need session-based or database-backed game state.

## Notes

- The leaderboard is local to each browser profile and is not shared between devices or users.
- `localStorage` can be cleared through browser settings, which removes saved scores and the saved theme preference.
- The project includes Python and Flask tests; browser-specific interactions are implemented in `static/main.js` and are not covered by a dedicated browser test runner.

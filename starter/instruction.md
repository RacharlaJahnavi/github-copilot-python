# Project Instructions

## Project
This is a Flask-based Sudoku web application.

## Code Style
- Use clear, readable Python and JavaScript.
- Keep functions small and focused.
- Reuse existing functions when possible.
- Avoid unnecessary dependencies.
- Add comments only where they improve understanding.
- Handle invalid input safely.

## Project Structure
- Flask application code belongs in `app.py`.
- Sudoku generation and solving logic belongs in `sudoku_logic.py`.
- Browser behavior belongs in `static/main.js`.
- Styling belongs in `static/styles.css`.
- HTML templates belong in `templates/`.
- Automated tests belong in `tests/`.

## Testing
- Use pytest for Python tests.
- Run `pytest` before committing changes.
- Do not remove or weaken existing tests just to make them pass.
- Add tests for important new behavior.

## Sudoku Requirements
- Generated puzzles must have exactly one solution.
- Prefilled cells must remain locked.
- Easy, Medium, and Hard difficulties must be supported.
- Hints must provide a correct value.
- Check must identify incorrect entries.

## UI Requirements
- Support light and dark modes.
- Keep the board responsive on desktop and mobile.
- Use clear visual styling for the nine 3x3 regions.
- Keep the interface simple and accessible.

## Git
- Make small, meaningful commits.
- Do not commit `.venv`, `__pycache__`, or generated files.
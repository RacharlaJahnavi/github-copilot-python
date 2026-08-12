from flask import Flask, render_template, jsonify, request
from sudoku_logic import generate_puzzle

app = Flask(__name__)

current_puzzle = None
current_solution = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/new")
def new_game():
    global current_puzzle, current_solution

    difficulty = request.args.get("difficulty", "medium")

    difficulty_clues = {
        "easy": 45,
        "medium": 35,
        "hard": 25
    }

    clues = difficulty_clues.get(difficulty, 35)

    current_puzzle, current_solution = generate_puzzle(clues)

    return jsonify({
        "puzzle": current_puzzle,
        "difficulty": difficulty
    })

@app.route("/hint", methods=["GET"])
def get_hint():
    global current_puzzle, current_solution

    if current_puzzle is None or current_solution is None:
        return jsonify({
            "error": "Please start a new game first."
        }), 400

    # Find an empty cell
    for row in range(9):
        for col in range(9):

            if current_puzzle[row][col] == 0:

                correct_value = current_solution[row][col]

                # Lock this cell in the current puzzle
                current_puzzle[row][col] = correct_value

                return jsonify({
                    "row": row,
                    "col": col,
                    "value": correct_value
                })

    return jsonify({
        "error": "There are no empty cells left."
    })

@app.route("/check", methods=["POST"])
def check_solution():
    global current_puzzle, current_solution

    data = request.get_json()

    if not data or "board" not in data:
        return jsonify({
            "error": "Invalid board data."
        }), 400

    board = data["board"]

    if current_puzzle is None or current_solution is None:
        return jsonify({
            "error": "Please start a new game first."
        }), 400

    incorrect = []
    incomplete = []

    for row in range(9):
        for col in range(9):

            # Original clues are already correct
            if current_puzzle[row][col] != 0:
                continue

            value = board[row][col]

            # Empty cell
            if value == 0 or value == "":
                incomplete.append([row, col])
                continue

            try:
                value = int(value)
            except (ValueError, TypeError):
                incorrect.append([row, col])
                continue

            # Wrong number
            if value != current_solution[row][col]:
                incorrect.append([row, col])

    if incorrect:
        return jsonify({
            "incorrect": incorrect,
            "incomplete": incomplete,
            "complete": False,
            "message": "Some cells are incorrect."
        })

    if incomplete:
        return jsonify({
            "incorrect": [],
            "incomplete": incomplete,
            "complete": False,
            "message": "Please fill all the cells."
        })

    return jsonify({
        "incorrect": [],
        "incomplete": [],
        "complete": True,
        "message": "Congratulations! You solved it!"
    })


if __name__ == "__main__":
    app.run(debug=True)
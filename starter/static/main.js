const SIZE = 9;
const SCORE_STORAGE_KEY = "sudokuScores";

let puzzle = [];

let timerInterval = null;

let timerStartTime = null;

let elapsedSeconds = 0;

let hintsUsed = 0;

let gameCompleted = false;


// =========================================
// TIMER
// =========================================

function startTimer() {

    stopTimer();

    timerStartTime = Date.now();

    elapsedSeconds = 0;

    updateTimerDisplay();

    timerInterval = setInterval(function () {

        elapsedSeconds++;

        updateTimerDisplay();

    }, 1000);
}


function stopTimer() {

    if (timerStartTime !== null) {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartTime) / 1000
        );
    }

    if (timerInterval !== null) {

        clearInterval(timerInterval);

        timerInterval = null;
    }

    timerStartTime = null;
}


function updateTimerDisplay() {

    if (timerStartTime !== null) {
        elapsedSeconds = Math.floor(
            (Date.now() - timerStartTime) / 1000
        );
    }

    const minutes =
        Math.floor(elapsedSeconds / 60);

    const seconds =
        elapsedSeconds % 60;

    document.getElementById("timer").innerText =
        String(minutes).padStart(2, "0") +
        ":" +
        String(seconds).padStart(2, "0");
}


// =========================================
// CREATE BOARD
// =========================================

function createBoardElement() {

    const boardDiv =
        document.getElementById("sudoku-board");

    boardDiv.innerHTML = "";


    for (let i = 0; i < SIZE; i++) {

        const rowDiv =
            document.createElement("div");

        rowDiv.className =
            "sudoku-row";


        for (let j = 0; j < SIZE; j++) {

            const input =
                document.createElement("input");

            input.type = "text";

            input.maxLength = 1;

            input.className =
                "sudoku-cell";

            input.dataset.row = i;

            input.dataset.col = j;


            input.addEventListener(
                "input",
                function (event) {

                    const input = event.target;

                    input.value =
                        event.target.value
                            .replace(/[^1-9]/g, "");

                    input.classList
                        .remove("incorrect");

                    validateCell(input);
                }
            );


            rowDiv.appendChild(input);
        }


        boardDiv.appendChild(rowDiv);
    }
}


async function validateCell(input) {

    if (input.disabled || input.value === "") {
        return;
    }

    const enteredValue = input.value;
    const inputs =
        document
            .getElementById("sudoku-board")
            .getElementsByTagName("input");
    const board = [];

    for (let i = 0; i < SIZE; i++) {
        board[i] = [];

        for (let j = 0; j < SIZE; j++) {
            const value = inputs[i * SIZE + j].value;
            board[i][j] = value === "" ? 0 : parseInt(value, 10);
        }
    }

    try {
        const response = await fetch("/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({board: board})
        });
        const data = await response.json();

        if (input.value !== enteredValue || input.disabled) {
            return;
        }

        const isIncorrect = data.incorrect && data.incorrect.some(
            function (position) {
                return position[0] === Number(input.dataset.row) &&
                    position[1] === Number(input.dataset.col);
            }
        );

        input.classList.toggle("incorrect", isIncorrect);
    } catch (error) {
        console.error(error);
    }
}


// =========================================
// RENDER PUZZLE
// =========================================

function renderPuzzle(puz) {

    puzzle = puz;

    createBoardElement();


    const inputs =
        document
            .getElementById("sudoku-board")
            .getElementsByTagName("input");


    for (let i = 0; i < SIZE; i++) {

        for (let j = 0; j < SIZE; j++) {

            const index =
                i * SIZE + j;

            const value =
                puzzle[i][j];

            const input =
                inputs[index];


            if (value !== 0) {

                input.value = value;

                input.disabled = true;

                input.className =
                    "sudoku-cell prefilled";

            } else {

                input.value = "";

                input.disabled = false;

                input.className =
                    "sudoku-cell";
            }
        }
    }
}


// =========================================
// NEW GAME
// =========================================

async function newGame() {

    stopTimer();

    try {

        const difficulty =
            document
                .getElementById("difficulty")
                .value;


        const response =
            await fetch(
                `/new?difficulty=${difficulty}`
            );


        const data =
            await response.json();


        renderPuzzle(data.puzzle);


        hintsUsed = 0;

        gameCompleted = false;


        document
            .getElementById("message")
            .innerText = "";


        startTimer();


    } catch (error) {

        console.error(error);

        document
            .getElementById("message")
            .innerText =
                "Unable to start a new game.";
    }
}


// =========================================
// CHECK SOLUTION
// =========================================

async function checkSolution() {

    const inputs =
        document
            .getElementById("sudoku-board")
            .getElementsByTagName("input");


    const board = [];


    for (let i = 0; i < SIZE; i++) {

        board[i] = [];


        for (let j = 0; j < SIZE; j++) {

            const index =
                i * SIZE + j;

            const value =
                inputs[index].value;


            board[i][j] =
                value === ""
                    ? 0
                    : parseInt(value, 10);
        }
    }


    try {

        const response =
            await fetch("/check", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    board: board
                })
            });


        const data =
            await response.json();


        const message =
            document.getElementById("message");


        for (let i = 0; i < inputs.length; i++) {

            if (!inputs[i].disabled) {

                inputs[i]
                    .classList
                    .remove("incorrect");
            }
        }


        if (data.error) {

            message.style.color =
                "#d32f2f";

            message.innerText =
                data.error;

            return;
        }


        if (data.incorrect) {

            for (const position
                of data.incorrect) {

                const row =
                    position[0];

                const col =
                    position[1];

                const index =
                    row * SIZE + col;


                if (!inputs[index].disabled) {

                    inputs[index]
                        .classList
                        .add("incorrect");
                }
            }
        }


        if (data.complete === true) {

            stopTimer();


            message.style.color =
                "#388e3c";

            message.innerText =
                "Congratulations! You solved it in " +
                formatScoreTime(elapsedSeconds) +
                " with " +
                hintsUsed +
                (hintsUsed === 1 ? " hint." : " hints.");


            if (!gameCompleted) {
                saveScore();
                gameCompleted = true;
            }

            return;
        }


        if (
            data.incorrect &&
            data.incorrect.length > 0
        ) {

            message.style.color =
                "#d32f2f";

            message.innerText =
                "Some cells are incorrect.";

            return;
        }


        message.style.color =
            "#d32f2f";

        message.innerText =
            "Please fill all the cells.";


    } catch (error) {

        console.error(error);

        document
            .getElementById("message")
            .innerText =
                "Unable to check the solution.";
    }
}


// =========================================
// HINT
// =========================================

async function useHint() {

    try {

        const response =
            await fetch("/hint");


        const data =
            await response.json();


        const message =
            document.getElementById("message");


        if (data.error) {

            message.style.color =
                "#d32f2f";

            message.innerText =
                data.error;

            return;
        }


        const inputs =
            document
                .getElementById("sudoku-board")
                .getElementsByTagName("input");


        const index =
            data.row * SIZE + data.col;


        const input =
            inputs[index];


        input.value =
            data.value;

        input.disabled = true;

        input.className =
            "sudoku-cell hint-cell";


        puzzle[data.row][data.col] =
            data.value;


        hintsUsed++;


        message.style.color =
            "#1976d2";

        message.innerText =
            "Hint used! One correct cell has been filled.";


    } catch (error) {

        console.error(error);

        document
            .getElementById("message")
            .innerText =
                "Unable to get a hint.";
    }
}


// =========================================
// SCOREBOARD
// =========================================

function loadScores() {

    try {

        const storedScores =
            JSON.parse(
                localStorage.getItem(SCORE_STORAGE_KEY)
            );


        if (!Array.isArray(storedScores)) {
            return [];
        }


        return storedScores.filter(function (score) {

            return score &&
                typeof score.name === "string" &&
                Number.isFinite(score.time) &&
                score.time >= 0 &&
                typeof score.difficulty === "string" &&
                Number.isFinite(score.hints) &&
                score.hints >= 0;
        });

    } catch (error) {

        console.error(error);
        return [];
    }
}


function saveScores(scores) {

    scores.sort(function (a, b) {

        return a.time - b.time;
    });


    scores = scores.slice(0, 10);


    try {

        localStorage.setItem(
            SCORE_STORAGE_KEY,
            JSON.stringify(scores)
        );

    } catch (error) {

        console.error(error);
    }
}


function saveScore() {

    let playerName =
        document
            .getElementById("player-name")
            .value
            .trim();


    if (playerName === "") {

        playerName = "Guest";
    }


    const difficulty =
        document
            .getElementById("difficulty")
            .value;


    const score = {

        name: playerName,

        time: elapsedSeconds,

        difficulty: difficulty,

        hints: hintsUsed
    };


    const scores = loadScores();


    scores.push(score);


    saveScores(scores);


    displayScores();
}


// =========================================
// DISPLAY SCORES
// =========================================

function displayScores() {

    const tbody =
        document.getElementById(
            "scoreboard-body"
        );


    if (!tbody) {
        return;
    }


    tbody.innerHTML = "";


    const scores = loadScores();


    scores.forEach(function (score, index) {

        const row =
            document.createElement("tr");


        const values = [
            index + 1,
            score.name,
            formatScoreTime(score.time),
            capitalize(score.difficulty),
            score.hints,
        ];


        values.forEach(function (value) {

            const cell =
                document.createElement("td");

            cell.textContent = value;
            row.appendChild(cell);
        });


        tbody.appendChild(row);
    });
}


// =========================================
// FORMAT TIME
// =========================================

function formatScoreTime(totalSeconds) {

    const minutes =
        Math.floor(totalSeconds / 60);

    const seconds =
        totalSeconds % 60;


    return (
        String(minutes).padStart(2, "0") +
        ":" +
        String(seconds).padStart(2, "0")
    );
}


// =========================================
// CAPITALIZE
// =========================================

function capitalize(text) {

    return text.charAt(0).toUpperCase()
        + text.slice(1);
}


// =========================================
// DARK MODE
// =========================================

function toggleDarkMode() {

    document.body.classList.toggle(
        "dark-mode"
    );


    const button =
        document.getElementById(
            "dark-mode"
        );


    if (
        document.body.classList
            .contains("dark-mode")
    ) {

        button.setAttribute("aria-pressed", "true");

        button.innerText =
            "☀️ Light Mode";


        localStorage.setItem(
            "darkMode",
            "enabled"
        );

    } else {

        button.setAttribute("aria-pressed", "false");

        button.innerText =
            "🌙 Dark Mode";


        localStorage.setItem(
            "darkMode",
            "disabled"
        );
    }
}


// =========================================
// LOAD SAVED DARK MODE
// =========================================

function loadDarkMode() {

    const button =
        document.getElementById(
            "dark-mode"
        );


    if (
        localStorage.getItem(
            "darkMode"
        ) === "enabled"
    ) {

        document.body.classList.add(
            "dark-mode"
        );


        button.setAttribute("aria-pressed", "true");

        button.innerText =
            "☀️ Light Mode";
    }
}


// =========================================
// PAGE LOAD
// =========================================

window.addEventListener(
    "load",
    function () {


        document
            .getElementById("new-game")
            .addEventListener(
                "click",
                newGame
            );


        document
            .getElementById("check-solution")
            .addEventListener(
                "click",
                checkSolution
            );


        document
            .getElementById("hint")
            .addEventListener(
                "click",
                useHint
            );


        document
            .getElementById("dark-mode")
            .addEventListener(
                "click",
                toggleDarkMode
            );


        document
            .getElementById("difficulty")
            .addEventListener(
                "change",
                newGame
            );


        loadDarkMode();


        displayScores();


        newGame();
    }
);
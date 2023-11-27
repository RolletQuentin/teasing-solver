let boardWidth = 3;
let boardHeight = 3;

function updateBoardSize() {
    const rowsSelect = document.getElementById("rows");
    const columnsSelect = document.getElementById("columns");

    const selectedRows = parseInt(rowsSelect.value);
    const selectedColumns = parseInt(columnsSelect.value);

    if (!isNaN(selectedRows) && !isNaN(selectedColumns)) {
        boardWidth = selectedColumns;
        boardHeight = selectedRows;
    } else {
        console.error("Invalid size selection");
    }
}

function startGame() {
    fetch("http://127.0.0.1:8000/start_game/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            x: parseInt(boardHeight),
            y: parseInt(boardWidth),
            seed: -1,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const board = data.board;
            const message = data.message;

            // Clear the board
            const boardElement = document.getElementById("board");
            boardElement.innerHTML = "";

            // Set the --columns CSS variable to adjust the number of columns
            boardElement.style.setProperty("--columns", boardWidth);

            // Create board cells
            for (let i = 0; i < boardHeight; i++) {
                for (let j = 0; j < boardWidth; j++) {
                    const cell = document.createElement("div");
                    cell.id = `case-${i * boardWidth + j}`;
                    cell.onclick = () => makeMove(i, j); // Utiliser i et j directement
                    boardElement.appendChild(cell);
                }
            }

            // Update UI with board and message
            updateUI(board, message);
        })
        .catch((error) => console.error("Error starting game: ", error));
}

function makeMove(x, y) {
    fetch("http://127.0.0.1:8000/make_move/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            x: parseInt(x),
            y: parseInt(y),
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const board = data.board;
            const message = data.message;
            updateUI(board, message);
        })
        .catch((error) => console.error("Error making move: ", error));
}

function updateUI(board, message) {
    const messageElement = document.getElementById("message");
    messageElement.innerText = message;

    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            const cellId = `case-${i * boardWidth + j}`;
            const boardCaseElement = document.getElementById(cellId);

            // Add debugging logs
            if (!boardCaseElement) {
                console.error(`Element with ID ${cellId} not found.`);
            }

            boardCaseElement.innerText = board[i][j] === 0 ? " " : board[i][j];
        }
    }
}

let solving = false;

function solvePuzzle() {
    if (!solving) {
        solving = true;
        animateSolution();
    }
}

function animateSolution() {
    fetch("http://127.0.0.1:8000/solve_game/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            geometry: "manhattan",
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const solution = data.solution;
            const elapsedTime = data.elapsed_time;

            if (solution.length > 0) {
                let currentIndex = 0;
                const intervalId = setInterval(() => {
                    if (currentIndex < solution.length) {
                        const board = solution[currentIndex];
                        updateUI(
                            board,
                            `Solving puzzle... Step ${currentIndex + 1}`
                        );
                        currentIndex++;
                    } else {
                        clearInterval(intervalId);
                        solving = false;
                        updateUI(
                            board,
                            `Puzzle solved in ${elapsedTime.toFixed(2)} seconds`
                        );
                    }
                }, 500);
            } else {
                console.error("No solution found");
                solving = false;
            }
        })
        .catch((error) => {
            console.error("Error solving puzzle: ", error);
            solving = false;
        });
}

// Call startGame() initially to create the initial board
startGame();

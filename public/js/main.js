let board = [];
let message = "";

function startGame() {
    fetch("http://127.0.0.1:8000/start_game/")
        .then((response) => response.json())
        .then((data) => {
            board = data.board;
            message = data.message;
            updateUI();
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
            (board = data.board), (message = data.message);
            updateUI();
        })
        .catch((error) => console.error("Error making move: ", error));
}

function updateUI() {
    const messageElement = document.getElementById("message");

    messageElement.innerText = message;

    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const boardCaseElement = document.getElementById(
                "case-" + (i * 3 + j)
            );
            boardCaseElement.innerText = board[i][j] == 0 ? " " : board[i][j];
        }
    }
}

from fastapi import FastAPI, HTTPException

from src.Teasing import Teasing

app = FastAPI()

game = None


@app.get("/start_game/")
async def start_game():
    global game
    game = Teasing()
    return {"message": "Game started!", "board": game.board.tolist()}


@app.post("/make_move/")
async def make_move(pos: tuple, direction: str):
    global game
    if game is None:
        raise HTTPException(
            status_code=400, detail="Game not started. Please start a game first.")

    pos = tuple(pos)
    try:
        game.move(pos, direction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if game.win():
        return {"message": "You won!", "board": game.board.tolist()}
    else:
        return {"message": "Move successful", "board": game.board.tolist}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.Teasing import Teasing


class Position(BaseModel):
    x: int
    y: int


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = None


@app.get("/start_game/")
async def start_game():
    global game
    game = Teasing()
    return {"message": "Game started!", "board": game.board.tolist()}


@app.post("/make_move/")
async def make_move(pos: Position):
    global game
    if game is None:
        raise HTTPException(
            status_code=400, detail="Game not started. Please start a game first.")

    pos = tuple((pos.x, pos.y))
    try:
        game.move(pos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if game.win():
        return {"message": "You won!", "board": game.board.tolist()}
    else:
        return {"message": "Move successful", "board": game.board.tolist()}

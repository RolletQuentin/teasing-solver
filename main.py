from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.Teasing import Teasing
from src.Solver import Solver


class Position(BaseModel):
    x: int
    y: int


class TeasingModel(BaseModel):
    x: int
    y: int
    seed: int


class SolverModel(BaseModel):
    geometry: str


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


@app.post("/start_game/")
async def start_game(teasing: TeasingModel):
    global game
    game = Teasing(teasing.x, teasing.y, teasing.seed)
    return {"message": "Game started!", "board": game.board.tolist()}


@app.get("/get_game_state/")
async def get_game_state():
    if game is None:
        raise HTTPException(
            status_code=400, detail="Game not started. Please start a game first.")
    return {"board": game.board.tolist()}


@app.post("/make_move/")
async def make_move(pos: Position):
    global game
    if game is None:
        raise HTTPException(
            status_code=400, detail="Game not started. Please start a game first.")

    try:
        pos = tuple((pos.x, pos.y))
        game.move(pos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Move successful", "board": game.board.tolist()}


@app.post("/solve_game/")
async def solve_game(solver_model: SolverModel):
    global game, solver
    if game is None:
        raise HTTPException(
            status_code=400, detail="Game not started. Please start a game first.")

    solver = Solver(solver_model.geometry)
    result = solver.a_star(game)
    return {"solution": [node.game.board.tolist() for node in result['solution']],
            "elapsed_time": result['elapsed_time']}

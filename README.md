# Teasing solver

This is a school project.
Here is an implementation of the teasing game, in Python, and a solver using the A\* alogorithm.

## Installation

First, you can clone the project :

```
git clone https://github.com/RolletQuentin/teasing-solver
cd teasing-solver
```

Then you have to activate an Python environment (optionnal) and install the requirements :

```
python3 -m venv .venv
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

## Run

Run this program :

```
.venv/bin/uvicorn main:app --reload
```

This will start an API to use the Web Iser Interface. You can then open the file `index.html` and try the application !

⚠️ Be careful ! Your Python version may not the same as my version ! ⚠️

## How to use it

When you are on the website, you can choose the size of the puzzle and then start a game. You can play to the puzzle (click on the tiles) or ask to the program to solve it.

The solver works with 3x3 puzzle in less than 1 second, please wait the solution.

For the 4x4, you can wait ~1/2 minutes.

For the 5x5, you can wait ~10 minutes.

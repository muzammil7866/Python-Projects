# N-Queen Problem using Hill Climbing and Stochastic Hill Climbing

This project solves the N-Queen problem using two local-search algorithms and provides both CLI and GUI execution modes.

## Implemented Algorithms

- Hill Climbing
- Stochastic Hill Climbing

## Project Files

- `nqueen.py`: solver implementation with CLI and Tkinter GUI
- `libs/`: shared search/util modules
- `images/`: queen image asset used for optional plotting
- `requirements.txt`: project dependencies

## Setup

From workspace root:

```powershell
& "C:\Users\muzam\Desktop\projects\Python Projects\AI Assignments\.venv\Scripts\python.exe" -m pip install -r ".\3\N Queen Problem using HillClimbing and StochasticHillClimbing\requirements.txt"
```

Move into this folder:

```powershell
Set-Location "C:\Users\muzam\Desktop\projects\Python Projects\AI Assignments\3\N Queen Problem using HillClimbing and StochasticHillClimbing"
```

## Run

Default CLI run:

```powershell
python .\nqueen.py
```

Custom run:

```powershell
python .\nqueen.py --n 8 --trials 10 --seed 42
```

GUI mode:

```powershell
python .\nqueen.py --gui
```

Optional plotting mode:

```powershell
python .\nqueen.py --plot
```

## CLI Arguments

- `--n`: number of queens (default `8`)
- `--trials`: number of runs per algorithm (default `10`)
- `--seed`: random seed for reproducibility
- `--plot`: plot resulting board states with matplotlib
- `--gui`: launch interactive Tkinter interface

## GUI Behavior

- Click `Random Board` to generate a new initial state.
- Click `Solve` to run selected algorithm.
- After a solved board is found, `Solve` is locked.
- `Solve` is unlocked only when inputs change (seed, board size, algorithm) or when `Random Board` is clicked.

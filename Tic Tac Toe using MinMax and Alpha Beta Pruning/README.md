# Tic Tac Toe using MinMax and Alpha Beta Pruning

This project implements Tic Tac Toe with optimal AI decision-making using MinMax and Alpha-Beta Pruning. It supports terminal and GUI modes.

## Implemented Algorithms

- MinMax
- Alpha-Beta Pruning

## Project Files

- `tictactoe.py`: game implementation with CLI and Tkinter GUI
- `libs/`: shared game/search/util modules
- `requirements.txt`: project dependencies

## Setup

From workspace root:

```powershell
& "C:\Users\muzam\Desktop\projects\Python Projects\AI Assignments\.venv\Scripts\python.exe" -m pip install -r ".\3\Tic Tac Toe using MinMax and Alpha Beta Pruning\requirements.txt"
```

Move into this folder:

```powershell
Set-Location "C:\Users\muzam\Desktop\projects\Python Projects\AI Assignments\3\Tic Tac Toe using MinMax and Alpha Beta Pruning"
```

## Run

Scripted demo run:

```powershell
python .\tictactoe.py
```

Human vs Human in terminal:

```powershell
python .\tictactoe.py --play
```

Human vs AI in terminal with MinMax:

```powershell
python .\tictactoe.py --play-ai --algorithm minimax
```

Human vs AI in terminal with Alpha-Beta:

```powershell
python .\tictactoe.py --play-ai --algorithm alphabeta
```

GUI mode:

```powershell
python .\tictactoe.py --gui
```

## CLI Arguments

- `--play`: terminal Human vs Human
- `--play-ai`: terminal Human vs AI
- `--algorithm`: AI algorithm for `--play-ai` and GUI AI mode
  - `minimax`
  - `alphabeta` (default)
- `--gui`: launch Tkinter GUI

## GUI Features

- Mode selection: Human vs Human or Human vs AI
- Algorithm selection for AI: MinMax or Alpha-Beta
- Live round status and score tracking
- Restart round and reset score controls

import argparse
from typing import Iterable, Tuple

import tkinter as tk
from tkinter import ttk

from libs.games import TicTacToe, alpha_beta_search, minmax_decision

Move = Tuple[int, int]


def print_board(game: TicTacToe, state) -> None:
    board = state.board
    print()
    for y in range(1, game.v + 1):
        row = []
        for x in range(1, game.h + 1):
            row.append(board.get((x, y), "."))
        print(" ".join(row))
    print()


def apply_moves(game: TicTacToe, moves: Iterable[Move]) -> None:
    state = game.initial
    print("Initial board:")
    print_board(game, state)

    for idx, move in enumerate(moves, start=1):
        player = game.to_move(state)
        if move not in game.actions(state):
            print(f"Move {idx} by {player} rejected (invalid move): {move}")
            continue

        state = game.result(state, move)
        print(f"Move {idx}: player {player} -> {move}")
        print_board(game, state)

        if game.terminal_test(state):
            utility_for_x = game.utility(state, "X")
            if utility_for_x == 0:
                print("Result: Draw")
            elif utility_for_x > 0:
                print("Result: X wins")
            else:
                print("Result: O wins")
            return

    print("Game not finished yet.")


def run_demo() -> None:
    # Same sample moves used in the notebook cell.
    demo_moves = [(3, 3), (1, 1), (1, 3)]
    game = TicTacToe()
    apply_moves(game, demo_moves)


def play_cli() -> None:
    game = TicTacToe()
    state = game.initial

    print("Tic-Tac-Toe (enter moves as: x y, values 1..3)")
    print_board(game, state)

    while not game.terminal_test(state):
        player = game.to_move(state)
        raw = input(f"Player {player} move: ").strip()
        try:
            x_str, y_str = raw.split()
            move = (int(x_str), int(y_str))
        except Exception:
            print("Invalid input format. Use: x y")
            continue

        if move not in game.actions(state):
            print("Invalid move. Cell is occupied or out of range.")
            continue

        state = game.result(state, move)
        print_board(game, state)

    utility_for_x = game.utility(state, "X")
    if utility_for_x == 0:
        print("Result: Draw")
    elif utility_for_x > 0:
        print("Result: X wins")
    else:
        print("Result: O wins")


def choose_ai_move(game: TicTacToe, state, algorithm: str) -> Move:
    if algorithm == "minimax":
        move = minmax_decision(state, game)
    else:
        move = alpha_beta_search(state, game)
    return move


def play_cli_ai(algorithm: str) -> None:
    game = TicTacToe()
    state = game.initial

    print(f"Tic-Tac-Toe Human vs AI ({algorithm})")
    print("You are X. Enter moves as: x y, values 1..3")
    print_board(game, state)

    while not game.terminal_test(state):
        player = game.to_move(state)
        if player == "X":
            raw = input("Your move: ").strip()
            try:
                x_str, y_str = raw.split()
                move = (int(x_str), int(y_str))
            except Exception:
                print("Invalid input format. Use: x y")
                continue

            if move not in game.actions(state):
                print("Invalid move. Cell is occupied or out of range.")
                continue
        else:
            move = choose_ai_move(game, state, algorithm)
            print(f"AI ({algorithm}) plays: {move}")

        state = game.result(state, move)
        print_board(game, state)

    utility_for_x = game.utility(state, "X")
    if utility_for_x == 0:
        print("Result: Draw")
    elif utility_for_x > 0:
        print("Result: X wins")
    else:
        print("Result: O wins")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Terminal Tic-Tac-Toe based on libs.games.TicTacToe")
    parser.add_argument("--play", action="store_true", help="Run interactive terminal play mode")
    parser.add_argument("--play-ai", action="store_true", help="Run terminal mode against AI")
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")
    parser.add_argument(
        "--algorithm",
        choices=("minimax", "alphabeta"),
        default="alphabeta",
        help="AI algorithm for --play-ai and GUI Human vs AI mode",
    )
    return parser.parse_args()


class TicTacToeGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe GUI")
        self.root.geometry("540x660")
        self.root.configure(bg="#f6f1e9")

        self.game = TicTacToe()
        self.state = self.game.initial
        self.mode_var = tk.StringVar(value="Human vs Human")
        self.algorithm_var = tk.StringVar(value="alphabeta")

        self.status_var = tk.StringVar(value="Player X turn")
        self.score_var = tk.StringVar(value="Wins - X: 0 | O: 0 | Draws: 0")
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        self.buttons = {}
        self._build_ui()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg="#264653", padx=16, pady=14)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Tic-Tac-Toe",
            fg="#f1faee",
            bg="#264653",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Play human-vs-human or human-vs-AI with Minimax/Alpha-Beta",
            fg="#d7ece8",
            bg="#264653",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        controls = tk.Frame(self.root, bg="#f6f1e9", padx=16, pady=8)
        controls.pack(fill="x")
        tk.Label(controls, text="Mode", bg="#f6f1e9", fg="#1f2933", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        mode_box = ttk.Combobox(controls, textvariable=self.mode_var, state="readonly", width=18)
        mode_box["values"] = ("Human vs Human", "Human vs AI")
        mode_box.grid(row=1, column=0, padx=(0, 12), sticky="w")

        tk.Label(controls, text="AI Algorithm", bg="#f6f1e9", fg="#1f2933", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")
        algorithm_box = ttk.Combobox(controls, textvariable=self.algorithm_var, state="readonly", width=12)
        algorithm_box["values"] = ("alphabeta", "minimax")
        algorithm_box.grid(row=1, column=1, padx=(0, 12), sticky="w")

        tk.Button(
            controls,
            text="Apply Mode",
            command=self.restart_round,
            bg="#2a9d8f",
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=4,
        ).grid(row=1, column=2, sticky="w")

        status = tk.Frame(self.root, bg="#f6f1e9", padx=16, pady=10)
        status.pack(fill="x")
        tk.Label(status, textvariable=self.status_var, bg="#f6f1e9", fg="#1f2933", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(status, textvariable=self.score_var, bg="#f6f1e9", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        board_frame = tk.Frame(self.root, bg="#f6f1e9", padx=16, pady=8)
        board_frame.pack(fill="both", expand=True)

        for row in range(3):
            board_frame.grid_rowconfigure(row, weight=1)
            board_frame.grid_columnconfigure(row, weight=1)

        for y in range(1, 4):
            for x in range(1, 4):
                btn = tk.Button(
                    board_frame,
                    text="",
                    command=lambda m=(x, y): self.on_click(m),
                    font=("Segoe UI", 32, "bold"),
                    relief="flat",
                    bg="#fffaf2",
                    activebackground="#f3e9d8",
                    fg="#1f2933",
                    width=4,
                    height=2,
                )
                btn.grid(row=y - 1, column=x - 1, sticky="nsew", padx=6, pady=6)
                self.buttons[(x, y)] = btn

        footer = tk.Frame(self.root, bg="#f6f1e9", padx=16, pady=12)
        footer.pack(fill="x")
        tk.Button(
            footer,
            text="Restart Round",
            command=self.restart_round,
            bg="#e76f51",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="left")
        tk.Button(
            footer,
            text="Reset Score",
            command=self.reset_score,
            bg="#2a9d8f",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=8,
        ).pack(side="left", padx=(10, 0))

    def _refresh_board(self) -> None:
        for move, btn in self.buttons.items():
            mark = self.state.board.get(move, "")
            btn.config(text=mark)
            if mark == "X":
                btn.config(fg="#1d3557")
            elif mark == "O":
                btn.config(fg="#b00020")
            else:
                btn.config(fg="#1f2933")

        is_terminal = self.game.terminal_test(self.state)
        for move, btn in self.buttons.items():
            btn.config(state="disabled" if is_terminal or move not in self.game.actions(self.state) else "normal")

    def _update_score_text(self) -> None:
        self.score_var.set(f"Wins - X: {self.x_wins} | O: {self.o_wins} | Draws: {self.draws}")

    def on_click(self, move: Move) -> None:
        if move not in self.game.actions(self.state) or self.game.terminal_test(self.state):
            return

        player = self.game.to_move(self.state)
        self.state = self.game.result(self.state, move)
        self._refresh_board()

        if self.game.terminal_test(self.state):
            utility_for_x = self.game.utility(self.state, "X")
            if utility_for_x == 1:
                self.x_wins += 1
                self.status_var.set("X wins this round")
            elif utility_for_x == -1:
                self.o_wins += 1
                self.status_var.set("O wins this round")
            else:
                self.draws += 1
                self.status_var.set("Round is a draw")
            self._update_score_text()
            return

        if self.mode_var.get() == "Human vs AI" and self.game.to_move(self.state) == "O":
            ai_algorithm = self.algorithm_var.get()
            ai_move = choose_ai_move(self.game, self.state, ai_algorithm)
            self.state = self.game.result(self.state, ai_move)
            self._refresh_board()

            if self.game.terminal_test(self.state):
                utility_for_x = self.game.utility(self.state, "X")
                if utility_for_x == 1:
                    self.x_wins += 1
                    self.status_var.set("X wins this round")
                elif utility_for_x == -1:
                    self.o_wins += 1
                    self.status_var.set(f"AI ({ai_algorithm}) wins this round")
                else:
                    self.draws += 1
                    self.status_var.set("Round is a draw")
                self._update_score_text()
                return

            self.status_var.set(f"Player {self.game.to_move(self.state)} turn")
            return

        self.status_var.set(f"Player {self.game.to_move(self.state)} turn")

    def restart_round(self) -> None:
        self.state = self.game.initial
        self.status_var.set("Player X turn")
        self._refresh_board()

    def reset_score(self) -> None:
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self._update_score_text()
        self.restart_round()

    def run(self) -> None:
        self._refresh_board()
        self.root.mainloop()


def launch_gui() -> None:
    app = TicTacToeGUI()
    app.run()


def main() -> None:
    args = parse_args()
    if args.gui:
        launch_gui()
    elif args.play_ai:
        play_cli_ai(args.algorithm)
    elif args.play:
        play_cli()
    else:
        run_demo()


if __name__ == "__main__":
    main()

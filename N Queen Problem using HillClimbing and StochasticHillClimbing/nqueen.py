import argparse
import random
from pathlib import Path
from typing import List, Optional, Tuple

import tkinter as tk
from tkinter import ttk

from libs.search import NQueensProblem


def random_start(n: int = 8) -> List[int]:
    return [random.randint(0, n - 1) for _ in range(n)]


def count_collisions(positions: List[int]) -> int:
    collisions = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if positions[i] == positions[j] or abs(i - j) == abs(positions[i] - positions[j]):
                collisions += 1
    return collisions


def acceptance_probability(current_collisions: int, neighbor_collisions: int, iteration: int) -> float:
    if neighbor_collisions <= current_collisions:
        return 1.0
    # Keep the notebook's gradually stricter acceptance behavior.
    t = max(iteration, 1)
    return 1.0 / (1 + (neighbor_collisions - current_collisions) * (t / 1000.0))


def successor(problem: NQueensProblem) -> NQueensProblem:
    state = list(problem.initial)
    queen_to_move = random.randint(0, len(state) - 1)
    new_position = random.randint(0, len(state) - 1)
    state[queen_to_move] = new_position

    nxt = NQueensProblem(len(state))
    nxt.initial = state
    return nxt


def hill_climbing(problem: NQueensProblem, max_iterations: int = 1000) -> Tuple[NQueensProblem, int]:
    current = problem
    if count_collisions(current.initial) == 0:
        return current, 0
    for i in range(max_iterations):
        neighbor = successor(current)
        if count_collisions(neighbor.initial) <= count_collisions(current.initial):
            current = neighbor
        if count_collisions(current.initial) == 0:
            return current, i + 1
    return current, max_iterations


def stochastic_hill_climbing(problem: NQueensProblem, max_iterations: int = 1000) -> Tuple[NQueensProblem, int]:
    current = problem
    if count_collisions(current.initial) == 0:
        return current, 0
    for i in range(max_iterations):
        neighbor = successor(current)
        p_accept = acceptance_probability(
            count_collisions(current.initial),
            count_collisions(neighbor.initial),
            i,
        )
        if random.random() <= p_accept:
            current = neighbor
        if count_collisions(current.initial) == 0:
            return current, i + 1
    return current, max_iterations


def plot_nqueens(solution: List[int]) -> None:
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from PIL import Image
    except Exception as exc:
        print(f"Plot skipped (missing plotting dependency): {exc}")
        return

    image_path = Path(__file__).parent / "images" / "queen_s.png"
    if not image_path.exists():
        print(f"Plot skipped (missing image): {image_path}")
        return

    n = len(solution)
    board = np.array([2 * int((i + j) % 2) for j in range(n) for i in range(n)]).reshape((n, n))
    im = np.array(Image.open(image_path)).astype(float) / 255

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    ax.set_title(f"{n} Queens")
    plt.imshow(board, cmap="binary", interpolation="nearest")

    for (k, v) in enumerate(solution):
        newax = fig.add_axes([
            0.064 + (k * 0.896 / n),
            ((n - v) * 0.896 / n) - 0.5 / n + n * 0.002,
            0.8 / n,
            0.8 / n,
        ], zorder=1)
        newax.imshow(im)
        newax.axis("off")

    fig.tight_layout()
    plt.show()


def run_trials(trials: int, n: int, seed: Optional[int], plot: bool) -> None:
    if seed is not None:
        random.seed(seed)

    first_initial_state: Optional[List[int]] = None

    print("=== Hill Climbing ===")
    hc_results = []
    for i in range(trials):
        initial_state = random_start(n)
        if i == 0:
            first_initial_state = initial_state[:]

        problem = NQueensProblem(n)
        problem.initial = initial_state
        result, iterations = hill_climbing(problem)
        hc_results.append((i + 1, initial_state, result.initial, iterations))

        print(
            f"Run {i + 1}: initial={initial_state}, final={result.initial}, "
            f"collisions={count_collisions(result.initial)}, iterations={iterations}"
        )
        if plot:
            plot_nqueens(result.initial)

    print("\nHC iterations:", [r[3] for r in hc_results])

    print("\n=== Stochastic Hill Climbing ===")
    shc_results = []
    for i in range(trials):
        if i == 0 and first_initial_state is not None:
            initial_state = first_initial_state[:]
        else:
            initial_state = random_start(n)

        problem = NQueensProblem(n)
        problem.initial = initial_state
        result, iterations = stochastic_hill_climbing(problem)
        shc_results.append((i + 1, initial_state, result.initial, iterations))

        print(
            f"Run {i + 1}: initial={initial_state}, final={result.initial}, "
            f"collisions={count_collisions(result.initial)}, iterations={iterations}"
        )
        if plot:
            plot_nqueens(result.initial)

    print("\nSHC iterations:", [r[3] for r in shc_results])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="N-Queens hill climbing and stochastic hill climbing.")
    parser.add_argument("--n", type=int, default=8, help="Number of queens (board size)")
    parser.add_argument("--trials", type=int, default=10, help="Number of runs per algorithm")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--plot", action="store_true", help="Plot board states using matplotlib/Pillow")
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")
    return parser.parse_args()


class NQueensGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("N-Queens Visual Solver")
        self.root.geometry("940x720")
        self.root.configure(bg="#f4efe7")

        self.board_size_var = tk.IntVar(value=8)
        self.seed_var = tk.StringVar(value="")
        self.algorithm_var = tk.StringVar(value="Hill Climbing")
        self.iterations_var = tk.StringVar(value="Iterations: -")
        self.collisions_var = tk.StringVar(value="Collisions: -")
        self.status_var = tk.StringVar(value="Set options and click Solve")

        self.current_solution: Optional[List[int]] = None
        self.solve_locked = False

        # Any user input change unlocks solve after a completed solution.
        self.seed_var.trace_add("write", self._on_input_changed)
        self.board_size_var.trace_add("write", self._on_input_changed)
        self.algorithm_var.trace_add("write", self._on_input_changed)

        self._build_ui()
        self._draw_board([0] * self.board_size_var.get(), draw_queens=False)

    def _on_input_changed(self, *_args) -> None:
        if self.solve_locked:
            self.solve_locked = False
            self.status_var.set("Input changed. Click Solve to run again.")

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg="#183a37", padx=18, pady=12)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="N-Queens: Hill Climbing vs Stochastic Hill Climbing",
            fg="#f7f3ea",
            bg="#183a37",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Choose board size and algorithm, then visualize the resulting arrangement.",
            fg="#dbe7e4",
            bg="#183a37",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w")

        controls = tk.Frame(self.root, bg="#f4efe7", padx=12, pady=12)
        controls.pack(fill="x")

        tk.Label(controls, text="Board Size", bg="#f4efe7", fg="#2f2f2f", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        size_box = ttk.Combobox(controls, textvariable=self.board_size_var, state="readonly", width=8)
        size_box["values"] = (4, 5, 6, 7, 8, 9, 10, 12)
        size_box.grid(row=1, column=0, padx=(0, 14), sticky="w")

        tk.Label(controls, text="Algorithm", bg="#f4efe7", fg="#2f2f2f", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")
        algo_box = ttk.Combobox(controls, textvariable=self.algorithm_var, state="readonly", width=28)
        algo_box["values"] = ("Hill Climbing", "Stochastic Hill Climbing")
        algo_box.grid(row=1, column=1, padx=(0, 14), sticky="w")

        tk.Label(controls, text="Seed (optional)", bg="#f4efe7", fg="#2f2f2f", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w")
        tk.Entry(controls, textvariable=self.seed_var, width=12).grid(row=1, column=2, padx=(0, 14), sticky="w")

        tk.Button(
            controls,
            text="Random Board",
            command=self.generate_random_board,
            bg="#f28f3b",
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=3, padx=(0, 10))

        tk.Button(
            controls,
            text="Solve",
            command=self.solve,
            bg="#2a9d8f",
            fg="white",
            relief="flat",
            padx=20,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=4)

        info = tk.Frame(self.root, bg="#f4efe7", padx=12, pady=4)
        info.pack(fill="x")
        tk.Label(info, textvariable=self.iterations_var, bg="#f4efe7", fg="#183a37", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 16))
        tk.Label(info, textvariable=self.collisions_var, bg="#f4efe7", fg="#183a37", font=("Segoe UI", 10, "bold")).pack(side="left")

        self.canvas = tk.Canvas(self.root, width=660, height=560, bg="#fffdf8", highlightthickness=0)
        self.canvas.pack(padx=12, pady=(8, 6), fill="both", expand=True)

        status_frame = tk.Frame(self.root, bg="#efe7d8", padx=12, pady=8)
        status_frame.pack(fill="x")
        tk.Label(status_frame, textvariable=self.status_var, bg="#efe7d8", fg="#3b3b3b", font=("Segoe UI", 10)).pack(anchor="w")

    def _draw_board(self, state: List[int], draw_queens: bool = True) -> None:
        n = len(state)
        self.canvas.delete("all")

        canvas_w = max(500, self.canvas.winfo_width())
        canvas_h = max(500, self.canvas.winfo_height())
        board_size = min(canvas_w - 40, canvas_h - 40)
        x0 = (canvas_w - board_size) / 2
        y0 = (canvas_h - board_size) / 2
        cell = board_size / n

        light = "#f2e9dc"
        dark = "#b08968"
        queen_fill = "#1d3557"
        queen_outline = "#0b1f33"

        for row in range(n):
            for col in range(n):
                x1 = x0 + col * cell
                y1 = y0 + row * cell
                x2 = x1 + cell
                y2 = y1 + cell
                color = light if (row + col) % 2 == 0 else dark
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        if draw_queens:
            for col, row in enumerate(state):
                cx = x0 + col * cell + (cell / 2)
                cy = y0 + row * cell + (cell / 2)
                r = cell * 0.28
                self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=queen_fill, outline=queen_outline, width=2)
                self.canvas.create_text(cx, cy, text="Q", fill="#f1faee", font=("Segoe UI", int(max(10, cell * 0.24)), "bold"))

    def _build_problem(self, n: int, initial_state: Optional[List[int]] = None) -> NQueensProblem:
        p = NQueensProblem(n)
        p.initial = initial_state if initial_state is not None else random_start(n)
        return p

    def generate_random_board(self) -> None:
        n = self.board_size_var.get()
        if self.seed_var.get().strip():
            try:
                random.seed(int(self.seed_var.get().strip()))
            except ValueError:
                self.status_var.set("Invalid seed. Enter an integer or leave empty.")
                return

        state = random_start(n)
        self.current_solution = state
        self.solve_locked = False
        self.iterations_var.set("Iterations: -")
        self.collisions_var.set(f"Collisions: {count_collisions(state)}")
        self.status_var.set("Random initial state generated")
        self._draw_board(state)

    def solve(self) -> None:
        if self.solve_locked:
            self.status_var.set("Board already solved. Click Random Board or change inputs to solve again.")
            return

        n = self.board_size_var.get()
        seed_text = self.seed_var.get().strip()
        if seed_text:
            try:
                random.seed(int(seed_text))
            except ValueError:
                self.status_var.set("Invalid seed. Enter an integer or leave empty.")
                return

        base_state = self.current_solution[:] if self.current_solution is not None and len(self.current_solution) == n else random_start(n)
        if count_collisions(base_state) == 0:
            base_state = random_start(n)
            self.status_var.set("Board was already solved. Generated a new random start state.")

        problem = self._build_problem(n, base_state)

        if self.algorithm_var.get() == "Hill Climbing":
            result, iterations = hill_climbing(problem)
        else:
            result, iterations = stochastic_hill_climbing(problem)

        final_state = list(result.initial)
        final_collisions = count_collisions(final_state)
        self.current_solution = final_state

        self._draw_board(final_state)
        self.iterations_var.set(f"Iterations: {iterations}")
        self.collisions_var.set(f"Collisions: {final_collisions}")
        if final_collisions == 0:
            self.solve_locked = True
            self.status_var.set("Solved: non-attacking configuration found")
        else:
            self.status_var.set("Local optimum reached; try another seed or random board")

    def run(self) -> None:
        self.root.mainloop()


def launch_gui() -> None:
    app = NQueensGUI()
    app.run()


def main() -> None:
    args = parse_args()
    if args.gui:
        launch_gui()
        return
    run_trials(trials=args.trials, n=args.n, seed=args.seed, plot=args.plot)


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox
import random
import heapq
import threading
import itertools

# ==========================================
# PART 1: The Logic (Robust & Self-Contained)
# ==========================================

class EightPuzzleLogic:
    """
    Game logic for the 8-Puzzle. 
    """
    def __init__(self, initial_state):
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        # We don't store state here to keep logic pure/stateless
        
    def actions(self, state):
        """Returns list of valid moves (indices to swap with 0)."""
        try:
            zero_idx = state.index(0)
        except ValueError:
            return [] # Safety check
            
        row, col = zero_idx // 3, zero_idx % 3
        moves = []
        
        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                move_idx = r * 3 + c
                moves.append(move_idx)
        return moves

    def result(self, state, move_idx):
        """Returns a new state tuple after swapping 0 with move_idx."""
        new_state = list(state)
        zero_idx = state.index(0)
        new_state[zero_idx], new_state[move_idx] = new_state[move_idx], new_state[zero_idx]
        return tuple(new_state)

# ==========================================
# PART 2: The Enhanced GUI
# ==========================================

class EightPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle AI Solver (Fixed)")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Game State
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        self.state = list(self.goal_state)
        self.logic = EightPuzzleLogic(tuple(self.state))
        self.is_solving = False

        self.buttons = []
        self.create_widgets()
        
        # Scramble initially
        self.scramble_animation()

    def create_widgets(self):
        # --- Header ---
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(pady=10)
        tk.Label(header_frame, text="8 Puzzle Challenge", font=("Helvetica", 22, "bold"), bg="#f0f0f0", fg="#333").pack()

        # --- Puzzle Grid ---
        self.puzzle_frame = tk.Frame(self.root, bg="#333", bd=5)
        self.puzzle_frame.pack(pady=10)

        for i in range(9):
            btn = tk.Button(self.puzzle_frame, text="", 
                          font=('Helvetica', 30, 'bold'),
                          width=4, height=2,
                          command=lambda idx=i: self.handle_click(idx))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)

        self.update_gui()

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to play")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, 
                                   font=("Arial", 12), bg="#f0f0f0", fg="blue")
        self.status_label.pack(pady=5)

        # --- Controls ---
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)

        self.scramble_btn = tk.Button(control_frame, text="Scramble", 
                                    font=('Arial', 14), bg="#ffcc00", width=10,
                                    command=self.scramble_animation)
        self.scramble_btn.pack(side=tk.LEFT, padx=10)

        self.solve_btn = tk.Button(control_frame, text="Solve (AI)", 
                                 font=('Arial', 14), bg="#4caf50", fg="white", width=10,
                                 command=self.start_solver_thread)
        self.solve_btn.pack(side=tk.LEFT, padx=10)

    def update_gui(self):
        """Refreshes the button faces based on self.state."""
        for i, val in enumerate(self.state):
            if val == 0:
                self.buttons[i].config(text="", bg="#d3d3d3", state=tk.DISABLED, relief=tk.SUNKEN)
            else:
                self.buttons[i].config(text=str(val), bg="#ffffff", fg="#333", state=tk.NORMAL, relief=tk.RAISED)

    def handle_click(self, index):
        """Handles manual user moves."""
        if self.is_solving: return

        zero_index = self.state.index(0)
        r_click, c_click = index // 3, index % 3
        r_zero, c_zero = zero_index // 3, zero_index % 3
        
        # Manhattan distance == 1 means adjacent
        dist = abs(r_click - r_zero) + abs(c_click - c_zero)

        if dist == 1:
            self.state[zero_index], self.state[index] = self.state[index], self.state[zero_index]
            self.update_gui()
            
            if tuple(self.state) == self.goal_state:
                self.status_var.set("🎉 Puzzle Solved!")
                messagebox.showinfo("Success", "You solved it!")

    # ==========================
    # Logic: Scramble
    # ==========================
    def scramble_animation(self):
        if self.is_solving: return
        self.status_var.set("Scrambling...")
        self.root.update()
        
        # Perform a random walk to ensure solvability
        current = tuple(self.goal_state)
        for _ in range(30): # 30 random moves
            actions = self.logic.actions(current)
            move = random.choice(actions)
            current = self.logic.result(current, move)
        
        self.state = list(current)
        self.update_gui()
        self.status_var.set("Ready")
        print("Scramble complete. State:", self.state)

    # ==========================
    # Logic: Solver (A*)
    # ==========================
    def manhattan_distance(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != 0:
                goal_pos = self.goal_state.index(tile)
                # Row difference + Column difference
                distance += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
        return distance

    def start_solver_thread(self):
        """Starts the solver in a separate thread to keep GUI responsive."""
        if tuple(self.state) == self.goal_state:
            self.status_var.set("Already solved!")
            return

        self.is_solving = True
        self.scramble_btn.config(state=tk.DISABLED)
        self.solve_btn.config(state=tk.DISABLED)
        self.status_var.set("AI is thinking...")
        print("Starting solver thread...")
        
        # Threading
        thread = threading.Thread(target=self.run_astar)
        thread.daemon = True
        thread.start()

    def run_astar(self):
        """The heavy lifting A* algorithm running in background."""
        try:
            start_state = tuple(self.state)
            
            # Tie-breaker counter to avoid comparing paths/states directly if costs are equal
            counter = itertools.count() 
            
            # Priority Queue: (f_score, count, g_score, state, path)
            # We use 'count' as a tie-breaker so Python never tries to compare 'path' (which is a list)
            pq = [(self.manhattan_distance(start_state), next(counter), 0, start_state, [])]
            visited = {start_state: 0}
            
            solution_path = None
            nodes_explored = 0
            
            while pq:
                f, _, g, current, path = heapq.heappop(pq)
                nodes_explored += 1
                
                if current == self.goal_state:
                    solution_path = path
                    break
                
                # Check neighbors
                for move_idx in self.logic.actions(current):
                    successor = self.logic.result(current, move_idx)
                    new_g = g + 1
                    
                    if successor not in visited or new_g < visited[successor]:
                        visited[successor] = new_g
                        h = self.manhattan_distance(successor)
                        # Push to heap with tie-breaker
                        heapq.heappush(pq, (new_g + h, next(counter), new_g, successor, path + [move_idx]))
            
            print(f"Solver finished. Explored {nodes_explored} nodes.")
            # When done, schedule the animation on the main GUI thread
            self.root.after(0, lambda: self.animate_solution(solution_path))
            
        except Exception as e:
            print(f"Error in solver thread: {e}")
            self.root.after(0, lambda: self.handle_solver_error(str(e)))

    def handle_solver_error(self, error_msg):
        self.status_var.set("Error Occurred")
        messagebox.showerror("Solver Error", f"An error occurred:\n{error_msg}")
        self.reset_ui_state()

    def animate_solution(self, path):
        """Animates the solution steps using .after() for smoothness."""
        if path is None:
            self.status_var.set("No solution found.")
            messagebox.showwarning("Failed", "AI could not find a solution.")
            self.reset_ui_state()
            return

        self.status_var.set(f"Solving... ({len(path)} steps)")
        print(f"Solution Path found: {len(path)} moves.")
        
        def step(k):
            if k < len(path):
                move_idx = path[k]
                # Swap logic
                zero_idx = self.state.index(0)
                self.state[zero_idx], self.state[move_idx] = self.state[move_idx], self.state[zero_idx]
                self.update_gui()
                # Schedule next step in 250ms
                self.root.after(250, step, k + 1)
            else:
                self.status_var.set(f"Solved in {len(path)} moves!")
                messagebox.showinfo("Done", "AI Solved the Puzzle!")
                self.reset_ui_state()

        step(0)

    def reset_ui_state(self):
        self.is_solving = False
        self.scramble_btn.config(state=tk.NORMAL)
        self.solve_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = EightPuzzleGUI(root)
    root.mainloop()
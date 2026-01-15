import tkinter as tk
from tkinter import messagebox
from queue import Queue
import threading
import time

# Define Maze Layout (0: Free, 1: Wall, 2: Goal, 3: Start)
MAZE_LAYOUT = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class MazeGUI:
    def __init__(self, root, title="Maze Solver"):
        self.root = root
        self.root.title(title)
        self.root.geometry("600x650") # Set a reasonable default size
        self.cell_size = 25
        self.rows = len(MAZE_LAYOUT)
        self.cols = len(MAZE_LAYOUT[0])
        self.is_running = False

        # --- Top Control Panel ---
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, pady=10)

        self.start_btn = tk.Button(control_frame, text="Start BFS", bg="#4CAF50", fg="white", 
                                   font=("Arial", 12, "bold"), command=self.start_bfs_thread)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.reset_btn = tk.Button(control_frame, text="Reset", bg="#f44336", fg="white",
                                   font=("Arial", 12, "bold"), command=self.reset_maze)
        self.reset_btn.pack(side=tk.LEFT, padx=10)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 10), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # --- Canvas ---
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, 
                                height=self.rows * self.cell_size, bg="white", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)
        
        self.rects = {} # Store rectangle IDs for faster updates
        self.draw_maze_initial()
        
        # Find start and goal dynamically
        self.start_pos = self.find_pos(3)
        self.goal_pos = self.find_pos(2)

    def find_pos(self, value):
        """Scans the grid to find the coordinates of a specific value."""
        for r in range(self.rows):
            for c in range(self.cols):
                if MAZE_LAYOUT[r][c] == value:
                    return (r, c)
        return None

    def draw_maze_initial(self):
        """Draws the initial state of the maze."""
        self.canvas.delete("all")
        self.rects = {}
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"
                tag = "free"
                if MAZE_LAYOUT[r][c] == 1: 
                    color = "#2c3e50" # Dark Blue-Grey for walls
                    tag = "wall"
                elif MAZE_LAYOUT[r][c] == 2: 
                    color = "#e74c3c" # Red for Goal
                    tag = "goal"
                elif MAZE_LAYOUT[r][c] == 3: 
                    color = "#f1c40f" # Yellow for Start
                    tag = "start"
                
                rect_id = self.canvas.create_rectangle(
                    c * self.cell_size, r * self.cell_size,
                    (c + 1) * self.cell_size, (r + 1) * self.cell_size,
                    fill=color, outline="#ecf0f1", tags=tag
                )
                self.rects[(r, c)] = rect_id

    def reset_maze(self):
        """Resets the maze to its initial state."""
        if self.is_running:
            return # Don't reset while running
        self.draw_maze_initial()
        self.status_var.set("Status: Ready")
        self.start_btn.config(state=tk.NORMAL)

    def safe_update_cell(self, r, c, color):
        """Thread-safe method to update cell color via the main loop."""
        if MAZE_LAYOUT[r][c] not in [2, 3]: # Don't overwrite Start or Goal
             # Schedule the canvas update on the main thread
            self.root.after(0, lambda: self.canvas.itemconfig(self.rects[(r, c)], fill=color))

    def start_bfs_thread(self):
        """Initiates the BFS algorithm in a separate thread."""
        if self.is_running: return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.status_var.set("Status: Running BFS...")
        
        # Run BFS in a separate thread to keep UI responsive
        bfs_thread = threading.Thread(target=self.run_bfs)
        bfs_thread.daemon = True # Thread dies if app closes
        bfs_thread.start()

    def run_bfs(self):
        """The core Breadth-First Search logic."""
        start_time = time.time()
        queue = Queue()
        queue.put((self.start_pos, []))
        visited = set()
        visited.add(self.start_pos)
        
        nodes_explored = 0
        found = False
        final_path = []

        while not queue.empty():
            (curr_r, curr_c), path = queue.get()
            nodes_explored += 1
            
            # Update Status Bar occasionally (every 10 nodes to avoid UI lag)
            if nodes_explored % 10 == 0:
                 self.root.after(0, lambda n=nodes_explored: self.status_var.set(f"Status: Exploring... Nodes Visited: {n}"))

            if (curr_r, curr_c) == self.goal_pos:
                found = True
                final_path = path
                break
            
            # Visualize "Visited/Explored" (Light Blue)
            if (curr_r, curr_c) != self.start_pos:
                self.safe_update_cell(curr_r, curr_c, "#AED6F1") # Light Blue
            
            # Delay for visualization effect
            time.sleep(0.02) # Adjustable speed
            
            # Directions: Up, Right, Down, Left
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = curr_r + dr, curr_c + dc
                
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if MAZE_LAYOUT[nr][nc] != 1 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.put(((nr, nc), path + [(nr, nc)]))
                        
                        # Visualize "Frontier" (Light Green) - added to queue but not fully explored
                        if (nr, nc) != self.goal_pos:
                            self.safe_update_cell(nr, nc, "#A9DFBF") # Light Green

        self.root.after(0, lambda: self.finish_search(found, final_path, nodes_explored, time.time() - start_time))

    def finish_search(self, found, path, nodes, duration):
        """Handles post-search actions (popups, drawing path)."""
        self.is_running = False
        self.reset_btn.config(state=tk.NORMAL)
        
        if found:
            self.draw_path(path)
            self.status_var.set(f"Status: Goal Reached! Length: {len(path)} | Nodes: {nodes} | Time: {duration:.2f}s")
            messagebox.showinfo("Result", f"Goal Reached!\n\nPath Length: {len(path)}\nNodes Explored: {nodes}\nTime: {duration:.2f}s")
        else:
            self.status_var.set("Status: No Path Found")
            messagebox.showwarning("Result", "No path found to the goal.")

    def draw_path(self, path):
        """Draws the final path step-by-step."""
        def step(i):
            if i < len(path):
                r, c = path[i]
                if MAZE_LAYOUT[r][c] != 2: # Don't color over goal
                    self.canvas.itemconfig(self.rects[(r, c)], fill="#3498DB") # Darker Blue for Path
                self.root.after(30, step, i + 1) # Schedule next step
        
        step(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root, "Maze Solver - BFS (Enhanced)")
    root.mainloop()
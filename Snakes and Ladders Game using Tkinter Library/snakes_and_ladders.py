# snakes_and_ladders.py
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- Constants & Configuration ---
BOARD_SIZE = 10
CELL_SIZE = 60
CANVAS_SIZE = CELL_SIZE * BOARD_SIZE

# Snakes: start_position -> end_position
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
# Ladders: start_position -> end_position
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

PLAYER_COLORS = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#17becf", "#8c564b", "#7f7f7f"
]

# --- Helper Functions ---

def pos_to_grid(pos):
    """
    Convert board position (1-100) to grid coordinates (row, col).
    Row 0 is top, Col 0 is left.
    The board is numbered 1 at bottom-left, 100 at top-left, in a boustrophedon (serpentine) pattern.
    """
    if pos < 1 or pos > 100:
        return None
    idx = pos - 1
    row_from_bottom = idx // BOARD_SIZE
    col_in_row = idx % BOARD_SIZE

    # Even rows from bottom (0, 2, 4...) go Left -> Right
    # Odd rows from bottom (1, 3, 5...) go Right -> Left
    if row_from_bottom % 2 == 0:
        col = col_in_row
    else:
        col = (BOARD_SIZE - 1) - col_in_row
    
    # Tkinter grid row 0 is top
    row = (BOARD_SIZE - 1) - row_from_bottom
    return (row, col)

def grid_to_center(row, col):
    """Convert grid (row, col) to pixel coordinates of the cell center."""
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    return x, y

def pos_to_center(pos):
    """Convert board position (1-100) directly to pixel center coordinates."""
    row_col = pos_to_grid(pos)
    if not row_col:
        return None
    return grid_to_center(*row_col)


class SnakesLaddersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes & Ladders Game")

        self.setup_ui()
        
        self.players = []
        self.tokens = []
        self.positions = []
        self.turn_idx = 0
        self.game_over = False

        # Initialize Game
        self.setup_players()
        self.draw_board()
        self.draw_snakes_ladders()
        self.create_tokens()
        self.update_info_label()

    def setup_ui(self):
        """Initialize all UI components."""
        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.roll_btn = tk.Button(self.root, text="Roll Dice", command=self.roll_dice, font=("Arial", 12, "bold"))
        self.roll_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.info_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.info_label.grid(row=1, column=1, sticky="ew", padx=10)

        self.dice_label = tk.Label(self.root, text="🎲 -", font=("Arial", 16, "bold"))
        self.dice_label.grid(row=1, column=2, sticky="ew", padx=10)

    def setup_players(self):
        """Ask user for number of players and their names."""
        num_players = None
        while num_players is None:
            try:
                num_players = simpledialog.askinteger("Players", "How many players? (2-6)", 
                                                      minvalue=2, maxvalue=6, parent=self.root)
                if num_players is None:
                    # Cancelled dialog
                    raise Exception("cancel")
            except Exception:
                if messagebox.askyesno("Quit", "Exit game?"):
                    self.root.destroy()
                    return
                else:
                    num_players = None
        
        for i in range(num_players):
            default_name = f"Player {i+1}"
            name = simpledialog.askstring("Player Name", f"Name for Player {i+1}:", 
                                          initialvalue=default_name, parent=self.root)
            if not name:
                name = default_name
            self.players.append(name)
        
        self.positions = [0] * num_players

    def draw_board(self):
        """Draw the 10x10 grid and numbers."""
        # Draw Grid Lines
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x0, y0 = c * CELL_SIZE, r * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#ccc", width=1)
        
        # Draw Numbers
        for pos in range(1, 101):
            rc = pos_to_grid(pos)
            if not rc:
                continue
            r, c = rc
            x, y = grid_to_center(r, c)
            # Offset text slightly to top-left of cell
            self.canvas.create_text(x - CELL_SIZE//2 + 12, y - CELL_SIZE//2 + 12, 
                                    text=str(pos), fill="#888", font=("Arial", 9))

    def draw_snakes_ladders(self):
        """Draw graphical representations of snakes and ladders."""
        # Ladders in green
        for start, end in LADDERS.items():
            x0, y0 = pos_to_center(start)
            x1, y1 = pos_to_center(end)
            self.canvas.create_line(x0, y0, x1, y1, fill="#2ca02c", width=6, capstyle=tk.ROUND)
        
        # Snakes in red
        for start, end in SNAKES.items():
            x0, y0 = pos_to_center(start)
            x1, y1 = pos_to_center(end)
            self.canvas.create_line(x0, y0, x1, y1, fill="#d62728", width=6, capstyle=tk.ROUND)

    def create_tokens(self):
        """Create player tokens off-board initially."""
        # Predefined offsets to prevent tokens from overlapping perfectly
        offsets = [
            (-12, -12), (12, -12), (-12, 12), (12, 12),
            (0, -18), (-18, 0), (18, 0), (0, 18)
        ]
        
        for i, name in enumerate(self.players):
            # Start position visualization (just off the board near "1")
            sx, sy = grid_to_center(BOARD_SIZE - 1, 0) # Near bottom-left
            ox, oy = offsets[i % len(offsets)]
            
            # Draw token
            token = self.canvas.create_oval(
                sx + ox - 12, sy + oy + 30, sx + ox + 12, sy + oy + 54,
                fill=PLAYER_COLORS[i % len(PLAYER_COLORS)], outline="black"
            )
            self.tokens.append(token)

    def update_info_label(self, msg=None):
        if self.game_over:
            self.info_label.config(text="Game Over!")
            return
        
        current_player_name = self.players[self.turn_idx]
        text = f"Turn: {current_player_name}"
        if msg:
            text += f" | {msg}"
        self.info_label.config(text=text)

    def roll_dice(self):
        if self.game_over:
            return
        
        # Disable button during animation
        self.roll_btn.config(state="disabled")
        
        final_value = random.randint(1, 6)
        self.animate_dice_roll(final_value, steps=10, delay=60)

    def animate_dice_roll(self, final_value, steps=8, delay=60):
        # Generate random sequence for effect
        sequence = [random.randint(1, 6) for _ in range(steps - 1)] + [final_value]
        
        def step(i=0):
            if i >= len(sequence):
                self.process_move(sequence[-1])
                return
            self.dice_label.config(text=f"🎲 {sequence[i]}")
            self.root.after(delay, step, i + 1)
        step()

    def process_move(self, die_value):
        idx = self.turn_idx
        current_pos = self.positions[idx]
        new_pos = current_pos + die_value
        
        if new_pos > 100:
            self.update_info_label(f"Rolled {die_value}. Overshoot! ({new_pos} > 100)")
            self.end_turn()
            return
        
        # Generate path for animation (step-by-step movement)
        path = list(range(current_pos + 1, new_pos + 1))
        self.animate_token_movement(path, lambda: self.check_tile_effects(idx))

    def animate_token_movement(self, path_positions, on_complete):
        if not path_positions:
            on_complete()
            return
        
        next_pos = path_positions.pop(0)
        self.positions[self.turn_idx] = next_pos
        self.move_token_visual(self.turn_idx, next_pos)
        
        # Delay between steps
        self.root.after(150, lambda: self.animate_token_movement(path_positions, on_complete))

    def move_token_visual(self, player_idx, pos):
        token = self.tokens[player_idx]
        
        # Calculate target position
        if pos < 1: pos = 1 # Safety
        rc = pos_to_grid(pos)
        r, c = rc
        target_x, target_y = grid_to_center(r, c)
        
        # Apply offset based on player index
        offsets = [
            (-12, -12), (12, -12), (-12, 12), (12, 12),
            (0, -18), (-18, 0), (18, 0), (0, 18)
        ]
        ox, oy = offsets[player_idx % len(offsets)]
        
        final_x = target_x + ox
        final_y = target_y + oy
        
        # Get current coords to calculate delta
        x0, y0, x1, y1 = self.canvas.coords(token)
        current_cx = (x0 + x1) / 2
        current_cy = (y0 + y1) / 2
        
        dx = final_x - current_cx
        dy = final_y - current_cy
        
        self.canvas.move(token, dx, dy)

    def check_tile_effects(self, player_idx):
        pos = self.positions[player_idx]
        
        final_dest = pos
        jump_type = None # "ladder", "snake", or None
        
        if pos in LADDERS:
            final_dest = LADDERS[pos]
            jump_type = "ladder"
        elif pos in SNAKES:
            final_dest = SNAKES[pos]
            jump_type = "snake"
        
        if jump_type:
            start, end = pos, final_dest
            msg = f"Hit a {jump_type}! {start} -> {end}"
            self.update_info_label(msg)
            # Animate the slide/climb
            self.animate_slide_token(player_idx, start, end, lambda: self.check_win_condition(player_idx))
        else:
            self.check_win_condition(player_idx)

    def animate_slide_token(self, player_idx, start_pos, end_pos, on_complete):
        # Smooth interpolation from start to end (visual only)
        start_x, start_y = pos_to_center(start_pos)
        end_x, end_y = pos_to_center(end_pos)
        
        token = self.tokens[player_idx]
        steps = 15
        
        def tween_step(step=0):
            if step > steps:
                # Ensure final logical position is set
                self.positions[player_idx] = end_pos
                self.move_token_visual(player_idx, end_pos)
                on_complete()
                return
            
            t = step / steps
            # Lerp
            current_target_x = start_x + (end_x - start_x) * t
            current_target_y = start_y + (end_y - start_y) * t
            
            # Move token relative to its current position to hit the lerp target
            x0, y0, x1, y1 = self.canvas.coords(token)
            cx, cy = (x0+x1)/2, (y0+y1)/2
            
            self.canvas.move(token, current_target_x - cx, current_target_y - cy)
            self.root.after(30, tween_step, step + 1)
            
        tween_step()

    def check_win_condition(self, player_idx):
        if self.positions[player_idx] == 100:
            self.game_over = True
            player_name = self.players[player_idx]
            self.update_info_label(f"WINNER: {player_name} 🎉")
            messagebox.showinfo("Victory!", f"Congratulations {player_name}, you won!")
            self.roll_btn.config(state="disabled")
        else:
            self.end_turn()

    def end_turn(self):
        self.roll_btn.config(state="normal") # Re-enable button
        self.turn_idx = (self.turn_idx + 1) % len(self.players)
        self.update_info_label()


def main():
    root = tk.Tk()
     # Center window on screen (optional polish)
    root.geometry(f"{CANVAS_SIZE+40}x{CANVAS_SIZE+100}")
    
    app = SnakesLaddersGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

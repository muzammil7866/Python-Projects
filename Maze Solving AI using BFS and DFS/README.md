# Maze Solving Projects (BFS & DFS Visualization)

A sophisticated maze exploration and pathfinding suite that demonstrates the fundamental differences between Breadth-First Search (BFS) and Depth-First Search (DFS) through interactive, real-time Tkinter visualizations.

## 🚀 Business & Educational Goals Achieved
- **Algorithm Transparency**: Provides a side-by-side comparison of how different data structures (Queue vs. Stack) fundamentally change search behavior.
- **Real-Time Visual Feedback**: Implements a thread-safe visualization layer that allows users to see the "Frontier" and "Explored" nodes as they happen.
- **UX Excellence**: Features a responsive GUI with control panels (Start/Reset) and a live status bar showing nodes explored and execution time.
- **Asynchronous Execution**: Utilizes Python's `threading` library to prevent UI freezing during heavy search operations, a critical pattern for robust desktop applications.
- **State-Space Modeling**: Efficiently maps 2D grid environments into searchable graph structures.

## 🧠 Navigation Algorithms

### 1. Breadth-First Search (BFS)
- **Algorithm**: `Maze Solving using Breadth First Search.py`
- **Data Structure**: FIFO Queue.
- **Property**: Guaranteed to find the **shortest path** in an unweighted grid.
- **Visual Style**: Circular expansion from the start point, exploring all neighbors at the current depth before moving deeper.
- **Color Legend**:
  - 🟢 **Light Green**: Frontier (added to queue).
  - 🔵 **Light Blue**: Explored nodes.
  - 🟦 **Dark Blue**: Final Optimal Path.

### 2. Depth-First Search (DFS)
- **Algorithm**: `Maze Solving using Depth First Search.py`
- **Data Structure**: LIFO Stack (Recursive-like behavior).
- **Property**: Explores as deep as possible before backtracking. Does **not** guarantee the shortest path.
- **Visual Style**: "Deep Diving" behavior, following a single path until a wall or goal is hit.
- **Color Legend**:
  - 🟣 **Dark Purple**: Frontier (added to stack).
  - 💜 **Light Purple**: Explored nodes.
  - 🟪 **Strong Purple**: Resulting Path.

## 🛠️ Technical Implementation
- **Threaded Search**: Algorithms run in background threads, communicating with the main Tkinter thread via `.after()` and safe canvas updates.
- **Dynamic Discovery**: Automatically scans the layout for Start (`3`) and Goal (`2`) markers.
- **Performance Tracking**: Calculates "Nodes Explored" and "Total Time" for comparative analysis.

## 📋 How to Run
Run either script using Python 3:
```bash
python "Maze Solving using Breadth First Search.py"
python "Maze Solving using Depth First Search.py"
```

### Controls
- **Start**: Initiates the search animation.
- **Reset**: Clears the visualization and prepares for a new run.
- **Status Bar**: Located at the bottom, providing real-time metrics.

# Snakes and Ladders Game using Tkinter

A classic Snakes and Ladders game application built with Python and the Tkinter GUI library. This project demonstrates interactive game development with visual animations and multiplayer logic.

## Project Description

This application recreates the traditional board game "Snakes and Ladders" in a digital format. Up to 6 players can compete on a 10x10 grid. The game features:
-   **Interactive GUI**: A clean, graphical board with player tokens.
-   **Animations**: Smooth animations for dice rolling and token movement across the board.
-   **Game Logic**: Full implementation of game rules, including snakes (sliding down), ladders (climbing up), and precise movement.
-   **Multiplayer Support**: Supports 2 to 6 players per session.

## Business Goals Achieved

This project serves several key objectives:
1.  **Demonstration of GUI Development**: Showcases the ability to create functional and interactive desktop applications using Python's standard GUI library, Tkinter.
2.  **Algorithm Implementation**: Successfully implements core game algorithms, including pathfinding on a grid, turn-based logic, and randomized events (dice rolls).
3.  **User Experience (UX) Design**: Provides an engaging user experience through visual feedback (animations, color-coding) and intuitive controls.
4.  **Code Modularity**: The codebase is structured with clear separation of concerns (configuration, logic, UI), demonstrating clean coding practices and maintainability.
5.  **Educational Value**: Serves as a practical example for understanding event-driven programming and coordinate systems in game development.

## How to Run the Game

### Prerequisites
-   Python 3.x installed on your system.
-   Tkinter (usually included with standard Python installations).

### Steps
1.  Navigate to the project directory:
    ```bash
    cd "Snakes and Ladders Game using Tkinter Library"
    ```
2.  Run the game script:
    ```bash
    python snakes_and_ladders.py
    ```
3.  Follow the on-screen prompts to enter the number of players and their names.
4.  Click **"Roll Dice"** to play!

## Game Rules
-   Players take turns rolling a digital die.
-   Tokens move forward the number of spaces rolled.
-   **Ladders**: If you land on the bottom of a ladder, you automatically climb to the top.
-   **Snakes**: If you land on the head of a snake, you slide down to its tail.
-   The first player to reach exactly square 100 wins the game.

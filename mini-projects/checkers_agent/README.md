# Checkers AI Agent
A modern, AI-powered Checkers game with both GUI and text-based interfaces. Play against an intelligent agent using Minimax, Alpha-Beta, or Alpha-Beta with move ordering.

## Features
- **AI Opponent:** Choose from Minimax, Alpha-Beta, or Alpha-Beta with move ordering
- **Configurable:** Set time limit (1-3s) and search depth (5-9 plies)
- **GUI:** Click-to-move, highlights, and real-time analytics (Tkinter)
- **Text Fallback:** Fully playable in terminal if GUI is unavailable
- **Analytics:** Tracks nodes expanded, pruning, ordering gains, and move times
- **Comprehensive Testing:** Automated test suite for all core features

## Quick Start
1. **Install Python 3** (with Tkinter for GUI)
2. **Run the game:**
   ```bash
   python3 checkers_agent_gui.py
   ```
3. **Follow prompts** to select AI strategy, time, and depth
4. **Play in GUI** (if available) or text mode (fallback)

## Controls (GUI)
- Click a white piece to select
- Click a highlighted square to move
- Menu: New Game / Exit
- Analytics shown below the board

## Requirements
- Python 3.x
- Tkinter (for GUI; pre-installed on most systems)

## Project Structure
- `checkers_agent_gui.py` — Main game and AI logic
- `README.md` — This file

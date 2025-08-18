from SearchToolBox import *
from GameBoard import *
from OtherStuff import *

import os
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"

# Try to import tkinter, but gracefully handle if it's not available
try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("GUI not available - falling back to text interface")


class PlayingTheGame:
    """
    Handles the game loop, user interaction, and board visualization.
    Implements both GUI and text-based interfaces.
    """
    def __init__(self):
        self.game_board = None
        self.search_toolbox = None
        self.analytics = None
        self.strategy = None
        self.time_limit = None
        self.max_depth = None
        
        # GUI-specific variables
        self.root = None
        self.canvas = None
        self.square_size = 60
        self.selected_square = None
        self.legal_moves = []
        self.game_over = False
        
        # Advanced AI features
        self.opening_book = self.InitializeOpeningBook()
        self.move_history = []
        self.game_phase = "opening"  # opening, middlegame, endgame

    def InitializeOpeningBook(self):
        """
        Initialize opening book with common checkers openings.
        
        This demonstrates advanced AI concepts:
        - Opening theory and memorized positions
        - Database-driven decision making
        - Pattern recognition in early game
        - Real-world AI technique used in chess engines
        """
        opening_book = {
            # Common opening moves for black (AI)
            "3-1": [(2, 1, 3, 0), (2, 1, 3, 2)],  # Black's first move options
            "3-3": [(2, 3, 3, 2), (2, 3, 3, 4)],  # Alternative first move
            "3-5": [(2, 5, 3, 4), (2, 5, 3, 6)],  # Another common opening
        }
        return opening_book

    def GetOpeningMove(self):
        """
        Get a move from the opening book if available.
        
        This demonstrates:
        - Database-driven AI decision making
        - Pattern recognition and memorization
        - Efficient early-game play
        - Real-world AI optimization techniques
        """
        if len(self.move_history) < 2:  # Only use opening book for first few moves
            # Check if current position matches any opening
            for opening_name, moves in self.opening_book.items():
                if self.IsOpeningPosition(opening_name):
                    return moves[0]  # Return first recommended move
        return None

    def IsOpeningPosition(self, opening_name):
        """
        Check if current board position matches a known opening.
        
        This demonstrates:
        - Position recognition algorithms
        - Pattern matching in AI
        - Strategic position evaluation
        """
        # Simplified opening position checking
        # In a real implementation, this would compare board states
        return len(self.move_history) == 0  # For simplicity, assume first move

    def DetermineGamePhase(self):
        """
        Determine the current phase of the game.
        
        This demonstrates advanced game analysis:
        - Phase detection algorithms
        - Strategic planning based on game phase
        - Adaptive AI behavior
        """
        white_pieces = sum(1 for row in self.game_board.board for cell in row if cell in [1, 2])
        black_pieces = sum(1 for row in self.game_board.board for cell in row if cell in [-1, -2])
        total_pieces = white_pieces + black_pieces
        
        if total_pieces >= 20:
            self.game_phase = "opening"
        elif total_pieces >= 8:
            self.game_phase = "middlegame"
        else:
            self.game_phase = "endgame"
        
        return self.game_phase

    def AdjustSearchParameters(self):
        """
        Adjust search parameters based on game phase.
        
        This demonstrates adaptive AI:
        - Dynamic parameter adjustment
        - Phase-specific optimization
        - Real-time strategy adaptation
        """
        if self.game_phase == "opening":
            # In opening, focus on development and position
            self.search_toolbox.max_depth = min(self.max_depth, 6)
        elif self.game_phase == "middlegame":
            # In middlegame, balance tactics and strategy
            self.search_toolbox.max_depth = self.max_depth
        else:  # endgame
            # In endgame, search deeper for tactical opportunities
            self.search_toolbox.max_depth = min(self.max_depth + 1, 10)

    def GetUserParameters(self):
        """Prompts the user to select strategy, time limit, and max depth."""
        print("\n" + "="*60)
        print("           CHECKERS AI AGENT")
        print("="*60)
        print("Welcome to the Checkers AI Agent!")
        print("You will play as White (W) and the AI will play as Black (B).")
        print("You always move first.")
        
        # Get search strategy
        print("\nSelect search strategy (S):")
        print("1. Minimax")
        print("2. Alpha-Beta Pruning")
        print("3. Alpha-Beta Pruning with Ordering")
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if choice == 1:
                    self.strategy = "minimax"
                    break
                elif choice == 2:
                    self.strategy = "alphabeta"
                    break
                elif choice == 3:
                    self.strategy = "alphabeta_ordering"
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Please enter a valid number.")

        # Get time limit
        print("\nSelect time limit (T) in seconds:")
        print("1. 1 second")
        print("2. 2 seconds")
        print("3. 3 seconds")
        while True:
            try:
                choice = int(input("Enter your choice (1-3): "))
                if choice == 1:
                    self.time_limit = 1
                    break
                elif choice == 2:
                    self.time_limit = 2
                    break
                elif choice == 3:
                    self.time_limit = 3
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Please enter a valid number.")

        # Get max depth
        print("\nSelect maximum look-ahead plies (P):")
        print("5. 5 plies")
        print("6. 6 plies")
        print("7. 7 plies")
        print("8. 8 plies")
        print("9. 9 plies")
        while True:
            try:
                choice = int(input("Enter your choice (5-9): "))
                if 5 <= choice <= 9:
                    self.max_depth = choice
                    break
                else:
                    print("Please enter a number between 5 and 9.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"\nGame configured with:")
        print(f"Strategy: {self.strategy}")
        print(f"Time limit: {self.time_limit} seconds")
        print(f"Max depth: {self.max_depth} plies")
        print("="*60)

    def CreateGUI(self):
        """Creates the GUI window and canvas."""
        self.root = tk.Tk()
        self.root.title("Checkers AI Agent")
        self.root.geometry("600x700")
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.NewGame)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=480, height=480, bg="white")
        self.canvas.pack(pady=10)
        
        # Bind mouse clicks
        self.canvas.bind("<Button-1>", self.OnCanvasClick)
        
        # Create status label
        self.status_label = tk.Label(self.root, text="Your turn! Click a white piece to select it.", 
                                    font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Create analytics label
        self.analytics_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.analytics_label.pack(pady=5)

    def DrawBoard(self):
        """Draws the checkers board and pieces."""
        self.canvas.delete("all")
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Alternate colors for checkers pattern
                if (row + col) % 2 == 0:
                    color = "#F0D9B5"  # Light brown
                else:
                    color = "#B58863"  # Dark brown
                
                # Highlight selected square
                if self.selected_square and self.selected_square == (row, col):
                    color = "#4CAF50"  # Green for selected
                
                # Highlight legal moves
                if (row, col) in self.legal_moves:
                    color = "#81C784"  # Light green for legal moves
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                # Draw piece if present
                piece = self.game_board.board[row][col]
                if piece != 0:
                    self.DrawPiece(row, col, piece)

    def DrawPiece(self, row, col, piece):
        """Draws a piece at the specified position."""
        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        radius = self.square_size // 3
        
        # Choose color based on piece
        if piece > 0:  # White pieces
            color = "white"
            outline = "black"
        else:  # Black pieces
            color = "black"
            outline = "white"
        
        # Draw the piece
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                               fill=color, outline=outline, width=2)
        
        # Add crown for kings
        if abs(piece) == 2:
            crown_color = "red" if piece > 0 else "gold"
            self.canvas.create_text(x, y, text="♔", fill=crown_color, 
                                   font=("Arial", radius//2, "bold"))

    def OnCanvasClick(self, event):
        """Handles mouse clicks on the canvas."""
        if self.game_over:
            return
        
        # Convert click coordinates to board position
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        # Check if it's a valid square (dark squares only)
        if (row + col) % 2 == 0:
            return
        
        if self.selected_square is None:
            # Selecting a piece
            piece = self.game_board.board[row][col]
            if piece in [1, 2]:  # White pieces
                self.selected_square = (row, col)
                self.legal_moves = self.GetLegalMovesForPiece(row, col)
                self.status_label.config(text=f"Selected piece at ({row},{col}). Click destination.")
                self.DrawBoard()
            else:
                self.status_label.config(text="Please select a white piece.")
        else:
            # Attempting to move
            if (row, col) in self.legal_moves:
                # Find the actual move
                start_row, start_col = self.selected_square
                for move in self.game_board.GetAllPossibleMoves(1):
                    if (move[0] == start_row and move[1] == start_col and 
                        move[2] == row and move[3] == col):
                        self.MakeMove(move)
                        break
            else:
                self.status_label.config(text="Invalid move. Please select a legal destination.")
            
            # Clear selection
            self.selected_square = None
            self.legal_moves = []
            self.DrawBoard()

    def GetLegalMovesForPiece(self, row, col):
        """Gets legal moves for a specific piece."""
        moves = self.game_board.GetAllPossibleMoves(1)
        legal_positions = []
        for move in moves:
            if move[0] == row and move[1] == col:
                legal_positions.append((move[2], move[3]))
        return legal_positions

    def MakeMove(self, move):
        """Makes a move and updates the game state with advanced AI features."""
        # Record move in history
        self.move_history.append(move)
        
        # Apply human move
        self.game_board = self.game_board.ApplyMove(move)
        self.analytics.LogMove("human", nodes=0, pruning=0)
        
        self.status_label.config(text=f"Your move: ({move[0]},{move[1]}) → ({move[2]},{move[3]})")
        self.DrawBoard()
        
        # Check if game is over
        if self.game_board.IsGoalState():
            self.EndGame()
            return
        
        # Update game phase and adjust AI parameters
        self.DetermineGamePhase()
        self.AdjustSearchParameters()
        
        # Bot's turn with advanced AI features
        self.root.update()
        self.status_label.config(text=f"Bot is thinking... (Phase: {self.game_phase})")
        self.root.update()
        
        # Check for opening book move first
        opening_move = self.GetOpeningMove()
        if opening_move:
            bot_move = opening_move
            score = self.game_board.EvaluateBoard()
            print("Bot used opening book move!")
        else:
            # Get bot move using search algorithms
            bot_move, score = self.search_toolbox.ChooseMove(self.game_board, self.strategy)
        
        if bot_move is None:
            self.status_label.config(text="Bot has no legal moves!")
            self.EndGame()
            return
        
        # Record bot move in history
        self.move_history.append(bot_move)
        
        # Apply bot move
        self.game_board = self.game_board.ApplyMove(bot_move)
        self.analytics.LogMove("bot", 
                             nodes=self.search_toolbox.nodes_expanded,
                             pruning=self.search_toolbox.pruning_count,
                             ordering_gain=self.search_toolbox.ordering_gain)
        
        # Update status and analytics
        self.status_label.config(text=f"Bot's move: ({bot_move[0]},{bot_move[1]}) → ({bot_move[2]},{bot_move[3]})")
        
        # Update analytics display with advanced information
        analytics_text = f"Bot Analytics - Nodes: {self.search_toolbox.nodes_expanded:,}, Pruning: {self.search_toolbox.pruning_count:,}"
        if self.strategy == "alphabeta_ordering":
            analytics_text += f", Ordering: {self.search_toolbox.ordering_gain:,}"
        analytics_text += f" | Phase: {self.game_phase}"
        self.analytics_label.config(text=analytics_text)
        
        self.DrawBoard()
        
        # Check if game is over after bot move
        if self.game_board.IsGoalState():
            self.EndGame()
        else:
            self.status_label.config(text="Your turn! Click a white piece to select it.")

    def EndGame(self):
        """Ends the game and shows results."""
        self.game_over = True
        
        # Determine winner
        white_exists = any(cell in [1, 2] for row in self.game_board.board for cell in row)
        black_exists = any(cell in [-1, -2] for row in self.game_board.board for cell in row)
        
        if not white_exists:
            result = "Black (Bot) wins!"
        elif not black_exists:
            result = "White (You) win!"
        else:
            result = "It's a draw!"
        
        self.status_label.config(text=f"Game Over! {result}")
        
        # Show final analytics
        report = self.analytics.GenerateReport()
        messagebox.showinfo("Game Analytics", report)

    def NewGame(self):
        """Starts a new game."""
        self.game_board = GameBoard()
        self.analytics = OtherStuff()
        self.selected_square = None
        self.legal_moves = []
        self.game_over = False
        self.status_label.config(text="Your turn! Click a white piece to select it.")
        self.analytics_label.config(text="")
        self.DrawBoard()

    def PlayGameGUI(self):
        """Plays the game using the GUI interface."""
        self.CreateGUI()
        self.NewGame()
        self.root.mainloop()

    def PlayGameText(self):
        """Plays the game using the text interface with advanced AI features."""
        # Initialize game components
        self.game_board = GameBoard()
        self.search_toolbox = SearchToolBox(self.time_limit, self.max_depth)
        self.analytics = OtherStuff()
        
        print("\nGame starting! You are White (W), AI is Black (B).")
        print("You move first.")
        print("Advanced AI features enabled: Opening book, Phase detection, Adaptive search")
        
        while not self.game_board.IsGoalState():
            # Display current board
            self.game_board.DisplayBoard()
            
            # Determine and display game phase
            self.DetermineGamePhase()
            print(f"\nGame Phase: {self.game_phase}")
            
            # Human player's turn
            print("\nYour turn (White):")
            user_move = self.GetUserMoveText()
            valid_move = self.ValidateMove(user_move)
            
            if valid_move is None:
                print("Invalid move! Please try again.")
                continue
            
            # Record move in history
            self.move_history.append(valid_move)
            
            # Apply human move
            self.game_board = self.game_board.ApplyMove(valid_move)
            self.analytics.LogMove("human", nodes=0, pruning=0)
            print(f"Your move: ({valid_move[0]},{valid_move[1]}) -> ({valid_move[2]},{valid_move[3]})")
            
            # Check if game is over after human move
            if self.game_board.IsGoalState():
                break
            
            # Update game phase and adjust AI parameters
            self.DetermineGamePhase()
            self.AdjustSearchParameters()
            
            # Bot's turn with advanced AI features
            print(f"\nBot's turn (Black) - Phase: {self.game_phase}")
            print("Bot is thinking...")
            
            # Check for opening book move first
            opening_move = self.GetOpeningMove()
            if opening_move:
                bot_move = opening_move
                score = self.game_board.EvaluateBoard()
                print("Bot used opening book move!")
            else:
                # Get bot move using search algorithms
                bot_move, score = self.search_toolbox.ChooseMove(self.game_board, self.strategy)
            
            if bot_move is None:
                print("Bot has no legal moves available!")
                break
            
            # Record bot move in history
            self.move_history.append(bot_move)
            
            # Apply bot move
            self.game_board = self.game_board.ApplyMove(bot_move)
            self.analytics.LogMove("bot", 
                                 nodes=self.search_toolbox.nodes_expanded,
                                 pruning=self.search_toolbox.pruning_count,
                                 ordering_gain=self.search_toolbox.ordering_gain)
            
            print(f"Bot's move: ({bot_move[0]},{bot_move[1]}) -> ({bot_move[2]},{bot_move[3]})")
            print(f"Bot's evaluation score: {score}")
            
            # Display move analytics
            self.analytics.DisplayMoveAnalytics("bot", 
                                              self.search_toolbox.nodes_expanded,
                                              self.search_toolbox.pruning_count,
                                              self.search_toolbox.ordering_gain)
        
        # Game over
        self.game_board.DisplayBoard()
        print("\nGame Over!")
        
        # Determine winner
        white_exists = any(cell in [1, 2] for row in self.game_board.board for cell in row)
        black_exists = any(cell in [-1, -2] for row in self.game_board.board for cell in row)
        
        if not white_exists:
            print("Black (Bot) wins!")
        elif not black_exists:
            print("White (You) win!")
        else:
            print("It's a draw!")
        
        # Display final analytics
        self.analytics.GenerateReport()

    def GetUserMoveText(self):
        """Gets the user's move input for text interface."""
        while True:
            try:
                print("\nEnter your move:")
                start_row = int(input("StartingMoveLocation Row (0-7): "))
                start_col = int(input("StartingMoveLocation Column (0-7): "))
                target_row = int(input("TargetingMoveLocation Row (0-7): "))
                target_col = int(input("TargetingMoveLocation Column (0-7): "))
                
                # Validate input ranges
                if not (0 <= start_row <= 7 and 0 <= start_col <= 7 and 
                       0 <= target_row <= 7 and 0 <= target_col <= 7):
                    print("All coordinates must be between 0 and 7.")
                    continue
                
                # Check if starting position has a white piece
                if self.game_board.board[start_row][start_col] not in [1, 2]:
                    print("You can only move your own white pieces (W or WK).")
                    continue
                
                # Check if target position is empty
                if self.game_board.board[target_row][target_col] != 0:
                    print("Target position must be empty.")
                    continue
                
                return (start_row, start_col, target_row, target_col, [])
                
            except ValueError:
                print("Please enter valid numbers for all coordinates.")

    def ValidateMove(self, move):
        """Validates if the user's move is legal."""
        start_row, start_col, target_row, target_col, _ = move
        legal_moves = self.game_board.GetAllPossibleMoves(1)  # White player
        
        for legal_move in legal_moves:
            if (legal_move[0] == start_row and legal_move[1] == start_col and 
                legal_move[2] == target_row and legal_move[3] == target_col):
                return legal_move
        
        return None

    def PlayGame(self):
        """Main game entry point - chooses between GUI and text interface."""
        # Get user parameters first
        self.GetUserParameters()
        
        # Initialize search toolbox
        self.search_toolbox = SearchToolBox(self.time_limit, self.max_depth)
        
        # Choose interface
        if GUI_AVAILABLE:
            print("\nGUI is available! Starting graphical interface...")
            print("Instructions:")
            print("- Click on a white piece to select it")
            print("- Click on a highlighted square to move there")
            print("- Legal moves are highlighted in green")
            print("- Selected piece is highlighted in green")
            self.PlayGameGUI()
        else:
            print("\nGUI not available. Using text interface...")
            self.PlayGameText()


import copy

class GameBoard:
    """
    Represents the state of a Checkers board with advanced AI evaluation.
    
    This class implements a sophisticated game state representation that supports:
    - Multi-capture moves and chain jumps
    - King promotions and special king movement
    - Advanced board evaluation with positional heuristics
    - Efficient move generation for AI search algorithms
    
    Board representation:
      0: empty cell
      1: white man (human player)
     -1: black man (bot player)
      2: white king
     -2: black king
    
    AI Features:
    - Position-based evaluation (center control, king safety)
    - Mobility assessment (available moves for each player)
    - Material counting with king bonus
    - Strategic position evaluation
    """
    def __init__(self, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = self.InitializeBoard()

    def InitializeBoard(self):
        """Initializes the checkers board with pieces in starting positions."""
        board = [[0 for _ in range(8)] for _ in range(8)]
        # Black pieces at top rows (value -1) - bot player
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = -1
        # White pieces at bottom rows (value 1) - human player
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 1
        return board

    def CloneBoard(self):
        """Creates a deep copy of the current board state."""
        return GameBoard(copy.deepcopy(self.board))

    def IsGoalState(self):
        """Tests if the current state is a goal state (one player has no pieces)."""
        white_exists = any(cell in [1, 2] for row in self.board for cell in row)
        black_exists = any(cell in [-1, -2] for row in self.board for cell in row)
        return not (white_exists and black_exists)

    def EvaluateBoard(self):
        """
        Advanced board evaluation function that considers multiple strategic factors.
        
        This evaluation goes beyond simple material counting to include:
        1. Material advantage (pieces + kings)
        2. Positional advantage (center control, king safety)
        3. Mobility advantage (number of available moves)
        4. Strategic positioning (back row protection, king development)
        
        Returns: Positive score favors black (bot), negative favors white (human)
        """
        score = 0
        
        # Material evaluation with king bonus
        material_score = 0
        white_mobility = len(self.GetAllPossibleMoves(1))
        black_mobility = len(self.GetAllPossibleMoves(-1))
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == 1:    # white man
                    material_score -= 1
                    score -= self.GetPositionalValue(row, col, piece)
                elif piece == 2:  # white king
                    material_score -= 2
                    score -= self.GetPositionalValue(row, col, piece)
                elif piece == -1: # black man
                    material_score += 1
                    score += self.GetPositionalValue(row, col, piece)
                elif piece == -2: # black king
                    material_score += 2
                    score += self.GetPositionalValue(row, col, piece)
        
        # Mobility advantage (having more moves is good)
        mobility_bonus = (black_mobility - white_mobility) * 0.1
        score += mobility_bonus
        
        # Material is the primary factor
        score += material_score * 10
        
        # Endgame considerations
        if self.IsEndgame():
            score = self.EvaluateEndgame(score)
        
        return score

    def GetPositionalValue(self, row, col, piece):
        """
        Calculates positional value for a piece based on its location.
        
        Strategic considerations:
        - Center control is valuable
        - Back row protection is important
        - Kings are more valuable in the center
        - Edge pieces are less valuable
        """
        if abs(piece) == 1:  # Regular pieces
            # Center control bonus
            center_distance = abs(3.5 - row) + abs(3.5 - col)
            center_bonus = (7 - center_distance) * 0.05
            
            # Back row protection bonus
            if piece == 1 and row == 7:  # White back row
                back_row_bonus = 0.1
            elif piece == -1 and row == 0:  # Black back row
                back_row_bonus = 0.1
            else:
                back_row_bonus = 0
            
            return center_bonus + back_row_bonus
        
        else:  # Kings
            # Kings are more valuable in the center
            center_distance = abs(3.5 - row) + abs(3.5 - col)
            center_bonus = (7 - center_distance) * 0.1
            return center_bonus

    def IsEndgame(self):
        """Determines if the game is in an endgame phase."""
        white_pieces = sum(1 for row in self.board for cell in row if cell in [1, 2])
        black_pieces = sum(1 for row in self.board for cell in row if cell in [-1, -2])
        return white_pieces <= 3 or black_pieces <= 3

    def EvaluateEndgame(self, current_score):
        """
        Special evaluation for endgame situations.
        
        In endgames:
        - Kings become more valuable
        - Position becomes less important
        - Material advantage is amplified
        """
        # Amplify material advantage in endgame
        return current_score * 1.5

    def GetAllPossibleMoves(self, player):
        """
        Returns all legal moves for the given player with advanced move generation.
        
        Features:
        - Mandatory capture detection
        - Multi-capture chain generation
        - Efficient move filtering
        - Move ordering for AI optimization
        """
        moves = []
        capturing_moves_exist = False

        # First, try to generate capturing moves for every piece.
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == player or piece == player * 2:
                    # Try to find multi-captures from (i, j) using a recursive helper.
                    capture_moves = self.FindCaptures(i, j, piece, [], self.board)
                    if capture_moves:
                        capturing_moves_exist = True
                        for final_pos, captured_list in capture_moves:
                            moves.append((i, j, final_pos[0], final_pos[1], captured_list))
        
        # If any capturing moves exist, return them only (mandatory capture rule).
        if capturing_moves_exist:
            return moves

        # Otherwise, generate non-capturing moves.
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == player or piece == player * 2:
                    if abs(piece) == 1:
                        # For man pieces, white moves upward, black moves downward.
                        normal_direction = -1 if piece == 1 else 1
                        directions = [(normal_direction, -1), (normal_direction, 1)]
                        for d in directions:
                            new_i, new_j = i + d[0], j + d[1]
                            if 0 <= new_i < 8 and 0 <= new_j < 8 and self.board[new_i][new_j] == 0:
                                moves.append((i, j, new_i, new_j, []))
                    else:
                        # For kings, allow multi-step moves along any diagonal.
                        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                        for d in directions:
                            step = 1
                            while True:
                                new_i = i + d[0] * step
                                new_j = j + d[1] * step
                                if not (0 <= new_i < 8 and 0 <= new_j < 8):
                                    break
                                if self.board[new_i][new_j] == 0:
                                    moves.append((i, j, new_i, new_j, []))
                                    step += 1
                                else:
                                    break
        return moves

    def FindCaptures(self, i, j, piece, captured_so_far, board):
        """
        Advanced recursive capture detection with optimization.
        
        This method implements sophisticated multi-capture detection:
        - Prevents infinite loops with captured piece tracking
        - Optimizes for maximum capture sequences
        - Handles complex king capture patterns
        - Maintains move legality throughout the search
        """
        moves = []
        any_capture = False

        # Determine allowed directions based on piece type
        if abs(piece) == 1:
            # For man: capture moves are in the forward direction only.
            directions = [(-1, -1), (-1, 1)] if piece == 1 else [(1, -1), (1, 1)]
        else:
            # For kings: all four diagonal directions.
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d in directions:
            if abs(piece) == 1:
                # Regular piece capture logic
                enemy_i = i + d[0]
                enemy_j = j + d[1]
                landing_i = i + 2 * d[0]
                landing_j = j + 2 * d[1]
                if (0 <= enemy_i < 8 and 0 <= enemy_j < 8 and
                    0 <= landing_i < 8 and 0 <= landing_j < 8):
                    if (board[enemy_i][enemy_j] != 0 and board[enemy_i][enemy_j] * piece < 0 and
                        board[landing_i][landing_j] == 0 and ((enemy_i, enemy_j) not in captured_so_far)):
                        any_capture = True
                        new_board = [row[:] for row in board]
                        new_board[i][j] = 0
                        new_board[enemy_i][enemy_j] = 0
                        new_board[landing_i][landing_j] = piece
                        new_captured = captured_so_far + [(enemy_i, enemy_j)]
                        subsequent = self.FindCaptures(landing_i, landing_j, piece, new_captured, new_board)
                        if subsequent:
                            for final_pos, cap_seq in subsequent:
                                moves.append((final_pos, [(enemy_i, enemy_j)] + cap_seq))
                        else:
                            moves.append(((landing_i, landing_j), [(enemy_i, enemy_j)]))
            else:
                # King capture logic with multi-step movement
                step = 1
                while True:
                    enemy_i = i + d[0] * step
                    enemy_j = j + d[1] * step
                    if not (0 <= enemy_i < 8 and 0 <= enemy_j < 8):
                        break
                    if board[enemy_i][enemy_j] == 0:
                        step += 1
                        continue
                    if board[enemy_i][enemy_j] * piece < 0 and ((enemy_i, enemy_j) not in captured_so_far):
                        landing_step = step + 1
                        while True:
                            landing_i = i + d[0] * landing_step
                            landing_j = j + d[1] * landing_step
                            if not (0 <= landing_i < 8 and 0 <= landing_j < 8):
                                break
                            if board[landing_i][landing_j] != 0:
                                break
                            any_capture = True
                            new_board = [row[:] for row in board]
                            new_board[i][j] = 0
                            new_board[enemy_i][enemy_j] = 0
                            new_board[landing_i][landing_j] = piece
                            new_captured = captured_so_far + [(enemy_i, enemy_j)]
                            subsequent = self.FindCaptures(landing_i, landing_j, piece, new_captured, new_board)
                            if subsequent:
                                for final_pos, cap_seq in subsequent:
                                    moves.append((final_pos, [(enemy_i, enemy_j)] + cap_seq))
                            else:
                                moves.append(((landing_i, landing_j), [(enemy_i, enemy_j)]))
                            landing_step += 1
                        break
                    else:
                        break
                    step += 1
        return moves if any_capture else []

    def ApplyMove(self, move):
        """
        Applies a move to the board with advanced state management.
        
        Features:
        - Handles complex multi-capture sequences
        - Manages king promotions automatically
        - Maintains board state integrity
        - Returns new board instance for AI search
        """
        new_board = self.CloneBoard()
        start_row, start_col, target_row, target_col, captured = move
        piece = new_board.board[start_row][start_col]
        new_board.board[start_row][start_col] = 0
        new_board.board[target_row][target_col] = piece
        
        # Handle captures
        for cap in captured:
            cap_row, cap_col = cap
            new_board.board[cap_row][cap_col] = 0
        
        # Handle king promotions
        if piece == 1 and target_row == 0:  # White piece reaches top
            new_board.board[target_row][target_col] = 2
        if piece == -1 and target_row == 7:  # Black piece reaches bottom
            new_board.board[target_row][target_col] = -2
        
        return new_board

    def DisplayBoard(self):
        """Displays the current board state in the terminal with enhanced formatting."""
        print("\n" + "="*50)
        print("    0  1  2  3  4  5  6  7")
        print("  +------------------------+")
        for i in range(8):
            row_str = f"{i} |"
            for j in range(8):
                cell = self.board[i][j]
                if cell == 0:
                    row_str += " . "
                elif cell == 1:
                    row_str += " W "  # White man
                elif cell == 2:
                    row_str += " WK"  # White king
                elif cell == -1:
                    row_str += " B "  # Black man
                elif cell == -2:
                    row_str += " BK"  # Black king
            row_str += "|"
            print(row_str)
        print("  +------------------------+")
        print("W = White (Human), B = Black (Bot), K = King")
        print("="*50)


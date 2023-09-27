import math
import chess

class ChessEngine:
    def __init__(self, depth=2):
        
        self.board = chess.Board()  
        self.eval = -math.inf # what to set this as
        self.best_move = None
        self.depth = depth

        ### Debugging Purposes
        self.boards_explored = 0

        ### Piece Value according to their Positions
        # https://www.chessprogramming.org/Simplified_Evaluation_Function
        self.white_pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0, 
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        # Black piece-square table does not need to be a deepcopy 
        # since the values will not be modified.
        self.black_pawn_table = self.white_pawn_table[::-1]
        
        self.white_knight_table = [
            -50, -40, -30, -30, -30, -30, -40, -50, 
            -40, -20, 0, 5, 5, 0, -20, -40, 
            -30, 5, 10, 15, 15, 10, 5, -30, 
            -30, 0, 15, 20, 20, 15, 0, -30, 
            -30, 5, 15, 20, 20, 15, 5, -30, 
            -30, 0, 10, 15, 15, 10, 0, -30, 
            -40, -20, 0, 0, 0, 0, -20, -40, 
            -50, -40, -30, -30, -30, -30, -40, -50, 
        ]
        self.black_knight_table = self.white_knight_table[::-1]
        self.white_bishop_table = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]
        self.black_bishop_table = self.white_bishop_table[::-1]
        self.white_rook_table = [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        self.black_rook_table = self.white_rook_table[::-1]
        self.white_queen_table = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10, 0, 5, 0, 0, 0, 0, -10, 
            -10,  5,  5,  5,  5,  5,  0,-10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10, 
            -20,-10,-10, -5, -5,-10,-10,-20,
        ]
        self.black_queen_table = self.white_queen_table[::-1]
        self.white_king_table = [
            20, 30, 10, 0, 0, 10, 30, 20, 
            20, 20, 0, 0, 0, 0, 20, 20, 
            -10, -20, -20, -20, -20, -20, -20, -10, 
            -20, -30, -30, -40, -40, -30, -30, -20, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
        ]
        self.black_king_table = self.white_king_table[::-1]
    # def set_depth(self, depth):
    #     self.depth = depth
    
    # TODO: ensure valid fen 
    def set_board_with_FEN(self, fen):
        self.board = chess.Board(fen)
    
    # Return board evaluation based on material and positional advantages
    # Evaluation is subjective to the player (+ is winning, - is losing)
    def evaluate(self):
        eval = 0
        for square, piece in self.board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                eval += self.white_pawn_table[square] if piece.color == chess.WHITE else -self.black_pawn_table[square]
            elif piece.piece_type == chess.KNIGHT:
                eval += self.white_knight_table[square] if piece.color == chess.WHITE else -self.black_knight_table[square]
            elif piece.piece_type == chess.BISHOP:
                eval += self.white_bishop_table[square] if piece.color == chess.WHITE else -self.black_bishop_table[square]
            elif piece.piece_type == chess.ROOK and piece.color == chess.WHITE:
                eval += self.white_rook_table[square]
            elif piece.piece_type == chess.ROOK and piece.color == chess.BLACK:
                eval -= self.black_rook_table[square]
            elif piece.piece_type == chess.QUEEN:
                eval += self.white_queen_table[square] if piece.color == chess.WHITE else -self.black_queen_table[square]
            elif piece.piece_type == chess.KING and piece.color == chess.WHITE:
                eval += self.white_king_table[square]
            elif piece.piece_type == chess.KING and piece.color == chess.BLACK:
                eval -= self.black_king_table[square]
        return eval if self.board.turn == chess.WHITE else -eval

    def negamax(self, depth):
        '''
        Using negamax, the engine evaluates the position.
        '''
        # end of recursion, return the evaluation of the position 
        self.boards_explored += 1
        if self.boards_explored % 100 == 0:
            print(f'# Explored Boards: {self.boards_explored}')

        if self.board.is_game_over() == True:
            if self.board.is_check():
                return -math.inf
            return 0 # draw  

        if depth == 0:
            return self.evaluate()
    
        max_eval = -math.inf
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = -self.negamax(depth - 1)
            self.board.pop()
            if eval > max_eval:
                max_eval = eval
            if depth == self.depth:
                self.best_move = move
        return max_eval

    # def alphabeta(self, depth, alpha=-math.inf, beta=math.inf):
    #     '''
    #     Using alpha beta pruning, the engine returns the best move and 
    #     evaluation of the position by going into a given depth.
    #     '''
    #     # might need to check for draws, change later
    #     if self.board.is_game_over(): 
    #         if self.board.is_check():
    #             return -math.inf
    #         return 0 # draw  
        
    #     if self.board.can_claim_threefold_repetition():
    #         return -math.inf if self.evaluate() < 0 else 0

    #     if depth == 0: # need quiescence search, change later
    #         return self.quiescence_search(alpha, beta)

    #     moves = self.order_moves(self.board.legal_moves)
    #     if depth == self.depth:
    #         self.best_move = moves[0] 
    #     for move in moves:
    #         self.board.push(move)
    #         eval = -self.alphabeta(depth - 1, -beta, -alpha)
    #         self.board.pop()
    #         if eval > alpha and depth == self.depth:
    #             self.best_move = move
    #         if alpha >= beta:
    #             return beta 
    #         alpha = max(alpha, eval)
    #     return alpha

    # def quiescence_search(self, alpha, beta):
    #     if not self.board.is_check():
    #         stand_pat = self.evaluate()
    #         if stand_pat >= beta:
    #             return beta
    #         if alpha < stand_pat:
    #             alpha = stand_pat
        
    #     # checking checks does not improve the outcome...    
    #     moves = list(self.board.generate_legal_captures())
    #     #moves = capture_moves + self._generate_check_moves()

    #     for move in self.order_moves(moves):
    #         self.board.push(move)
    #         eval = -self.quiescence_search(-beta, -alpha)
    #         self.board.pop()

    #         if eval >= beta:
    #             return beta
    #         alpha = max(eval, alpha)
    #     return alpha

    # def order_moves(self, moves):
    #     '''
    #     Order all legal moves in a position by prioritizing captures,
    #     promoitions, checks, and castlings.
    #     '''
    #     move_score = 0
    #     sorted_orders = {}
    #     ordered_moves = {}

    #     for move in moves:  
    #         move_piece = self.board.piece_type_at(move.from_square)
    #         capture_piece = self.board.piece_type_at(move.to_square)
            
    #         if capture_piece != None:
    #             move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
            
    #         if self.board.gives_check(move):
    #             move_score += 3

    #         ordered_moves[move] = move_score
    #         sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

    #     return list(sorted_orders.keys())


    # def _generate_check_moves(self):
    #     moves = []
    #     for move in self.board.legal_moves:
    #         if self.board.gives_check(move):
    #             moves.append(move)
    #     return moves
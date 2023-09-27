import chess
import logging

class ChessEngine:
    def __init__(self, depth):
        self.board = chess.Board()  
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
            -20,-10,-10, -5, -5,-10,-10,-20
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
            -30, -40, -40, -50, -50, -40, -40, -30
        ]
        self.black_king_table = self.white_king_table[::-1]
    def set_depth(self, depth):
        self.depth = depth
    
    # TODO: ensure valid fen ?
    def set_board_with_FEN(self, fen):
        self.board = chess.Board(fen)
    
    # Return board evaluation based on material and positional advantages
    # Evaluation is subjective to the player (+ is winning, - is losing)
    # Material Evaluation from: https://www.chessprogramming.org/Simplified_Evaluation_Function
    def evaluate(self):
        eval = 0
        for square, piece in self.board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    eval += (100 + self.white_pawn_table[square])
                else:
                    eval -= (100 + self.black_pawn_table[square])
            elif piece.piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    eval += (320 + self.white_knight_table[square])
                else:
                    eval -= (320 + self.black_knight_table[square])
            elif piece.piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    eval += (330 + self.white_bishop_table[square])
                else:
                    eval -= (330 + self.black_bishop_table[square])    
            elif piece.piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    eval += (500 + self.white_rook_table[square])
                else:
                    eval -= (500 + self.black_rook_table[square])
            elif piece.piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    eval += (900 + self.white_queen_table[square])
                else:
                    eval -= (900 + self.black_queen_table[square])    
            elif piece.piece_type == chess.KING and piece.color == chess.WHITE:
                eval += (self.white_king_table[square] + 20000)
            elif piece.piece_type == chess.KING and piece.color == chess.BLACK:
                eval -= (self.black_king_table[square] + 20000)
        return eval if self.board.turn == chess.WHITE else -eval

    def alphabeta(self, alpha, beta, depth):
        logging.info(f'alphabeta(): depth={depth}')
        # check for checkmate/draw
        if self.board.is_game_over(): 
            if self.board.is_check():
                return float('-inf')
            return 0 # draw  
        
        # TODO: how to check if 3fold rep is good for bad
        # if self.board.can_claim_threefold_repetition():
        #     return float('-inf') if self.evaluate() < 0 else 0
        
        
        if depth == 0: return self.quiescence_search(alpha, beta)

        moves = self.order_moves()
        if depth == self.depth:
            self.best_move = moves[0]
        for move in moves:
            ### Debugging Purposes
            # if depth == 4:
            #     print(f"Move {self.board.san(move)} is being considered...")
            self.board.push(move)
            eval = -self.alphabeta(-beta, -alpha, depth-1)
            self.board.pop()
            if eval >= beta: return beta
            if eval > alpha:
                alpha = eval
                if depth == self.depth:
                    self.best_move = move
                    # print(f"Depth {depth}: Move: {self.board.san(self.best_move)} is best with eval: {eval}")
        return alpha


    # TODO: need to deal with CHECK horizon effects..?
    def quiescence_search(self, alpha, beta):
        stand_pat = self.evaluate()
        if stand_pat >= beta: return beta
        if alpha < stand_pat: alpha = stand_pat
        for capture in self.board.generate_legal_captures():
            self.board.push(capture)
            eval = -self.quiescence_search(-beta, -alpha)
            self.board.pop()
            if eval >= beta: return beta
            alpha = max(alpha, eval)
        return alpha
    
    def order_moves(self):
        sorted_orders = {}
        ordered_moves = {}
        for move in self.board.generate_legal_moves(): 
            move_score = 0 
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            # MVV/LVA
            if capture_piece:
                move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
            # Checks
            if self.board.gives_check(move) :
                move_score += 1
            ordered_moves[move] = move_score
            # Promotions
            if move_piece == chess.PAWN and chess.square_rank(move.to_square) % 7 == 0:
                move_score += 100
            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))
        return list(sorted_orders.keys())

    def print_board(self):
        for rank in range(7,-1,-1):
            for file in range(8):
                square = rank * 8 + file
                piece = self.board.piece_at(square)
                if piece:
                    print(self.board.piece_at(square).unicode_symbol(), end=' ')
                else:
                    print("+", end=' ')
            print()

    def _get_piece_value(self, piece_type):
        if piece_type == chess.PAWN:
            return 100
        elif piece_type == chess.KNIGHT:
            return 320
        elif piece_type == chess.BISHOP:
            return 330
        elif piece_type == chess.ROOK:
            return 500
        elif piece_type == chess.QUEEN:
            return 900
        elif piece_type == chess.KING:
            return 20000
        
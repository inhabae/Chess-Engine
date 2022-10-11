import math
import chess


'''
Given a FEN, the program returns the best move.
Has opening lines, basic endgame knowledge.

consider moves -> min_max evaluation using alpha beta -> evaluate

Criteria:
1. Material imbalance
2. Piece Activity

'''
class ChessEngine:
    def __init__(self, fen=chess.STARTING_FEN):
        self.board = chess.Board(fen)

        # list that store positonal values for each piece on a specific square
        # chess.A1 = 0, chess.B1 = 1, ... , chess.H8 = 63
        # e.g. self.white_pawn_table[chess.A5] is 5

        self.black_pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

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

        self.knight_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ]
        self.bishop_table = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]
        self.black_rook_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ]
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

        self.queen_table = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]
    
        self.black_king_table = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]

        self.white_king_table = [
           20, 30, 10,  0,  0, 10, 30, 20,
           20, 20,  0,  0,  0,  0, 20, 20,
           -10,-20,-20,-20,-20,-20,-20,-10,
           -20,-30,-30,-40,-40,-30,-30,-20,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30
        ]

        # store evaluation of the current position
        self.current_eval = self.evaluate()

        # store best move
        self.best_move = None

        # store depth for searching moves
        self.depth_limit = 4

    def evaluate(self):
        '''
        Evaluate
        '''
        material = 0
        for square in chess.SQUARES:
            if self.board.piece_at(square):
                piece_color = self.board.piece_at(square).color
                piece_type = self.board.piece_at(square).piece_type
                if piece_type == chess.PAWN:
                    material += (105 + self.white_pawn_table[square]) if piece_color == chess.WHITE else (-105 - self.black_pawn_table[square])
                elif piece_type == chess.KNIGHT:
                    material += (320 + self.knight_table[square]) if piece_color == chess.WHITE else (-320 - self.knight_table[square])
                elif piece_type == chess.BISHOP:
                    material += (330 + self.bishop_table[square]) if piece_color == chess.WHITE else (-330 - self.bishop_table[square])
                elif piece_type == chess.ROOK:
                    material += (500 + self.white_rook_table[square]) if piece_color == chess.WHITE else (-500 - self.black_rook_table[square])
                elif piece_type == chess.QUEEN:
                    material += (900 + self.queen_table[square]) if piece_color == chess.WHITE else (-900 - self.queen_table[square])
                else: 
                    material += (self.white_king_table[square]) if piece_color == chess.WHITE else (-self.black_king_table[square])
        return material if self.board.turn == chess.WHITE else -material


    def negamax(self, depth):
        '''
        Using negamax, the engine evaluates the position.
        '''
        # end of recursion, return the evaluation of the position 
        if self.board.is_game_over() == True:
            if self.board.is_check():
                return -math.inf
            return 0 # draw  

        if depth == 0:
            eval = self.evaluate()
            return eval

        max_eval = -math.inf
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = -self.negamax(depth - 1)
            self.board.pop()
            max_eval = max(max_eval, eval)
        return max_eval

    def alphabeta(self, depth, alpha=-math.inf, beta=math.inf):
        '''
        Using alpha beta pruning, the engine returns the best move and 
        evaluation of the position by going into a given depth.
        '''
        # might need to check for draws, change later
        if self.board.is_game_over(): 
            if self.board.is_check():
                return -math.inf
            return 0 # draw  
        
        if self.board.can_claim_threefold_repetition():
            return -math.inf if self.evaluate() < 0 else 0

        if depth == 0: # need quiescence search, change later
            eval = self.quiescence_search(alpha, beta)
            return eval

        moves = self.order_moves(self.board.legal_moves)
        if depth == self.depth_limit:
            self.best_move = moves[0] 
        for move in moves:
            self.board.push(move)
            eval = -self.alphabeta(depth - 1, -beta, -alpha)
            self.board.pop()
            if eval > alpha and depth == self.depth_limit:
                self.best_move = move
            if alpha >= beta:
                return beta 
            alpha = max(alpha, eval)
        return alpha

    def quiescence_search(self, alpha, beta):
        stand_pat = self.evaluate()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        moves = self.board.generate_legal_captures()
        for move in self.order_moves(moves):
            self.board.push(move)
            eval = -self.quiescence_search(-beta, -alpha)
            self.board.pop()

            if eval >= beta:
                return beta
            alpha = max(eval, alpha)
        return alpha

    # def check_endgame(self):
    #     '''
    #     Check if the game state is an endgame.
    #     If True, modify the piece value dictionary for kings so that
    #     they can move to the center.
    #     '''
    #     if self.not_endgame:
    #         bf = self.board.board_fen()
    #         piece_count = 0
    #         for char in bf:
    #             if char.isalpha() and char.islower() != 'p':
    #                 piece_count += 1
                
    #         king_tables = [
    #             -50,-40,-30,-20,-20,-30,-40,-50,
    #             -30,-20,-10,  0,  0,-10,-20,-30,
    #             -30,-10, 20, 30, 30, 20,-10,-30,
    #             -30,-10, 30, 40, 40, 30,-10,-30,
    #             -30,-10, 30, 40, 40, 30,-10,-30,
    #             -30,-10, 20, 30, 30, 20,-10,-30,
    #             -30,-30,  0,  0,  0,  0,-30,-30,
    #             -50,-30,-30,-30,-30,-30,-30,-50
    #         ]

    #         if bf.count('q') +  bf.count('Q') == 0 or piece_count <= 6:
    #             for s in chess.SQUARES:
    #                 self.value_w_king[s] = king_tables[s]
    #                 self.value_b_king[s] = king_tables[s]
    #             self.not_endgame = False

    def order_moves(self, moves):
        '''
        Order all legal moves in a position by prioritizing captures,
        promoitions, checks, and castlings.
        '''
        move_score = 0
        sorted_orders = {}
        ordered_moves = {}

        for move in moves:  
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            
            if capture_piece != None:
                move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
            
            if self.board.gives_check(move):
                move_score += 50

            ordered_moves[move] = move_score
            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

        return list(sorted_orders.keys())
    

    def _get_piece_value(self, piece_type):
        if piece_type == chess.PAWN:
            return 105
        elif piece_type == chess.KNIGHT:
            return 320
        elif piece_type == chess.BISHOP:
            return 330
        elif piece_type == chess.ROOK:
            return 500
        elif piece_type == chess.QUEEN:
            return 900
        return 0
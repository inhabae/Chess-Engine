import math
import chess
import random


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
        self.current_eval = self.init_evaluate() if self.board.turn == chess.WHITE else -self.init_evaluate()

        # store evaluation of the possible position
        self.pos_eval = 0

        # store move to use for evaluation
        self.new_move = None

    def init_evaluate(self):
        '''
        Set the initial evaluation of a position, in case a position is given to the engine.
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
        return material

    def evaluate(self, move):
        '''
        Return the difference between white and black's materials after a move.
        '''
        to_square = move.to_square
        from_square = move.from_square
        self.pos_eval = 0

        moved_piece = self.board.piece_at(move.from_square)
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            captured_piece_type = self.board.piece_at(move.to_square).piece_type
            captured_piece_color = self.board.piece_at(move.to_square).color
        
        if moved_piece.piece_type == chess.PAWN:
            if moved_piece.color == chess.WHITE:
                self.pos_eval += self.current_eval - self.white_pawn_table[from_square] + self.white_pawn_table[to_square]
            else:
                self.pos_eval += self.current_eval - self.black_pawn_table[from_square] + self.black_pawn_table[to_square]
        elif moved_piece.piece_type == chess.KNIGHT: 
            self.pos_eval += self.current_eval - self.knight_table[from_square] + self.knight_table[to_square]
        elif moved_piece.piece_type == chess.BISHOP:
            self.pos_eval += self.current_eval - self.bishop_table[from_square] + self.bishop_table[to_square]
        elif moved_piece.piece_type == chess.ROOK:
            if moved_piece.color == chess.WHITE:
                self.pos_eval += self.current_eval - self.white_rook_table[from_square] + self.white_rook_table[to_square]
            else:
                self.pos_eval += self.current_eval - self.black_rook_table[from_square] + self.black_rook_table[to_square]
        elif moved_piece.piece_type == chess.QUEEN:
            self.pos_eval += self.current_eval - self.queen_table[from_square] + self.queen_table[to_square]
        else:
            if moved_piece.color == chess.WHITE:
                self.pos_eval += self.current_eval - self.white_king_table[from_square] + self.white_king_table[to_square]
            else:
                self.pos_eval += self.current_eval - self.black_king_table[from_square] + self.black_king_table[to_square]

        if captured_piece == None:
            pass
        elif captured_piece_type == chess.PAWN:
            positional_value = self.white_pawn_table[to_square] if captured_piece_color == chess.WHITE else self.black_pawn_table[to_square]
            self.pos_eval += 105 + positional_value
        elif captured_piece_type == chess.KNIGHT:
            positional_value = self.knight_table[to_square]
            self.pos_eval += 320 + positional_value
        elif captured_piece_type == chess.BISHOP:
            positional_value = self.bishop_table[to_square]
            self.pos_eval += 330 + positional_value
        elif captured_piece_type == chess.ROOK:
            positional_value = self.white_rook_table[to_square] if captured_piece_color == chess.WHITE else self.black_rook_table[to_square]
            self.pos_eval += 500 + positional_value
        elif captured_piece_type == chess.QUEEN:
            positional_value = self.queen_table[to_square]
            self.pos_eval += 320 + positional_value

        return self.pos_eval

    def alphabeta(self, depth, alpha=-math.inf, beta=math.inf):
        '''
        Using alpha beta pruning, the engine returns the best move and 
        evaluation of the position by going into a given depth.
        '''
        # might need to check for draws, change later
        if self.board.is_game_over(): 
            eval =  -math.inf
            return None, eval
        
        if self.board.can_claim_threefold_repetition():
            return None, -math.inf if self.search_all_captures(alpha, beta) < 0 else  None, 0

        if depth == 0: # need quiescence search, change later
            self.board.pop()
            eval = self.evaluate(self.new_move)
            self.board.push(self.new_move)
            return None, eval
        moves = self.order_moves()
        best_move = random.choice(moves)

        for move in moves:
            self.new_move = move # store move used for evaluate()
            self.board.push(move)
            eval = -self.alphabeta(depth - 1, -beta, -alpha)[1]

            #for checking certain moves
            # if depth == 4:
            #     print(f"current best move {best_move}")
            #     print(f"move {move} has an eval of {eval}")

            self.board.pop()
            if eval > alpha:
                best_move = move
            if alpha >= beta:
                return best_move, beta 
            alpha = max(alpha, eval)
                
        return best_move, alpha

    # def search_all_captures(self, alpha, beta):
    #     '''
    #     Using alpha beta pruning, the function searches only capture moves until
    #     there is longer a good capture move.
    #     '''

    #     eval = self.evaluate()

    #     if eval >= beta:
    #         return beta
    #     alpha = max(alpha, eval)

    #     moves = self.get_capture_moves()

    #     for move in moves:
    #         self.board.push(move)
    #         eval = -1 * self.search_all_captures(-beta, -alpha)
    #         self.board.pop()

    #         if eval >= beta:
    #             return beta
    #         alpha = max(alpha, eval)

    #     return alpha

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

    def order_moves(self):
        '''
        Order all legal moves in a position by prioritizing captures,
        promoitions, checks, and castlings.
        '''
        moves = list(self.board.legal_moves)
        move_score = 0
        sorted_orders = {}
        ordered_moves = {}

        capture_moves = {}

        for move in moves:  
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            
            # if capture_piece != None:
            #     move_score = self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
    

            if self.board.is_castling(move):
                move_score += 1
            
            if self.board.gives_check(move):
                move_score += 10

            ordered_moves[move] = move_score
            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

        return list(sorted_orders.keys())
    
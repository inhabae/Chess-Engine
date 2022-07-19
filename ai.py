from json.encoder import INFINITY
from optparse import Values
import chess
import random


'''
Given a FEN, the program returns the best move.
Has opening lines, basic endgame knowledge.

consider moves -> min_max evaluation -> return 

Criteria:
1. King Safety
2. Center Control
3. Material Advantage

'''
class ChessAI:
    def __init__(self, fen=chess.STARTING_FEN):
        self.board = chess.Board(fen)
        self.move_number = 0

        self.minimax_num = 0 # for testing
        self.ab_num = 0 # for testing
        self.s_flag = 0

        self.value_w_pawn = {}
        self.value_b_pawn = {} 

        self.value_knight = {}
        self.value_bishop = {}
        self.value_w_rook = {}
        self.value_b_rook = {}

        self.value_queen = {}
        self.value_w_king = {}
        self.value_b_king = {}

        self.occupied_squares = []
        
        self.initialize_table()

    def count_materials(self):
        '''
        Takes in the color of a player's pieces: 'white' or 'black',
        Returns the total value of materials of the player.
        '''
        material = 0

        for square in chess.SQUARES:
            if self.board.piece_at(square):
                piece_color = self.board.piece_at(square).color
                piece_type = self.board.piece_at(square).piece_type
                if piece_type == chess.PAWN:
                    material += (105 + self.value_w_pawn[square]) if piece_color == chess.WHITE else (-105 - self.value_b_pawn[square])
                elif piece_type == chess.KNIGHT:
                    material += (320 + self.value_knight[square]) if piece_color == chess.WHITE else (-320 - self.value_knight[square])
                elif piece_type == chess.BISHOP:
                    material += (330 + self.value_bishop[square]) if piece_color == chess.WHITE else (-330 - self.value_bishop[square])
                elif piece_type == chess.ROOK:
                    material += (500 + self.value_w_rook[square]) if piece_color == chess.WHITE else (-500 - self.value_b_rook[square])
                elif piece_type == chess.QUEEN:
                    material += (900 + self.value_queen[square]) if piece_color == chess.WHITE else (-900 - self.value_queen[square])
                elif piece_type == chess.KING:
                    material += 20000 + self.value_w_king[square] if piece_color == chess.WHITE else (-20000 - self.value_b_king[square])
        return material

    def evaluate(self):
        '''
        Return an evaluation for the player with a turn.
        If the player is winning +, if losing -.
        '''
        # material diff evaluation
        evaluation = self.count_materials() # white - black

        return evaluation if self.board.turn == chess.WHITE else -evaluation

    def alphabeta(self, depth, alpha=-INFINITY, beta=INFINITY):
        '''
        Using alpha beta pruning, the engine evaluates the position. 
        '''
        if self.board.is_game_over():
            eval =  -INFINITY
            return None, eval

        if depth == 0:
            val = self.evaluate()
            #return None, val
            
            return None, self.search_all_captures(alpha, beta)
        
        moves = self.order_moves()
        best_move = random.choice(moves)


        for move in moves:
            self.board.push(move)
            eval = -self.alphabeta(depth - 1, -beta, -alpha)[1]

            #for checking certain moves
            # if depth == 4:
            #     print(f"current best move {best_move}")
            #     print(f"move {move} has an eval of {eval}")

            self.board.pop()

            if eval > alpha:
                best_move = move

            if eval >= beta:
                return best_move, beta
            
            alpha = max(alpha, eval)
                
        return best_move, alpha
        
    def _get_piece_value(self, piece):
        if piece == chess.PAWN:
            return 1
        elif piece == chess.KNIGHT or piece == chess.BISHOP:
            return 3
        elif piece == chess.ROOK:
            return 5
        elif piece == chess.QUEEN:
            return 9
        elif piece == chess.KING:
            return 1

    def search_all_captures(self, alpha, beta):
        eval = self.evaluate()

        if eval >= beta:
            return beta
        alpha = max(alpha, eval)

        moves = self.get_capture_moves()

        for move in moves:

            #print(self.board)
            self.board.push(move)
            eval = -1 * self.search_all_captures(-beta, -alpha)
            
            #print(f"move: {move}, eval: {eval}")
            self.board.pop()

            if eval >= beta:
                return beta
            alpha = max(alpha, eval)

            # elif self.board.gives_check(move):
            #     self.board.push(move)
            #     eval = -1 * self.search_all_captures(-beta, -alpha)
            #     self.board.pop()

            #     if eval >= beta:
            #         return beta
            #     alpha = max(alpha, eval)

        return alpha


    def initialize_table(self):
        pawn_table_white = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        pawn_table_black = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        knight_tables = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ]
        bishop_tables = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]
        rook_table_white = [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        rook_table_black = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ]

        queen_tables = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]

        king_tables_white = [
           20, 30, 10,  0,  0, 10, 30, 20,
           20, 20,  0,  0,  0,  0, 20, 20,
           -10,-20,-20,-20,-20,-20,-20,-10,
           -20,-30,-30,-40,-40,-30,-30,-20,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30
        ]

        king_tables_black = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]

        for square in chess.SQUARES:
            self.value_w_pawn[square] = pawn_table_white[square]
            self.value_b_pawn[square] = pawn_table_black[square]

            self.value_knight[square] = knight_tables[square]
            self.value_bishop[square] = bishop_tables[square]

            self.value_w_rook[square] = rook_table_white[square]
            self.value_b_rook[square] = rook_table_black[square]

            self.value_queen[square] = queen_tables[square]
            self.value_w_king[square] = king_tables_white[square]
            self.value_b_king[square] = king_tables_black[square]

    def check_endgame(self):
        # if 'q' not in self.board.board_fen() and 'Q' not in self.board.board_fen():
        #     pass
        # elif 'q' not in self.board.board_fen() 
        pass

    def order_moves(self):
        moves = list(self.board.legal_moves)
        move_score = 0
        sorted_orders = {}
        ordered_moves = {}

        for move in moves:
            
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            

            #print(move_piece, capture_piece)
            if capture_piece != None:
                move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
                #print(f"move: {move}; move score: {move_score}")
            
            if (move_piece == chess.PAWN and chess.square_rank(move.to_square) == 7):
                move_score += self._get_piece_value(move.promotion)

            if self.board.is_castling(move):
                move_score += 1
            
            if self.board.gives_check(move):
                move_score += 10
            # end of ordering
            ordered_moves[move] = move_score
            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

        return list(sorted_orders.keys())
    
    def get_capture_moves(self):
        moves = list(self.board.legal_moves)
        move_score = 0
        sorted_orders = {}
        ordered_moves = {}

        for move in moves:
            
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            
            if capture_piece != None:
                move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
                #print(f"move: {move}; move score: {move_score}")
                ordered_moves[move] = move_score
            # end of ordering
            
        sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

        return list(sorted_orders.keys())
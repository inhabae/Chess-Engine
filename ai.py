from json.encoder import INFINITY
import chess
import random
from collections import OrderedDict

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


    def count_materials(self, player_color):
        '''
        Takes in the color of a player's pieces: 'white' or 'black',
        Returns the total value of materials of the player.
        '''
        material = 0
        bf = self.board.board_fen()

        if player_color == chess.WHITE:
            material = 9 * bf.count('Q') + 5 * bf.count('R') + 3 * bf.count('B') + 3 * bf.count('N') + bf.count('P') 

        elif player_color == chess.BLACK:
            material = 9 * bf.count('q') + 5 * bf.count('r') + 3 * bf.count('b') + 3 * bf.count('n') + bf.count('p') 

        return material 
            

    def evaluate(self, maximizing_color):
        # material diff evaluation
        white_eval = self.count_materials(chess.WHITE)
        black_eval = self.count_materials(chess.BLACK)

        # castle around move 10
        safe_qs_sq = [
            chess.A1, chess.B1, chess.C1,
            chess.A8, chess.B8, chess.C8
        ]
        safe_ks_sq = [
            chess.G1, chess.H1,
            chess.G8, chess.H8
        ]
        
        rook_mask = self.board.occupied_co[maximizing_color] & self.board.rooks
    
        if self.board.king(maximizing_color) in safe_ks_sq and not(rook_mask & chess.BB_FILE_H):
            if maximizing_color == chess.WHITE:
                white_eval += 1 if self.move_number < 10 else 1.5
            else: 
                black_eval += 1 if self.move_number < 10 else 1.5
        
        # elif self.board.king(maximizing_color) in safe_qs_sq and not(rook_mask & chess.BB_FILE_A):
        #     if maximizing_color == chess.WHITE:
        #         white_eval += 0.99 if self.move_number < 10 else 1.5
        #     else: 
        #         black_eval += 0.99 if self.move_number < 10 else 1.5
        

        # knight on edge is bad
        knight_mask = self.board.occupied_co[maximizing_color] & self.board.knights
        if knight_mask & chess.BB_FILE_A or knight_mask & chess.BB_FILE_H:
            if maximizing_color == chess.WHITE:
                white_eval -= 0.9
            else:
                black_eval -= 0.9
            

        evaluation = white_eval - black_eval
        return evaluation if maximizing_color == chess.WHITE else -1 * evaluation
    
    def minimax(self, depth, maximizing_player, maximizing_color):
        if depth == 0 or self.board.is_game_over():
            return None, self.evaluate(maximizing_color)
        
        moves = list(self.board.legal_moves)
        best_move = random.choice(moves)

        if maximizing_player:
            max_eval = -INFINITY
            for move in moves:
                self.minimax_num += 1
                self.board.push(move)
                eval = self.minimax(depth - 1, False, maximizing_color)[1]

                # print(f"Eval: {eval}, Move: {move}")

                self.board.pop()
                if eval > max_eval:
                    best_move = move
                    max_eval = eval
            return best_move, max_eval

        else:
            min_eval = INFINITY
            for move in moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, True, maximizing_color)[1]

                self.board.pop()
                if eval < min_eval:
                    best_move = move
                    min_eval = eval
            return best_move, min_eval

    def alphabeta(self, depth, maximizing_player=True, maximizing_color=chess.WHITE, alpha=-INFINITY, beta=INFINITY):
        '''
        Using alpha beta pruning, the engine evaluates the position. 
        '''
        if self.board.is_game_over():
            eval =  INFINITY if maximizing_player != True else -INFINITY
            return None, eval

        if depth == 0:
            val = self.evaluate(maximizing_color)
            return None, self.search_all_captures(val, val, maximizing_color)
        
        moves = self.order_moves()
        #moves = list(self.board.legal_moves)

        best_move = random.choice(moves)

        if maximizing_player:
            max_eval = -INFINITY
            for move in moves:
                self.ab_num += 1
                self.board.push(move)
                eval = self.alphabeta(depth - 1, False, maximizing_color, alpha, beta)[1]


                # # for checking certain moves
                # if depth == 4:
                #     print(f"move {move} has an eval of {eval}")

                self.board.pop()
                if eval > max_eval:
                    best_move = move
                    max_eval = eval

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval

        else:
            min_eval = INFINITY
            for move in moves:
                self.ab_num += 1
                self.board.push(move)
                eval = self.alphabeta(depth - 1, True, maximizing_color, alpha, beta)[1]

                #print(f"\tmove {move} has eval of {eval}")

                self.board.pop()
                if eval < min_eval:
                    best_move = move
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def order_moves(self):
        moves = list(self.board.legal_moves)
        move_score = 0
        ordered_moves = {}

        for move in moves:
            
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            
            if capture_piece != None:
                move_score = 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
            
            if (move_piece == chess.PAWN and chess.square_rank(move.to_square) == 7):
                move_score += self._get_piece_value(move.promotion)

            if self.board.is_castling(move):
                move_score += 5
            
            # end of ordering
            ordered_moves[move] = move_score
            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))

        return list(sorted_orders.keys())
        
    def _get_piece_value(self, piece):
        if piece == chess.PAWN:
            return 1
        elif piece == chess.KNIGHT or chess.BISHOP:
            return 3
        elif piece == chess.ROOK:
            return 5
        elif piece == chess.QUEEN:
            return 9

    def search_all_captures(self, alpha, beta, maximizing_color):
        eval = self.evaluate(maximizing_color)

        if eval >= beta:
            return beta
        alpha = max(alpha, eval)

        for move in list(self.board.legal_moves):
            if self.board.is_capture(move):
                self.board.push(move)
                eval = -1 * self.search_all_captures(-beta, -alpha, maximizing_color)
                self.board.pop()

                if eval >= beta:
                    return beta
                alpha = max(alpha, eval)

            elif self.board.is_check(move):
                self.board.push(move)
                eval = -1 * self.search_all_captures(-beta, -alpha, maximizing_color)
                self.board.pop()

                if eval >= beta:
                    return beta
                alpha = max(alpha, eval)

        return alpha

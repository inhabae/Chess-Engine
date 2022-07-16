from json.encoder import INFINITY
import chess
import functools
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


    def count_materials(self, player_color):
        '''
        Takes in the color of a player's pieces: 'white' or 'black',
        Returns the total value of materials of the player.
        '''
        material = 0
        bf = self.board.board_fen()

        if player_color == 'white':
            material = 9 * bf.count('Q') + 5 * bf.count('R') + 3 * bf.count('B') + 3 * bf.count('N') + bf.count('P') 

        elif player_color == 'black':
            material = 9 * bf.count('q') + 5 * bf.count('r') + 3 * bf.count('b') + 3 * bf.count('n') + bf.count('p') 

        return material 
            

    def evaluate(self, maximizing_color):
        white_eval = self.count_materials('white')
        black_eval = self.count_materials('black')

        evaluation = white_eval - black_eval
        return evaluation if maximizing_color == 'white' else -1 * evaluation
    
    def minimax(self, depth, maximizing_player, maximizing_color):
         
        if depth == 0 or self.board.is_game_over():
            return None, self.evaluate(maximizing_color)
        
        moves = list(self.board.legal_moves)
        best_move = random.choice(moves)

        if maximizing_player:
            max_eval = -INFINITY
            for move in moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, False, maximizing_color)[1]

                # if depth == 3:
                #     print(f"Depth: {depth}; Move: {move}; eval: {eval}")
                # if depth == 1:
                #     print(f"\t\tDepth: {depth}; Move: {move}; eval: {eval}")
                
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
                
                #print(f"Depth: {depth}; Move: {move}; eval: {eval}")

                self.board.pop()
                if eval < min_eval:
                    best_move = move
                    min_eval = eval
            return best_move, min_eval

    def alphabeta(self, depth, maximizing_player, maximizing_color, alpha, beta):
        '''
        Using alpha beta pruning, the engine evaluates the position. 
        '''
        if depth == 0 or self.board.is_game_over():
            return None, self.evaluate(maximizing_color)
        
        moves = list(self.board.legal_moves)
        best_move = random.choice(moves)

        if maximizing_player:
            max_eval = -INFINITY
            for move in moves:
                self.board.push(move)
                eval = self.alphabeta(depth - 1, False, maximizing_color, alpha, beta)[1]
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
                self.board.push(move)
                eval = self.alphabeta(depth - 1, True, maximizing_color, alpha, beta)[1]

                self.board.pop()
                if eval < min_eval:
                    best_move = move
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval


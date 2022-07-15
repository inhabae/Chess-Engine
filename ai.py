from json.encoder import INFINITY
import chess

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
        self.turn = None
        self.fen = fen
        self.alphabeta_num = 0
        self.minmax_num = 0

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
            

    def evaluate(self):
        white_eval = self.count_materials('white')
        black_eval = self.count_materials('black')

        evaluation = white_eval - black_eval
        #print(f"turn: {self.board.turn} ; eval is {evaluation}")
        return evaluation
       
    def update_board(self, fen):
        '''for testing, update the board given fen'''
        self.board = chess.Board(fen)

    def minimax(self, depth, maximizing_player):
        '''
        Using minimax, the engine evaluates the position.
        '''
        # end of recursion, return the evaluation of the position   
        if depth == 0:
            return self.evaluate()
        
        if self.board.is_game_over() == True:
            if self.board.is_check():
                return -INFINITY
            return 0 # draw

        if maximizing_player:
            max_eval = -INFINITY
            for move in self.board.legal_moves:
                #print(f"board before:\n {self.board}")
                self.board.push(move)
                self.minmax_num += 1 # comment out later
                eval = self.minimax(depth - 1, False) # recursion
                #print(f"board after:\n {self.board}")
                #print(f"minimax eval is {eval}")
                self.board.pop()
                max_eval = max(max_eval, eval)
            #print(f"max eval is {max_eval}")
            return max_eval

        else:
            min_eval = INFINITY
            for move in self.board.legal_moves:
                self.board.push(move)
                self.minmax_num+=1 # comment out later
                eval = self.minimax(depth - 1, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def alphabeta(self, depth, maximizing_player, alpha, beta):
        '''
        Using alpha beta pruning, the engine evaluates the position. 
        '''
        # end of recursion, return the evaluation of the position   
        if depth == 0:
            return self.evaluate()
        
        if self.board.is_game_over() == True:
            if self.board.is_check():
                return -INFINITY
            return 0
        if maximizing_player:
            max_eval = -INFINITY
            for move in self.board.legal_moves:
                self.board.push(move)
                self.alphabeta_num += 1
                eval = self.alphabeta(depth - 1, False, alpha, beta)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = INFINITY
            for move in self.board.legal_moves:
                self.board.push(move)
                self.alphabeta_num += 1
                eval = self.alphabeta(depth - 1, True, alpha, beta)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

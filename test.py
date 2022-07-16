import chess
import random
import ai as ai




ai_chess = ai.ChessAI()

ai_chess.board = chess.Board('8/7K/2kp4/8/3p4/3P4/8/5qr1 b - - 1 1')
print(ai_chess.minimax(3, True, 'black'))

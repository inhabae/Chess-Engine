import chess
import random
import ai as ai




ai_chess = ai.ChessAI()

ai_chess.board = chess.Board('2r2bkb/2r1pppp/2q5/2r5/8/2R5/2Q1PPPP/2R2BKB w - - 0 1')
print(ai_chess.alphabeta(4)[0])

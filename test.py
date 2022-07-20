import chess
import random
import engine as engine




ai_chess = engine.ChessEngine()

ai_chess.board = chess.Board('2r2bkb/2r1pppp/2q5/2r5/8/2R5/2Q1PPPP/2R2BKB w - - 0 1')
print(ai_chess.alphabeta(4)[0])

import engine as engine
import chess

chess_ai = engine.ChessEngine()
"""
print("Testing for evaluate() with a pawn move 1. e4 and 1.Nf3:")
print("Expected: White should gain 40 points, as the e-pawn moves from -20 to 20.")
chess_ai.evaluate(chess.Move.from_uci("e2e4"))
print(f"Actual: {chess_ai.pos_eval}")

chess_ai.pos_eval  = 0
print("Expected: White should gain 50 points, as the knight moves from -40 to 10.")
chess_ai.evaluate(chess.Move.from_uci("g1f3"))
print(f"Actual: {chess_ai.pos_eval}")

print("Testing for evaluate() with a capture move:")
chess_ai = engine.ChessEngine('kb6/pp4r1/5Q2/8/8/8/PP6/KB6 w - - 0 1')
print("Expected: White should gain 500 points, as queen captures a rook.")
### initial values should be Q on f6 (905) - R on g7 (500) = 405
### after a capture, white gains 500 and lose a positional value of 5 = 900
eval = chess_ai.evaluate(chess.Move.from_uci("f6g7"))
print(f"Actual: before capture: {chess_ai.current_eval}, after: {eval}")

### Check to see if a positional value is correctly reflected in the evaluation
chess_ai = engine.ChessEngine('kb6/pp6/5Q2/8/8/8/PP3r2/KB6 w - - 0 1')
print("Expected: White should gain 505 points, as queen captures a rook on a good square.")
### initial values should be Q on f6 (905) - R on f2 (510) = 395
### after a capture, white gains 510 and lose a positional value of 5 = 900
eval = chess_ai.evaluate(chess.Move.from_uci("f6f2"))
print(f"Actual: before capture: {chess_ai.current_eval}, after: {eval}")

chess_ai = engine.ChessEngine('kb6/pp6/5Q2/8/8/8/PP3r2/KB6 w - - 0 1')
print("Expected: White should gain 515 points, as queen from a bad square captures a rook on a good square.")
### initial values should be Q on e1 (895) - R on f2 (510) = 385
### after a capture, white gains 510 and a positional value of 5 = 900
eval = chess_ai.evaluate(chess.Move.from_uci("f6f2"))
print(f"Actual: before capture: {chess_ai.current_eval}, after: {eval}")

chess_ai = engine.ChessEngine('kb6/pp6/8/3r4/8/8/PP6/KB1Q4 w - - 0 1')
print("Expected: White should gain 515 points, as queen from a bad square captures a rook.")
### initial values should be Q on d1 (895) - R on d5 (500) = 395
### after a capture, white gains 500 and a positional value of 10 = 905
eval = chess_ai.evaluate(chess.Move.from_uci("d1d5"))
print(f"Actual: before capture: {chess_ai.current_eval}, after: {eval}")
"""


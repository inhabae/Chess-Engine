import engine as engine

chess_ai = engine.ChessEngine()
'''
print("Testing for evaluate() with a pawn move 1. e4 and 1.Nf3:")
print("White should gain 40 points, as the e-pawn moves from -20 to 20.")
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('e2e4')
after_eval = chess_ai.evaluate()
print(f"before 1. e4: {before_eval}; after 1. e4: {after_eval}")

print("Black should gain 50 points, as the knight moves from -40 to 10.")
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('g8f6')
after_eval = chess_ai.evaluate()
print(f"before 1... Nf6: {before_eval}; after 1... Nf6: {after_eval}")

print("Testing for evaluate() with a capture move:")
chess_ai = engine.ChessEngine('kb6/pp4r1/5Q2/8/8/8/PP6/KB6 w - - 0 1')
print("White should gain 500 points, as queen captures a rook.")
### initial values should be Q on f6 (905) - R on g7 (500) = 405
### after a capture, white gains 500 and loses a positional value of 5 = 900
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('f6g7')
after_eval = chess_ai.evaluate()
print(f"before 1. Qxg7: {before_eval}; after 1. Qxg7: {after_eval}")


### Check to see if a positional value is correctly reflected in the evaluation
chess_ai = engine.ChessEngine('kb6/pp6/5Q2/8/8/8/PP3r2/KB6 w - - 0 1')
print("Expected: White should gain 505 points, as queen captures a rook on a good square.")
### initial values should be Q on f6 (905) - R on f2 (510) = 395
### after a capture, white gains 510 and lose a positional value of 5 = 900
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('f6f2')
after_eval = chess_ai.evaluate()
print(f"before 1. Qxf2: {before_eval}; after 1. Qxf2: {after_eval}")

chess_ai = engine.ChessEngine('kb6/pp6/8/8/8/8/PP3r2/KB2Q3 w - - 0 1')
print("Expected: White should gain 515 points, as queen from a bad square captures a rook on a good square.")
### initial values should be Q on e1 (895) - R on f2 (510) = 385
### after a capture, white gains 510 and a positional value of 5 = 900
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('e1f2')
after_eval = chess_ai.evaluate()
print(f"before 1. Qxf2: {before_eval}; after 1. Qxf2: {after_eval}")


chess_ai = engine.ChessEngine('kb6/pp6/8/3r4/8/8/PP6/KB1Q4 w - - 0 1')
print("Expected: White should gain 505 points, as queen from a bad square captures a rook.")
### initial values should be Q on d1 (895) - R on d5 (500) = 395
### after a capture, white gains 500 and a positional value of 10 = 905
before_eval = chess_ai.evaluate()
chess_ai.board.push_uci('d1d5')
after_eval = chess_ai.evaluate()
print(f"before 1. Qxd5: {before_eval}; after 1. Qxd5: {after_eval}")

### Check evaluate() for white to move AND black to move
chess_ai = engine.ChessEngine('k1q5/ppp5/8/8/8/8/PPP5/KRQ5 w - - 0 1')
print("White to Move: White is up 500 points with an extra rook.")
print(f"Evaluation: {chess_ai.current_eval}")
chess_ai = engine.ChessEngine('k1q5/ppp5/8/8/8/8/PPP5/KRQ5 b - - 0 1')
print("White to Move: Black is down 500 points, a full rook down.")
print(f"Evaluation: {chess_ai.current_eval}")

### Check evaluate() with multiple moves to see how evaluation changes.
chess_ai = engine.ChessEngine('k1q5/ppp5/8/8/8/8/PPP5/KRQ5 w - - 0 1')
print(chess_ai.board)
print(f"Evaluation: {chess_ai.evaluate()}")
chess_ai.board.push_san('b2b4')
print(chess_ai.board)
print(f"Evaluation: {chess_ai.evaluate()}")


print("Testing for negamax() with mate in 2:")
chess_ai = engine.ChessEngine('2bqkbn1/2pppp2/np2N3/r3P1p1/p2N2B1/5Q2/PPPPKPP1/RNB2r2 w - - 0 1')
print(f"Before evaluation: {chess_ai.current_eval}")
eval = chess_ai.negamax(3)
print(f"After evaluation: {eval}")


print("Testing for negamax() with a bad capture that leads to mate:")
chess_ai = engine.ChessEngine('6k1/5ppp/8/8/n7/8/2r2PPP/R5K1 w - - 0 1')
print(f"Before evaluation: {chess_ai.current_eval}")
eval = chess_ai.negamax(3)
print(f"and eval is {eval}")
'''

print("Testing for alphabeta() with mate in 2:")
chess_ai = engine.ChessEngine('2bqkbn1/2pppp2/np2N3/r3P1p1/p2N2B1/5Q2/PPPPKPP1/RNB2r2 w - - 0 1')
print(f"Before evaluation: {chess_ai.current_eval}")
eval = chess_ai.alphabeta(4)
print(f"After evaluation: {eval}")
print(chess_ai.best_move)

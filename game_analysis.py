import engine as engine

### Check why engine chose a certain move (usually bad) to see
### how to improve the engine.

### Why not e4 or d4 instead of moving a pawn one square up?
# chess_ai = engine.ChessEngine('rnbqkb1r/pppppp1p/5np1/8/8/2N2N2/PPPPPPPP/R1BQKB1R w KQkq - 0 3')
# eval = chess_ai.alphabeta(4)
# print(f"{chess_ai.best_move} is the move, with eval of {eval}")

### compare evals of e4 and d3
# print("Evaluation of 3. e4")
# chess_ai = engine.ChessEngine('rnbqkb1r/pppppp1p/5np1/8/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 0 3')
# print(chess_ai.current_eval)
# print("Evaluation of 3. d3")
# chess_ai = engine.ChessEngine('rnbqkb1r/pppppp1p/5np1/8/8/2NP1N2/PPP1PPPP/R1BQKB1R b KQkq - 0 3')
# print(chess_ai.current_eval)

### e4 has a better outcome, so why did engine choose this line?

### Why not castle instead of Kf1
# chess_ai = engine.ChessEngine('r2qk2r/p1p2ppp/2pbpn2/3p1b2/3P4/2N1PN2/PPPB1PPP/R2QK2R w KQkq - 2 8')
# eval = chess_ai.alphabeta(4)
# print(f"{chess_ai.best_move} is the move, with eval of {eval}")

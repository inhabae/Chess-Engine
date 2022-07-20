import cProfile
import engine as engine


chess_ai = engine.ChessEngine('2rqkb1r/3bn1pp/1pnp1p2/p1p1p3/P1B1P3/1PNPBN1P/2P2PP1/R2Q1RK1 w k - 0 11')

cProfile.run('chess_ai.alphabeta(4)')
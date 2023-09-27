import engine as engine
import chess
import math

DEPTH = 4

chess_engine = engine.ChessEngine(DEPTH)

### Test evaluate()
chess_engine.set_board_with_FEN('8/8/8/8/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('8/ppp2pp1/8/3pp2p/3PP2P/8/PPP2PP1/8 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('2b3n1/ppp2pp1/2n5/1B1pp2p/1b1PP2P/2N5/PPP2PP1/2B3N1 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('8/8/8/6q1/6Q1/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('4k3/8/8/8/8/8/8/4K3 w - - 0 1')
assert chess_engine.evaluate() == 0
# symmetrical board: eval should be 0
chess_engine.set_board_with_FEN('r1b1k1nr/ppp2pp1/2n5/1B1pp1qp/1b1PP1QP/2N5/PPP2PP1/R1B1K1NR w KQkq - 0 1')
assert chess_engine.evaluate() == 0
# symmetrical board except white pawn on h5 and black pawn on h6
# white gets a +5 and black gets a + 5: eval is 0
chess_engine.set_board_with_FEN('r1b1k1nr/ppp2pp1/2n4p/1B1pp1qP/1b1PP1Q1/2N5/PPP2PP1/R1B1K1NR w KQkq - 0 1')
assert chess_engine.evaluate() == 0
# symmetrical board with queens, eval should be 0
chess_engine.set_board_with_FEN('8/8/qqqqqqqq/8/8/QQQQQQQQ/8/8 w - - 0 1')
assert chess_engine.evaluate() == 0
# asymmetrical board with about +600 advantage for blaack
chess_engine.set_board_with_FEN('1k1q4/8/8/8/8/1N6/8/1K6 w - - 1 1')
assert chess_engine.evaluate() < -500

### Test alphabeta()
# mate in 1
chess_engine.set_board_with_FEN('4k3/2Q5/6N1/8/8/8/8/4K3 w - - 0 1') 
assert chess_engine.alphabeta(-math.inf, math.inf, 4) == float('inf')
# mate in 2
chess_engine.set_board_with_FEN('r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w')
assert chess_engine.alphabeta(-math.inf, math.inf, 4) == math.inf
# mate in 4
chess_engine.set_board_with_FEN('r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w')
assert chess_engine.alphabeta(-math.inf, math.inf, 4) == math.inf
# mated in 1
chess_engine.set_board_with_FEN('8/8/8/8/8/5rk1/8/6K1 w - - 0 1')
assert chess_engine.alphabeta(-math.inf, math.inf, 4) == float('-inf')
# mated in 2
chess_engine.set_board_with_FEN('7k/8/8/8/2q5/1r6/7K/8 w - - 0 1')
assert chess_engine.alphabeta(-math.inf, math.inf, 4) == float('-inf')

# find good move
print("Find good move (1):")
chess_engine.set_board_with_FEN('1k1q4/8/8/N7/8/8/8/1K6 w - - 0 1')
chess_engine.alphabeta(-math.inf, math.inf, 4)
print(chess_engine.board.san(chess_engine.best_move))
# find good move
print("Find good move (2):")
chess_engine.set_board_with_FEN('r1bqk1nr/pppp1ppp/2n5/4p1N1/1bB1P3/8/PPPP1PPP/RNBQK2R w KQkq - 0 1')
chess_engine.alphabeta(-math.inf, math.inf, 4)
print(chess_engine.board.san(chess_engine.best_move))









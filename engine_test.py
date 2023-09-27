import engine as engine
import chess


chess_engine = engine.ChessEngine()

# Test evaluate()
chess_engine.set_board_with_FEN('8/8/8/8/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('4K3/8/8/8/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == -50
chess_engine.set_board_with_FEN('8/8/8/1K6/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == -40
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
print(chess_engine.evaluate())
assert chess_engine.evaluate() == 0
# symmetrical board except white pawn on h5 and black pawn on h6
# white gets a +5 and black gets a + 5: eval is 0
chess_engine.set_board_with_FEN('r1b1k1nr/ppp2pp1/2n4p/1B1pp1qP/1b1PP1Q1/2N5/PPP2PP1/R1B1K1NR w KQkq - 0 1')
assert chess_engine.evaluate() == 0
# symmetrical board with queens, eval should be 0
chess_engine.set_board_with_FEN('qqqqqqqq/qQqQQqQq/qqqqqqqq/8/8/QQQQQQQQ/QqQqqQqQ/QQQQQQQQ w - - 0 1')
assert chess_engine.evaluate() == 0
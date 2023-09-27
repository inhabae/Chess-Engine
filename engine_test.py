import engine as engine
import chess

def reverse_board(board):
    return board[63:55:-1] + board[55:47:-1] + board[47:39:-1] + board[39:31:-1] + \
        board[31:23:-1] + board[23:15:-1] + board[15:7:-1] + board[7::-1]

def print_reverse_board(board):
    for i in board[63:55:-1]:
        print(i, end=', ')
    print()
    for i in board[55:47:-1]:
        print(i, end=', ')
    print()
    for i in board[47:39:-1]:
        print(i, end=', ')
    print()
    for i in board[39:31:-1]:
        print(i, end=', ')
    print()
    for i in board[31:23:-1]:
        print(i, end=', ')
    print()
    for i in board[23:15:-1]:
        print(i, end=', ')
    print()
    for i in board[15:7:-1]:
        print(i, end=', ')
    print()
    for i in board[7::-1]:
        print(i, end=', ')
    print()

def convert_board(board):
    for rank in range(7,-1,-1):
        for file in range(8):
            square = rank * 8 + file
            print(board[square], end=', ')
        print()

chess_engine = engine.ChessEngine()
# Check if each table is a reverse of the opposite color
assert chess_engine.white_pawn_table == reverse_board(chess_engine.black_pawn_table)
assert chess_engine.white_knight_table == reverse_board(chess_engine.black_knight_table)
assert chess_engine.white_bishop_table == reverse_board(chess_engine.black_bishop_table)
assert chess_engine.white_rook_table == reverse_board(chess_engine.black_rook_table)
assert chess_engine.white_queen_table == reverse_board(chess_engine.black_queen_table)
assert chess_engine.white_king_table == reverse_board(chess_engine.black_king_table)



# Test evaluate()
chess_engine.set_board_with_FEN('8/8/8/8/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == 0
chess_engine.set_board_with_FEN('4K3/8/8/8/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == -50
chess_engine.set_board_with_FEN('8/8/8/1K6/8/8/8/8 w - - 0 1')
assert chess_engine.evaluate() == -40
# symmetrical board except white pawn on h5 and black pawn on h6
# white gets a +5 and black gets a + 5: eval is 0
chess_engine.set_board_with_FEN('r1b1k1nr/ppp2pp1/2n4p/1B1pp1qP/1b1PP1Q1/2N5/PPP2PP1/R1B1K1NR w KQkq - 0 1')
print(chess_engine.evaluate())
assert chess_engine.evaluate() == -5


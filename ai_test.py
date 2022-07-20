from json.encoder import INFINITY
from operator import xor
import engine as engine
import chess

# print("Testing for count_materials():")
chess_ai = engine.ChessEngine()
# print("At the starting board, each player should have 39 points.")
# print("Expected: The White has 39 material points.")
# print(f"Actual: The White has {chess_ai.count_materials('white')} material points.")

# chess_ai.update_board('8/5k2/p7/1pP5/2p2PP1/P3P3/1K1p1Qp1/8 w - - 0 1')
# print("At the given board, White has 14 points, whereas Black has 5.")
# print(f"The White has {chess_ai.count_materials('white')} material points.")
# print(f"The Black has {chess_ai.count_materials('black')} material points.")

# chess_ai.update_board('8/3k4/8/8/8/8/8/3K4 w - - 0 1')
# print("At the given board, neither has a single material point.")
# print(f"The White has {chess_ai.count_materials('white')} material points.")
# print(f"The Black has {chess_ai.count_materials('black')} material points.")

# print("\nTesting for evaluate():")
# chess_ai.update_board('8/5k2/p7/1pP5/2p2PP1/P3P3/1K1p1Qp1/8 w - - 0 1')
# print("At the given board, White is up 9 material points.")
# print(f"Evaluation: {chess_ai.evaluate()}")

# chess_ai.update_board('8/3k4/8/1q4r1/8/8/3N4/3K4 w - - 0 1')
# print("At the given board, Black is up 11 material points.")
# print(f"Evaluation: {chess_ai.evaluate()}")

# # chess_ai.update_board('k7/8/5r2/8/8/8/5Q2/K7 w - - 0 1')
# # print("At the given board, White has a winning move, capturing the Black Rook.")
# # print("Thus, the correct evaluation with depth of 1 would be +9, up a whole Queen.")
# # print(chess_ai.minimax(1, True))

# # chess_ai.update_board('7R/p2b4/5r1p/1pbk2p1/1PpppP2/6P1/P1BP1Q1P/1K1N4 w - - 0 1')
# # chess_ai.minimax(3, True)
# # chess_ai.alphabeta(3, True, -INFINITY, INFINITY)
# # print(f"At the given board, Minimax looks through {chess_ai.minmax_num} number of positions.")
# # print(f"At the given board, alpha beta pruning looks through {chess_ai.alphabeta_num} number of positions.")

# chess_ai.update_board('k7/8/5r2/8/8/8/5Q2/K7 w - - 0 1')
# print("At the given board, White has a winning move, capturing the Black Rook.")
# print("Thus, the correct evaluation with depth of 1 would be +9, up a whole Queen.")
# print(chess_ai.alphabeta(3, True, -INFINITY, INFINITY))
# #print(chess_ai.minimax(3, True))
# chess_ai.print_nextmove()




# chess_ai.update_board('k7/8/5r2/5p2/8/8/5Q2/K7 w - - 0 1')
# print("At the given board..")
# #print("Thus, the correct evaluation with depth of 1 would be +9, up a whole Queen.")
# print(chess_ai.alphabeta(3, True, -INFINITY, INFINITY))
# #print(chess_ai.minimax(3, True))
# chess_ai.print_nextmove()

#chess_ai.board = chess.Board('7K/8/2kp4/8/3p4/3P4/8/5qr1 w - - 0 1')

# chess_ai.board = chess.Board('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1')
# print(chess_ai.board)

#chess_ai.alphabeta(10, True, -INFINITY, INFINITY)
# print(chess_ai.minimax(1, True))

# chess_ai.board.push(chess_ai.next_move) # the problem
# print(chess_ai.next_move)

#x = chess_ai.minimax(4, True, chess_ai.board.turn)[0]
# x = chess_ai.alphabeta(3, True, chess_ai.board.turn, -INFINITY, INFINITY)[0]


# print(f"best move: {x}; move #'s: {chess_ai.ab_num}")
#print("moves with minimax 97910; moves with ab 5234")
#print(f"moves with minimax {chess_ai.minimax_num}; moves with ab {chess_ai.ab_num}")

# chess_ai.board = chess.Board('6kn/5ppp/8/8/n7/8/5PPP/3Q2K1 w - - 0 1')
# best_move = chess_ai.alphabeta(1, True, chess_ai.board.turn, -INFINITY, INFINITY)[0]

# print(best_move)

# chess_ai.board = chess.Board('r1bqkbnr/p2pp1p1/1pp2p1p/8/1n2N3/4P3/PPPP1PPP/RNBQKB1R w KQkq - 1 7')
# best_move = chess_ai.alphabeta(5, True, chess_ai.board.turn, -INFINITY, INFINITY)[0]
# print(best_move)


# in game 4
#chess_ai.board = chess.Board('8/p1p3k1/Nb4p1/8/5RK1/7N/PP1r1P2/8 w - - 7 33')
# best_move = chess_ai.alphabeta(4)[0]
# print(best_move)

# knight_mask = chess_ai.board.occupied_co[chess_ai.board.turn] & chess_ai.board.knights 
# print(knight_mask)

# if knight_mask & chess.BB_FILE_A:
#     print("yes in a")

# if knight_mask & chess.BB_FILE_B:
#     print("yes in b")


# if knight_mask:
#     knight_edge = chess.msb(knight_mask)

# print(knight_edge)

# safe_qs_sq = [
#             chess.A1, chess.B1, chess.C1,
#             chess.A8, chess.B8, chess.C8
#         ]
# safe_ks_sq = [
#     chess.G1, chess.H1,
#     chess.G8, chess.H8
# ]


# chess_ai.board = chess.Board('r1bqkbnr/ppp2ppp/2np4/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4')

# # rook_mask = chess_ai.board.occupied_co[chess_ai.board.turn] & chess_ai.board.rooks
# # print(rook_mask ^ chess.BB_FILE_A)
# chess_ai.board = chess.Board('5k1n/4pppp/q7/8/4r3/1N2P3/5PPP/5RKQ w - - 0 1')

# best_move, eval = chess_ai.alphabeta(4)
# print(f"best move: {best_move}, eval: {eval}")



'''Thorough Testing of Evaluate():'''
# chess_ai.board = chess.Board('5k1n/4pppp/q7/8/4r3/1N2P3/5PPP/5RKQ w - - 0 1')
# print(f"eval: {chess_ai.evaluate()} -> 0") 

# chess_ai.board = chess.Board('5k1n/4pppp/q7/2N5/4r3/4P3/5PPP/5RKQ b - - 1 1')
# print(f"eval: {chess_ai.evaluate()} -> 0") 
# chess_ai.board = chess.Board('5k1n/4pppp/q7/2N5/4r3/4P3/5PPP/5RKQ b - - 1 1')
# print(f"eval: {chess_ai.evaluate()} -> 0") 

# chess_ai.board = chess.Board('5k1n/4pppp/q7/2N5/8/4P3/5PPP/5RKQ b - - 1 1')
# print(f"eval: {chess_ai.evaluate()} -> 0") 
# chess_ai.board = chess.Board('5k1n/4pppp/q7/2N5/8/4P3/5PPP/5RKQ w - - 1 1')
# print(f"eval: {chess_ai.evaluate()} -> 0") 

# # black can capture a knight for free
# chess_ai.board = chess.Board('5krn/4pppp/1q6/2N5/8/4P3/5PPP/5RKQ b - - 1 1')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}")

# # if white turn, knight forks and wins a queen
# chess_ai.board = chess.Board('5krn/4pppp/1q6/2N5/8/4P3/5PPP/5RKQ w - - 1 1')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}")

# # if white turn, mate in 2
# chess_ai.board = chess.Board('3rrkqn/4pppp/8/2N1N3/8/4P3/5PPP/5RKQ w - - 1 1')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}")

# if black turn, avoid mate in 2 and give eval of +2
# chess_ai.board = chess.Board('3rrkqn/4pppp/8/2N1N3/8/4P3/5PPP/5RKQ b - - 1 1')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}")

# # testing mate eval:
# chess_ai.board = chess.Board('3R2k1/5ppp/8/8/8/8/5PPP/6K1 b - - 0 1')
# move, eval = chess_ai.alphabeta(2)
# print(f"Move {move} has an eval of {eval}")

# chess_ai.board = chess.Board('3R2k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1')
# move, eval = chess_ai.alphabeta(2)
# print(f"Move {move} has an eval of {eval}")

# checks if best move is updated correctly
# print()
# chess_ai.board = chess.Board('2r2bkb/2r1pppp/2q5/2r5/8/2R5/2Q1PPPP/2R2BKB w - - 0 1')
# move, eval = chess_ai.alphabeta(1)
# print(f"Move {move} has an eval of {eval}, accurate is -5")

# # check if the engine searches until theres no more good captures
# chess_ai.board = chess.Board('2r2bkb/2r1pppp/2q5/2r5/8/2R5/2Q1PPPP/2R2BKB w - - 0 1')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}, accurate is -5")

# check if it picks up mate in 1
# chess_ai.board = chess.Board('4k3/1RR5/8/8/8/8/8/1K6 w - - 0 1')
# move, eval = chess_ai.alphabeta(1)
# print(f"Move {move} has an eval of {eval}")

# chess_ai.board = chess.Board('2Q2b2/p1p1kprp/5q1B/2p1p3/8/5N2/PPP2P1P/3RK2R w K - 4 18')
# move, eval = chess_ai.alphabeta(4)
# print(f"Move {move} has an eval of {eval}")

chess_ai.board = chess.Board('6k1/5ppp/8/5r1R/8/8/5P2/6K1 w - - 0 1')
move, eval = chess_ai.alphabeta(4)
print(f"Move {move} has an eval of {eval}")
from json.encoder import INFINITY
import ai as ai
import chess

# print("Testing for count_materials():")
chess_ai = ai.ChessAI()
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

chess_ai.board = chess.Board('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1')
print(chess_ai.board)

#chess_ai.alphabeta(10, True, -INFINITY, INFINITY)
# print(chess_ai.minimax(1, True))

# chess_ai.board.push(chess_ai.next_move) # the problem
# print(chess_ai.next_move)

#x = chess_ai.minimax(4, True, chess_ai.board.turn)[0]
x = chess_ai.alphabeta(3, True, chess_ai.board.turn, -INFINITY, INFINITY)[0]


print(f"best move: {x}; move #'s: {chess_ai.ab_num}")
#print("moves with minimax 97910; moves with ab 5234")
#print(f"moves with minimax {chess_ai.minimax_num}; moves with ab {chess_ai.ab_num}")


from json.encoder import INFINITY
import ai as ai
import random
import chess

ai_chess = ai.ChessAI()

"""for testing chess module"""
# for move in range(100):
#     print(f"Turn {move}:")

#     user_move = random.choice(list(ai_chess.board.legal_moves))
#     ai_chess.board.push(user_move)
#     print(ai_chess.board)
#     print("")
#     user_move = random.choice(list(ai_chess.board.legal_moves))
#     ai_chess.board.push(user_move)
#     print(ai_chess.board)

while True:
    ai_chess.board.push(ai_chess.alphabeta(1, True, ai_chess.board.turn, -INFINITY, INFINITY)[0]) # computer will be white
    print(ai_chess.board)
    while True:
        try:
            user_move = input("Enter ur move: ")
            ai_chess.board.push_san(user_move)
        except AttributeError: 
            print("At Error occured, try again!")
            
        except ValueError: 
            print("Va Error occured, try again!")
        else: 
            break

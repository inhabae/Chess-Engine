from json.encoder import INFINITY
import ai as ai
import chess


ai_chess = ai.ChessAI()

while True:
    print(ai_chess.board)
    ai_chess.alphabeta(3, True, -INFINITY, INFINITY)
    ai_chess.print_nextmove()
    ai_chess.board.push(ai_chess.next_move)
    print(ai_chess.board)
    while True:
        try:
            user_move = input("enter ur next move: ")
            ai_chess.board.push_san(user_move)
        except AttributeError: 
            print("At Error occured, try again!")
            
        except ValueError: 
            print("Va Error occured, try again!")
        else: 
            break

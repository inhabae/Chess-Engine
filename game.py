import engine as engine
import logging
import chess

logging.basicConfig(format='%(asctime)s %(message)s')

def opponent_turn(chess_engine):
    while True:
        try:
            chess_engine.board.push_san(input("Enter opponent's move: "))
        except AttributeError:
            print("Unknown move, try again!")
        except ValueError: 
            print("Unknown move, try again!")
        else: 
            break # break out of the while loop after making opponent's move

def engine_turn(chess_engine):
    eval = chess_engine.negamax(depth) # how to eval and return move
    
    print(f"\n{chess_engine.board.san(chess_engine.best_move)} with eval of {eval}")
    chess_engine.board.push(chess_engine.best_move)

# Initializing the engine
depth = 2
chess_engine = engine.ChessEngine(depth)

# Assign the engine color, white or black
while True:
    engine_color = input("Engine color ('white' or 'black): ")
    if engine_color == 'white':
        break
    elif engine_color == 'black':
        opponent_turn(chess_engine)
    else:
        print("Please enter a valid color for the engine.\n")

while True:
    if chess_engine.board.is_game_over():
        logging.info('Game is over.')
        break
    engine_turn(chess_engine)
    if chess_engine.board.is_game_over():
        logging.info('Game is over.')
        break
    opponent_turn(chess_engine)
import engine as engine
import logging

class Undo(Exception):
    def __init__(self):
        pass

DEPTH = 4
logging.basicConfig(filename='log', level=logging.DEBUG)

def opponent_turn(chess_engine):
    while True:
        try:
            user_input = input("Enter opponent's move ('undo' to undo the last input): ")
            if user_input == 'undo':
                chess_engine.board.pop()
                chess_engine.board.pop()
                raise Undo
            chess_engine.board.push_san(user_input)
        except AttributeError:
            print("Unknown move, try again!")
        except ValueError: 
            print("Unknown move, try again!")
        except Undo:
            chess_engine.print_board()
            print("Move is undone.", end=' ')
        else: 
            break # break out of the while loop after making opponent's move
    chess_engine.print_board()

def engine_turn(chess_engine):
    eval = chess_engine.alphabeta(float('-inf'), float('inf'), DEPTH)
    print(f"\n{chess_engine.board.san(chess_engine.best_move)} with eval: {eval}")
    chess_engine.board.push(chess_engine.best_move)
    chess_engine.print_board()

# Initializing the engine
chess_engine = engine.ChessEngine(DEPTH)

# Assign the engine color, white or black
while True:
    engine_color = input("Engine color ('white' or 'black): ")
    if engine_color == 'white':
        break
    elif engine_color == 'black':
        opponent_turn(chess_engine)
        break
    else:
        print("Please enter a valid color for the engine.\n")
while True:
    if chess_engine.board.is_game_over(): break
    engine_turn(chess_engine)
    if chess_engine.board.is_game_over(): break
    opponent_turn(chess_engine)
import engine as engine

class Undo(Exception):
    def __init__(self):
        pass

DEPTH = 4
def opponent_turn(chess_engine):
    while True:
        try:
            user_input = input("Enter opponent's move ('undo' to undo the last input): ")
            if user_input == 'undo':
                # TODO: check castling pop
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
    chess_engine.check_endgame()
    eval = chess_engine.alphabeta(-30000, 30000, DEPTH)
    print(f"\n{chess_engine.board.san(chess_engine.best_move)} with eval: {eval}")
    chess_engine._check_castling(chess_engine.best_move)
    chess_engine.board.push(chess_engine.best_move)
    chess_engine.print_board()
def main():
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

def engine_play(chess_engine):
    chess_engine.check_endgame()
    eval = chess_engine.alphabeta(-30000, 30000, DEPTH)
    print(f"{chess_engine.board.san(chess_engine.best_move)}")
    chess_engine._check_castling(chess_engine.best_move)
    chess_engine.board.push(chess_engine.best_move)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
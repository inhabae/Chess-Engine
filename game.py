import engine as engine
import chess.syzygy
import chess


def check_syzygy_endgame(board):
    '''
    Checks if a given board is in a 5 piece endgame.
    If True, return True otherwise False.
    '''
    piece_num = 0
    for char in board.board_fen():
        if char.isalpha():
            piece_num += 1 
    
    if piece_num < 6:
        return True


# Initializing the engine
chess_engine = engine.ChessEngine()

# Assign the engine color, white or black
while True:
    engine_color = input("Engine color: ")
    if engine_color == 'w' or engine_color.lower() == 'white':
        break
    elif engine_color == 'b' or engine_color.lower() == 'black':
        while True:
            try:
                user_move = input("Enter ur move: ")
                chess_engine.board.push_san(user_move)
            except AttributeError: 
                print("Unknown move, try again!")
                
            except ValueError: 
                print("Unknown move, try again!")
            else: 
                break
        break
    else:
        print("Please enter a valid color for the engine.\n")


while True:
    game_over = False # flag to quit game if True


    # Computer Move

    # if 5 piece endgame, stop using alphabeta and use the tablebase instead
    if check_syzygy_endgame(chess_engine.board):
        with chess.syzygy.open_tablebase("3-4-5") as tablebase:
            wdl = tablebase.probe_wdl(chess_engine.board)
            dtz = tablebase.probe_dtz(chess_engine.board)

            moves = chess_engine.order_moves()
            best_move_flag = False
            for move in moves:
                board_copy = chess_engine.board.copy()
                print(type(chess_engine.board), type(board_copy))
                board_copy.push(move)

                if tablebase.probe_wdl(board_copy) == -wdl:
                    if -1 * tablebase.probe_dtz(board_copy) <= dtz:
                        chess_engine.board.push(move)
                        break
    else:
        move, eval = chess_engine.alphabeta(4)
        print(f"\n{chess_engine.board.san(move)}; Eval: {eval}")
        chess_engine.board.push(move)
    
    print(chess_engine.board)
        
    # Human Move
    while True:
        if chess_engine.board.is_game_over():
            game_over = True
            break   
        try:
            user_move = input("Enter ur move: ")
            chess_engine.board.push_san(user_move)
        except AttributeError: 
            print("Unknown move, try again!")
            
        except ValueError: 
            print("Unknown move, try again!")
        else: 
            break

    if game_over:
        break

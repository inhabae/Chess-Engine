from json.encoder import INFINITY
import ai as ai
import chess.syzygy
import chess


def check_endgame(board):
    piece_num = 0
    for char in board.board_fen():
        if char.isalpha():
            piece_num += 1 
    
    if piece_num < 6:
        return True


ai_chess = ai.ChessAI()
ai_chess.board = chess.Board('3k4/8/4K3/8/4Q3/8/8/8 w - - 0 1')


engine_color = input("Engine color (w/b): ")
if engine_color == 'w':
    pass
else:
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

while True: # get engine move

    game_over = False
    if check_endgame(ai_chess.board): # if 5 piece endgame
        with chess.syzygy.open_tablebase("3-4-5") as tablebase:
            wdl = tablebase.probe_wdl(ai_chess.board)
            dtz = tablebase.probe_dtz(ai_chess.board)

            moves = ai_chess.order_moves()
            best_move_flag = False
            for move in moves:
                board_copy = ai_chess.board.copy()
                print(type(ai_chess.board), type(board_copy))
                board_copy.push(move)

                if tablebase.probe_wdl(board_copy) == -wdl:
                    if -1 * tablebase.probe_dtz(board_copy) <= dtz:
                        ai_chess.board.push(move)
                        break
    else:
        move = ai_chess.alphabeta(4)[0]
        print(f"\n{ai_chess.board.san(move)}")
        ai_chess.board.push(move)
    
    print(ai_chess.board)
        
    while True: # get human move
        if ai_chess.board.is_game_over():
            game_over = True
            break   
        try:
            user_move = input("Enter ur move: ")
            ai_chess.board.push_san(user_move)
        except AttributeError: 
            print("At Error occured, try again!")
            
        except ValueError: 
            print("Va Error occured, try again!")
        else: 
            break

    if game_over:
        break

"""
Play a game between two engines. Save a PGN of the game.
"""

import engine as engine2
import game as game2
import engine_2022 as engine_2022
import chess

engineOne = engine_2022.ChessEngine(depth=4)
engineTwo = engine2.ChessEngine(depth=4)

# choose which engine is W/B
while True:
    engineOne_color = input("engineOne color ('white' or 'black): ")
    if engineOne_color == 'white' or engineOne_color == 'black': break
    else:
        print("Please enter a valid color for the engine.\n")
        
# # play a game
move_count = 1
if engineOne_color == 'white':
    while True:
        engineOne.alphabeta(4)
        print(f"{move_count}.", end=" ")
        print(engineOne.board.san(engineOne.best_move), end=" ")
        engineOne.board.push(engineOne.best_move)
        if engineOne.board.is_game_over(): break
        engineTwo.board = engineOne.board

        game2.engine_play(engineTwo)
        if engineTwo.board.is_game_over(): break
        engineOne.board = engineTwo.board
        move_count += 1
else:
    while True:
        game2.engine_play(engineTwo)
        if engineTwo.board.is_game_over(): break
        engineOne.board = engineTwo.board
        
        engineOne.alphabeta(4)
        engineOne.board.push(engineOne.best_move)
        if engineOne.board.is_game_over(): break
        engineTwo.board = engineOne.board
        move_count += 1



# engineOne.alphabeta(4)
# print(engineOne.board)
# engineOne.board.push(engineOne.best_move)
# print(engineOne.board)
# engineTwo.board = engineOne.board

# engineTwo.alphabeta(float('-inf'), float('inf'), 4)
# print(engineTwo.board)
# engineTwo.board.push(engineTwo.best_move)
# print(engineTwo.board)
# engineOne.board = engineTwo.board
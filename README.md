# Chess-Engine
A Python-based Chess engine that has a rating equivalent to 1200 on chess.com.

# Features
Alpha Beta Pruning
* Assessing alpha and beta in a given position, the engine disregards branches that the opponent is likely not to choose, which decreases search time.
* The engine keeps on searching until there is no "good captures", which tries to mitigate the horizon effect.

Move Ordering
* The engine orders all possible legal moves prior to evaluating, which results in a more effective search.

Assign value by Positions
* The engine evaluates a position better if the player's pieces are positoned well. This is done by accessing a value of the piece on a specific square; for example, a knight on e4 (center) gains 20 points whereas a knight on a1 (corner) loses 50 material points.

Syzygy Endgame
* Once there are only 5 pieces left on the board, the engine uses a tablebase endgame to play the best precalculated move to ensure the maximum chances.

# How It Looks

<img width="500" alt="Screen Shot 2022-07-20 at 2 52 29 PM" src="https://user-images.githubusercontent.com/65887459/180088757-d5f09568-2864-466d-bd36-57753098f020.png">

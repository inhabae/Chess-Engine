# Chess-Engine
A Python-based Chess engine that has a rating equivalent to 1300 on chess.com.

# Features
Alpha Beta Pruning
* Assessing alpha and beta in a given position, the engine disregards branches that the opponent is likely not to choose, which decreases the number of branches the engine considers.

Quiscence Search
* The engine keeps on searching until there is no "good captures" or "checks", which tries to mitigate the horizon effect. For example, when the engine can look ahead one half-move it thinks that queen capturing a protected pawn is a good move. However, the move is indeed a bad one, as the queen will be captured very next move. 

Move Ordering
* The engine orders given moves prior to evaluation, which significantly enhances the performance of alpha beta pruning.
* Moves such as good captures, promotions, and checks are given a higher point.

Assign Positional Values to Pieces
* The engine gives a higher evaluation if the player's pieces are positoned well. The engine uses different tables for different pieces; for example, a mobile knight on e4 (center) gains 20 points whereas an inactive knight on a1 (corner) loses 50 material points.

Syzygy Endgame
* Once there are only 5 pieces left on the board, the engine uses a tablebase endgame to play the best precalculated moves to ensure the maximum chances to win or draw.

# How It Looks
<img width="371" alt="Screen Shot 2022-10-11 at 1 19 48 PM" src="https://user-images.githubusercontent.com/65887459/195190432-237af847-eb06-470a-b137-998602af5803.png">


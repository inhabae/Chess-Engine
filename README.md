# Chess Engine

A Python-based chess engine rated approximately **1350 on Chess.com** (rapid), with wins recorded against players up to 1500.

## Features

### Alpha-Beta Pruning
Prunes branches the opponent is unlikely to take, dramatically reducing the search tree and enabling deeper lookahead within the same time budget.

### Quiescence Search
Extends the search beyond the fixed depth whenever captures or checks remain on the board, mitigating the horizon effect. Without this, the engine might incorrectly evaluate a queen capturing a protected pawn as good — only to have the queen lost on the very next move.

### Move Ordering
Moves are scored and sorted before evaluation to maximize alpha-beta pruning efficiency. Good captures (via MVV/LVA), promotions, and checks are prioritized, while moves into pawn-attacked squares are penalized.

### Piece-Square Tables
Each piece type is assigned positional bonuses based on its square, drawn from the [Simplified Evaluation Function](https://www.chessprogramming.org/Simplified_Evaluation_Function). A knight on e4 (center) gains +20, while one on a1 (corner) loses 50 points. Separate tables exist for middlegame and endgame king positioning.

### Transposition Table (Zobrist Hashing)
Positions are hashed using Zobrist hashing and cached in a transposition table. Previously evaluated positions at sufficient depth are retrieved directly, avoiding redundant computation. Nodes are stored as exact, alpha-bound, or beta-bound entries.

### King Safety
Rewards castling and bonuses pawns sheltering the king on f2/g2/h2 (kingside) or a2/b2/c2 (queenside). Uncastled kings are penalized.

### Syzygy Endgame Tablebases
When 5 or fewer pieces remain, the engine switches from search to a Syzygy tablebase lookup, guaranteeing optimal play in all supported endgame positions.

## Architecture

| File | Description |
|---|---|
| `engine.py` | Core engine: evaluation, alpha-beta, quiescence search, move ordering, Zobrist hashing |
| `game.py` | Human vs. engine interface |
| `communicator.py` | Engine vs. engine match runner |
| `engine_test.py` | Unit tests for evaluation and search correctness |
| `engine_2022.py` | Earlier engine version (no transposition table) |

## Screenshots

**Interface**

<img width="371" alt="Engine interface" src="https://user-images.githubusercontent.com/65887459/195190432-237af847-eb06-470a-b137-998602af5803.png">

**Memorable Game: Bg4!!**

<img width="537" alt="Bg4 pin" src="https://user-images.githubusercontent.com/65887459/195191252-6f27116e-54af-4926-bcd9-2b00b88b821c.png">

The engine finds **Bg4!!**, pinning White's rook to the queen and winning the exchange. After the opponent captured with hxg4, the engine played **Qh1#** — checkmate.

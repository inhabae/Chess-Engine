import chess
import random

HASH_EXACT = 0
HASH_ALPHA = 1
HASH_BETA = 2

END_DEPTH = 100

class TranspositionEntry:
    def __init__(self, key, depth, value, flag, best_move):
        self.key = key      # Zobrist hash key
        self.depth = depth  # Search depth when this entry was stored
        self.value = value  # score value
        self.flag = flag    # Type of node (exact, alpha, beta)
        self.best_move = best_move  # Best move

class ChessEngine:
    def __init__(self, depth):
        self.board = chess.Board() 
        self.best_move = None
        self.depth = depth
        self.castled = [0,0]
        self.is_endgame = False

        # Initializing Transposition Table
        # Key: hash, Value: TranspositionEntry
        self.transposition_table = dict()

        # Initializing Zobrist Hashing
        self.compute_zobrist_hashing = []
        random.seed(100)
        for i in range(781):
            self.compute_zobrist_hashing.append(random.getrandbits(64))

        ### Piece Value according to their Positions
        # https://www.chessprogramming.org/Simplified_score_Function
        self.white_pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0, 
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        self.black_pawn_table = self.white_pawn_table[::-1]
        self.white_knight_table = [
            -50, -30, -30, -30, -30, -30, -30, -50, 
            -40, -20, 0, 5, 5, 0, -20, -40, 
            -30, 5, 10, 15, 15, 10, 5, -30, 
            -30, 0, 15, 20, 20, 15, 0, -30, 
            -30, 5, 15, 20, 20, 15, 5, -30, 
            -30, 0, 10, 15, 15, 10, 0, -30, 
            -40, -20, 0, 0, 0, 0, -20, -40, 
            -50, -30, -30, -30, -30, -30, -30, -50, 
        ]
        self.black_knight_table = self.white_knight_table[::-1]
        self.white_bishop_table = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]
        self.black_bishop_table = self.white_bishop_table[::-1]
        self.white_rook_table = [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        self.black_rook_table = self.white_rook_table[::-1]
        self.white_queen_table = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10, 0, 5, 0, 0, 0, 0, -10, 
            -10,  5,  5,  5,  5,  5,  0,-10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10, 
            -20,-10,-10, -5, -5,-10,-10,-20
        ]
        self.black_queen_table = self.white_queen_table[::-1]
        self.white_king_table = [
            20, 30, 10, 0, 0, 10, 30, 20, 
            20, 20, 0, 0, 0, 0, 20, 20, 
            -10, -20, -20, -20, -20, -20, -20, -10, 
            -20, -30, -30, -40, -40, -30, -30, -20, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30, 
            -30, -40, -40, -50, -50, -40, -40, -30
        ]
        self.black_king_table = self.white_king_table[::-1]
    def set_depth(self, new_depth):
        self.depth = new_depth
    def set_board_with_FEN(self, fen):
        self.board = chess.Board(fen) 
    
    # Return board score based on material, positional advantages, etc.
    # Score is subjective to the player (+ is winning, - is losing)
    # Material score from: https://www.chessprogramming.org/Simplified_score_Function
    def get_score(self):
        score = 0
        piece_map = self.board.piece_map()
        # Material + Position score
        for square, piece in piece_map.items():
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    score += (100 + self.white_pawn_table[square])
                else:
                    score -= (100 + self.black_pawn_table[square])
            elif piece.piece_type == chess.KNIGHT:
                if piece.color == chess.WHITE:
                    score += (320 + self.white_knight_table[square])
                else:
                    score -= (320 + self.black_knight_table[square])
            elif piece.piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    score += (330 + self.white_bishop_table[square])
                else:
                    score -= (330 + self.black_bishop_table[square])    
            elif piece.piece_type == chess.ROOK:
                if piece.color == chess.WHITE:
                    score += (500 + self.white_rook_table[square])
                else:
                    score -= (500 + self.black_rook_table[square])
            elif piece.piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    score += (900 + self.white_queen_table[square])
                else:
                    score -= (900 + self.black_queen_table[square])    
            elif piece.piece_type == chess.KING and piece.color == chess.WHITE:
                score += (self.white_king_table[square] + 20000)
            elif piece.piece_type == chess.KING and piece.color == chess.BLACK:
                score -= (self.black_king_table[square] + 20000)
        # King Safety score
        ### NOTE: ONLY WORKS IN GAME, NOT AN ANALYSIS
        if not self.is_endgame:
            white_castle, black_castle = self.castled[0], self.castled[1]
            # if white castled
            if white_castle == 0:
                score -= 15
            elif white_castle == 1: # kingside
                for square in [chess.F2, chess.G2, chess.H2]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score += 5
                for square in [chess.F3, chess.G3, chess.H3]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score += 3    
            elif white_castle == 2: # queenside
                for square in [chess.A2, chess.B2, chess.C2]:
                    if piece_map.get(square, None): # if there's a piece at the square
                        if piece_map[square].piece_type == chess.PAWN:
                            score += 5
                for square in [chess.A3, chess.B3, chess.C3]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score += 3    
            # if blacked castled
            if black_castle == 0:
                score += 15
            elif black_castle == 1: # kingside
                for square in [chess.F7, chess.G7, chess.H7]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score -= 5
                for square in [chess.F6, chess.G6, chess.H6]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score -= 3  
            elif black_castle == 2: # queenside
                for square in [chess.A7, chess.B7, chess.C7]:
                    if piece_map.get(square, None): # if there's a piece at the square
                        if piece_map[square].piece_type == chess.PAWN:
                            score -= 5
                for square in [chess.A6, chess.B6, chess.C6]:
                    if piece_map.get(square, None): 
                        if piece_map[square].piece_type == chess.PAWN:
                            score -= 3       
        return score if self.board.turn else -score

    def alphabeta(self, alpha, beta, depth):
        zobrist_key = self.compute_zobrist_hash()
        if zobrist_key in self.transposition_table and self.transposition_table[zobrist_key].depth >= depth:
            entry = self.transposition_table[zobrist_key]
            if entry.flag == HASH_EXACT:
                return entry.value
            elif entry.flag == HASH_ALPHA and entry.value <= alpha:
               return alpha
            elif entry.flag == HASH_BETA and entry.value >= beta:
                return beta

        # check for checkmate/draw
        if self.board.is_game_over(): 
            if self.board.is_check():
                self.record_hash(zobrist_key, END_DEPTH, -30000, HASH_EXACT, None)
                return -30000
            self.record_hash(zobrist_key, END_DEPTH, 0, HASH_EXACT, None)
            return 0
        if self.board.can_claim_draw():
            self.record_hash(zobrist_key, END_DEPTH, 0, HASH_EXACT, None)
            return 0
        
        if depth == 0:
            return self.quiescence_search(alpha, beta)
    
        best_move = None
        best_score = -30000
        moves = self.order_moves(self.board.legal_moves)

        for move in moves:
            self._check_castling(move)
            self.board.push(move)
            score = -self.alphabeta(-beta, -alpha, depth-1)
            self.board.pop()
            self._uncheck_castling(move)

            # Ranking quicker mates higher
            if abs(score) >= 20000:
                if score > 0:
                    score -= 1000
                else:
                    score += 1000

            if score >= beta: 
                self.record_hash(zobrist_key, depth, beta, HASH_BETA, move)
                return beta
            if score > best_score: 
                best_score = score
                best_move = move
                if depth == self.depth:
                    self.best_move = best_move
            alpha = max(alpha, score)
        if best_score <= alpha:
            self.record_hash(zobrist_key, depth, best_score, HASH_ALPHA, best_move)
        else: 
            self.record_hash(zobrist_key, depth, best_score, HASH_EXACT, best_move)
        return alpha

    # TODO: need to deal with CHECK horizon effects..?
    # TODO: does this need check uncheck castling?
    def quiescence_search(self, alpha, beta):
        zobrist_key = self.compute_zobrist_hash()
        # if known position that has been searched deep
        if zobrist_key in self.transposition_table and self.transposition_table[zobrist_key].depth >= 0:
            entry = self.transposition_table[zobrist_key]
            if entry.flag == HASH_EXACT:
                return entry.value
            elif entry.flag == HASH_ALPHA and entry.value <= alpha:
                return alpha
            elif entry.flag == HASH_BETA and entry.value >= beta:
                return beta

        # check for checkmate/draw
        if self.board.is_game_over(): 
            if self.board.is_check():
                self.record_hash(zobrist_key, END_DEPTH, -30000, HASH_EXACT, None)
                return -30000
            self.record_hash(zobrist_key, END_DEPTH, 0, HASH_EXACT, None)
            return 0
        if self.board.can_claim_draw():
            self.record_hash(zobrist_key, END_DEPTH, 0, HASH_EXACT, None)
            return 0
        
        if not self.board.is_check():
            stand_pat = self.get_score()
            if stand_pat >= beta:
                self.record_hash(zobrist_key, 0, beta, HASH_BETA, None)
                return beta
            if stand_pat > alpha: 
                alpha = stand_pat
        
        if self.board.is_check():
            moves = self.order_moves(self.board.generate_legal_moves())
        else:
            moves = self.order_moves(self.board.generate_legal_captures())

        for move in moves:
            self.board.push(move)
            score = -self.quiescence_search(-beta, -alpha)
            self.board.pop()

            if score >= beta: 
                self.record_hash(zobrist_key, 0, beta, HASH_BETA, None)
                return beta
            if score > alpha:
                alpha = score
        self.record_hash(zobrist_key, 0, alpha, HASH_EXACT, None)
        return alpha
    
    # Given a list of moves, return it after ordering it from most significant to least
    def order_moves(self, moves):
        sorted_orders = {}
        ordered_moves = {}
        for move in moves: 
            move_score = 0 
            move_piece = self.board.piece_type_at(move.from_square)
            capture_piece = self.board.piece_type_at(move.to_square)
            # MVV/LVA
            if capture_piece:
                move_score += 10 * self._get_piece_value(capture_piece) - self._get_piece_value(move_piece)
            # Checks
            if self.board.gives_check(move) :
                move_score += 1
            ordered_moves[move] = move_score
            # Promotions
            if move_piece == chess.PAWN and chess.square_rank(move.to_square) % 7 == 0:
                move_score += 100
            # Discourse moving pieces to a square attacked by opponent pawn
            pawn_attacks = chess.BB_PAWN_ATTACKS[not self.board.turn][move.to_square] & self.board.pawns
            if bool(chess.SquareSet(pawn_attacks)):
                move_score -= self._get_piece_value(move_piece)

            sorted_orders = dict(sorted(ordered_moves.items(), key=lambda x:x[1], reverse=True))
        return list(sorted_orders.keys())
    
    def check_endgame(self):
        if not self.is_endgame:
            queen_num = 0
            rook_num = 0
            minor_piece_num = 0
            for piece in self.board.piece_map().values():
                ptype = piece.piece_type
                if ptype == chess.PAWN or ptype == chess.KING:
                    pass
                elif ptype == chess.QUEEN:
                    queen_num += 1
                elif ptype == chess.ROOK:
                    rook_num += 1
                else:
                    minor_piece_num += 1

            if queen_num == 0 and minor_piece_num + rook_num <= 4:
                self.is_endgame = True
                self.white_king_table = [
                    -50,-30,-30,-30,-30,-30,-30,-50,
                    -30,-30,  0,  0,  0,  0,-30,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-20,-10,  0,  0,-10,-20,-30,
                    -50,-40,-30,-20,-20,-30,-40,-50
                ]
                self.black_king_table = self.white_king_table[::-1]

    def check_super_endgame(self):
        if self.is_endgame: 
            if self.depth < 8:
                if len(self.board.piece_map().keys()) <= 6:
                    self.set_depth(8)
                    print("ENDGAME DEEP SEARCH ACTIVATED")
    
    # TODO: IMPLEMENT THIS
    # def limit_king_movement(self):
    #     if self.endgame:
    #         piece_num = len(self.board.piece_map())
            
    def compute_zobrist_hash(self):
        """
        0-767: 0-11, 12-23, 24-35, 36-47...,756-767
                a1     a2     a3     a4       h8

            0   1   2   3   4   5
            BP  BN  BB  BR  BQ  BK
            6   7   8   9   10  11
            WP  WN  WB  WR  WQ  WK

            Index for Square-Piece:
            12 * SQUARE + [PieceType + 6 if Color else PieceType] - 1

        768: BLACK TO MOVE

        769-772: CASTLING SIDE
            769: White KS Castle Right
            770: White QS Castle Right
            771: Black KS Castle Right
            772: Black QS Castle Right

        773-780: FILE FOR ENPASS SQUARE
            773 + squarefile(Square) (0-7) 
            a-file: 0, h-file 7
        """

        hashes = 0
        # 0-767
        for sq, piece in self.board.piece_map().items():
            hash_code = piece.piece_type + 6 if piece.color else piece.piece_type
            hash_code += (sq * 12 - 1)
            hashes ^= self.compute_zobrist_hashing[hash_code]
        # 768
        if not self.board.turn: hashes ^= self.compute_zobrist_hashing[768]
        # 769-772
        if self.board.has_kingside_castling_rights(chess.WHITE): hashes ^= self.compute_zobrist_hashing[769]
        if self.board.has_queenside_castling_rights(chess.WHITE): hashes ^= self.compute_zobrist_hashing[770]
        if self.board.has_kingside_castling_rights(chess.BLACK): hashes ^= self.compute_zobrist_hashing[771]
        if self.board.has_queenside_castling_rights(chess.BLACK): hashes ^= self.compute_zobrist_hashing[772]
        # 773-780
        if self.board.ep_square: hashes ^= self.compute_zobrist_hashing[773 + chess.square_file(self.board.ep_square)]
        return hashes 

    def record_hash(self, key, depth, value, flag, best_move):
        self.transposition_table[key] = TranspositionEntry(key, depth, value, flag, best_move)

    def print_board(self):
        for rank in range(7,-1,-1):
            for file in range(8):
                square = rank * 8 + file
                piece = self.board.piece_at(square)
                if piece:
                    print(self.board.piece_at(square).unicode_symbol(), end=' ')
                else:
                    print("+", end=' ')
            print()

    def _get_piece_value(self, piece_type):
        if piece_type == chess.PAWN:
            return 100
        elif piece_type == chess.KNIGHT:
            return 320
        elif piece_type == chess.BISHOP:
            return 330
        elif piece_type == chess.ROOK:
            return 500
        elif piece_type == chess.QUEEN:
            return 900
        elif piece_type == chess.KING:
            return 20000
        
    def _check_castling(self, move):
        if self.board.is_castling(move):
            if self.board.is_kingside_castling(move): # kingside
                self.castled[int(not self.board.turn)] = 1
            else: # queenside
                self.castled[int(not self.board.turn)] = 2
    
    def _uncheck_castling(self, move):
        if self.board.is_castling(move):
            if self.board.is_kingside_castling(move):
                self.castled[int(not self.board.turn)] = 0
            else:
                self.castled[int(not self.board.turn)] = 0


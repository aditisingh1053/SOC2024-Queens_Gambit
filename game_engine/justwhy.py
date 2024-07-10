import chess
import chess.svg
import math
import sys
import numpy as np
import copy
class My_Engine():
    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = chess.Board(fen)
        self.killer_moves = {}
        self.history_heuristic = {}

    def get_child(self, move):
        new_engine = My_Engine(self.board.fen())
        new_engine.make_move(move)
        return new_engine

    def get_legal_moves(self):
        return list(self.board.legal_moves)
    
    def make_move(self, move):
        self.board.push(move)

    def order_moves(self) -> list:
        """Returns a list of legal moves ordered according to the number of legal moves in the next state, then by check. If a move leads to a checkmate, it is returned immediately."""
        moves_dict = dict()
        board = copy.deepcopy(self.board)
        for move in self.board.legal_moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return [move]
            moves_dict[move] = len(list(board.legal_moves))
            if board.is_check():
                moves_dict[move] -= 1<<20
            board.pop()
        return sorted(moves_dict, key=lambda x: moves_dict[x])
    
    def evaluate_board(self, max_player: bool) -> int:

        if self.board.is_checkmate():
            if max_player:
                return -math.inf
            else:
                return math.inf
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        eval = 0

        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 320,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        piece_square_tables = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, -20, -20, 10, 10, 5,
                5, -5, -10, 0, 0, -10, -5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, 5, 10, 25, 25, 10, 5, 5,
                10, 10, 20, 30, 30, 20, 10, 10,
                50, 50, 50, 50, 50, 50, 50, 50,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ],
            chess.BISHOP: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ],
            chess.ROOK: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                20, 30, 10, 0, 0, 10, 30, 20,
                20, 20, 0, 0, 0, 0, 20, 20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30
            ]
        }

        for piece_type in piece_values:
            for square in self.board.pieces(piece_type, chess.WHITE):
                eval += piece_values[piece_type] + piece_square_tables[piece_type][square]
            for square in self.board.pieces(piece_type, chess.BLACK):
                eval -= piece_values[piece_type] + piece_square_tables[piece_type][square]

        # Mobility (yeh isliye ki jyada moves ko thodi preference mil jaaye)
        eval += 10 * len(list(self.board.legal_moves))

        # King Safety
        eval += 50 if self.board.has_kingside_castling_rights(chess.WHITE) else 0
        eval += 50 if self.board.has_kingside_castling_rights(chess.BLACK) else 0
        eval += 50 if self.board.has_queenside_castling_rights(chess.WHITE) else 0
        eval += 50 if self.board.has_queenside_castling_rights(chess.BLACK) else 0

        # Control of the Center
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for square in center_squares:
            if self.board.piece_at(square):
                piece = self.board.piece_at(square)
                if piece.color == chess.WHITE:
                    eval += 10
                else:
                    eval -= 10

        return eval


    def alpha_beta_pruning(self, alpha: float, beta: float, depth: int, max_player: bool) -> tuple:
        if depth == 0 or self.board.is_game_over():
            # print (self.evaluate_board(max_player))
            return self.evaluate_board(max_player), None
        if max_player:
            max_eval = -math.inf
            best_move = None
            for move in self.order_moves():
                new = self.get_child(move)
                eval, _move = new.alpha_beta_pruning(alpha, beta, depth - 1, not max_player)
                if eval >= max_eval:
                    best_move = move
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in self.order_moves():
                new = self.get_child(move)
                eval, _move = new.alpha_beta_pruning(alpha, beta, depth - 1, not max_player)
                if eval <= min_eval:
                    best_move = move
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
   
    def puzzle_solving(self, depth: int) -> None:
        """Makes the best move for the current player using alpha-beta pruning until the depth of `depth`."""
        global storage
        _val, move = self.alpha_beta_pruning(-math.inf, math.inf, depth, True)
        for i in range(depth):
            self.make_move(move)
            if self.board.is_game_over():
                return
            _val, move = self.alpha_beta_pruning(-math.inf, math.inf, depth-i, True)
     
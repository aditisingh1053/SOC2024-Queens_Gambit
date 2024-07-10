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
        """Returns the static evaluation of the current board position."""
        if self.board.is_checkmate():
            if max_player:
                return -math.inf
            else:
                return math.inf
        if self.board.is_stalemate():
            return 0
        # return 0
        # map = self.board.piece_map()
        fen = self.board.fen().split(' ')[0]
        ref = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100}
        count = dict()
        pieces = ['k', 'q', 'r', 'b', 'n', 'p']
        for ch in fen:
            if ch.lower() in pieces:
                if ch in count:
                    count[ch] += 1
                else:
                    count[ch] = 0
        score = 0
        for piece in pieces:
            
            score += ((count[piece] if piece in count else 0) - (count[piece.upper()] if piece.upper() in count else 0)) * ref[piece]
        return -score if (max_player and self.board.turn == chess.WHITE) or (not max_player and self.board.turn == chess.BLACK) else score

    def alpha_beta_pruning(self, alpha: float, beta: float, depth: int, max_player: bool) -> tuple:
        if depth == 0 or self.board.is_game_over():
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
     
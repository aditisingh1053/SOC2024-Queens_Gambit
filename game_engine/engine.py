import chess
import chess.svg
import math

class My_Engine:
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

    def evaluate_board(self):
        if self.board.is_checkmate():
            if self.board.turn:
                return -9999  # Black wins
            else:
                return 9999  # White wins
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        eval = 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        for piece_type in piece_values:
            eval += len(self.board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            eval -= len(self.board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        return eval

    def order_moves(self, depth):
        moves = list(self.board.legal_moves)
        move_scores = []

        for move in moves:
            score = 0
            # MVV-LVA
            if self.board.is_capture(move):
                victim_value = self.get_piece_value(self.board.piece_at(move.to_square))
                attacker_value = self.get_piece_value(self.board.piece_at(move.from_square))
                score += 10 * victim_value - attacker_value

            # Killer Moves
            if (depth, move) in self.killer_moves:
                score += 1000

            # History Heuristic
            score += self.history_heuristic.get((self.board.turn, move), 0)

            move_scores.append((score, move))

        move_scores.sort(reverse=True, key=lambda x: x[0])
        ordered_moves = [move for score, move in move_scores]
        return ordered_moves

    def get_piece_value(self, piece):
        if piece is None:
            return 0
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100
        }
        return piece_values[piece.piece_type]

    def alphabeta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = -float('inf')
            for move in self.order_moves(depth):
                self.board.push(move)
                eval = self.alphabeta(depth - 1, alpha, beta, False)
                self.board.pop()
                if eval >= beta:
                    # Killer Move
                    self.killer_moves[(depth, move)] = self.killer_moves.get((depth, move), 0) + 1
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.order_moves(depth):
                self.board.push(move)
                eval = self.alphabeta(depth - 1, alpha, beta, True)
                self.board.pop()
                if eval <= alpha:
                    # Killer Move
                    self.killer_moves[(depth, move)] = self.killer_moves.get((depth, move), 0) + 1
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def select_best_move(self, depth):
        best_move = None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in self.order_moves(depth):
            self.board.push(move)
            board_value = self.alphabeta(depth - 1, alpha, beta, False)
            self.board.pop()
            self.history_heuristic[(self.board.turn, move)] = self.history_heuristic.get((self.board.turn, move), 0) + 1

            if board_value > best_value:
                best_value = board_value
                best_move = move

        return best_move
    
    def run_engine(self: 'My_Engine', depth: int) -> None:
        move = self.select_best_move(depth)
        self.make_move(move)
        if self.board.is_game_over():
            return 
        else:
            return self.run_engine(depth)




    def display_board(self):
        return chess.svg.board(self.board)


#     

import chess
import chess.svg
import math

class My_Engine:
    def __init__(self, fen='8/8/8/1b6/1k6/8/KBB5 b - - 0 1'):
        self.board = chess.Board(fen)
        self.killer_moves = {}
        self.history_heuristic = {}
        self.evaluation_cache = {}

    def get_child(self, move):
        new_engine = My_Engine(self.board.fen())
        new_engine.make_move(move)
        return new_engine

    def get_legal_moves(self):
        return list(self.board.legal_moves)
    
    def make_move(self, move):
        self.board.push(move)

    def evaluate_board(self):
        fen = self.board.fen()
        if fen in self.evaluation_cache:
            return self.evaluation_cache[fen]

        if self.board.is_checkmate():
            value = -9999 if self.board.turn else 9999
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            value = 0
        else:
            value = 0
            piece_values = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3,
                chess.ROOK: 5,
                chess.QUEEN: 9,
                chess.KING: 0
            }

            for piece_type in piece_values:
                value += len(self.board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
                value -= len(self.board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        self.evaluation_cache[fen] = value
        return value

    def order_moves(self, depth):
        moves = list(self.board.legal_moves)
        move_scores = []

        for move in moves:
            score = 0
            if self.board.is_capture(move):
                victim_value = self.get_piece_value(self.board.piece_at(move.to_square))
                attacker_value = self.get_piece_value(self.board.piece_at(move.from_square))
                score += 10 * victim_value - attacker_value
            if (depth, move) in self.killer_moves:
                score += 1000
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
            return self.evaluate_board(), None

        if maximizing_player:
            max_eval = -float('inf')
            for move in self.order_moves(depth):
                self.board.push(move)
                eval = self.alphabeta(depth - 1, alpha, beta, False)
                self.board.pop()
                if eval >= beta:
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

                # Check for immediate checkmate
                if self.board.is_checkmate():
                    return move  # Immediately return if checkmate found

        return best_move
    
    def run_engine(self, depth):
        while not self.board.is_game_over():
            move = self.select_best_move(depth)
            self.make_move(move)

            # Display the board after each move
            # print(self.display_board())
            # print("Move:", move)

            if self.board.is_game_over():
                # print("Result:", self.board.result())
                break

        return self.board.result()

    def puzzle_solving(self,depth):
        move=self.select_best_move(depth)
        for i in range (depth):
            self.make_move(move)
            if self.board.is_game_over():
                return
            move=self.select_best_move(depth-i)

        


    def display_board(self):
        return chess.svg.board(self.board)


# Test with the given FEN position expecting a checkmate
# engine = My_Engine('8/8/8/1b6/1k6/8/KBB5 b - - 0 1')
# print(engine.run_engine(3))

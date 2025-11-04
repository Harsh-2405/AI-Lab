# ai.py
# Alpha-Beta minimax for Isolation.
# Heuristic: mobility difference (AI legal moves - human legal moves)

import math
from board import Board

class AI:
    def __init__(self, ai_id=Board.P2, human_id=Board.P1, max_depth=3):
        """
        ai_id and human_id must match Board.P1 / Board.P2 values.
        max_depth controls search depth (higher is stronger but slower).
        """
        self.ai_id = ai_id
        self.human_id = human_id
        self.max_depth = max_depth

    def heuristic(self, board: Board):
        """Simple evaluation: difference in number of legal moves."""
        ai_pos = board.p2_pos if self.ai_id == Board.P2 else board.p1_pos
        human_pos = board.p1_pos if self.human_id == Board.P1 else board.p2_pos
        return len(board.get_moves(ai_pos)) - len(board.get_moves(human_pos))

    def minimax(self, board: Board, ai_pos, human_pos, depth, alpha, beta, maximizing):
        """
        Minimax with Alpha-Beta pruning.
        Returns: (score, best_move) where best_move is a (row,col) or None.
        'maximizing' True means it's AI's turn in this node.
        """
        # select current player's position
        cur_pos = ai_pos if maximizing else human_pos
        moves = board.get_moves(cur_pos)

        # terminal: current player has no moves -> current player loses
        if not moves:
            return (-1000000 if maximizing else 1000000), None

        # depth limit reached -> evaluate board
        if depth == 0:
            return self.heuristic(board), None

        if maximizing:
            value = -math.inf
            best_move = None
            for mv in moves:
                # apply AI move
                from_pos = board.apply_move(self.ai_id, mv)
                new_ai_pos = mv
                score, _ = self.minimax(board, new_ai_pos, human_pos, depth - 1, alpha, beta, False)
                # undo
                board.undo_move(self.ai_id, from_pos, mv)
                if score > value:
                    value = score
                    best_move = mv
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # beta cut-off
            return value, best_move
        else:
            value = math.inf
            best_move = None
            for mv in moves:
                from_pos = board.apply_move(self.human_id, mv)
                new_human_pos = mv
                score, _ = self.minimax(board, ai_pos, new_human_pos, depth - 1, alpha, beta, True)
                board.undo_move(self.human_id, from_pos, mv)
                if score < value:
                    value = score
                    best_move = mv
                beta = min(beta, value)
                if alpha >= beta:
                    break  # alpha cut-off
            return value, best_move

    def best_move(self, board: Board):
        """
        Return the chosen move (row,col) for the AI according to minimax search.
        Returns None if there are no legal moves.
        """
        ai_pos = board.p2_pos if self.ai_id == Board.P2 else board.p1_pos
        human_pos = board.p1_pos if self.human_id == Board.P1 else board.p2_pos
        score, move = self.minimax(board, ai_pos, human_pos, self.max_depth, -math.inf, math.inf, True)
        return move

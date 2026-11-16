"""Depth-limited minimax.

Mainly the reference that alpha-beta has to match: on every test position
both should return the same root value (and the same move when both use the
same move order).

    minimax(board, depth, maximizing):
        if terminal or depth == 0:
            return evaluate(board)
        if maximizing:
            return max(minimax(child, depth-1, False) for each move)
        else:
            return min(minimax(child, depth-1, True) for each move)

Scoring a real win as WIN_SCORE - ply (and a loss as -(WIN_SCORE - ply))
makes the agent prefer faster wins and slower losses.
"""

from __future__ import annotations

from ..evaluation import EVALUATIONS
from ..game import CENTER_ORDER, make_move, other, valid_moves, winner  # noqa: F401
from .base import Agent

WIN_SCORE = 1_000_000


class MinimaxAgent(Agent):
    name = "minimax"

    def __init__(self, depth: int = 4, evaluation: str = "window", ordered: bool = True) -> None:
        super().__init__()
        self.depth = depth
        self.evaluate = EVALUATIONS[evaluation]
        self.ordered = ordered  # try columns center-first instead of left-to-right
        self.last_value = None  # root value of the last search (for the alpha-beta check)
        self.name = f"minimax(d={depth},{evaluation})"

    def move_order(self, board) -> list[int]:
        moves = valid_moves(board)
        return [c for c in CENTER_ORDER if c in moves] if self.ordered else moves

    def get_move(self, board, player) -> int:
        # TODO: loop over self.move_order(board), call self.minimax on each
        # child, keep the best column, store the best value in self.last_value.
        raise NotImplementedError("MinimaxAgent.get_move is not written yet")

    def minimax(self, board, depth: int, maximizing: bool, player: int, ply: int) -> float:
        """Value of `board` from `player`'s point of view.

        Remember to do `self.nodes += 1` here so the Pruning experiment can
        count nodes.
        """
        raise NotImplementedError

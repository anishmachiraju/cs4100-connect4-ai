"""Minimax with alpha-beta pruning.

Same answer as minimax, fewer nodes.
    alpha = best score MAX can already guarantee
    beta  = best score MIN can already guarantee
    if alpha >= beta: stop exploring this node's remaining children

Center-first ordering ([3, 2, 4, 1, 5, 0, 6]) finds good moves early, so
more branches get pruned. The Pruning experiment compares ordered=True and
ordered=False.
"""

from __future__ import annotations

import math  # noqa: F401

from ..evaluation import EVALUATIONS
from ..game import CENTER_ORDER, make_move, other, valid_moves, winner  # noqa: F401
from .base import Agent
from .minimax import WIN_SCORE  # noqa: F401


class AlphaBetaAgent(Agent):
    name = "alphabeta"

    def __init__(self, depth: int = 6, evaluation: str = "window", ordered: bool = True) -> None:
        super().__init__()
        self.depth = depth
        self.evaluate = EVALUATIONS[evaluation]
        self.ordered = ordered
        self.last_value = None
        self.name = f"alphabeta(d={depth},{evaluation})"

    def move_order(self, board) -> list[int]:
        moves = valid_moves(board)
        return [c for c in CENTER_ORDER if c in moves] if self.ordered else moves

    def get_move(self, board, player) -> int:
        # TODO: like MinimaxAgent.get_move, but call self.alphabeta with
        # alpha=-inf, beta=+inf and update alpha at the root.
        raise NotImplementedError("AlphaBetaAgent.get_move is not written yet")

    def alphabeta(self, board, depth: int, alpha: float, beta: float,
                  maximizing: bool, player: int, ply: int) -> float:
        """Remember `self.nodes += 1` for the node counts."""
        raise NotImplementedError

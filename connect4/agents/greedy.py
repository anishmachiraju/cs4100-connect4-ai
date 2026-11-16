"""Baseline: win now, otherwise block now, otherwise play randomly.

TODO:
    1. For each valid column, try the move. If it wins, play it.
    2. For each valid column, try the OPPONENT's move there. If it would win
       for them, play that column to block it.
    3. Otherwise pick a random valid column.
"""

from __future__ import annotations

import random

from ..game import check_win, make_move, other, valid_moves  # noqa: F401
from .base import Agent


class GreedyAgent(Agent):
    name = "greedy"

    def __init__(self, seed: int | None = None) -> None:
        super().__init__()
        self.rng = random.Random(seed)

    def get_move(self, board, player) -> int:
        raise NotImplementedError("GreedyAgent.get_move is not written yet")

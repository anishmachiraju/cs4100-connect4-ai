"""Baseline: play any valid column at random. Every real agent should beat this."""

from __future__ import annotations

import random

from ..game import valid_moves
from .base import Agent


class RandomAgent(Agent):
    name = "random"

    def __init__(self, seed: int | None = None) -> None:
        super().__init__()
        self.rng = random.Random(seed)

    def get_move(self, board, player) -> int:
        self.nodes += 1
        return self.rng.choice(valid_moves(board))

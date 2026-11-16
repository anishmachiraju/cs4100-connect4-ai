"""The interface every agent follows.

An agent gets a board and the player it is moving for, and returns a column.
The runner calls `select_move`, which times the call and resets the node
counter, so experiments can read `last_nodes` and `last_time` after each move.

To write a new agent:
    class MyAgent(Agent):
        name = "my-agent"
        def get_move(self, board, player):
            self.nodes += 1          # count every board you look at
            return some_column
"""

from __future__ import annotations

import time

import numpy as np


class Agent:
    name = "agent"

    def __init__(self) -> None:
        self.nodes = 0          # boards examined during the current move
        self.last_nodes = 0     # nodes examined on the previous move
        self.last_time = 0.0    # seconds spent on the previous move

    def get_move(self, board: np.ndarray, player: int) -> int:
        """Return a column (0-6) to play. Subclasses implement this."""
        raise NotImplementedError

    def select_move(self, board: np.ndarray, player: int) -> int:
        """Wrapper the runner calls: records nodes searched and time taken."""
        self.nodes = 0
        start = time.perf_counter()
        col = self.get_move(board, player)
        self.last_time = time.perf_counter() - start
        self.last_nodes = self.nodes
        return col

    def reset(self) -> None:
        """Called before each new game. Override if the agent keeps state."""

    def __repr__(self) -> str:
        return self.name

"""Monte Carlo tree search with UCB1.

Each simulation does four steps:
    1. Selection: from the root, keep picking the child with the highest
           UCB1 = wins / visits + c * sqrt(ln(parent.visits) / visits)
    2. Expansion: add one untried move as a new child.
    3. Simulation (rollout): play random moves until the game ends.
    4. Backpropagation: update wins and visits on every node on the path.

After `simulations` iterations, play the MOST-VISITED child of the root.

Careful with whose point of view `wins` is stored from. A common choice:
each node stores wins for the player who made the move INTO that node, so
the parent can just pick the child with the best win rate.
"""

from __future__ import annotations

import math
import random

from ..game import make_move, other, valid_moves, winner  # noqa: F401
from .base import Agent


class Node:
    def __init__(self, board, player_to_move: int, parent=None, move=None) -> None:
        self.board = board
        self.player_to_move = player_to_move
        self.parent = parent
        self.move = move                      # column that led here
        self.children: list[Node] = []
        self.untried = valid_moves(board)     # moves not expanded yet
        self.wins = 0.0                       # draws count as 0.5
        self.visits = 0

    def ucb1(self, c: float) -> float:
        if self.visits == 0:
            return math.inf
        return self.wins / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)


class MCTSAgent(Agent):
    name = "mcts"

    def __init__(self, simulations: int = 1000, c: float = math.sqrt(2), seed: int | None = None) -> None:
        super().__init__()
        self.simulations = simulations
        self.c = c
        self.rng = random.Random(seed)
        self.name = f"mcts(n={simulations})"

    def get_move(self, board, player) -> int:
        # TODO:
        # root = Node(board, player)
        # for _ in range(self.simulations):
        #     node = self.select(root)
        #     node = self.expand(node)
        #     result = self.simulate(node)
        #     self.backpropagate(node, result)
        # return max(root.children, key=lambda n: n.visits).move
        raise NotImplementedError("MCTSAgent.get_move is not written yet")

    def select(self, node: Node) -> Node:
        raise NotImplementedError

    def expand(self, node: Node) -> Node:
        raise NotImplementedError

    def simulate(self, node: Node) -> int:
        """Random playout. Return the winner (1, 2) or 0 for a draw.
        Count `self.nodes += 1` per simulation (or per rollout move)."""
        raise NotImplementedError

    def backpropagate(self, node: Node, result: int) -> None:
        raise NotImplementedError

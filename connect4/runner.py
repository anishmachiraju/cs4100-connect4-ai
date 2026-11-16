"""Play one game between two agents and record what happened.

Both the interactive game (play.py) and the experiments (tournament.py) go
through play_game, so every mode follows the same rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .agents.base import Agent
from .game import (PLAYER1, PLAYER2, current_player, is_valid_move, make_move,
                   new_board, other, render, winner)


@dataclass
class GameResult:
    winner: int                       # 1, 2, or 0 for a draw
    moves: list[int]                  # columns played, in order (after the opening)
    final_board: np.ndarray
    nodes: dict[int, list[int]] = field(default_factory=lambda: {1: [], 2: []})
    times: dict[int, list[float]] = field(default_factory=lambda: {1: [], 2: []})

    def score(self, player: int) -> float:
        """1 for a win, 0.5 for a draw, 0 for a loss."""
        if self.winner == 0:
            return 0.5
        return 1.0 if self.winner == player else 0.0


def play_game(agent1: Agent, agent2: Agent, board: np.ndarray | None = None,
              verbose: bool = False, color: bool = False) -> GameResult:
    """agent1 plays as player 1 (X), agent2 as player 2 (O).

    Pass `board` to start from an opening position; whoever's turn it is on
    that board moves first.
    """
    board = new_board() if board is None else board.copy()
    agents = {PLAYER1: agent1, PLAYER2: agent2}
    for a in agents.values():
        a.reset()
    player = current_player(board)
    result = GameResult(winner=-1, moves=[], final_board=board)

    if verbose:
        print("\n" + render(board, color))

    while winner(board) is None:
        agent = agents[player]
        col = agent.select_move(board, player)
        if not is_valid_move(board, col):
            raise ValueError(f"{agent} played an invalid column: {col}")
        board = make_move(board, col, player)
        result.moves.append(col)
        result.nodes[player].append(agent.last_nodes)
        result.times[player].append(agent.last_time)
        if verbose:
            print(f"\n{agent} (Player {player}) played column {col + 1}")
            print(render(board, color))
        player = other(player)

    result.winner = winner(board)
    result.final_board = board
    return result

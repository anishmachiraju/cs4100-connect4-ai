"""Hand-built positions with known answers. Every search agent must pass these.

Agents that aren't written yet are skipped, so this file goes green as each
one gets implemented. Columns here are 0-indexed.
"""

import pytest

from connect4.agents import make_agent
from connect4.game import board_from_moves, current_player

# (name, moves to reach the position, set of correct columns)
WIN_IN_1 = ("win in 1", "010101", {0})       # X has three in col 0; O also threatens col 1
MUST_BLOCK = ("must block", "01010", {0})    # O to move, X threatens col 0
WIN_IN_3 = ("win in 3", "2233", {1, 4})      # X makes an open three on the bottom row

SEARCH_AGENTS = [
    "minimax:depth=4",
    "alphabeta:depth=4",
    "alphabeta:depth=4,ordered=false",
    "mcts:simulations=2000,seed=0",
]
CASES = [(a, p) for a in SEARCH_AGENTS for p in (WIN_IN_1, MUST_BLOCK, WIN_IN_3)]
CASES += [("greedy:seed=0", WIN_IN_1), ("greedy:seed=0", MUST_BLOCK)]


@pytest.mark.parametrize("spec,position", CASES, ids=[f"{a}-{p[0]}" for a, p in CASES])
def test_sanity_position(spec, position):
    _, moves, answers = position
    board = board_from_moves(moves)
    agent = make_agent(spec)
    try:
        col = agent.select_move(board, current_player(board))
    except NotImplementedError:
        pytest.skip(f"{spec} not implemented yet")
    assert col in answers

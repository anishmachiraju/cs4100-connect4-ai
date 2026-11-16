"""Evaluation functions for depth-limited search.

Each function takes (board, player) and returns a number: higher is better
for `player`. Minimax and alpha-beta pick one by name, e.g.
AlphaBetaAgent(depth=4, evaluation="center").

The Evaluation experiment plays these against each other at equal depths.
"""

from __future__ import annotations

from .game import COLS, EMPTY, WINDOWS, other, window_values  # noqa: F401


def center_count(board, player) -> float:
    """Weak evaluation: my pieces in the center column minus theirs.

    TODO
    """
    raise NotImplementedError


def window_score(board, player) -> float:
    """Medium evaluation: score all 69 four-cell windows (see game.WINDOWS).

    Starting weights from the project notes (tune these):
        3 mine + 1 empty      +5
        2 mine + 2 empty      +2
        3 theirs + 1 empty    -4
        each of my pieces in the center column  +3

    TODO
    """
    raise NotImplementedError


def tuned(board, player) -> float:
    """Third evaluation, built from failure analysis of lost games
    (for example Allis's odd/even threat rules).

    TODO
    """
    raise NotImplementedError


EVALUATIONS = {
    "center": center_count,
    "window": window_score,
    "tuned": tuned,
}

"""Matchups between agents, for the experiments.

Plan from the proposal:
  * Every game starts from a shared list of 50 random openings.
  * Each opening is played twice with sides swapped (100 games per matchup),
    because deterministic agents would otherwise replay the same game.
  * Score = win 1, draw 0.5, loss 0, reported with a 95% confidence interval.

    python -m connect4.tournament random random --games 20
"""

from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field

import numpy as np

from .agents import make_agent
from .game import board_from_moves, valid_moves, winner
from .runner import GameResult, play_game


def make_openings(n: int = 50, plies: int = 4, seed: int = 0) -> list[list[int]]:
    """n distinct random openings of `plies` moves each, none already decided.

    TODO: decide on plies and save the list to a file so every experiment
    uses the same openings.
    """
    rng = random.Random(seed)
    seen, openings = set(), []
    while len(openings) < n:
        board, moves = board_from_moves([]), []
        for _ in range(plies):
            col = rng.choice(valid_moves(board))
            moves.append(col)
            board = board_from_moves(moves)
        if winner(board) is None and tuple(moves) not in seen:
            seen.add(tuple(moves))
            openings.append(moves)
    return openings


@dataclass
class MatchupResult:
    a: str
    b: str
    games: list[GameResult] = field(default_factory=list)
    a_scores: list[float] = field(default_factory=list)  # A's score in each game

    @property
    def score(self) -> float:
        return sum(self.a_scores) / len(self.a_scores)

    def confidence_interval(self, z: float = 1.96) -> tuple[float, float]:
        """Normal-approximation 95% CI on A's mean score.

        TODO: games from the same opening pair are not independent; consider
        computing the CI over opening pairs instead of single games.
        """
        n = len(self.a_scores)
        mean = self.score
        sd = float(np.std(self.a_scores, ddof=1)) if n > 1 else 0.0
        half = z * sd / math.sqrt(n) if n else 0.0
        return mean - half, mean + half


def run_matchup(spec_a: str, spec_b: str, openings: list[list[int]]) -> MatchupResult:
    """Play every opening twice, once with A as player 1 and once as player 2."""
    out = MatchupResult(spec_a, spec_b)
    for moves in openings:
        start = board_from_moves(moves)
        for a_is_p1 in (True, False):
            a, b = make_agent(spec_a), make_agent(spec_b)
            p1, p2 = (a, b) if a_is_p1 else (b, a)
            result = play_game(p1, p2, board=start)
            out.games.append(result)
            out.a_scores.append(result.score(1 if a_is_p1 else 2))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one matchup from shared openings.")
    parser.add_argument("a", help='agent A spec, e.g. "alphabeta:depth=4"')
    parser.add_argument("b", help="agent B spec")
    parser.add_argument("--openings", type=int, default=50, help="number of openings (games = 2x this)")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)

    res = run_matchup(args.a, args.b, make_openings(args.openings, seed=args.seed))
    lo, hi = res.confidence_interval()
    wins = sum(s == 1.0 for s in res.a_scores)
    draws = sum(s == 0.5 for s in res.a_scores)
    losses = len(res.a_scores) - wins - draws
    print(f"{args.a} vs {args.b}: {len(res.a_scores)} games")
    print(f"  A wins {wins}, draws {draws}, losses {losses}")
    print(f"  A score {res.score:.3f}  (95% CI {lo:.3f} to {hi:.3f})")
    # TODO: write per-game rows (moves, nodes, times) to results/*.csv for plotting.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

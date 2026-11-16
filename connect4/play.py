"""Play Connect 4 in the terminal.

    python -m connect4.play                         # person vs person
    python -m connect4.play --p2 random             # person vs random agent
    python -m connect4.play --p2 alphabeta:depth=6  # once alpha-beta is written
    python -m connect4.play --p1 mcts:simulations=1000 --p2 alphabeta:depth=4

Any agent in connect4/agents/__init__.py:AGENTS works for either side.
"""

from __future__ import annotations

import argparse
import sys

from .agents import AGENTS, HumanAgent, QuitGame, make_agent
from .runner import play_game


def build(spec: str, player: int):
    agent = make_agent(spec)
    if isinstance(agent, HumanAgent) and agent.label is None:
        agent.label = f"Player {player} ({'X' if player == 1 else 'O'})"
    return agent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Play Connect 4.")
    parser.add_argument("--p1", default="human", help=f"player 1 (X), one of: {', '.join(AGENTS)}")
    parser.add_argument("--p2", default="human", help="player 2 (O), same choices")
    parser.add_argument("--no-color", action="store_true", help="plain X/O without colors")
    args = parser.parse_args(argv)

    color = not args.no_color and sys.stdout.isatty()
    p1, p2 = build(args.p1, 1), build(args.p2, 2)
    print(f"Connect 4: {p1} (X) vs {p2} (O)")

    while True:
        try:
            result = play_game(p1, p2, verbose=True, color=color)
        except (QuitGame, KeyboardInterrupt):
            print("\nGame abandoned.")
            return 0
        except NotImplementedError as e:
            print(f"\nThat agent isn't written yet: {e}")
            return 1

        if result.winner == 0:
            print("\nDraw: the board is full.")
        else:
            w = p1 if result.winner == 1 else p2
            print(f"\nPlayer {result.winner} ({w}) wins in {len(result.moves)} moves!")

        try:
            again = input("Play again? (y/n): ").strip().lower()
        except EOFError:
            again = "n"
        if again != "y":
            return 0


if __name__ == "__main__":
    raise SystemExit(main())

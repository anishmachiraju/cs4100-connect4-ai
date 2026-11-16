"""Agent registry: build any agent from a short text spec.

    make_agent("human")
    make_agent("random")
    make_agent("alphabeta:depth=4,evaluation=center")
    make_agent("mcts:simulations=3000")

play.py and tournament.py use this, so a new agent only needs one line in
AGENTS below to show up everywhere.
"""

from __future__ import annotations

from .alphabeta import AlphaBetaAgent
from .base import Agent
from .greedy import GreedyAgent
from .human import HumanAgent, QuitGame
from .mcts import MCTSAgent
from .minimax import MinimaxAgent
from .random_agent import RandomAgent

AGENTS: dict[str, type[Agent]] = {
    "human": HumanAgent,
    "random": RandomAgent,
    "greedy": GreedyAgent,
    "minimax": MinimaxAgent,
    "alphabeta": AlphaBetaAgent,
    "mcts": MCTSAgent,
}


def _parse_value(text: str):
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    return text


def make_agent(spec: str) -> Agent:
    """Turn "name:key=value,key=value" into an agent instance."""
    name, _, args = spec.partition(":")
    name = name.strip().lower()
    if name not in AGENTS:
        raise ValueError(f"unknown agent {name!r}; choose from {', '.join(AGENTS)}")
    kwargs = {}
    if args:
        for pair in args.split(","):
            key, _, value = pair.partition("=")
            kwargs[key.strip()] = _parse_value(value.strip())
    return AGENTS[name](**kwargs)


__all__ = [
    "AGENTS", "Agent", "AlphaBetaAgent", "GreedyAgent", "HumanAgent",
    "MCTSAgent", "MinimaxAgent", "QuitGame", "RandomAgent", "make_agent",
]

"""A person typing column numbers in the terminal."""

from __future__ import annotations

from ..game import COLS, is_valid_move
from .base import Agent


class QuitGame(Exception):
    """Raised when the person types q."""


class HumanAgent(Agent):
    name = "human"

    def __init__(self, label: str | None = None) -> None:
        super().__init__()
        self.label = label

    def get_move(self, board, player) -> int:
        who = self.label or f"Player {player}"
        while True:
            try:
                raw = input(f"{who}, choose a column (1-{COLS}, q to quit): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                raise QuitGame
            if raw in {"q", "quit", "exit"}:
                raise QuitGame
            if not raw.isdigit():
                print("  Type a number.")
                continue
            col = int(raw) - 1  # people count columns from 1
            if not is_valid_move(board, col):
                print("  That column is full or doesn't exist. Try again.")
                continue
            return col

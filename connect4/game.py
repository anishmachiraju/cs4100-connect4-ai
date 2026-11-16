"""Connect 4 board and rules.

The board is a 6x7 NumPy array. Row 0 is the TOP of the board, so pieces
fall toward row 5. Cells hold EMPTY (0), or the player number (1 or 2).

Every function here is pure: make_move returns a new board and never
changes the one you pass in. That keeps the search code simple. If it gets
too slow later, add an in-place drop/undo pair (or switch to bitboards)
without changing the function names the agents use.
"""

from __future__ import annotations

import numpy as np

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

# Columns sorted center-first. Search agents should try moves in this order
# so alpha-beta finds good moves early and prunes more.
CENTER_ORDER = [3, 2, 4, 1, 5, 0, 6]


def new_board() -> np.ndarray:
    """Return an empty board."""
    return np.zeros((ROWS, COLS), dtype=np.int8)


def other(player: int) -> int:
    """Return the opponent of `player`."""
    return PLAYER2 if player == PLAYER1 else PLAYER1


def is_valid_move(board: np.ndarray, col: int) -> bool:
    """A move is valid if the column exists and its top cell is empty."""
    return 0 <= col < COLS and board[0, col] == EMPTY


def valid_moves(board: np.ndarray) -> list[int]:
    """Columns that are not full, in left-to-right order."""
    return [c for c in range(COLS) if board[0, c] == EMPTY]


def next_open_row(board: np.ndarray, col: int) -> int:
    """Lowest empty row in `col` (the row a piece would land in)."""
    for r in range(ROWS - 1, -1, -1):
        if board[r, col] == EMPTY:
            return r
    raise ValueError(f"column {col} is full")


def make_move(board: np.ndarray, col: int, player: int) -> np.ndarray:
    """Drop `player`'s piece into `col` and return the NEW board."""
    if not is_valid_move(board, col):
        raise ValueError(f"invalid move: column {col}")
    child = board.copy()
    child[next_open_row(board, col), col] = player
    return child


def _build_windows() -> list[tuple[tuple[int, int], ...]]:
    """All 69 lines of four cells: 24 horizontal, 21 vertical, 24 diagonal."""
    windows = []
    for r in range(ROWS):
        for c in range(COLS - 3):
            windows.append(tuple((r, c + i) for i in range(4)))  # horizontal
    for r in range(ROWS - 3):
        for c in range(COLS):
            windows.append(tuple((r + i, c) for i in range(4)))  # vertical
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            windows.append(tuple((r + i, c + i) for i in range(4)))  # down-right
            windows.append(tuple((r + 3 - i, c + i) for i in range(4)))  # up-right
    return windows


WINDOWS = _build_windows()
assert len(WINDOWS) == 69


def window_values(board: np.ndarray) -> list[list[int]]:
    """The contents of every window, e.g. [1, 1, 0, 2]. Handy for evaluations."""
    return [[int(board[r, c]) for r, c in w] for w in WINDOWS]


def check_win(board: np.ndarray, player: int) -> bool:
    """True if `player` has four in a row anywhere."""
    for w in WINDOWS:
        if all(board[r, c] == player for r, c in w):
            return True
    return False


def is_full(board: np.ndarray) -> bool:
    return not (board[0] == EMPTY).any()


def winner(board: np.ndarray) -> int | None:
    """1 or 2 if that player has won, 0 for a draw, None if the game goes on."""
    if check_win(board, PLAYER1):
        return PLAYER1
    if check_win(board, PLAYER2):
        return PLAYER2
    if is_full(board):
        return 0
    return None


def is_terminal(board: np.ndarray) -> bool:
    return winner(board) is not None


def utility(board: np.ndarray, player: int) -> int:
    """+1 if `player` won, -1 if they lost, 0 for a draw (terminal boards only)."""
    w = winner(board)
    if w is None:
        raise ValueError("utility() called on a non-terminal board")
    if w == 0:
        return 0
    return 1 if w == player else -1


def current_player(board: np.ndarray) -> int:
    """Player 1 moves first, so equal piece counts means it is player 1's turn."""
    ones = int((board == PLAYER1).sum())
    twos = int((board == PLAYER2).sum())
    return PLAYER1 if ones == twos else PLAYER2


def board_from_moves(moves: str | list[int]) -> np.ndarray:
    """Build a board by playing columns in order, starting with player 1.

    Accepts a list like [3, 3, 4] or a string like "334" (0-indexed columns).
    Useful for writing test positions and opening lists.
    """
    board = new_board()
    player = PLAYER1
    for col in moves:
        board = make_move(board, int(col), player)
        player = other(player)
    return board


# ---------------------------------------------------------------- display

SYMBOLS = {EMPTY: ".", PLAYER1: "X", PLAYER2: "O"}
_COLORS = {PLAYER1: "\033[91m", PLAYER2: "\033[93m"}  # red, yellow
_RESET = "\033[0m"


def render(board: np.ndarray, color: bool = False) -> str:
    """Text picture of the board with 1-based column numbers underneath."""
    lines = []
    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            v = int(board[r, c])
            s = SYMBOLS[v]
            if color and v != EMPTY:
                s = f"{_COLORS[v]}{s}{_RESET}"
            cells.append(s)
        lines.append("| " + " ".join(cells) + " |")
    lines.append("+" + "-" * (2 * COLS + 1) + "+")
    lines.append("  " + " ".join(str(c + 1) for c in range(COLS)))
    return "\n".join(lines)

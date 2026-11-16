import numpy as np
import pytest

from connect4.agents import RandomAgent, make_agent
from connect4.game import (COLS, ROWS, WINDOWS, board_from_moves, check_win,
                           current_player, is_terminal, make_move, new_board,
                           utility, valid_moves, winner)
from connect4.runner import play_game


def test_empty_board():
    b = new_board()
    assert b.shape == (ROWS, COLS)
    assert valid_moves(b) == list(range(COLS))
    assert winner(b) is None
    assert current_player(b) == 1


def test_piece_falls_to_bottom_and_stacks():
    b = make_move(new_board(), 3, 1)
    assert b[5, 3] == 1
    b = make_move(b, 3, 2)
    assert b[4, 3] == 2


def test_make_move_does_not_change_input():
    b = new_board()
    make_move(b, 0, 1)
    assert not b.any()


def test_full_column_is_invalid():
    b = board_from_moves([0] * 6)
    assert 0 not in valid_moves(b)
    with pytest.raises(ValueError):
        make_move(b, 0, 1)


def test_69_windows():
    assert len(WINDOWS) == 69
    assert len(set(WINDOWS)) == 69


def test_horizontal_win():
    b = board_from_moves("0011223")  # X on 0,1,2,3 bottom row
    assert check_win(b, 1) and winner(b) == 1


def test_vertical_win():
    b = board_from_moves("0101010")
    assert check_win(b, 1) and not check_win(b, 2)


def test_diagonal_wins():
    up_right = board_from_moves("01122323343")  # X climbs from (5,0) to (2,3)
    assert check_win(up_right, 1)
    down_right = board_from_moves("65544343323")
    assert check_win(down_right, 1)


def test_draw_on_full_board():
    # Fill columns in a pattern that never makes four in a row.
    order = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0,
             2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2,
             4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4,
             6, 6, 6, 6, 6, 6]
    b = new_board()
    p = 1
    for c in order:
        b = make_move(b, c, p)
        p = 3 - p
    assert winner(b) == 0
    assert is_terminal(b) and utility(b, 1) == 0


def test_random_vs_random_finishes():
    for seed in range(20):
        r = play_game(RandomAgent(seed), RandomAgent(seed + 100))
        assert r.winner in (0, 1, 2)
        assert winner(r.final_board) == r.winner


def test_make_agent_parses_args():
    a = make_agent("alphabeta:depth=3,evaluation=center,ordered=false")
    assert a.depth == 3 and a.ordered is False
    with pytest.raises(ValueError):
        make_agent("nope")

# Connect 4 AI

CS 4100 (Artificial Intelligence) final project, Northeastern University, Fall 2026.
Anish Machiraju and Phoebe Hall.

We build Connect 4 agents in plain Python and test which pays off most: deeper alpha-beta search, a better evaluation function, or more Monte Carlo simulations.

## Quick start

```bash
pip install -r requirements.txt
python -m connect4.play                  # person vs person in the terminal
python -m connect4.play --p2 random      # person vs the random agent
python -m pytest                         # engine tests + sanity positions
```

Any agent can play either side. Pass options after a colon:

```bash
python -m connect4.play --p2 alphabeta:depth=6
python -m connect4.play --p1 mcts:simulations=1000 --p2 alphabeta:depth=4,evaluation=center
python -m connect4.tournament alphabeta:depth=4 random --openings 50
```

## Agents
- Random and greedy baselines
- Minimax and alpha-beta pruning with center-first move ordering
- Monte Carlo tree search with UCB1

| Part | File | Status |
|---|---|---|
| Board and rules | `connect4/game.py` | done |
| Game runner | `connect4/runner.py` | done |
| Terminal game | `connect4/play.py` | done |
| Human player | `connect4/agents/human.py` | done |
| Random baseline | `connect4/agents/random_agent.py` | done |
| Greedy baseline | `connect4/agents/greedy.py` | stub |
| Minimax | `connect4/agents/minimax.py` | stub |
| Alpha-beta | `connect4/agents/alphabeta.py` | stub |
| MCTS (UCB1) | `connect4/agents/mcts.py` | stub |
| Evaluation functions | `connect4/evaluation.py` | stub |
| Tournament (openings, swapped sides, CI) | `connect4/tournament.py` | basic version works |

Stubs raise `NotImplementedError`. Their sanity tests are skipped until they're written, and then they have to pass.

## Layout

```
connect4/
  game.py            board as a 6x7 NumPy array, moves, win check, the 69 windows
  evaluation.py      center count, window score, tuned (picked by name)
  runner.py          play_game(agent1, agent2) -> GameResult (winner, moves, nodes, times)
  play.py            interactive terminal game
  tournament.py      shared openings, each played twice with sides swapped
  agents/
    base.py          Agent interface: get_move(board, player) -> column
    __init__.py      registry + make_agent("name:key=value")
    human.py  random_agent.py  greedy.py  minimax.py  alphabeta.py  mcts.py
tests/
  test_game.py       rules and engine
  test_sanity.py     win in 1, must block, win in 3
```

## Adding an agent

1. Subclass `Agent` in `connect4/agents/`, implement `get_move(board, player)`, and do `self.nodes += 1` for every board you examine.
2. Add one line to `AGENTS` in `connect4/agents/__init__.py`.

It then works in `play.py`, `tournament.py` and the sanity tests.

## Experiments
- **Pruning:** nodes and time per move, minimax vs alpha-beta
- **Evaluation:** three evaluation functions at equal depths
- **Simulations:** MCTS at different simulation counts against alpha-beta
- **Accuracy:** moves on solver-labeled positions from [connect4-pons-eval](https://huggingface.co/datasets/davidquarel/connect4-pons-eval)

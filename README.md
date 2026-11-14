# Connect 4 AI

CS 4100 (Artificial Intelligence) final project, Northeastern University, Fall 2026.
Anish Machiraju and Phoebe Hall.

We build Connect 4 agents in plain Python and test which pays off most: deeper alpha-beta search, a better evaluation function, or more Monte Carlo simulations.

## Agents
- Random and greedy baselines
- Minimax and alpha-beta pruning with center-first move ordering
- Monte Carlo tree search with UCB1

## Experiments
- **Pruning:** nodes and time per move, minimax vs alpha-beta
- **Evaluation:** three evaluation functions at equal depths
- **Simulations:** MCTS at different simulation counts against alpha-beta
- **Accuracy:** moves on solver-labeled positions from [connect4-pons-eval](https://huggingface.co/datasets/davidquarel/connect4-pons-eval)

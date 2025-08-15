# Zeckendorf_Learning_Model
In 2018, Baird-Smith et al. (arXiv:1809.04881) created the Zeckendorf Game: given an integer n and the initial decomposition of n * F(1), two players alternate by using moves related to the recurrence relation F(n+1) = F(n) + F(n−1), and the player to move last wins. They provided a non-constructive (strategy-stealing) proof that Player 2 always has a winning strategy. We build a reinforcement learning model for this game, in an effort to construct such a general winning strategy.

We implement the minimax algorithm with alpha-beta pruning in "minimax.py". It traverses the game tree and classifies game states as winning or losing. As we traverse the tree, we record the visited states and their winning status in a hash map, which we systematically reference to prevent redundant traversals.

The data collected from the minimax algorithm for relatively small versions of the game (n < 300) is used to train a neural network in "policy_network.py". With apt training, the neural network, given a game state as input, outputs a policy and a value - the policy signifies how promising the moves from the state are, and the value signifies how winning the state is. PyTorch provides the framework for our neural network. 

Finally, we implement a Monte Carlo Tree Search (MCTS) in "mcts.py". Guided by the neural network described above, the MCTS traverses the game tree for relatively large versions of the game (300 <= n < 2000). The data from the MCTS is fed back into the neural network. 

The more the model repeats this training and testing routine, as imposed by the instance variable "num_iterations", the more accurately it classifies game states as winning or losing. Upon specifying "num" and "num_iterations" in "regression.py", the model's classification of game states in the Zeckendorf game with n = num will be written to a CSV file called "table{num}.csv" in your local project directory.

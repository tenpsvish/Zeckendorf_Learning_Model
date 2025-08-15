import pandas as pd
from state import State
from game import Game


class Minimax:

    def __init__(self, game):
        self.game = game
        self.state_dict = {}
        self.winning = self.is_winning()
        self.create_table()
        self.table = self.create_table()

    # Label all states in the game as winning (1) or losing (0)
    def is_winning(self):
        return self.is_winning_general(self.game.get_initial_state())

    # is_winning_general returns (winner, depth),
    # winner: 1 / 0 if (the player who plays the move resulting in) state is winning / losing
    # depth: maximum number of moves left in the game, including the above move.
    def is_winning_general(self, state):
        if state in self.state_dict:
            state.set_winning(self.state_dict.get(state))
            return state.get_winning()
        depth = 0
        for next_state in state.get_children():
            (winner, next_depth) = self.is_winning_general(next_state)
            if winner == 1:  # The opponent has a winning next move
                self.state_dict.update(
                    {state: (0, next_depth + 1)})
                state.set_winning((0, next_depth + 1))
                return (0, next_depth + 1)
            else:
                depth = max(depth, next_depth)
        self.state_dict.update({state: (1, depth + 1)})
        state.set_winning((1, depth + 1))
        return (1, depth + 1)

    def create_table(self):
        rows = [state.get_stack_list() + [is_winning[0]]
                for state, is_winning in self.state_dict.items()]
        cols = [f"F_{i+1}"
                for i in range(self.game.get_num_stacks())] + ["Winning"]
        return pd.DataFrame(rows, columns=cols)

    # Getter methods

    def get_game(self):
        return self.game

    def get_state_dict(self):
        return self.state_dict

    def get_table(self):
        return self.table

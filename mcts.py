import math


class MCTS:

    # args = {num_searches : , C : }
    def __init__(self, game, policy_network, args):
        self.game = game
        self.policy_network = policy_network
        self.args = args

    def search(self):
        initial_state = self.game.get_initial_state()
        count = 0

        while count < self.args["num_searches"]:
            current_state = initial_state
            expanded_states = self.game.get_expanded_states()

            while current_state in expanded_states:
                current_index = expanded_states.index(current_state)
                if current_state.is_expanded:
                    self.game.copy_data(expanded_states[current_index], current_state)


            if current_state.is_terminal():
                # If state exists in state dictionary, backpropagate state data, i.e., (num_visits, total_value).
                # If not, get the state's policy (and value) from the policy network,
                # store them in the state and state_dictionary,
                # then backpropagate (1, value)
                if current_state in self.game.get_state_dict():
                    current_state.increment_num_visits(1)
                    current_state.increment_value(1)
                    self.game.backpropagate(current_state, 1, 1)

            else:
                next_states = self.game.expand(current_state)
                for next_state in next_states:
                    if next_state in self.game.visited_states():
                        state_data = self.game.get_state_dict().get(next_state)
                        next_state.increment_num_visits(state_data[0])
                        next_state.increment_value(state_data[1])
                        self.game.backpropagate(
                            next_state, state_data[0], state_data[1])
                    else:
                        state_data = self.policy_net(next_state)
                        self.game.backpropagate(next_state, 1, state_data[1])

# from state import State
import torch
import torch.nn as nn
import torch.nn.functional as F


class PolicyNetwork(nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()

        # Create the input (dense) layer
        # that encodes a vector of length input_size
        # in a vector of length 64
        self.input_layer = nn.Linear(input_size, 64)

        # Create a fully connected layer
        # that encodes the (encoded) vector of length 64
        # in another vector of length 64,
        # adding another layer of abstraction to the model.
        # This allows the model to identify complex patterns.
        self.intermediate_layer = nn.Linear(64, 64)

        # Create the policy output layer
        # that maps the second (encoded) vector of length 64
        # to a vector of length output_size
        self.policy_head = nn.Linear(64, output_size)

        # Create the value output layer
        # which maps the second (encoded) vector of length 64
        # to a vector of length 1
        self.value_head = nn.Linear(64, 1)

    # Defines how each input (i.e., state) is processed by the network
    def forward(self, state):
        # Apply ReLU activation to the input layer
        encoded_vector1 = F.relu(self.input_layer(state.process()))

        # Apply ReLU activation to the second layer,
        # allowing the network to learn complex patterns
        encoded_vector2 = F.relu(self.intermediate_layer(encoded_vector1))

        # Policy output
        policy_logits = self.policy_head(encoded_vector2)
        policy_probs = F.softmax(policy_logits, dim=1)

        # Masked output
        masked_probs = self.mask_invalid_moves(
            policy_probs, state.get_next_moves())

        # Value output
        value_logit = self.value_head(encoded_vector2)

        # Output in [0,1], where 1 = win, 0 = loss
        value = torch.sigmoid(value_logit)

        return masked_probs, value

    # The policy network does not account for the validity of moves by default.
    # This method masks out invalid moves.
    def mask_invalid_moves(self, policy_probs, valid_moves):
        masked_probs = torch.zeros_like(policy_probs)
        masked_probs[valid_moves] = policy_probs[valid_moves]
        masked_probs /= masked_probs.sum()
        return masked_probs

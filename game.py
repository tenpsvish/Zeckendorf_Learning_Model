from fibonacci import Fibonacci
from state import State


class Game:
    # A Zeckendorf game with num_chips starting at state.
    def __init__(self, num_chips, min_stacks=0, initial_state=None):
        self.num_chips = num_chips
        if initial_state == None:
            self.num_stacks = max(
                min_stacks, Fibonacci.max_fibonacci(num_chips))
            stack_list = [0] * self.num_stacks
            stack_list[0] = num_chips
            self.initial_state = State(stack_list)
        else:
            self.num_stacks = len(initial_state.get_stack_list())
            self.initial_state = initial_state
        self.child_dict = {}
        self.populate()

    # Static methods
    @staticmethod
    def get_next_moves(state):
        next_moves = []
        stack_list = state.get_stack_list()
        for stack_num in range(len(stack_list)):
            if stack_num == 0 and stack_list[0] >= 2:
                next_moves.append((0, "combo"))
            if stack_num >= 1 and stack_list[stack_num] >= 2:
                next_moves.append((stack_num, "split"))
            if stack_num >= 1 and stack_list[stack_num] >= 1 and stack_list[stack_num - 1] >= 1:
                next_moves.append((stack_num, "combo"))
        return next_moves

    @staticmethod
    def play(state, move, kind):
        new_stack = state.get_stack_list().copy()
        if kind == "combo":
            if move == 0:
                new_stack[0] -= 2
                new_stack[1] += 1
            else:
                new_stack[move] -= 1
                new_stack[move - 1] -= 1
                new_stack[move + 1] += 1
        else:  # i.e., kind == "split"
            if move == 1:
                new_stack[1] -= 2
                new_stack[0] += 1
                new_stack[2] += 1
            else:
                new_stack[move] -= 2
                new_stack[move - 2] += 1
                new_stack[move + 1] += 1
        return State(new_stack)

    # Create the game tree
    def populate(self):
        self.populate_general(self.initial_state)

    def populate_general(self, state):
        if state in self.child_dict:  # state has been visited before
            state.set_children(self.child_dict.get(state))
            return
        children = [Game.play(state, next_move[0], next_move[1])
                    for next_move in Game.get_next_moves(state)]
        self.child_dict.update({state: children})
        state.set_children(children)
        for child in state.get_children():
            self.populate_general(child)
        return

    # Getter methods
    def get_num_chips(self):
        return self.num_chips

    def get_num_stacks(self):
        return self.num_stacks

    def get_initial_state(self):
        return self.initial_state

    def get_child_dict(self):
        return self.child_dict

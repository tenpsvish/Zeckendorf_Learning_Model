class State:

    # Assume there is at least one stack,
    # i.e., len(stack_list) >= 1
    def __init__(self, stack_list):
        self.stack_list = stack_list
        self.children = []
        self.is_winning = (-1, 0)

    def __eq__(self, other):
        if not isinstance(other, State):
            # Does not attempt to compare against other classes
            return NotImplemented
        return self.stack_list == other.stack_list

    # Allows to create a dictionary of states in the game, storing their children and winning status.
    def __hash__(self):
        return hash(tuple(self.stack_list))

    # Setter methods
    def set_children(self, children):
        self.children = children

    def set_winning(self, is_winning):
        self.is_winning = is_winning

    # Getter methods
    def get_stack_list(self):
        return self.stack_list

    def get_children(self):
        return self.children

    def get_winning(self):
        return self.is_winning

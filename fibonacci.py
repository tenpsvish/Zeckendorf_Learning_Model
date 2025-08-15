import numpy as np
from state import State


class Fibonacci:

    @staticmethod
    def get_fibonacci(k):
        golden_ratio = (1 + np.sqrt(5)) / 2
        return int(np.round((golden_ratio ** k + (1 - golden_ratio) ** k) / np.sqrt(5)))

    @staticmethod
    def num_chips(state):
        num_chips = 0
        stack_list = state.get_stack_list()
        for stack_num in len(stack_list):
            num_chips += stack_list[stack_num] * \
                Fibonacci.get_fibonacci(stack_num + 2)
        return num_chips

    @staticmethod
    def max_fibonacci(num):
        count = 0
        while Fibonacci.get_fibonacci(count + 2) <= num:
            count += 1
        return count

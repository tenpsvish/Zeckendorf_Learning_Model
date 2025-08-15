import pandas as pd
from state import State
from game import Game
from fibonacci import Fibonacci
from minimax import Minimax

N = 20
game = Game(20)
minimax = Minimax(game)
minimax.get_table().to_csv(f"table{N}.csv")

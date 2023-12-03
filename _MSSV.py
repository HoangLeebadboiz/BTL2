import numpy as np
from _2110318 import Evaluator


def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    state = Evaluator(cur_state)
    print(state.evalGame())
    # print(valid_moves)
    # for x in valid_moves:
    # print(x.index_local_board, x.x, x.y, x.value)
    print(len(valid_moves))
    if len(valid_moves) != 0:
        s = np.random.choice(valid_moves)
        # print(s, type(s))
        # print(type(cur_state))
        return s
    return None

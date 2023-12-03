import copy
from state import State
from state import UltimateTTT_Move
from _2110318 import Evaluator


def select_move_util(cur_state, remain_time, depth, ini):

    if depth == 0:
        if ini % 2 != 0:
            max_point = -999999
            chosenMove = None
            move = None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) == 0:
                return (chosenMove, move, max_point)
            for i in valid_moves:
                b = simulate_move(cur_state, i)
                evaluate = Evaluator(b)
                point = evaluate.evalGame()
                if point > max_point:
                    max_point = point
                    chosenMove = b
                    move = i
            return (chosenMove, move, max_point)
        else:
            min_point = 999999
            chosenMove = None
            move = None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) == 0:
                return (chosenMove, move, min_point)
            for i in valid_moves:
                b = simulate_move(cur_state, i)
                evaluate = Evaluator(b)
                point = evaluate.evalGame()
                if point < min_point:
                    min_point = point
                    chosenMove = b
                    move = i
            return (chosenMove, move, min_point)
    elif (ini - depth) % 2 == 0:  # Min
        min_point = 999999
        chosenMove = None
        move = None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) == 0:
            return (chosenMove, move, min_point)
        for i in valid_moves:
            b = simulate_move(cur_state, i)
            point = select_move_util(b, remain_time, depth-1, ini)[2]
            if point < min_point:
                min_point = point
                chosenMove = b
                move = i
        return (chosenMove, move, min_point)
    else:
        max_point = -999999
        chosenMove = None
        move = None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) == 0:
            return (chosenMove, move, max_point)
        for i in valid_moves:
            b = simulate_move(cur_state, i)
            point = select_move_util(b, remain_time, depth-1, ini)[2]
            if point > max_point:
                max_point = point
                chosenMove = b
                move = i
        return (chosenMove, move, max_point)


def simulate_move(cur_state: State, move: UltimateTTT_Move):
    res = copy.deepcopy(cur_state)
    if not res.is_valid_move(move):
        raise ValueError(
            "move {0} on local board is not valid".format(move)
        )
    local_board = res.blocks[move.index_local_board]
    local_board[move.x, move.y] = move.value

    res.player_to_move *= -1
    res.previous_move = move

    if res.global_cells[move.index_local_board] == 0:  # not 'X' or 'O'
        if res.game_result(local_board):
            res.global_cells[move.index_local_board] = move.value
    return res


def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    """if len(valid_moves) == 81:
        return valid_moves[36]"""
    if len(valid_moves) == 0:
        return None
    ini = 0
    if cur_state.get_valid_moves[0].value == 1:
        ini = 3
    else:
        ini = 2
    chosen = select_move_util(cur_state, remain_time, 2, ini)
    b = simulate_move(cur_state, chosen[1])
    """print(chosen[1])
    print(b.global_cells)
    evaluate = Evaluator(b)
    point = evaluate.evalGame()
    print(point)
    print(chosen[2])"""
    return chosen[1]

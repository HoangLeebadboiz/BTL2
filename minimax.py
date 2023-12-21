import copy
from state import State
from state import UltimateTTT_Move
from _2110318 import Evaluator
import numpy as np


def select_move_util(cur_state, remain_time, depth, alpha, beta, player):

    if depth == 0:
        if player == 1:  # Max
            chosenMove = None
            move = None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) != 0:
                for i in valid_moves:
                    b = simulate_move(cur_state, i)
                    evaluate = Evaluator(b)
                    point = evaluate.evalGame()
                    if point == 5000:
                        alpha = point
                        chosenMove = b
                        move = i
                        break
                    if point > alpha:
                        alpha = point
                        chosenMove = b
                        move = i
                        if beta <= alpha:
                            break
                return (chosenMove, move, alpha)
            return (chosenMove, move, 0)
        else:  # Min
            chosenMove = None
            move = None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) != 0:
                for i in valid_moves:
                    b = simulate_move(cur_state, i)
                    evaluate = Evaluator(b)
                    point = evaluate.evalGame()
                    if point == -5000:
                        beta = point
                        chosenMove = b
                        move = i
                        break
                    if point < beta:
                        beta = point
                        chosenMove = b
                        move = i
                        if beta <= alpha:
                            break
                return (chosenMove, move, beta)
            return (chosenMove, move, 0)
    elif player == -1:  # Min
        chosenMove = None
        move = None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) != 0:
            player *= -1
            for i in valid_moves:
                b = simulate_move(cur_state, i)
                evaluate = Evaluator(b)
                point = evaluate.evalGame()
                if point == -5000:
                    beta = point
                    chosenMove = b
                    move = i
                    break
                point = select_move_util(
                    b, remain_time, depth-1, alpha, beta, player)[2]
                if point < beta:
                    beta = point
                    chosenMove = b
                    move = i
                    if beta <= alpha:
                        break
            return (chosenMove, move, beta)
        return (chosenMove, move, 0)
    else:
        chosenMove = None
        move = None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) != 0:
            player *= -1
            for i in valid_moves:
                b = simulate_move(cur_state, i)
                evaluate = Evaluator(b)
                point = evaluate.evalGame()
                if point == 5000:
                    alpha = point
                    chosenMove = b
                    move = i
                    break
                point = select_move_util(
                    b, remain_time, depth-1, alpha, beta, player)[2]
                if point > alpha:
                    alpha = point
                    chosenMove = b
                    move = i
                    if beta <= alpha:
                        break
            return (chosenMove, move, alpha)
        return (chosenMove, move, 0)


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


def utils(cur_state):
    if cur_state.previous_move != None:
        index_local_board = cur_state.previous_move.x * 3 + cur_state.previous_move.y
    else:
        index_local_board = -1

    board = np.array([block.flatten() for block in cur_state.blocks])
    return board, index_local_board


def select_move(cur_state, remain_time):

    board, currentBoard = utils(cur_state)

    valid_moves = cur_state.get_valid_moves

    if len(valid_moves) != 0:
        depth = 3
        player = cur_state.player_to_move
        alpha = float('-inf')
        beta = float('inf')

        if currentBoard == -1:
            return UltimateTTT_Move(0, 0, 0, player)
        else:
            chosen = select_move_util(cur_state, remain_time,
                                      depth, alpha, beta, player)
            return chosen[1]

    return None

import numpy as np
import copy
from state import State
from state import UltimateTTT_Move

def check_win(small_board):
    for i in range(3):
        if small_board[i][0] + small_board[i][1] + small_board[i][2] == 3:
            return 1
        if small_board[0][i] + small_board[1][i] + small_board[2][i] == 3:
            return 1
        if small_board[i][0] + small_board[i][1] + small_board[i][2] == -3:
            return -1
        if small_board[0][i] + small_board[1][i] + small_board[2][i] == -3:
            return -1
        
    if small_board[0][0] + small_board[1][1] + small_board[2][2] == 3:
        return 1
    if small_board[0][2] + small_board[1][1] + small_board[2][0] == 3:
        return 1
    if small_board[0][0] + small_board[1][1] + small_board[2][2] == -3:
        return -1
    if small_board[0][2] + small_board[1][1] + small_board[2][0] == -3:
        return -1
    return 0

def evaluate_square(small_board):
    res = 0
    points = [0.2,0.17,0.2,0.17,0.22,0.17,0.2,0.17,0.2]
    #calculate positional play, least priority
    for i in range(9):
        res += points[i]*small_board[i//3][i%3]
    #calculate 2 in a row
    for i in range(3):
        if small_board[i][0] + small_board[i][1] + small_board[i][2] == 2:
            res += 6
        if small_board[0][i] + small_board[1][i] + small_board[2][i] == 2:
            res += 6
        if small_board[i][0] + small_board[i][1] + small_board[i][2] == -2:
            res -= 6
        if small_board[0][i] + small_board[1][i] + small_board[2][i] == -2:
            res -= 6
    #because 2 in a diagonal have more priority, res should be greater
    if small_board[0][0] + small_board[1][1] + small_board[2][2] == 2:
        res += 7
    if small_board[0][2] + small_board[1][1] + small_board[2][0] == 2:
        res += 7
    if small_board[0][0] + small_board[1][1] + small_board[2][2] == -2:
        res -= 7
    if small_board[0][2] + small_board[1][1] + small_board[2][0] == -2:
        res -= 7
    #calculate winning small
    res += check_win(small_board)*12
    #Now return value
    return res

def evaluate_whole(cur_state:State):  
    res = 0
    mul = [1.4,1,1.4,1,1.75,1,1.4,1,1.4]
    pos = -1
    if cur_state.free_move == False:
        pos = cur_state.previous_move.index_local_board
    for i in range(9):
        #Chơi theo vị trí
        res += evaluate_square(cur_state.blocks[i]) *1.5*mul[i]
        if pos == i:#Xem vị trí như nào
            #Chưa phân thắng bại, phải để ý nhiều hơn.
            if cur_state.global_cells[i] == 0:
                res += evaluate_square(cur_state.blocks[i])*mul[i]
            #Đã phân thắng bại, không nên để ý.
            elif 0 in cur_state.blocks[i]:
                res -= evaluate_square(cur_state.blocks[i])*1.5*mul[i]
        res += cur_state.global_cells[i]*mul[i]

    globalSquare = [[0 for i in range(3)] for j in range(3)]
    for i in range(9):
        globalSquare[i//3][i%3]=cur_state.global_cells[i]
    res += evaluate_square(globalSquare)*150
    res += check_win(globalSquare)*5000
    if cur_state.previous_move.value == -1:
        res = -res
    return res


def simulate_move(cur_state, move):
        res = copy.deepcopy(cur_state)
        if not res.is_valid_move(move):
            raise ValueError(
                "move {0} on local board is not valid".format(move)
            )
        local_board = res.blocks[move.index_local_board]
        local_board[move.x, move.y] = move.value
        
        res.player_to_move *= -1          
        res.previous_move = move
        
        if res.global_cells[move.index_local_board] == 0: # not 'X' or 'O'
            if res.game_result(local_board):
                res.global_cells[move.index_local_board] = move.value
        return res

def select_move_util(cur_state,remain_time,depth,ini):

    if depth == 0:
        if ini%2 == 0:
            max_point=-9999999
            chosenMove=None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) == 0: return evaluate_whole(cur_state)
            for i in valid_moves:
                b=simulate_move(cur_state,i)
                point = evaluate_whole(b)
                if point > max_point:
                    max_point = point
                    chosenMove= b
            return (chosenMove,point)
        else:
            min_point=9999999
            chosenMove=None
            valid_moves = cur_state.get_valid_moves
            if len(valid_moves) == 0: return evaluate_whole(cur_state)
            for i in valid_moves:
                b=simulate_move(cur_state,i)
                point = evaluate_whole(b)
                
                if point < min_point:
                    min_point = point
                    chosenMove= b
            return (chosenMove,point)
    elif (ini - depth) % 2 != 0: #Min
        min_point=9999999
        chosenMove=None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) == 0: return evaluate_whole(cur_state)
        for i in valid_moves:
            b = simulate_move(cur_state,i)
            point = select_move_util (b,remain_time,depth-1,ini)[1]
            
            if point < min_point:
                    max_point = point
                    chosenMove= b
            return (chosenMove,point)
    else:
        max_point=-9999999
        chosenMove=None
        valid_moves = cur_state.get_valid_moves
        if len(valid_moves) == 0: return evaluate_whole(cur_state)
        for i in valid_moves:
            b = simulate_move(cur_state,i)
            point = select_move_util (b,remain_time,depth-1,ini)[1]
            point = evaluate_whole(b)
            
            if point > max_point:
                max_point = point
                chosenMove= b
        return (chosenMove,point)





def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if len(valid_moves) == 0:
        return None
    chosen = select_move_util(cur_state,remain_time,3,3)[0]
    return chosen.previous_move


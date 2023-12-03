import numpy as np

corners = [0, 2, 6, 8]
sides = [1, 3, 5, 7]
middle = [4]
case_win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
win_percent_onekey = np.array(
    [[0.33, 0.5, 0.33], [0.5, 0.25, 0.5], [0.33, 0.5, 0.33]])
positionLocalScore = np.array(
    [[0.3, 0.2, 0.3], [0.2, 0.4, 0.2], [0.3, 0.2, 0.3]])
positionGloScore = np.array([1.35, 1, 1.35, 1, 1.7, 1, 1.35, 1, 1.35])


class Evaluator:
    def __init__(self, cur_state):
        self.global_board = cur_state.global_cells
        self.blocks = cur_state.blocks
        # self.valid_boards = self.get_valid_Board(cur_state)
        self.player = cur_state.get_valid_moves[0].value

    def evalGame(self):
        score = 0
        if self.checkwin(self.global_board):
            score += -self.player * 5000
        else:
            for i in range(9):
                score += (self.evalLocalBoard(i))
            score += self.evalGloBoard()
        return score

    def evalLocalBoard(self, index_board):
        score = 0
        Glo_board = self.global_board.copy().reshape((3, 3))
        new_positionGloScore = self.score_position(Glo_board).reshape(-1)
        if self.global_board[index_board] != 0:
            score = self.global_board[index_board] * \
                new_positionGloScore[index_board] * 200
        else:
            LocalBoard = self.blocks[index_board].copy()
            Glo_score = positionGloScore.reshape((3, 3))
            new_positionLocalScore = self.score_position(LocalBoard)
            for row in range(3):
                for col in range(3):
                    score += LocalBoard[row][col] * \
                        (new_positionLocalScore[row]
                         [col] + Glo_score[row][col]/1.7)
            score += self.prepare_win(LocalBoard)*6
        return score

    def evalGloBoard(self):
        score = 0
        """for i in range(9):
            score += self.global_board[i]*positionGloScore[i]"""
        Glo_board = self.global_board.reshape((3, 3))
        score += self.prepare_win(Glo_board)*200
        return score

    @staticmethod
    def checkwin(Board):
        if ((Board[0] == Board[1] == Board[2] != 0) or
                (Board[3] == Board[4] == Board[5] != 0) or
                (Board[6] == Board[7] == Board[8] != 0) or
                (Board[0] == Board[3] == Board[6] != 0) or
                (Board[1] == Board[4] == Board[7] != 0) or
                (Board[2] == Board[5] == Board[8] != 0) or
                (Board[0] == Board[4] == Board[8] != 0) or
                (Board[2] == Board[4] == Board[6] != 0)):

            return True
        return False

    def prepare_win(self, Board):
        num_check = 0
        for i in range(3):
            if self.row_check(i, Board) != None:
                num_check += self.row_check(i, Board)
            if self.col_check(i, Board) != None:
                num_check += self.col_check(i, Board)
        if self.diagonal_check_1(Board) != None:
            num_check += self.diagonal_check_1(Board)
        if self.diagonal_check_2(Board) != None:
            num_check += self.diagonal_check_2(Board)
        return num_check

    def score_position(self, board):
        new_positionLocalScore = positionLocalScore.copy()
        for i in range(3):
            if self.row_check(i, board) == None:
                new_positionLocalScore[i] -= win_percent_onekey[i] * \
                    new_positionLocalScore[i]
            if self.col_check(i, board) == None:
                for j in range(3):
                    new_positionLocalScore[j][i] -= win_percent_onekey[j][i] * \
                        new_positionLocalScore[j][i]
        if self.diagonal_check_1(board) == None:
            for i in range(3):
                new_positionLocalScore[i][i] -= win_percent_onekey[i][i] * \
                    new_positionLocalScore[i][i]
        if self.diagonal_check_2(board) == None:
            for i in range(3):
                new_positionLocalScore[i][2-i] -= win_percent_onekey[i][2-i] * \
                    new_positionLocalScore[i][2-i]
        return new_positionLocalScore

    @staticmethod
    def row_check(row, board):
        X_count = 0
        O_count = 0
        NA = 0
        for i in board[row]:
            if i == 1:
                X_count += 1
            elif i == -1:
                O_count += 1
            else:
                NA += 1
        if X_count > 0 and O_count > 0:
            return None
        if X_count == 2 and NA == 1:
            return 1
        if O_count == 2 and NA == 1:
            return -1
        return 0

    @staticmethod
    def col_check(col, board):
        X_count = 0
        O_count = 0
        NA = 0
        for i in range(3):
            if board[i][col] == 1:
                X_count += 1
            elif board[i][col] == -1:
                O_count += 1
            else:
                NA += 1
        if X_count > 0 and O_count > 0:
            return None
        if X_count == 2 and NA == 1:
            return 1
        if O_count == 2 and NA == 1:
            return -1
        return 0

    @staticmethod
    def diagonal_check_1(board):
        X_count_1 = 0
        O_count_1 = 0
        NA_1 = 0
        for i in range(3):
            if board[i][i] == 1:
                X_count_1 += 1
            elif board[i][i] == -1:
                O_count_1 += 1
            else:
                NA_1 += 1
        if X_count_1 > 0 and O_count_1 > 0:
            return None
        if X_count_1 == 2 and NA_1 == 1:
            return 1
        if O_count_1 == 2 and NA_1 == 1:
            return -1
        return 0

    @staticmethod
    def diagonal_check_2(board):
        X_count_2 = 0
        O_count_2 = 0
        NA_2 = 0
        for i in range(3):
            if board[i][2-i] == 1:
                X_count_2 += 1
            elif board[i][2-i] == -1:
                O_count_2 += 1
            else:
                NA_2 += 1
        if X_count_2 > 0 and O_count_2 > 0:
            return None
        if X_count_2 == 2 and NA_2 == 1:
            return 1
        if O_count_2 == 2 and NA_2 == 1:
            return -1
        return 0

    """@staticmethod
    def get_valid_Board(cur_state):
        valid_boards = set()
        for state in cur_state.get_valid_moves:
            valid_boards.add(state.index_local_board)
        return valid_boards"""

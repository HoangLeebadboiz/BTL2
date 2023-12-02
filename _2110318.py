import numpy as np

corners = [0, 2, 6, 8]
sides = [1, 3, 5, 7]
middle = [4]
case_win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
positionLocalScore = [[0.3, 0.2, 0.3], [0.2, 0.4, 0.2], [0.3, 0.2, 0, 3]]
positionGloScore = [1.35, 1, 1.35, 1, 1.7, 1, 1.35, 1, 1.35]


class Evaluator:
    def __init__(self, cur_state):
        self.global_board = cur_state.global_cells
        self.blocks = cur_state.blocks
        self.valid_boards = self.get_valid_Board(cur_state)
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
        if self.global_board[index_board] != 0:
            score = self.global_board[index_board] * \
                positionGloScore[index_board] * 100
        else:
            LocalBoard = self.blocks[index_board].copy()
            Glo_score = np.array(positionGloScore).reshape((3, 3))
            for row in range(3):
                for col in range(3):
                    score += LocalBoard[row][col] * \
                        (positionLocalScore[row]
                         [col] + Glo_score[row][col]/1.7)
            score += self.prepare_win(LocalBoard)*30
        return score

    def evalGloBoard(self):
        score = 0
        """for i in range(9):
            score += self.global_board[i]*positionGloScore[i]"""
        Glo_board = self.global_board.reshape((3, 3))
        score += self.prepare_win(Glo_board)*150
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

    @staticmethod
    def prepare_win(Board):
        num_check = 0

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
            if X_count == 2 and NA == 1:
                return 1
            if O_count == 2 and NA == 1:
                return -1
            return 0

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
            if X_count == 2 and NA == 1:
                return 1
            if O_count == 2 and NA == 1:
                return -1
            return 0

        def diagonal_check(board):
            X_count_1 = 0
            O_count_1 = 0
            NA_1 = 0
            X_count_2 = 0
            O_count_2 = 0
            NA_2 = 0
            check = 0
            for i in range(3):
                if board[i][i] == 1:
                    X_count_1 += 1
                elif board[i][i] == -1:
                    O_count_1 += 1
                else:
                    NA_1 += 1
            for i in range(3):
                if board[i][2-i] == 1:
                    X_count_2 += 1
                elif board[i][2-i] == -1:
                    O_count_2 += 1
                else:
                    NA_2 += 1
            if X_count_1 == 2 and NA_1 == 1:
                check += 1
            if O_count_1 == 2 and NA_1 == 1:
                check -= 1
            if X_count_2 == 2 and NA_2 == 1:
                check += 1
            if O_count_2 == 2 and NA_2 == 1:
                check -= 1
            return check
        for i in range(3):
            num_check += (row_check(i, Board) + col_check(i, Board))
        num_check += diagonal_check(Board)
        return num_check

    @staticmethod
    def get_valid_Board(cur_state):
        valid_boards = set()
        for state in cur_state.get_valid_moves:
            valid_boards.add(state.index_local_board)
        return valid_boards

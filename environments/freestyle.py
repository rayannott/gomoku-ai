from typing import Literal
from utils.utils import Pos, FieldCell
from utils.exceptions import OccupiedCell

class Board:
    def __init__(self, board_shape=(15, 15)) -> None:
        self.board_shape = board_shape
        self.b: list[list[FieldCell]] = [[0]*self.board_shape[1] for _ in range(self.board_shape[0])]
        self.last_placed: Pos | None = None # last placed stone position 
        # board is filled with integers: 0 - empty cell, 1 - black, -1 - white

    def eval(self) -> int:
        '''
        Evaluates current board state.
        '''
        pass

    def display(self) -> None:
        label = {1: 'B', -1: 'W', 0: '-'}
        for row in self.b:
            print(' '.join([label[el] for el in row]))

    def place(self, where: Pos, what: FieldCell) -> None:
        '''
        Place a stone at a particular place on the board.
        :param what - either integer literal (1 or -1) or Stone enum (Stone.BLACK or Stone.WHITE)
        '''
        row, col = where
        if self.b[row][col]:
            raise OccupiedCell(f'The cell {where} is occupied')
        
        self.b[row][col] = what
        
        self.last_placed = where

    def cell_on_board(self, pos: Pos):
        return 0 <= pos[0] < self.board_shape[0] and 0 <= pos[1] < self.board_shape[1]

    def is_over(self) -> FieldCell:
        '''
        Checks if the game is over and outputs the winner's color.
        '''
        if self.last_placed is None:
            return 0
        
        r, c = self.last_placed
        current_color = self.b[r][c]

        deltas = [(0, 1), (1, 0), (-1, 1), (1, 1)]
        for d in deltas:
            streak = 1
            i, j = 1, -1
            positive, negative = True, True
            while True:
                if positive and self.cell_on_board((r + i*d[0], c + i*d[1])) and self.b[r + i*d[0]][c+i*d[1]] == current_color:
                    streak += 1
                    i += 1
                else:
                    positive = False
                if negative and self.cell_on_board((r + j*d[0], c + j*d[1])) and self.b[r + j*d[0]][c+j*d[1]] == current_color:
                    streak += 1
                    j -= 1
                else:
                    negative = False
                if not (positive or negative):
                    break    
            # print('streak:', d, streak)
        if streak == 5:
            return current_color
        return 0


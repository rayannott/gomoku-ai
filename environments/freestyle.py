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
        for row in self.b:
            print(' '.join(map(str, row)))

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

    def is_over(self) -> FieldCell:
        '''
        Checks if the game is over and outputs the winner's color.
        '''
        r, c = self.last_placed
        

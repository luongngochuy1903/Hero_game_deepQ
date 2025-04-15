import numpy as np

class StaticBoard:
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

    def generate_board(self,):
        self.grid = np.array([
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
    ])
    def get_size(self):
        return self.rows, self.cols
    def get_cell(self,pos):
        row,col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    def is_valid_move(self, pos):
        row,col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] == 0 # vị trí hợp lệ là vị trí có giá trị 0
        return False
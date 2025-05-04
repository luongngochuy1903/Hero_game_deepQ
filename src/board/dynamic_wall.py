import random

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ROWS, COLS = 13, 13
Q_TABLE_PATH = "model/dynamic_model/q_table.pkl"

class DynamicBoard:
    def __init__(self, rows, cols, residents):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.residents = residents.copy()
        self.q_pos = (0, 0)
        self.count_to_change = 0

    def _update_walls(self, num_walls):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        walls_placed = 0
        while walls_placed < num_walls:
            x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[x][y] == 0 and (x, y) != (0, 0) and (x, y) not in self.residents:
                self.grid[x][y] = 1
                walls_placed += 1
        return self.grid
    
    def generate_board(self):
        return self.grid
    
    def is_valid_move(self, pos):
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] == 0
        return False
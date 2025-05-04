class StaticBoard:
    def __init__(self, rows, cols, residents):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.residents = residents.copy()
        self.q_pos = (0, 0)

    def generate_board(self):
        
        fixed_walls = [
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
    (0, 1), (12, 11), (1, 2), (1, 3), (11, 10), (11, 9), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (2, 6), (0, 9), (0, 10), (2, 8), (2, 9), (2, 10), (2, 11), (3, 10), (4, 3), (5, 7), (4, 7), (5, 11),
    (7, 1), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (10, 6), (12, 2), (12, 3), (10, 1),
    (10, 2), (10, 3), (10, 4), (9, 2), (8, 9), (7, 5), (8, 5)]
        self.grid =  [[0 for _ in range(13)] for _ in range(13)]
        for x, y in fixed_walls:
            self.grid[x][y] = 1


    def get_size(self):
        return self.rows, self.cols

    def get_cell(self, pos):
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def is_valid_move(self, pos):
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] == 0
        return False
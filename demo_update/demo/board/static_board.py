import numpy as np
import time
import os
class StaticBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)

    def generate_board(self):
        self.grid = np.array([
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        ])

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

    def print_board(self, path=None):
        path_set = set(path) if path else set()
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in path_set:
                    print("P", end=" ")
                elif self.grid[r][c] == 1:
                    print("█", end=" ")
                else:
                    print(".", end=" ")
            print()
    # def print_path_in_steps(self, path):
    #     # In từng bước của agent trên bản đồ
    #     for step in range(len(path)):
    #         print(f"Step {step + 1}:")
    #         self.print_board(path[:step + 1])  # In bản đồ đến bước hiện tại
    #         print("-" * 40)
    #         time.sleep(0.5)  # Delay giữa các bước
    
    def print_visited_step_by_step(self, visited, start, end):
        visited_set = set()

        for step in visited:
            visited_set.add(step)
            # os.system("cls" if os.name == "nt" else "clear") xóa quá trình

            for i in range(self.rows):
                for j in range(self.cols):
                    pos = (i, j)
                    if pos == start:
                        print("S", end=" ")
                    elif pos == end:
                        print("E", end=" ")
                    elif self.grid[i][j] == 1:
                        print("#", end=" ")
                    elif pos in visited_set:
                        print("V", end=" ")
                    else:
                        print(".", end=" ")
                print()
            print("-" * 40)
            time.sleep(0.1)  # Thời gian chờ giữa các bước



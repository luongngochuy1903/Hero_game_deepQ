import numpy as np
import time
import os
class StaticBoard:
    def __init__(self, rows, cols, princesses):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.princesses = princesses.copy()
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
    
    def print_visited_step_by_step(self, visited, start,end):
        visited_set = set()

        for step in visited:
            visited_set.add(step)
            # os.system("cls" if os.name == "nt" else "clear") xóa quá trình

            for i in range(self.rows):
                for j in range(self.cols):
                    pos = (i, j)
                    if pos == start:
                        print("S", end=" ")
                    elif pos in end:
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

    def print_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                pos = (i, j)
                if pos == self.q_pos:
                    print("Q", end=" ")
                elif pos in self.princesses:
                    print("E", end=" ")
                elif self.grid[i][j] == 1:
                    print("#", end=" ")
                else:
                    print(".", end=" ")
            print()
        print("-" * 40)
        time.sleep(0.5)


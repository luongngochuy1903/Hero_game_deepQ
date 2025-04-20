import random
import time
import numpy as np
import os
import pickle
from algorithms.q_learning_agent_dynamic import QLearningAgent 

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ROWS, COLS = 13, 13
Q_TABLE_PATH = "../Hero_game_deepQ/dynamic_model/q_table.pkl"

class MazeGame:
    def __init__(self, rows, cols, princesses):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.princesses = princesses.copy()
        self.q_pos = (0, 0)
        self.count_to_change = 0

    def _update_walls(self, num_walls):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        walls_placed = 0
        while walls_placed < num_walls:
            x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[x][y] == 0 and (x, y) != (0, 0) and (x, y) not in self.princesses:
                self.grid[x][y] = 1
                walls_placed += 1
        return self.grid
    
    def generate_board(self):
        return self.grid
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
        time.sleep(1)
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
        time.sleep(1)
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
    def is_valid_move(self, pos):
        row, col = pos
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col] == 0
        return False
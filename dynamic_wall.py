import random
import time
import numpy as np
import os
import pickle
from q_learning_agent import QLearningAgent 

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ROWS, COLS = 13, 13
Q_TABLE_PATH = "A:/AI_cuoiki/Hero_game_deepQ/dynamic_model/q_table.pkl"

class MazeGame:
    def __init__(self, rows, cols, princesses):
        self.rows = rows
        self.cols = cols
        self.maze = [[0 for _ in range(cols)] for _ in range(rows)]
        self.princesses = princesses.copy()
        self.q_pos = (0, 0)
        self.count_to_change = 0

    def _update_walls(self, num_walls):
        self.maze = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        walls_placed = 0
        while walls_placed < num_walls:
            x, y = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.maze[x][y] == 0 and (x, y) != (0, 0) and (x, y) not in self.princesses:
                self.maze[x][y] = 1
                walls_placed += 1
        return self.maze

    def print_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                pos = (i, j)
                if pos == self.q_pos:
                    print("Q", end=" ")
                elif pos in self.princesses:
                    print("E", end=" ")
                elif self.maze[i][j] == 1:
                    print("#", end=" ")
                else:
                    print(".", end=" ")
            print()
        print("-" * 40)
        time.sleep(1)



if __name__ == "__main__":
    princesses = [(2, 1), (9, 4), (12, 12)]
    game = MazeGame(ROWS, COLS, princesses=princesses)
    agent = QLearningAgent(game, Q_TABLE_PATH)
    agent.run()

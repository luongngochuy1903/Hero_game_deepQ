import random
import time
import numpy as np
import os
import pickle

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ROWS, COLS = 13, 13
Q_TABLE_PATH = "A:/AI_cuoiki/Hero_game_deepQ/dynamic_model/q_table.pkl"

class QLearningAgent:
    def __init__(self, game, q_table_path):
        self.game = game
        self.state = game.q_pos
        self.q_table = self._load_q_table(q_table_path)

    def _load_q_table(self, path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                print("Đã load q_table từ file.")
                return pickle.load(f)
        else:
            raise FileNotFoundError("Không tìm thấy file q_table.pkl trong thư mục")

    def move(self, action):
        x, y = self.state
        if action == "UP":
            return x - 1, y
        elif action == "DOWN":
            return x + 1, y
        elif action == "LEFT":
            return x, y - 1
        elif action == "RIGHT":
            return x, y + 1
        return x, y

    def run(self):
        while self.game.princesses:
            x, y = self.state
            action_index = np.argmax(self.q_table[(x, y)])
            action = ACTIONS[action_index]
            next_state = self.move(action)

            nx, ny = next_state
            if 0 <= nx < self.game.rows and 0 <= ny < self.game.cols and self.game.maze[nx][ny] != 1:
                self.state = next_state
                self.game.q_pos = self.state

            self.game.count_to_change += 1
            self.game.print_maze()
            if self.state in self.game.princesses:
                print(f"[Q-Learning] Cứu công chúa tại {self.state}")
                self.game.princesses.remove(self.state)
            if self.game.count_to_change == 3:
                self.game.count_to_change = 0
                self.game.maze = self.game._update_walls(20)
            print(f"Q value của state hiện tại: {self.q_table[self.state]}")
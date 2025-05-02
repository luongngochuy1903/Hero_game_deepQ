# import random
# import time
# import numpy as np
# import os
# import pickle
# DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
# ROWS, COLS = 13, 13
# Q_TABLE_PATH = "model/static_model/q_table.pkl"
# class QLearningAgent:
#     # def __init__(self, q_table_path):
#     #     self.game = game
#     #     self.state = game.q_pos
#     #     self.q_table = self._load_q_table(q_table_path)
#     #     self.game.generate_board()

#     def __init__(self):
#         self.name = "Q-Learning"
#         self.q_table = self._load_q_table(Q_TABLE_PATH)

#     def _load_q_table(self, path):
#         if os.path.exists(path):
#             with open(path, "rb") as f:
#                 print("Đã load q_table từ file.")
#                 return pickle.load(f)
#         else:
#             raise FileNotFoundError("Không tìm thấy file q_table.pkl trong thư mục")

#     def move(self, action):
#         x, y = self.state
#         if action == "UP":
#             return x - 1, y
#         elif action == "DOWN":
#             return x + 1, y
#         elif action == "LEFT":
#             return x, y - 1
#         elif action == "RIGHT":
#             return x, y + 1
#         return x, y

#     def run(self, board, start):
#         princesses = board.princesses.copy()
#         self.state = start
#         # self.grid = board
#         visited = []
#         while princesses:
#             x, y = self.state
#             action_index = np.argmax(self.q_table[(x, y)])
#             action = ACTIONS[action_index]
#             next_state = self.move(action)

#             nx, ny = next_state
#             # if 0 <= nx < self.game.rows and 0 <= ny < self.game.cols and self.game.grid[nx][ny] != 1:
#             #     self.state = next_state
#             #     self.game.q_pos = self.state
#             if board.is_valid_move(next_state):
#                 self.state = next_state
#             visited.append(self.state)
#             if self.state in princesses:
#                 print(f"[Q-Learning] Cứu công chúa tại {self.state}")
#                 princesses.remove(self.state)
#             print(f"Q value của state hiện tại: {self.q_table[self.state]}")
        
#         return {
#             "path": visited
#         }

import random
import time
import numpy as np
import os
import pickle

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
ROWS, COLS = 13, 13
Q_TABLE_PATH = "model/static_model/q_table.pkl"

class QLearningAgent:
    def __init__(self):
        self.name = "Q-Learning"
        self.q_table = self._load_q_table(Q_TABLE_PATH)

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

    def run(self, board, start):
        visited = []  # Danh sách các vị trí trên đường đi tối ưu
        path = []  # Danh sách các vị trí của cư dân
        self.state = start  # Vị trí bắt đầu
        visited.append(tuple(self.state))  # Thêm vị trí bắt đầu
        visited_set = {tuple(self.state)}  # Theo dõi các vị trí đã thăm để tránh lặp
        princesses = set(board.princesses)  # Tập hợp các vị trí cư dân

        while princesses:
            x, y = self.state  # Lấy tọa độ x, y từ state

            # Truy cập Q-value từ mảng q_table[x, y] (shape: (4,))
            try:
                q_values = self.q_table[x, y]  # Lấy mảng Q-value cho trạng thái (x, y)
            except IndexError:
                print(f"Q-Learning: Trạng thái ({x}, {y}) ngoài phạm vi q_table")
                break

            # Chọn hành động có Q-value cao nhất (chính sách greed)
            action_index = np.argmax(q_values)
            action = ACTIONS[action_index]
            next_state = self.move(action)

            # Kiểm tra xem bước đi có hợp lệ và chưa được thăm không
            if (board.is_valid_move(next_state) and tuple(next_state) not in visited_set):
                self.state = next_state  # Cập nhật vị trí hiện tại
                visited.append(tuple(self.state))  # Thêm vào danh sách visited
                visited_set.add(tuple(self.state))  # Cập nhật tập hợp đã thăm

                # Kiểm tra xem có tìm thấy cư dân không
                if tuple(self.state) in princesses:
                    print(f"[Q-Learning] Cứu công chúa tại {self.state}")
                    path.append(tuple(self.state))  # Thêm vị trí cư dân vào path
                    princesses.discard(tuple(self.state))  # Xóa cư dân đã tìm thấy

                # In Q-value của trạng thái hiện tại để debug
                try:
                    print(f"Q value của state hiện tại ({self.state[0]}, {self.state[1]}): {self.q_table[self.state[0], self.state[1]]}")
                except IndexError:
                    print(f"Q-Learning: Không thể in Q-value cho trạng thái ({self.state[0]}, {self.state[1]})")

            else:
                # Nếu bước đi không hợp lệ hoặc đã thăm, dừng để tránh lặp
                print(f"Q-Learning: Bước đi không hợp lệ hoặc đã thăm tại {next_state}")
                break

        # Nếu không tìm thấy cư dân, thông báo
        if not path:
            print("Q-Learning: Không tìm thấy đường đến cư dân")

        return {
            "visited": visited,  # Các vị trí trên đường đi tối ưu
            "path": visited  # Các vị trí của cư dân
        }
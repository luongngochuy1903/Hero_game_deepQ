# import random
# import time
# import numpy as np
# import os
# import pickle

# DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
# ROWS, COLS = 13, 13
# Q_TABLE_PATH = "model/dynamic_model/q_table.pkl"

# class QLearningAgent:
#     # def __init__(self, game, q_table_path):
#     #     self.game = game
#     #     self.state = game.q_pos
#     #     self.q_table = self._load_q_table(q_table_path)
    
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
            
#             if board.is_valid_move(next_state) and board.grid[nx][ny] != 1:
#                 self.state = next_state
#             visited.append(self.state)
#             board.count_to_change += 1
#             # self.game.print_maze()
#             # if self.state in self.game.princesses:
#             #     print(f"[Q-Learning] Cứu công chúa tại {self.state}")
#             #     self.game.princesses.remove(self.state)
#             # if self.game.count_to_change == 3:
#             #     self.game.count_to_change = 0
#             #     self.game.grid = self.game._update_walls(20)
#             # print(f"Q value của state hiện tại: {self.q_table[self.state]}")
            
#             if self.state in princesses:
#                 print(f"[Q-Learning] Cứu công chúa tại {self.state}")
#                 princesses.remove(self.state)
#             if board.count_to_change == 3:
#                 board.count_to_change = 0
#                 board.grid = board._update_walls(20)
#             print(f"Q value của state hiện tại: {self.q_table[self.state]}")
        
#         # print("Đường đi theo thuật toán q_learning: ")
#         # print(visited)
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
Q_TABLE_PATH = "model/dynamic_model/q_table.pkl"

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
        visited = []  # Danh sách các vị trí trên đường đi tạm thời
        path = []  # Danh sách các vị trí của cư dân
        self.state = start  # Vị trí bắt đầu
        visited.append(tuple(self.state))  # Thêm vị trí bắt đầu
        visited_set = {tuple(self.state)}  # Theo dõi các vị trí đã thăm
        princesses = set(board.princesses)  # Tập hợp các vị trí cư dân

        # Chạy cho đến khi tìm thấy một cư dân hoặc đạt max_steps_per_run
        while True:
            if not princesses:
                break  # Dừng nếu đã tìm thấy tất cả cư dân

            x, y = self.state

            # Truy cập Q-value từ mảng q_table[x, y]
            try:
                q_values = self.q_table[x, y]  # Lấy mảng Q-value (shape: (4,))
            except IndexError:
                print(f"Q-Learning: Trạng thái ({x}, {y}) ngoài phạm vi q_table")
                break

            # Chọn hành động có Q-value cao nhất
            action_index = np.argmax(q_values)
            action = ACTIONS[action_index]
            next_state = self.move(action)
            nx, ny = next_state

            # Kiểm tra bước đi hợp lệ
            if (board.is_valid_move(next_state) and 
                board.grid[nx][ny] != 1 and 
                tuple(next_state) not in visited_set):
                self.state = next_state
                visited.append(tuple(self.state))
                visited_set.add(tuple(self.state))

                # Kiểm tra cư dân
                if tuple(self.state) in princesses:
                    print(f"[Q-Learning] Cứu công chúa tại {self.state}")
                    path.append(tuple(self.state))
                    princesses.discard(tuple(self.state))

                # In Q-value để debug
                try:
                    print(f"Q value của state hiện tại ({self.state[0]}, {self.state[1]}): {self.q_table[self.state[0], self.state[1]]}")
                except IndexError:
                    print(f"Q-Learning: Không thể in Q-value cho trạng thái ({self.state[0]}, {self.state[1]})")

            else:
                print(f"Q-Learning: Bước đi không hợp lệ hoặc đã thăm tại {next_state}")
                break

        if not path and len(visited) == 1:
            print("Q-Learning: Không tìm thấy đường đi hợp lệ từ vị trí bắt đầu")

        return {
            "visited": visited,  # Các vị trí trên đường đi tạm thời
            "path": path  # Các vị trí của cư dân được tìm thấy
        }
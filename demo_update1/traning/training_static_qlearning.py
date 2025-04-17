import tkinter as tk
import time
from collections import deque
import numpy as np
import random
import pickle
import os


ROWS, COLS = 13, 13
CELL_SIZE = 40

fixed_walls = [
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
    (0, 1), (12, 11), (1, 2), (1, 3), (11, 10), (11, 9), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (2, 6), (0, 9), (0, 10), (2, 8), (2, 9), (2, 10), (2, 11), (3, 10), (4, 3), (5, 7), (4, 7), (5, 11),
    (7, 1), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (10, 6), (12, 2), (12, 3), (10, 1),
    (10, 2), (10, 3), (10, 4), (9, 2), (8, 9), (7, 5), (8, 5)
]

maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for x, y in fixed_walls:
    maze[x][y] = 1

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
q_table = None
save_path = "../Hero_game_deepQ/static_model/q_table.pkl"
if os.path.exists(save_path):
    with open(save_path, "rb") as f:
        q_table = pickle.load(f)
else:
    q_table = np.random.uniform(low=-1, high=1, size=(ROWS, COLS, len(ACTIONS)))

def get_reward(current_path, state, end, maze, prev_state):
    x,y = state
    if x < 0 or x >= ROWS or y < 0 or y >= COLS or maze[x][y] == 1:
        return -200
    if state in end:
        return 30
    min_distance = min(abs(x - ex) + abs(y - ey) for (ex, ey) in end)
    
    if prev_state:
        prev_min_distance = min(abs(prev_state[0] - ex) + abs(prev_state[1] - ey) for (ex, ey) in end)
        distance_reward = (prev_min_distance - min_distance) * 2  
    else:
        distance_reward = 0
    
    revisit_penalty = -2 if state in current_path else 0
    
    total_reward = distance_reward + revisit_penalty
    return total_reward

def move_q_learning(state, action):
    x, y = state
    if action == "UP":
        return x - 1, y
    elif action == "DOWN":
        return x + 1, y
    elif action == "LEFT":
        return x, y - 1
    elif action == "RIGHT":
        return x, y + 1
    return state

start = (0, 0)
end = [(12, 12), (2, 1), (9, 4)]
for x, y in end:
    maze[x][y] = 2

c_learning_rate = 0.2
c_discount_value = 0.93
c_no_of_eps = 10000
epsilon = 1.0
epsilon_min = 0.1
epsilon_decay = 0.9995
tolerance = 0.0001

max_step = 120
max_ep_reward = -2000
ep_max = -1
successful_paths = []

for ep in range(c_no_of_eps):
    state = start
    temp_end = end.copy()
    for x,y in end:
        maze[x][y] = 2
    current_path = []
    ep_reward = 0
    princess_found = 0
    step = 0

    while step < max_step and princess_found < 3:
        if np.random.random() < epsilon:
            action = random.choice(ACTIONS)
        else:
            action = ACTIONS[np.argmax(q_table[state])]

        next_state = move_q_learning(state, action)
        x, y = next_state
        if x < 0 or x >= ROWS or y < 0 or y >= COLS or maze[x][y] == 1:
            reward = get_reward(current_path, next_state, temp_end, maze, state)
            next_state = state 
        else:
            reward = get_reward(current_path, next_state, temp_end, maze, state)
        current_path.append(state)
        ep_reward += reward
        current_q = q_table[state][ACTIONS.index(action)]
        new_q = (1 - c_learning_rate) * current_q + c_learning_rate * (reward + c_discount_value * np.max(q_table[next_state]))
        q_table[state][ACTIONS.index(action)] = new_q

        state = next_state
        step += 1

        if state in temp_end:
            princess_found += 1
            temp_end.remove(state)
            maze[state[0]][state[1]] = 0

    current_path.append(state)
    if ep_reward > max_ep_reward:
        max_ep_reward = ep_reward
        ep_max = ep
        successful_paths.append((ep, current_path))

    epsilon =  max(epsilon_min, epsilon * epsilon_decay)

    if princess_found == 3:
        print(f"tại ep {ep} đã cứu được {princess_found} công chúa")

with open(save_path, "wb") as f:
    pickle.dump(q_table, f)
successful_paths.sort(key=lambda x:x[0], reverse=True)
# =====================
# UI Tkinter
# =====================
COLORS = {
    0: "white",  # đường đi
    1: "black",  # tường
    2: "pink",   # công chúa
    "S": "blue", # người chơi
}

class MazeUI:
    def __init__(self, root, maze, path, end_points):
        self.root = root
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()
        self.maze = maze
        self.path = path
        self.end_points = end_points.copy()
        self.hero_index = 0
        self.hero_pos = path[0]
        self.draw_maze()
        self.root.after(300, self.update_hero)

    def draw_maze(self):
        for i in range(ROWS):
            for j in range(COLS):
                cell_type = self.maze[i][j]
                color = COLORS.get(cell_type, "white")
                if (i, j) in self.end_points:
                    color = COLORS[2]
                self.canvas.create_rectangle(
                    j*CELL_SIZE, i*CELL_SIZE, (j+1)*CELL_SIZE, (i+1)*CELL_SIZE,
                    fill=color, outline="gray"
                )

    def update_hero(self):
        if self.hero_index >= len(self.path):
            return

        # Vị trí hiện tại: xóa màu xanh cũ, tô trắng lại
        x, y = self.hero_pos
        self.canvas.create_rectangle(
            y*CELL_SIZE, x*CELL_SIZE, (y+1)*CELL_SIZE, (x+1)*CELL_SIZE,
            fill=COLORS[0], outline="gray"
        )

        # Di chuyển đến bước kế tiếp
        self.hero_pos = self.path[self.hero_index]
        x, y = self.hero_pos

        # Vẽ vị trí mới của nhân vật
        self.canvas.create_rectangle(
            y*CELL_SIZE, x*CELL_SIZE, (y+1)*CELL_SIZE, (x+1)*CELL_SIZE,
            fill=COLORS["S"], outline="gray"
        )

        self.hero_index += 1
        self.root.after(300, self.update_hero)

# =====================
# Chạy giao diện
# =====================
root = tk.Tk()
root.title("Q-learning Rescue Princess")
chosen_path = successful_paths[0][1]
print(chosen_path)
for x, y in end:
    maze[x][y] = 2
app = MazeUI(root, maze, chosen_path, end)
root.mainloop()

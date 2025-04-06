import pickle
import os
import numpy as np
import threading
from collections import deque
import time

q_table = None
q_table_path = "A:/AI_cuoiki/Hero_game_deepQ/static_model/q_table.pkl"
if os.path.exists(q_table_path):
    with open(q_table_path, "rb") as f:
        q_table = pickle.load(f)
    print("Đã load q_table từ file.")
else:
    raise FileNotFoundError("Không tìm thấy file q_table.pkl trong thư mục")

fixed_walls = [
    (6, 0), (6, 1), (6, 2), (6,3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
    (0, 1), (12, 11), (1, 2), (1, 3), (11, 10), (11, 9), (3, 0), (3, 1), (3, 2), (3,3), (3, 4), (3, 5), (2, 6), (0, 9), (0, 10),
    (2, 8), (2, 9), (2, 10), (2, 11), (3, 10), (4, 3), (5, 7), (4, 7), (5, 11), (7, 1),
    (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (10, 6), (12, 2), (12, 3), (10, 1), (10, 2), (10, 3), (10, 4), (9, 2),
    (8, 9), (7, 5), (8, 5)
]

rows, cols = 13, 13
maze = [[0 for _ in range(cols)] for _ in range(rows)]

# Hàm BFS 
def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start[0], start[1], [])])
    visited = set()
    visited.add(start)

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == end:
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(x, y)]))

    return None 

DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
state_size = [13, 13]

def move_q_learning(state, ACTIONS):
    x,y = state
    if ACTIONS == "UP":
        return x-1, y
    elif ACTIONS == "DOWN":
        return x+1, y
    elif ACTIONS == "RIGHT":
        return x, y+1
    elif ACTIONS == "LEFT":
        return x,y-1
    return state

def agent_q_learning():
    state = shared_state["q_pos"]
    end_list = shared_state["princesses"][:]

    while end_list:
        action = ACTIONS[np.argmax(q_table[state])]
        next_state = move_q_learning(state, action)

        x, y = next_state
        if 0 <= x < rows and 0 <= y < cols and maze[x][y] != 1:
            state = next_state

        shared_state["q_pos"] = state
        shared_state["princesses"] = [e for e in end_list]

        print_maze_sync(maze)

        if state in end_list:
            print(f"[Q Agent] Cứu công chúa tại {state}")
            end_list.remove(state)

def agent_bfs():
    state = shared_state["bfs_pos"]
    end_list = shared_state["princesses"][:]

    while end_list:
        nearest = min(end_list, key=lambda e: abs(state[0]-e[0]) + abs(state[1]-e[1]))
        path = bfs(maze, state, nearest)
        if not path:
            print("[BFS Agent] Không tìm được đường!")
            return
        for step in path:
            state = step
            shared_state["bfs_pos"] = state
            shared_state["princesses"] = [e for e in end_list]
            print_maze_sync(maze)

        print(f"[BFS Agent] Cứu công chúa tại {nearest}")
        end_list.remove(nearest)


shared_state = {
    "q_pos": (0, 0),
    "bfs_pos": (12, 12),
    "princesses": [(2, 1), (9, 4), (6, 6)]
}
print_lock = threading.Lock()

maze = [[0 for _ in range(cols)] for _ in range(rows)]
for x, y in fixed_walls:
    maze[x][y] = 1
for x, y in shared_state["princesses"]:
    maze[x][y] = 2

def print_maze_sync(maze):
    with print_lock:
        q = shared_state["q_pos"]
        b = shared_state["bfs_pos"]
        ends = shared_state["princesses"]

        for i in range(rows):
            for j in range(cols):
                pos = (i, j)
                if pos == q and pos == b:
                    print("X", end=" ")  
                elif pos == q:
                    print("Q", end=" ") 
                elif pos == b:
                    print("B", end=" ")  
                elif pos in ends:
                    print("E", end=" ")  
                elif maze[i][j] == 1:
                    print("#", end=" ")  
                else:
                    print(".", end=" ")  
            print()
        print("----------------------------------------")
        time.sleep(0.5)

if __name__ == "__main__":
    t1 = threading.Thread(target=agent_q_learning)
    t2 = threading.Thread(target=agent_bfs)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("🎉 Hoàn tất cứu công chúa!")
